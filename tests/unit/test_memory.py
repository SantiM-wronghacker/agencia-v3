from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from memory.db import AgenciaDB
from memory.fts import FTSSearch
from memory.context import ContextMemory


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _populated_db() -> tuple[AgenciaDB, str, str]:
    """Returns (db, run_id, step_id) with one full observation inserted."""
    db = AgenciaDB(":memory:")
    run_id = "run-fts-1"
    step_id = "step-fts-1"
    ts = datetime.now(timezone.utc)

    db.create_run(run_id, "test_group", "pipeline", "tarea fts")
    db.create_step(step_id, run_id, 0, "strategy", "tarea fts", ts)
    db.complete_step(run_id, step_id, "análisis financiero de ventas Q3", "fake", 100, True)
    db.save_observation(run_id, step_id, "análisis financiero de ventas Q3")
    db.complete_run(run_id, "análisis financiero de ventas Q3", 100, True)
    return db, run_id, step_id


# ---------------------------------------------------------------------------
# AgenciaDB tests
# ---------------------------------------------------------------------------

def test_db_initializes_schema():
    db = AgenciaDB(":memory:")
    with db._connect() as conn:
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = {row[0] for row in cur.fetchall()}
    assert "runs" in tables
    assert "steps" in tables
    assert "observations" in tables


def test_create_and_complete_run():
    db = AgenciaDB(":memory:")
    db.create_run("run-1", "test_group", "pipeline", "tarea de prueba")

    run = db.get_run("run-1")
    assert run is not None
    assert run["status"] == "running"

    db.complete_run("run-1", "output final", 1500, True)
    run = db.get_run("run-1")
    assert run["status"] == "completed"
    assert run["success"] == 1


# ---------------------------------------------------------------------------
# FTSSearch tests
# ---------------------------------------------------------------------------

def test_fts_search_finds_relevant_content():
    db, _, _ = _populated_db()
    results = FTSSearch(db).search("financiero ventas")
    assert len(results) > 0
    assert "financiero" in results[0]["content"].lower()


def test_fts_search_empty_query_returns_empty():
    db, _, _ = _populated_db()
    results = FTSSearch(db).search("")
    assert results == []


# ---------------------------------------------------------------------------
# ContextMemory tests
# ---------------------------------------------------------------------------

def test_context_injection_returns_empty_when_no_history():
    db = AgenciaDB(":memory:")
    memory = ContextMemory(db)
    context = memory.inject_context("strategy", "plan de negocio")
    assert context == ""


def test_context_injection_returns_relevant_content():
    db = AgenciaDB(":memory:")
    run_id = "run-ctx-1"
    step_id = "step-ctx-1"
    ts = datetime.now(timezone.utc)

    db.create_run(run_id, "test_group", "pipeline", "tarea ctx")
    db.create_step(step_id, run_id, 0, "strategy", "tarea ctx", ts)
    db.complete_step(run_id, step_id, "estrategia de expansión para mercado B2B", "fake", 100, True)
    db.save_observation(run_id, step_id, "estrategia de expansión para mercado B2B")
    db.complete_run(run_id, "ok", 100, True)

    memory = ContextMemory(db)
    context = memory.inject_context("strategy", "estrategia expansión")
    assert context != ""
    assert "expansión" in context or "estrategia" in context


# ---------------------------------------------------------------------------
# BaseAgent + DB integration
# ---------------------------------------------------------------------------

def test_agent_saves_to_db_when_db_provided():
    db = AgenciaDB(":memory:")

    fake_llm = MagicMock()
    fake_llm.provider_name = "fake"
    fake_llm.generate.return_value = "respuesta guardada"

    with patch("core.agent.get_llm", return_value=fake_llm):
        from core.agent import BaseAgent
        agent = BaseAgent("test_role", db=db)

    result = agent.run("tarea de prueba")
    assert result.success is True

    runs = db.get_recent_runs()
    assert len(runs) >= 1
    assert runs[0]["group_name"] == "test_role"
