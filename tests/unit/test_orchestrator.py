"""Tests for core/orchestrator.py."""
from unittest.mock import MagicMock, patch

import pytest

from core.group import AgentGroup
from core.orchestrator import Orchestrator
from memory.db import AgenciaDB


def _make_agent(role: str = "test"):
    fake_llm = MagicMock()
    fake_llm.provider_name = "fake"
    fake_llm.generate.return_value = f"output of {role}"
    with patch("core.agent.get_llm", return_value=fake_llm):
        from core.agent import BaseAgent
        return BaseAgent(role)


# ---------------------------------------------------------------------------

def test_orchestrator_assigns_db_to_groups_without_db():
    db = AgenciaDB(":memory:")
    orchestrator = Orchestrator(db=db)
    group = AgentGroup("test", [], mode="pipeline")
    assert group.db is None
    orchestrator.register(group)
    assert group.db is db


def test_orchestrator_does_not_overwrite_existing_db():
    db1 = AgenciaDB(":memory:")
    db2 = AgenciaDB(":memory:")
    orchestrator = Orchestrator(db=db1)
    group = AgentGroup("test", [], mode="pipeline")
    group.db = db2
    orchestrator.register(group)
    # group already had a DB — must not be overwritten
    assert group.db is db2


def test_orchestrator_list_groups_includes_all_registered():
    orchestrator = Orchestrator()
    for name in ("alpha", "beta", "gamma"):
        orchestrator.register(AgentGroup(name, [], mode="pipeline"))
    groups = orchestrator.list_groups()
    assert len(groups) == 3
    names = {g["name"] for g in groups}
    assert names == {"alpha", "beta", "gamma"}


def test_orchestrator_list_groups_returns_correct_shape():
    orchestrator = Orchestrator()
    agent = _make_agent("rol1")
    orchestrator.register(AgentGroup("g1", [agent], mode="pipeline"))
    info = orchestrator.list_groups()[0]
    assert info["name"] == "g1"
    assert info["mode"] == "pipeline"
    assert info["agent_count"] == 1
    assert info["agent_roles"] == ["rol1"]


def test_orchestrator_run_unknown_group_raises_value_error():
    orchestrator = Orchestrator()
    with pytest.raises(ValueError, match="grupo_x"):
        orchestrator.run("grupo_x", "tarea")


def test_orchestrator_get_group_returns_none_for_unknown():
    orchestrator = Orchestrator()
    assert orchestrator.get_group("no_existe") is None


def test_orchestrator_get_group_returns_registered_group():
    orchestrator = Orchestrator()
    group = AgentGroup("existente", [], mode="pipeline")
    orchestrator.register(group)
    assert orchestrator.get_group("existente") is group
