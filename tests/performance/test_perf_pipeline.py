"""Performance (benchmark) tests — no external services required.

All tests are tagged @pytest.mark.slow so they can be skipped in fast CI runs:
    pytest -m "not slow" tests/unit/ tests/integration/
"""
from __future__ import annotations

import time
from datetime import datetime, timezone
from uuid import uuid4

import pytest

from memory.db import AgenciaDB
from memory.fts import FTSSearch
from memory.context import ContextMemory


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _populate_db(db: AgenciaDB, n: int, keyword: str = "marketing") -> tuple[str, str]:
    """Insert *n* observations tied to a single run/step. Returns (run_id, step_id)."""
    run_id = str(uuid4())
    step_id = str(uuid4())
    db.create_run(run_id, "perf_group", "pipeline", f"tarea de prueba de rendimiento")
    db.create_step(step_id, run_id, 0, "perf_agent", "input de prueba",
                   datetime.now(timezone.utc))
    db.complete_step(run_id, step_id, f"output de prueba", "fake", 1, True)
    for i in range(n):
        db.save_observation(
            run_id, step_id,
            f"Observación {i}: estrategia de {keyword} digital para empresa {i}",
            "output",
        )
    db.complete_run(run_id, "output final", n * 2, True)
    return run_id, step_id


# ---------------------------------------------------------------------------
# FTS performance
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_fts_search_performance_with_1000_observations(db):
    """FTS5 devuelve resultados en <100ms con 1000 observaciones."""
    _populate_db(db, 1000, keyword="marketing")

    start = time.perf_counter()
    results = FTSSearch(db).search("marketing")
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert isinstance(results, list)
    assert len(results) > 0
    assert elapsed_ms < 100, (
        f"FTS tardó demasiado: {elapsed_ms:.1f}ms (límite: 100ms)"
    )


@pytest.mark.slow
def test_fts_search_empty_query_is_fast(db):
    """FTS retorna lista vacía inmediatamente para query en blanco (<5ms)."""
    _populate_db(db, 500)
    start = time.perf_counter()
    results = FTSSearch(db).search("")
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert results == []
    assert elapsed_ms < 5


@pytest.mark.slow
def test_fts_search_by_role_performance(db):
    """FTS search_by_role filtra correctamente en <100ms."""
    _populate_db(db, 500, keyword="ventas")
    start = time.perf_counter()
    results = FTSSearch(db).search_by_role("ventas", "perf_agent")
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert isinstance(results, list)
    assert elapsed_ms < 100


# ---------------------------------------------------------------------------
# DB write throughput
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_db_write_100_runs_in_under_2s(db):
    """La DB puede registrar 100 runs completos en menos de 2 segundos."""
    start = time.perf_counter()
    for i in range(100):
        run_id = str(uuid4())
        step_id = str(uuid4())
        db.create_run(run_id, f"group_{i}", "pipeline", f"tarea {i}")
        db.create_step(step_id, run_id, 0, f"agent_{i}", f"input {i}",
                       datetime.now(timezone.utc))
        db.complete_step(run_id, step_id, f"output {i}", "fake", 50, True)
        db.complete_run(run_id, f"resultado {i}", 100, True)
    elapsed = time.perf_counter() - start
    assert elapsed < 2.0, f"100 runs tardaron {elapsed:.2f}s (límite: 2s)"


@pytest.mark.slow
def test_db_get_recent_runs_performance(db):
    """get_recent_runs() con 500 runs previos responde en <50ms."""
    for i in range(500):
        run_id = str(uuid4())
        db.create_run(run_id, "perf_group", "pipeline", f"tarea {i}")
        db.complete_run(run_id, f"output {i}", 100, True)

    start = time.perf_counter()
    runs = db.get_recent_runs(limit=10)
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert len(runs) == 10
    assert elapsed_ms < 50, f"get_recent_runs tardó {elapsed_ms:.1f}ms (límite: 50ms)"


# ---------------------------------------------------------------------------
# Context memory
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_context_memory_1000_entries_build_fast(db):
    """ContextMemory construye contexto de 1000 observaciones en <200ms."""
    run_id, step_id = _populate_db(db, 1000, keyword="contexto")

    ctx = ContextMemory(db)
    start = time.perf_counter()
    result = ctx.inject_context("perf_agent", "contexto digital")
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert isinstance(result, str)
    assert elapsed_ms < 200, (
        f"ContextMemory tardó {elapsed_ms:.1f}ms (límite: 200ms)"
    )


# ---------------------------------------------------------------------------
# Coverage gate (quality gate marcado explícitamente)
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_fts_no_results_for_nonexistent_term(db):
    """FTS retorna lista vacía para término inexistente, sin lanzar excepción."""
    _populate_db(db, 200, keyword="finanzas")
    results = FTSSearch(db).search("xyzzy_nonexistent_term_12345")
    assert results == []


@pytest.mark.slow
def test_db_observation_persists_and_is_searchable(db):
    """Una observación insertada es inmediatamente buscable via FTS."""
    run_id = str(uuid4())
    step_id = str(uuid4())
    db.create_run(run_id, "gate_group", "pipeline", "gate test")
    db.create_step(step_id, run_id, 0, "gate_agent", "gate input",
                   datetime.now(timezone.utc))
    db.complete_step(run_id, step_id, "gate output", "fake", 10, True)

    unique_term = f"zxqvortex_{uuid4().hex[:8]}"
    db.save_observation(run_id, step_id, f"Análisis de {unique_term} para el cliente", "output")

    results = FTSSearch(db).search(unique_term)
    assert len(results) >= 1
    assert unique_term in results[0]["content"]
