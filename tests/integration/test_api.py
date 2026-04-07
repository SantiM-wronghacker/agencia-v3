"""
Tests de integración para la API de agencia-v3.

Usan httpx.AsyncClient contra la app FastAPI real (in-process).
La DB y el orchestrator se aíslan por test mediante override de dependencias.
Los grupos en tests usan agentes vacíos para no invocar LLMs reales.
"""
import pytest
import httpx

from api.routes import app
from api.dependencies import get_db, get_orchestrator
from core.group import AgentGroup
from core.orchestrator import Orchestrator
from memory.db import AgenciaDB


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def test_db():
    """DB en memoria aislada por test."""
    return AgenciaDB(":memory:")


@pytest.fixture()
def test_orchestrator(test_db):
    """Orchestrator con grupos vacíos (sin agentes reales) para tests rápidos."""
    orch = Orchestrator(db=test_db)
    for name in ("content_pipeline", "business_analysis", "legal_review", "ops_automation"):
        orch.register(AgentGroup(name, [], mode="pipeline", db=test_db))
    return orch


@pytest.fixture()
async def client(test_db, test_orchestrator):
    """AsyncClient con dependencias sobreescritas."""
    app.dependency_overrides[get_db] = lambda: test_db
    app.dependency_overrides[get_orchestrator] = lambda: test_orchestrator

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as c:
        yield c

    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

async def test_health_endpoint_returns_ok(client):
    response = await client.get("/api/v2/dashboard/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


async def test_get_groups_returns_list(client):
    response = await client.get("/groups")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 4


async def test_post_group_run_returns_run_id(client):
    response = await client.post(
        "/groups/content_pipeline/run",
        json={"task": "test task"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "run_id" in body
    assert body["status"] == "started"
    assert body["group_name"] == "content_pipeline"


async def test_post_group_run_unknown_group_returns_404(client):
    response = await client.post(
        "/groups/no_existe/run",
        json={"task": "test"},
    )
    assert response.status_code == 404


async def test_memory_search_requires_query(client):
    response = await client.get("/memory/search")
    assert response.status_code in (400, 422)


async def test_memory_search_returns_list(client):
    response = await client.get("/memory/search?q=test")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_run_unknown_returns_404(client):
    response = await client.get("/groups/content_pipeline/runs/run-no-existe")
    assert response.status_code == 404


async def test_get_group_runs_returns_list(client):
    response = await client.get("/groups/content_pipeline/runs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ---------------------------------------------------------------------------
# Test que verifica agent_counts del orchestrator real
# ---------------------------------------------------------------------------

def test_real_groups_have_correct_agent_counts():
    """Verifica que los grupos reales tienen los agentes correctos."""
    from groups import (
        create_content_pipeline,
        create_business_analysis,
        create_legal_review,
        create_ops_automation,
    )
    assert len(create_content_pipeline().agents) == 4
    assert len(create_business_analysis().agents) == 4
    assert len(create_legal_review().agents) == 4
    assert len(create_ops_automation().agents) == 3
