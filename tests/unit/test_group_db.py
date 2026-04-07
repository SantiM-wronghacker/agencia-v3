from unittest.mock import MagicMock, patch

import pytest

from core.base import GroupResult
from core.group import AgentGroup
from core.orchestrator import Orchestrator
from memory.db import AgenciaDB
from memory.fts import FTSSearch


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_fake_llm(return_value: str = "output de prueba"):
    fake = MagicMock()
    fake.provider_name = "fake"
    fake.generate.return_value = return_value
    return fake


def _make_agent(role: str, return_value: str = "output de prueba"):
    fake_llm = _make_fake_llm(return_value)
    with patch("core.agent.get_llm", return_value=fake_llm):
        from core.agent import BaseAgent
        agent = BaseAgent(role)
    return agent


def _make_group(db: AgenciaDB, mode: str = "pipeline") -> tuple[AgentGroup, str, str]:
    agent1 = _make_agent("rol_a", "output_a")
    agent2 = _make_agent("rol_b", "output_b")
    group = AgentGroup("test", [agent1, agent2], mode=mode, db=db)
    return group, "rol_a", "rol_b"


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_group_creates_run_in_db():
    db = AgenciaDB(":memory:")
    group, _, _ = _make_group(db)
    group.execute("tarea")
    runs = db.get_recent_runs()
    assert len(runs) == 1
    assert runs[0]["group_name"] == "test"


def test_group_saves_all_steps():
    db = AgenciaDB(":memory:")
    group, _, _ = _make_group(db)
    result = group.execute("tarea")
    steps = db.get_steps(result.run_id)
    assert len(steps) == 2


def test_group_saves_observations():
    db = AgenciaDB(":memory:")
    group, _, _ = _make_group(db)
    group.execute("tarea")
    results = FTSSearch(db).search("output")
    assert len(results) >= 1


def test_agent_does_not_duplicate_when_managed():
    """Agente con db propia + managed_by_group=True no debe escribir en su DB."""
    agent_db = AgenciaDB(":memory:")
    fake_llm = _make_fake_llm("respuesta")
    with patch("core.agent.get_llm", return_value=fake_llm):
        from core.agent import BaseAgent
        agent = BaseAgent("rol_test", db=agent_db)

    # Llama con managed_by_group=True como lo haría un grupo
    import uuid
    agent.run("tarea", run_id=str(uuid.uuid4()), managed_by_group=True)

    # El agente NO debe haber escrito en su propia DB
    assert db.get_recent_runs() == [] if (db := agent_db) else True
    runs = agent_db.get_recent_runs()
    assert runs == []


def test_orchestrator_registers_and_runs_group():
    db = AgenciaDB(":memory:")
    group, _, _ = _make_group(db)
    orchestrator = Orchestrator(db=db)
    orchestrator.register(group)
    result = orchestrator.run("test", "tarea")
    assert isinstance(result, GroupResult)
    assert result.success is True


def test_orchestrator_raises_on_unknown_group():
    orchestrator = Orchestrator()
    with pytest.raises(ValueError):
        orchestrator.run("no_existe", "tarea")


def test_orchestrator_list_groups():
    db = AgenciaDB(":memory:")
    group, _, _ = _make_group(db)
    orchestrator = Orchestrator(db=db)
    orchestrator.register(group)
    groups = orchestrator.list_groups()
    assert len(groups) == 1
    assert groups[0]["name"] == "test"
    assert "agent_roles" in groups[0]
    assert groups[0]["agent_count"] == 2


def test_orchestrator_propagates_db_to_group():
    """El orchestrator asigna su DB a grupos sin DB propia."""
    db = AgenciaDB(":memory:")
    agent1 = _make_agent("rol_a")
    group = AgentGroup("sin_db", [agent1], mode="pipeline")
    assert group.db is None

    orchestrator = Orchestrator(db=db)
    orchestrator.register(group)
    assert group.db is db
