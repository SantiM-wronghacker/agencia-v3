"""Tests for tools/ infrastructure."""
from unittest.mock import MagicMock, patch

import pytest

from tools.base import BaseTool, ToolRegistry, ToolResult, tool
from tools.utils.http import HTTPClient
from tools.utils.text import extract_json, truncate


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_fake_llm(responses):
    """Returns a mock LLM whose generate() cycles through responses."""
    llm = MagicMock()
    llm.provider_name = "fake"
    if isinstance(responses, list):
        llm.generate.side_effect = responses
    else:
        llm.generate.return_value = responses
    return llm


def _make_agent(llm, tools=None):
    with patch("core.agent.get_llm", return_value=llm):
        from core.agent import BaseAgent
        return BaseAgent("test_role", tools=tools)


# ---------------------------------------------------------------------------
# ToolRegistry
# ---------------------------------------------------------------------------

def test_tool_registry_registers_tool():
    # Use a unique name to avoid cross-test pollution
    @tool
    class MyTool(BaseTool):
        name = "my_tool_registry_test"
        description = "test"

        def run(self, **kwargs) -> ToolResult:
            return self._success("ok")

    assert ToolRegistry.get("my_tool_registry_test") is MyTool


def test_tool_registry_list_all_includes_registered():
    @tool
    class ListedTool(BaseTool):
        name = "listed_tool_test"
        description = "listed desc"

        def run(self, **kwargs) -> ToolResult:
            return self._success("ok")

    names = [t["name"] for t in ToolRegistry.list_all()]
    assert "listed_tool_test" in names


def test_tool_registry_get_returns_none_for_unknown():
    assert ToolRegistry.get("totally_unknown_xyz") is None


# ---------------------------------------------------------------------------
# ToolResult
# ---------------------------------------------------------------------------

def test_tool_result_success():
    result = ToolResult(success=True, output="ok", tool_name="test")
    assert result.success is True
    assert result.output == "ok"
    assert result.tool_name == "test"


def test_tool_result_error():
    result = ToolResult(success=False, output="", error="fallo")
    assert result.success is False
    assert result.error == "fallo"


def test_base_tool_success_helper():
    class SimpleTool(BaseTool):
        name = "simple"
        description = "d"

        def run(self, **kwargs) -> ToolResult:
            return self._success("output", {"key": "value"})

    t = SimpleTool()
    r = t.run()
    assert r.success is True
    assert r.output == "output"
    assert r.raw_data == {"key": "value"}
    assert r.tool_name == "simple"


def test_base_tool_error_helper():
    class ErrTool(BaseTool):
        name = "err"
        description = "d"

        def run(self, **kwargs) -> ToolResult:
            return self._error("algo salió mal")

    r = ErrTool().run()
    assert r.success is False
    assert r.error == "algo salió mal"
    assert r.output == ""


# ---------------------------------------------------------------------------
# BaseAgent — no tools
# ---------------------------------------------------------------------------

def test_agent_with_no_tools_runs_normally():
    llm = _make_fake_llm("respuesta directa")
    agent = _make_agent(llm)
    result = agent.run("tarea")
    assert result.success is True
    assert result.tool_calls == []


# ---------------------------------------------------------------------------
# BaseAgent — with tools
# ---------------------------------------------------------------------------

def test_agent_detects_tool_call_in_output():
    class FakeSearch(BaseTool):
        name = "web_search"
        description = "busca en la web"

        def run(self, query: str = "", **kwargs) -> ToolResult:
            return self._success(f"Resultados para: {query}")

    llm = _make_fake_llm([
        '{"use_tool": "web_search", "args": {"query": "test"}}',
        "respuesta final sin tool",
    ])
    agent = _make_agent(llm, tools=[FakeSearch()])
    result = agent.run("busca info sobre X")
    assert result.success is True
    assert len(result.tool_calls) == 1
    assert result.tool_calls[0].tool_name == "web_search"


def test_agent_respects_max_tool_calls():
    class LoopTool(BaseTool):
        name = "loop_tool"
        description = "tool que siempre se llama"

        def run(self, **kwargs) -> ToolResult:
            return self._success("resultado")

    # LLM always returns a tool call JSON — never a final answer
    always_tool = '{"use_tool": "loop_tool", "args": {}}'
    llm = _make_fake_llm([always_tool] * 10)
    agent = _make_agent(llm, tools=[LoopTool()])
    result = agent.run("tarea")
    # MAX_TOOL_CALLS = 3, so at most 3 tool calls recorded
    assert len(result.tool_calls) <= 3


def test_agent_handles_tool_failure_gracefully():
    class FailTool(BaseTool):
        name = "fail_tool"
        description = "tool que siempre falla"

        def run(self, **kwargs) -> ToolResult:
            return self._error("fallo interno")

    llm = _make_fake_llm([
        '{"use_tool": "fail_tool", "args": {}}',
        "respuesta final después del fallo",
    ])
    agent = _make_agent(llm, tools=[FailTool()])
    result = agent.run("tarea")
    # Agent must still complete successfully
    assert result.success is True
    assert len(result.tool_calls) == 1
    assert result.tool_calls[0].result.success is False


def test_agent_tool_not_found_returns_error_result():
    llm = _make_fake_llm([
        '{"use_tool": "nonexistent_tool", "args": {}}',
        "respuesta final",
    ])
    agent = _make_agent(llm, tools=[])  # no tools registered
    result = agent.run("tarea")
    assert result.success is True
    assert len(result.tool_calls) == 1
    assert result.tool_calls[0].result.success is False
    assert "no disponible" in result.tool_calls[0].result.error


# ---------------------------------------------------------------------------
# HTTPClient
# ---------------------------------------------------------------------------

def test_http_client_returns_none_on_error():
    client = HTTPClient("http://localhost:9999")
    result = client.get("/nonexistent")
    assert result is None


def test_http_client_post_returns_none_on_error():
    client = HTTPClient("http://localhost:9999")
    result = client.post("/nonexistent", json={"key": "val"})
    assert result is None


# ---------------------------------------------------------------------------
# text utils
# ---------------------------------------------------------------------------

def test_text_truncate_shortens():
    assert truncate("hello world", 5) == "he..."


def test_text_truncate_no_op_when_short():
    assert truncate("hi", 10) == "hi"


def test_text_truncate_exact_length():
    assert truncate("abc", 3) == "abc"


def test_extract_json_finds_json_in_text():
    text = 'aquí hay texto {"key": "value"} y más texto'
    result = extract_json(text)
    assert result == {"key": "value"}


def test_extract_json_returns_none_when_no_json():
    assert extract_json("texto sin json") is None


def test_extract_json_returns_none_on_invalid_json():
    assert extract_json("{ invalid json }") is None


def test_extract_json_handles_nested():
    text = '{"use_tool": "search", "args": {"q": "test"}}'
    result = extract_json(text)
    assert result["use_tool"] == "search"
    assert result["args"]["q"] == "test"
