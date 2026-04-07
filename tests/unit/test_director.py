"""Tests for core/director.py — ROLES dict and agent construction."""
from unittest.mock import MagicMock, patch

import pytest

from core.director import ROLES, _build_agents

_VALID_TASK_TYPES = {"reasoning", "general", "long_doc", "simple"}


def test_director_has_all_six_roles():
    assert set(ROLES.keys()) == {"strategy", "finance", "legal", "marketing", "tech", "ops"}


def test_director_roles_have_required_fields():
    for name, info in ROLES.items():
        assert "emoji" in info, f"Rol '{name}' sin emoji"
        assert "desc" in info, f"Rol '{name}' sin desc"
        assert "task_type" in info, f"Rol '{name}' sin task_type"


def test_director_task_types_are_valid():
    for name, info in ROLES.items():
        assert info["task_type"] in _VALID_TASK_TYPES, (
            f"Rol '{name}' tiene task_type inválido: {info['task_type']!r}"
        )


def test_director_creates_agent_per_role():
    fake_llm = MagicMock()
    fake_llm.provider_name = "fake"
    fake_llm.generate.return_value = "ok"
    with patch("core.agent.get_llm", return_value=fake_llm):
        agents = _build_agents()
    assert set(agents.keys()) == set(ROLES.keys())


def test_director_agent_roles_match_keys():
    fake_llm = MagicMock()
    fake_llm.provider_name = "fake"
    fake_llm.generate.return_value = "ok"
    with patch("core.agent.get_llm", return_value=fake_llm):
        agents = _build_agents()
    for rol, agent in agents.items():
        assert agent.role == rol


def test_director_reasoning_roles_use_correct_task_type():
    assert ROLES["strategy"]["task_type"] == "reasoning"
    assert ROLES["finance"]["task_type"] == "reasoning"
    assert ROLES["tech"]["task_type"] == "reasoning"


def test_director_legal_uses_long_doc():
    assert ROLES["legal"]["task_type"] == "long_doc"


def test_director_ops_and_marketing_use_general():
    assert ROLES["ops"]["task_type"] == "general"
    assert ROLES["marketing"]["task_type"] == "general"
