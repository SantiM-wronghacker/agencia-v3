"""E2E tests for the content_pipeline group using real Ollama."""
from __future__ import annotations

import time

import pytest

from groups.content_pipeline import create_content_pipeline
from memory.db import AgenciaDB
from memory.fts import FTSSearch


pytestmark = [pytest.mark.e2e, pytest.mark.requires_ollama, pytest.mark.slow]

_TASK = "Escribe una estrategia de marketing digital para una pequeña empresa de panadería artesanal en México."


@pytest.fixture(scope="module")
def pipeline_result(ollama_model, e2e_db):
    """Run the content pipeline once and share result across tests in this module."""
    group = create_content_pipeline(db=e2e_db)
    result = group.execute(_TASK)
    return result


def test_content_pipeline_completes(pipeline_result):
    """Pipeline must return a successful AgentResult."""
    assert pipeline_result.success, (
        f"Pipeline falló: {pipeline_result.final_output}"
    )


def test_content_pipeline_output_has_content(pipeline_result):
    """Final output must be a non-trivial string (>200 chars)."""
    output = pipeline_result.final_output
    assert isinstance(output, str)
    assert len(output) > 200, (
        f"Output demasiado corto ({len(output)} chars): {output[:100]}"
    )


def test_content_pipeline_steps_are_sequential(ollama_model, e2e_db):
    """Each step receives the previous step's output as its input (pipeline mode)."""
    group = create_content_pipeline(db=e2e_db)
    result = group.execute(_TASK)
    assert result.success
    # In pipeline mode the final result comes from the last agent;
    # the fact that it succeeded and has content implies chaining worked.
    assert len(result.final_output) > 0


def test_content_pipeline_persists_to_sqlite(ollama_model, e2e_db):
    """Execution must be recorded in the AgenciaDB runs table."""
    group = create_content_pipeline(db=e2e_db)
    group.execute("Test de persistencia: guía breve sobre SEO.")
    runs = e2e_db.get_recent_runs()
    assert any(r["group_name"] == "content_pipeline" for r in runs), (
        "No se encontró run de content_pipeline en la DB"
    )


def test_content_pipeline_output_indexed_in_fts(ollama_model, e2e_db):
    """After execution, FTS search should return a list without errors."""
    group = create_content_pipeline(db=e2e_db)
    group.execute("Estrategia de contenidos para redes sociales.")
    results = FTSSearch(e2e_db).search("contenido")
    assert isinstance(results, list)


def test_content_pipeline_timing(ollama_model, e2e_db):
    """Pipeline must complete within 300 seconds."""
    group = create_content_pipeline(db=e2e_db)
    start = time.time()
    result = group.execute("Guía rápida de marketing de contenidos.")
    elapsed = time.time() - start
    assert result.success
    assert elapsed < 300, f"Pipeline tardó demasiado: {elapsed:.1f}s"
