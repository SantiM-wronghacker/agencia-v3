"""Extended tests for LLM providers — all HTTP/API calls mocked."""
from unittest.mock import MagicMock, patch

import pytest

from llm.base import LLMUnavailableError
from llm.ollama import OllamaLLM
from llm.groq import GroqLLM
from llm.gemini import GeminiLLM
from llm.mistral import MistralLLM
from llm import get_llm


# ---------------------------------------------------------------------------
# OllamaLLM
# ---------------------------------------------------------------------------

def test_ollama_list_models_returns_list():
    model1 = MagicMock()
    model1.model = "mistral:7b"
    model2 = MagicMock()
    model2.model = "llama3:8b"
    mock_list_resp = MagicMock()
    mock_list_resp.models = [model1, model2]

    with patch("llm.ollama.ollama_client.Client") as MockClient:
        MockClient.return_value.list.return_value = mock_list_resp
        llm = OllamaLLM()
        models = llm.list_models()

    assert "mistral:7b" in models
    assert "llama3:8b" in models
    assert len(models) == 2


def test_ollama_generate_returns_string():
    mock_response = MagicMock()
    mock_response.message.content = "texto generado"

    with patch("llm.ollama.ollama_client.Client") as MockClient:
        MockClient.return_value.chat.return_value = mock_response
        llm = OllamaLLM()
        result = llm.generate("system prompt", "user message")

    assert result == "texto generado"


def test_ollama_generate_raises_llm_unavailable_on_error():
    with patch("llm.ollama.ollama_client.Client") as MockClient:
        MockClient.return_value.chat.side_effect = Exception("connection refused")
        llm = OllamaLLM()
        with pytest.raises(LLMUnavailableError):
            llm.generate("system", "user")


def test_ollama_is_available_false_on_connection_error():
    with patch("llm.ollama.httpx.get", side_effect=Exception("connection refused")):
        llm = OllamaLLM()
        assert llm.is_available() is False


def test_ollama_list_models_returns_empty_on_error():
    with patch("llm.ollama.ollama_client.Client") as MockClient:
        MockClient.return_value.list.side_effect = Exception("error")
        llm = OllamaLLM()
        assert llm.list_models() == []


# ---------------------------------------------------------------------------
# GroqLLM
# ---------------------------------------------------------------------------

def test_groq_generate_returns_string():
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "respuesta groq"

    with patch("llm.groq.Groq") as MockGroq:
        MockGroq.return_value.chat.completions.create.return_value = mock_response
        llm = GroqLLM()
        result = llm.generate("system", "user")

    assert result == "respuesta groq"


def test_groq_generate_raises_on_api_error():
    with patch("llm.groq.Groq") as MockGroq:
        MockGroq.return_value.chat.completions.create.side_effect = Exception("api error")
        llm = GroqLLM()
        with pytest.raises(LLMUnavailableError):
            llm.generate("s", "u")


def test_groq_uses_correct_model():
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "ok"

    with patch("llm.groq.Groq") as MockGroq:
        mock_create = MockGroq.return_value.chat.completions.create
        mock_create.return_value = mock_response
        llm = GroqLLM()
        llm.generate("sys", "usr")
        call_kwargs = mock_create.call_args

    assert call_kwargs[1]["model"] == "llama-3.3-70b-versatile"


# ---------------------------------------------------------------------------
# GeminiLLM
# ---------------------------------------------------------------------------

def test_gemini_generate_returns_string():
    mock_response = MagicMock()
    mock_response.text = "respuesta gemini"

    with patch("llm.gemini.genai.Client") as MockClient:
        MockClient.return_value.models.generate_content.return_value = mock_response
        llm = GeminiLLM()
        result = llm.generate("system", "user")

    assert isinstance(result, str)
    assert result == "respuesta gemini"


def test_gemini_generate_raises_on_error():
    with patch("llm.gemini.genai.Client") as MockClient:
        MockClient.return_value.models.generate_content.side_effect = Exception("quota exceeded")
        llm = GeminiLLM()
        with pytest.raises(LLMUnavailableError):
            llm.generate("s", "u")


# ---------------------------------------------------------------------------
# MistralLLM
# ---------------------------------------------------------------------------

def test_mistral_generate_returns_string():
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "respuesta mistral"

    with patch("llm.mistral.Mistral") as MockMistral:
        MockMistral.return_value.chat.complete.return_value = mock_response
        llm = MistralLLM()
        result = llm.generate("s", "u")

    assert result == "respuesta mistral"


def test_mistral_generate_raises_on_error():
    with patch("llm.mistral.Mistral") as MockMistral:
        MockMistral.return_value.chat.complete.side_effect = Exception("api error")
        llm = MistralLLM()
        with pytest.raises(LLMUnavailableError):
            llm.generate("s", "u")


# ---------------------------------------------------------------------------
# Router (llm/__init__.py)
# ---------------------------------------------------------------------------

def test_router_auto_uses_groq_for_reasoning():
    from config.settings import settings

    with patch.object(settings, "LLM_PROVIDER", "auto"):
        with patch("llm.GroqLLM") as MockGroq, \
             patch("llm.OllamaLLM") as MockOllama, \
             patch("llm.GeminiLLM") as MockGemini, \
             patch("llm.MistralLLM") as MockMistral:

            groq_inst = MagicMock()
            groq_inst.is_available.return_value = True
            groq_inst.provider_name = "groq"
            MockGroq.return_value = groq_inst

            ollama_inst = MagicMock()
            ollama_inst.is_available.return_value = True
            ollama_inst.provider_name = "ollama"
            MockOllama.return_value = ollama_inst

            MockGemini.return_value.is_available.return_value = False
            MockMistral.return_value.is_available.return_value = False

            result = get_llm(task_type="reasoning")

    assert result.provider_name == "groq"


def test_router_auto_uses_gemini_for_long_doc():
    from config.settings import settings

    with patch.object(settings, "LLM_PROVIDER", "auto"):
        with patch("llm.GroqLLM") as MockGroq, \
             patch("llm.OllamaLLM") as MockOllama, \
             patch("llm.GeminiLLM") as MockGemini, \
             patch("llm.MistralLLM") as MockMistral:

            gemini_inst = MagicMock()
            gemini_inst.is_available.return_value = True
            gemini_inst.provider_name = "gemini"
            MockGemini.return_value = gemini_inst

            MockGroq.return_value.is_available.return_value = False
            MockOllama.return_value.is_available.return_value = False
            MockMistral.return_value.is_available.return_value = False

            result = get_llm(task_type="long_doc")

    assert result.provider_name == "gemini"
