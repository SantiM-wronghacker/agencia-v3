"""E2E test fixtures — require a running Ollama instance."""
from __future__ import annotations

import pytest

from memory.db import AgenciaDB


# ---------------------------------------------------------------------------
# Marker registration
# ---------------------------------------------------------------------------

def pytest_configure(config):
    config.addinivalue_line("markers", "e2e: end-to-end tests that require real infrastructure")
    config.addinivalue_line("markers", "requires_ollama: tests that require Ollama running locally")
    config.addinivalue_line("markers", "slow: tests that may take more than 30 seconds")


# ---------------------------------------------------------------------------
# Ollama availability
# ---------------------------------------------------------------------------

_PREFERRED_MODELS = ["llama3:8b", "gpt-oss:20b", "mistral:7b", "phi3:mini", "llama2:7b"]


@pytest.fixture(scope="session")
def check_ollama_available():
    """Skip the entire e2e session if Ollama is not reachable."""
    try:
        from llm.ollama import OllamaLLM
        llm = OllamaLLM()
        if not llm.is_available():
            pytest.skip("Ollama no disponible — omitiendo tests e2e")
        models = llm.list_models()
        if not models:
            pytest.skip("Ollama no tiene modelos descargados — omitiendo tests e2e")
    except Exception as exc:
        pytest.skip(f"Ollama no accesible: {exc}")


@pytest.fixture(scope="session")
def ollama_model(check_ollama_available) -> str:
    """Return the best available Ollama model name and configure settings to use it."""
    from llm.ollama import OllamaLLM
    from config.settings import settings

    available = OllamaLLM().list_models()
    chosen = available[0]
    for preferred in _PREFERRED_MODELS:
        if preferred in available:
            chosen = preferred
            break

    # Patch settings so all agents created during this session use the right model
    settings.OLLAMA_MODEL = chosen
    settings.LLM_PROVIDER = "ollama"

    return chosen


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def e2e_db(tmp_path_factory):
    """AgenciaDB backed by a real file for e2e tests."""
    db_path = tmp_path_factory.mktemp("e2e") / "e2e_test.db"
    return AgenciaDB(str(db_path))
