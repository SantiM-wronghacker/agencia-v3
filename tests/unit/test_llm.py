from unittest.mock import MagicMock, patch

import pytest

from llm.base import LLMUnavailableError
from llm.gemini import GeminiLLM
from llm.groq import GroqLLM
from llm.mistral import MistralLLM
from llm.ollama import OllamaLLM


# --- OllamaLLM ---

def test_ollama_is_available_when_running():
    mock_response = MagicMock()
    mock_response.status_code = 200
    with patch("llm.ollama.httpx.get", return_value=mock_response):
        llm = OllamaLLM(host="http://localhost:11434", model="mistral:7b")
        assert llm.is_available() is True


def test_ollama_unavailable_on_connection_error():
    with patch("llm.ollama.httpx.get", side_effect=Exception("connection refused")):
        llm = OllamaLLM(host="http://localhost:11434", model="mistral:7b")
        assert llm.is_available() is False


# --- GroqLLM ---

def test_groq_unavailable_without_key():
    with patch("llm.groq.settings") as mock_settings:
        mock_settings.GROQ_API_KEY = ""
        llm = GroqLLM()
        assert llm.is_available() is False


def test_groq_available_with_key():
    with patch("llm.groq.settings") as mock_settings:
        mock_settings.GROQ_API_KEY = "gsk_test_key"
        llm = GroqLLM()
        assert llm.is_available() is True


# --- GeminiLLM ---

def test_gemini_unavailable_without_key():
    with patch("llm.gemini.settings") as mock_settings:
        mock_settings.GEMINI_API_KEY = ""
        llm = GeminiLLM()
        assert llm.is_available() is False


def test_gemini_available_with_key():
    with patch("llm.gemini.settings") as mock_settings:
        mock_settings.GEMINI_API_KEY = "AIza_test_key"
        llm = GeminiLLM()
        assert llm.is_available() is True


# --- MistralLLM ---

def test_mistral_unavailable_without_key():
    with patch("llm.mistral.settings") as mock_settings:
        mock_settings.MISTRAL_API_KEY = ""
        llm = MistralLLM()
        assert llm.is_available() is False


def test_mistral_available_with_key():
    with patch("llm.mistral.settings") as mock_settings:
        mock_settings.MISTRAL_API_KEY = "test_mistral_key"
        llm = MistralLLM()
        assert llm.is_available() is True


# --- Router get_llm ---

def test_router_returns_ollama_when_provider_is_ollama():
    with patch("llm.settings") as mock_settings:
        mock_settings.LLM_PROVIDER = "ollama"
        from llm import get_llm
        llm = get_llm()
        assert isinstance(llm, OllamaLLM)


def test_router_auto_falls_back_to_ollama():
    """Con auto y todas las APIs sin key, debe retornar OllamaLLM si Ollama responde."""
    mock_response = MagicMock()
    mock_response.status_code = 200

    with patch("llm.settings") as mock_settings, \
         patch("llm.ollama.httpx.get", return_value=mock_response), \
         patch("llm.groq.settings") as groq_settings, \
         patch("llm.mistral.settings") as mistral_settings:

        mock_settings.LLM_PROVIDER = "auto"
        groq_settings.GROQ_API_KEY = ""
        mistral_settings.MISTRAL_API_KEY = ""

        from llm import get_llm
        llm = get_llm(task_type="general")
        assert isinstance(llm, OllamaLLM)
