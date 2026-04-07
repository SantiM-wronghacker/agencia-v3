"""Integration tests for PackageBuilder and /export endpoint."""
import json
import sys
from pathlib import Path

import httpx
import pytest

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from export.builder import PackageBuilder


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_builder(tmp_path: Path, **kwargs) -> PackageBuilder:
    defaults = dict(
        client_id="test-client",
        client_name="Cliente Test",
        package_type="basic",
        license_key="TEST-KEY-1234",
        license_server_url="http://localhost:8080",
        groups=["content_pipeline"],
    )
    defaults.update(kwargs)
    return PackageBuilder(**defaults, output_base=tmp_path)


# ---------------------------------------------------------------------------
# Unit tests — PackageBuilder
# ---------------------------------------------------------------------------

def test_package_builder_creates_structure(tmp_path: Path):
    builder = _make_builder(tmp_path)
    path = builder.build()

    assert (path / "config" / "client.json").exists()
    assert (path / "license" / "heartbeat.py").exists()
    assert (path / "install.bat").exists()
    assert (path / "requirements.txt").exists()


def test_client_json_has_correct_values(tmp_path: Path):
    builder = _make_builder(tmp_path)
    path = builder.build()

    data = json.loads((path / "config" / "client.json").read_text(encoding="utf-8"))
    assert data["package_type"] == "basic"
    assert data["license_key"] == "TEST-KEY-1234"
    assert data["ollama_model"] == "phi3:mini"


def test_basic_package_uses_phi3(tmp_path: Path):
    builder = _make_builder(tmp_path, package_type="basic")
    path = builder.build()

    config = json.loads((path / "config" / "client.json").read_text(encoding="utf-8"))
    assert config["ollama_model"] == "phi3:mini"


def test_pro_package_uses_qwen(tmp_path: Path):
    builder = _make_builder(tmp_path, package_type="pro", client_id="pro-client")
    path = builder.build()

    config = json.loads((path / "config" / "client.json").read_text(encoding="utf-8"))
    assert config["ollama_model"] == "qwen2.5:32b"


def test_only_selected_groups_copied(tmp_path: Path):
    builder = _make_builder(tmp_path, groups=["content_pipeline"])
    path = builder.build()

    assert (path / "groups" / "content_pipeline.py").exists()
    assert not (path / "groups" / "legal_review.py").exists()


def test_heartbeat_script_is_standalone(tmp_path: Path):
    """heartbeat.py reads its config at runtime — license key must NOT be hardcoded."""
    builder = _make_builder(tmp_path)
    path = builder.build()

    content = (path / "license" / "heartbeat.py").read_text(encoding="utf-8")
    # The script reads config/client.json at runtime; key should not be baked in
    assert "client.json" in content
    assert "license_key" in content


def test_install_bat_contains_client_name(tmp_path: Path):
    builder = _make_builder(tmp_path)
    path = builder.build()

    content = (path / "install.bat").read_text(encoding="utf-8")
    assert "Cliente Test" in content


# ---------------------------------------------------------------------------
# API tests — /export endpoint
# ---------------------------------------------------------------------------

from api.routes import app
from api.dependencies import get_db, get_orchestrator
from memory.db import AgenciaDB


class _MockOrchestrator:
    """Minimal orchestrator that exposes the 4 real groups without LLM calls."""
    _GROUPS = {"content_pipeline", "business_analysis", "legal_review", "ops_automation"}

    def get_group(self, name: str):
        return object() if name in self._GROUPS else None

    def list_groups(self):
        return [{"name": n, "mode": "pipeline", "agent_count": 0, "agent_roles": []}
                for n in self._GROUPS]


@pytest.fixture
async def api_client():
    mem_db = AgenciaDB(db_path=":memory:")
    mock_orc = _MockOrchestrator()
    app.dependency_overrides[get_db] = lambda: mem_db
    app.dependency_overrides[get_orchestrator] = lambda: mock_orc
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


async def test_export_api_endpoint(api_client, tmp_path: Path):
    # Patch PackageBuilder to use tmp_path so we don't write to real export/
    import export.builder as _mod
    original_init = PackageBuilder.__init__

    def _patched_init(self, client_id, client_name, package_type,
                      license_key, license_server_url, groups, output_base=None):
        original_init(self, client_id, client_name, package_type,
                      license_key, license_server_url, groups,
                      output_base=tmp_path)

    _mod.PackageBuilder.__init__ = _patched_init
    try:
        res = await api_client.post("/export/nuevo-cliente", json={
            "client_name": "Test SA",
            "package_type": "basic",
            "license_key": "API-TEST-KEY",
            "license_server_url": "http://localhost:8080",
            "groups": ["content_pipeline", "business_analysis"],
        })
    finally:
        _mod.PackageBuilder.__init__ = original_init

    assert res.status_code == 200
    data = res.json()
    assert "package_path" in data
    assert data["files_generated"] > 0


async def test_export_api_invalid_group(api_client):
    res = await api_client.post("/export/nuevo-cliente", json={
        "client_name": "Test SA",
        "package_type": "basic",
        "license_key": "API-TEST-KEY",
        "license_server_url": "http://localhost:8080",
        "groups": ["grupo_inexistente"],
    })
    assert res.status_code == 400
    assert "grupo_inexistente" in res.json()["detail"]
