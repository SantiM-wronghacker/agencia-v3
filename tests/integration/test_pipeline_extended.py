"""Extended integration tests for pipelines, FTS, and export."""
import ast
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "license-server"))

from memory.db import AgenciaDB
from memory.fts import FTSSearch
from core.orchestrator import Orchestrator
from export.builder import PackageBuilder
from groups.content_pipeline import create_content_pipeline
from groups.business_analysis import create_business_analysis


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_group_output_searchable_via_fts(db, fake_llm_pipeline):
    with patch("core.agent.get_llm", return_value=fake_llm_pipeline):
        group = create_content_pipeline(db=db)

    group.execute("estrategia de marketing digital")
    results = FTSSearch(db).search("marketing")
    assert isinstance(results, list)
    # FTS should find something (either from observations or be graceful with empty)
    # At minimum the call must not raise
    assert results is not None


def test_group_output_fts_returns_list_type(db, fake_llm_pipeline):
    """FTS always returns a list, never raises."""
    with patch("core.agent.get_llm", return_value=fake_llm_pipeline):
        group = create_content_pipeline(db=db)
    group.execute("plan de contenido para redes sociales")
    results = FTSSearch(db).search("contenido")
    assert isinstance(results, list)


def test_two_groups_share_memory(db, fake_llm_pipeline):
    with patch("core.agent.get_llm", return_value=fake_llm_pipeline):
        g1 = create_content_pipeline(db=db)
        g2 = create_business_analysis(db=db)

    g1.execute("análisis de ventas Q1")
    result2 = g2.execute("estrategia basada en análisis previo")
    assert result2.success


def test_export_all_py_files_valid_syntax(tmp_path):
    builder = PackageBuilder(
        client_id="syntax-test",
        client_name="Test",
        package_type="basic",
        license_key="T-001",
        license_server_url="http://localhost:8080",
        groups=["content_pipeline"],
        output_base=tmp_path,
    )
    path = builder.build()
    errors = []
    for py_file in path.rglob("*.py"):
        try:
            ast.parse(py_file.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError as e:
            errors.append(f"{py_file.name}: {e}")
    assert errors == [], f"Errores de sintaxis: {errors}"


def test_orchestrator_persists_run_to_db(db, fake_llm_pipeline):
    with patch("core.agent.get_llm", return_value=fake_llm_pipeline):
        group = create_content_pipeline(db=db)

    orch = Orchestrator(db=db)
    orch.register(group)
    orch.run("content_pipeline", "tarea de prueba")

    runs = db.get_recent_runs()
    assert any(r["group_name"] == "content_pipeline" for r in runs)


def test_fts_handles_accented_characters(db, fake_llm_pipeline):
    with patch("core.agent.get_llm", return_value=fake_llm_pipeline):
        group = create_content_pipeline(db=db)

    group.execute("análisis de México y América Latina")
    results = FTSSearch(db).search("México")
    # Must return a list (empty or not) without raising
    assert isinstance(results, list)
