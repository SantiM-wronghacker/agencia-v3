"""End-to-end tests for AgentGroup pipelines, export, and license server."""
import ast
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "license-server"))

from memory.db import AgenciaDB
from memory.fts import FTSSearch
from llm.base import LLMUnavailableError
from export.builder import PackageBuilder
from db import LicenseDB


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fake_llm(response: str) -> MagicMock:
    llm = MagicMock()
    llm.provider_name = "fake"
    llm.generate.return_value = response
    return llm


def _make_pipeline_llms(responses: list[str]) -> list[MagicMock]:
    return [_fake_llm(r) for r in responses]


def _iso_ago(hours: int) -> str:
    dt = datetime.now(timezone.utc) - timedelta(hours=hours)
    return dt.isoformat()


def _paid_until(days: int) -> str:
    dt = datetime.now(timezone.utc) + timedelta(days=days)
    return dt.date().isoformat()


# ---------------------------------------------------------------------------
# Content pipeline — full flow
# ---------------------------------------------------------------------------

def test_content_pipeline_full_flow():
    from groups.content_pipeline import create_content_pipeline

    responses = [
        "Investigación: IA en empresas mexicanas. Puntos clave: automatización, productividad.",
        "Artículo: La IA transforma las empresas mexicanas en el siglo XXI.",
        "Artículo optimizado con keywords: IA, empresas, México, transformación digital.",
        "Versión final revisada y pulida: completo y bien estructurado.",
    ]
    llms = _make_pipeline_llms(responses)

    db = AgenciaDB(":memory:")
    with patch("core.agent.get_llm", side_effect=llms):
        group = create_content_pipeline(db=db)

    result = group.execute("IA en empresas mexicanas")

    assert result.success is True
    assert len(result.steps) == 4
    assert all(s.success for s in result.steps)

    # Pipeline chain: each step gets previous step's output as input
    assert result.steps[1].input == result.steps[0].output
    assert result.steps[2].input == result.steps[1].output
    assert result.steps[3].input == result.steps[2].output

    # DB persistence
    runs = db.get_recent_runs()
    assert len(runs) == 1
    steps = db.get_steps(result.run_id)
    assert len(steps) == 4

    # FTS indexed the observations
    observations = FTSSearch(db).search("empresas mexicanas")
    assert len(observations) > 0


# ---------------------------------------------------------------------------
# Business analysis — full flow
# ---------------------------------------------------------------------------

def test_business_analysis_full_flow():
    from groups.business_analysis import create_business_analysis

    responses = [
        "Datos de ventas Q1: crecimiento 12%, margen 35%, clientes top 5.",
        "Estrategia recomendada: expansión en canal digital, reducir CAC.",
        "Proyección financiera: +18% ingresos en Q2 con inversión de $50k.",
        "Reporte ejecutivo: análisis Q1 completado con recomendaciones claras.",
    ]
    llms = _make_pipeline_llms(responses)

    db = AgenciaDB(":memory:")
    with patch("core.agent.get_llm", side_effect=llms):
        group = create_business_analysis(db=db)

    result = group.execute("análisis de ventas Q1")

    assert result.success is True
    assert len(result.steps) == 4


# ---------------------------------------------------------------------------
# Pipeline stops on first failure
# ---------------------------------------------------------------------------

def test_pipeline_stops_on_first_failure():
    from groups.content_pipeline import create_content_pipeline

    # First agent raises LLMUnavailableError; rest never execute
    fail_llm = MagicMock()
    fail_llm.provider_name = "fake"
    fail_llm.generate.side_effect = LLMUnavailableError("sin LLM")
    good_llm = _fake_llm("nunca debería llegar")

    db = AgenciaDB(":memory:")
    with patch("core.agent.get_llm", side_effect=[fail_llm, good_llm, good_llm, good_llm]):
        group = create_content_pipeline(db=db)

    result = group.execute("tarea")

    assert result.success is False
    assert len(result.steps) == 1
    assert result.steps[0].success is False


# ---------------------------------------------------------------------------
# Export integrity
# ---------------------------------------------------------------------------

def test_export_then_check_structure(tmp_path: Path):
    builder = PackageBuilder(
        client_id="integrity-test",
        client_name="Test SA",
        package_type="basic",
        license_key="INT-KEY-9999",
        license_server_url="http://localhost:8080",
        groups=["content_pipeline", "legal_review"],
        output_base=tmp_path,
    )
    path = builder.build()

    # client.json is valid JSON
    raw = (path / "config" / "client.json").read_text(encoding="utf-8")
    data = json.loads(raw)
    assert data["client_id"] == "integrity-test"

    # install.bat is not empty
    bat = (path / "install.bat").read_text(encoding="utf-8")
    assert len(bat.strip()) > 0

    # heartbeat.py is syntactically valid Python
    hb = (path / "license" / "heartbeat.py").read_text(encoding="utf-8")
    tree = ast.parse(hb)  # raises SyntaxError if invalid
    assert tree is not None

    # requirements.txt has at least 3 lines
    reqs = (path / "requirements.txt").read_text(encoding="utf-8").strip().splitlines()
    assert len(reqs) >= 3

    # groups/ has exactly the requested groups (plus __init__.py)
    group_files = {f.stem for f in (path / "groups").iterdir() if f.suffix == ".py" and f.stem != "__init__"}
    assert group_files == {"content_pipeline", "legal_review"}


# ---------------------------------------------------------------------------
# License server — multi-heartbeat flow
# ---------------------------------------------------------------------------

def test_license_server_heartbeat_flow():
    # Replicate _compute_status logic directly to avoid HTTP layer complexity
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "license-server"))
    from main import _compute_status

    db = LicenseDB(":memory:")
    client_id = db.create_client(
        name="Test Client",
        license_key="FLOW-KEY-001",
        package_type="basic",
        paid_until=_paid_until(30),
    )
    client = db.get_client(client_id)

    # Heartbeat 1: no prior heartbeats → active
    last_hb = db.get_last_heartbeat(client_id)
    active, status, _, _, _ = _compute_status(client, last_hb)
    assert active is True
    assert status == "active"
    db.record_heartbeat(client_id, "127.0.0.1", "basic", status)

    # Heartbeat 2: simulate 25h offline — update recorded heartbeat timestamp
    db._persistent_conn.execute(
        "UPDATE heartbeats SET timestamp=? WHERE client_id=?",
        [_iso_ago(25), client_id],
    )
    db._persistent_conn.commit()

    last_hb = db.get_last_heartbeat(client_id)
    active, status, _, _, _ = _compute_status(client, last_hb)
    assert active is True
    assert status == "warning"
    db.record_heartbeat(client_id, "127.0.0.1", "basic", status)

    # Heartbeat 3: simulate 130h offline — move ALL prior heartbeats to 130h ago
    # so get_last_heartbeat (ORDER BY timestamp DESC) returns the 130h-ago one
    db._persistent_conn.execute(
        "UPDATE heartbeats SET timestamp=? WHERE client_id=?",
        [_iso_ago(130), client_id],
    )
    db._persistent_conn.commit()

    last_hb = db.get_last_heartbeat(client_id)
    active, status, _, _, _ = _compute_status(client, last_hb)
    assert active is True
    assert status == "grace"
    db.record_heartbeat(client_id, "127.0.0.1", "basic", status)

    # DB has 3 heartbeat records
    heartbeats = db.get_client_heartbeats(client_id, limit=10)
    assert len(heartbeats) == 3
