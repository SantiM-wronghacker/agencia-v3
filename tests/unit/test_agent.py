from unittest.mock import MagicMock, patch

import pytest

from core.base import AgentResult, GroupResult
from core.group import AgentGroup


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_fake_llm(return_value: str = "respuesta de prueba", raises=None):
    fake_llm = MagicMock()
    fake_llm.provider_name = "fake"
    if raises:
        fake_llm.generate.side_effect = raises
    else:
        fake_llm.generate.return_value = return_value
    return fake_llm


def _make_agent(role: str = "test_role", return_value: str = "respuesta de prueba", raises=None):
    fake_llm = _make_fake_llm(return_value=return_value, raises=raises)
    with patch("core.agent.get_llm", return_value=fake_llm):
        from core.agent import BaseAgent
        agent = BaseAgent(role)
    return agent


# ---------------------------------------------------------------------------
# BaseAgent tests
# ---------------------------------------------------------------------------

def test_agent_loads_generic_prompt_when_no_template():
    from core.agent import BaseAgent
    with patch("core.agent.get_llm", return_value=_make_fake_llm()):
        agent = BaseAgent("rol_inexistente")
    assert "rol_inexistente" in agent.system_prompt


def test_agent_run_returns_agent_result():
    agent = _make_agent(role="analista", return_value="respuesta de prueba")
    result = agent.run("tarea de prueba")
    assert isinstance(result, AgentResult)
    assert result.success is True
    assert result.output == "respuesta de prueba"
    assert result.role == agent.role
    assert result.duration_ms >= 0


def test_agent_run_returns_failure_on_llm_error():
    from llm.base import LLMUnavailableError
    agent = _make_agent(raises=LLMUnavailableError("sin LLM"))
    result = agent.run("tarea de prueba")
    assert result.success is False
    assert result.error is not None


# ---------------------------------------------------------------------------
# AgentGroup tests
# ---------------------------------------------------------------------------

def test_group_pipeline_passes_output_as_input():
    agent1 = _make_agent(role="paso1", return_value="output_1")
    agent2 = _make_agent(role="paso2", return_value="output_2")

    group = AgentGroup("test", [agent1, agent2], mode="pipeline")
    result = group.execute("tarea inicial")

    assert result.steps[1].input == "output_1"


def test_group_pipeline_stops_on_failure():
    from llm.base import LLMUnavailableError
    agent1 = _make_agent(role="paso1", raises=LLMUnavailableError("fallo"))
    agent2 = _make_agent(role="paso2", return_value="nunca debería llegar")

    group = AgentGroup("test", [agent1, agent2], mode="pipeline")
    result = group.execute("tarea")

    assert len(result.steps) == 1
    assert result.success is False


def test_group_parallel_all_receive_same_input():
    agent1 = _make_agent(role="agente1", return_value="resp1")
    agent2 = _make_agent(role="agente2", return_value="resp2")

    group = AgentGroup("test", [agent1, agent2], mode="parallel")
    result = group.execute("tarea compartida")

    assert result.steps[0].input == "tarea compartida"
    assert result.steps[1].input == "tarea compartida"


def test_group_invalid_mode_raises_value_error():
    with pytest.raises(ValueError):
        AgentGroup("test", [], mode="invalido")
