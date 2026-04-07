"""Extended tests for memory/context.py and memory/fts.py."""
from datetime import datetime, timezone

import pytest

from memory.context import ContextMemory
from memory.db import AgenciaDB
from memory.fts import FTSSearch


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _insert_observation(db: AgenciaDB, run_id: str, step_id: str,
                         role: str, group: str, content: str) -> None:
    ts = datetime.now(timezone.utc)
    db.create_run(run_id, group, "pipeline", "tarea de prueba")
    db.create_step(step_id, run_id, 0, role, "tarea de prueba", ts)
    db.complete_step(run_id, step_id, content, "fake", 100, True)
    db.save_observation(run_id, step_id, content)
    db.complete_run(run_id, content, 100, True)


# ---------------------------------------------------------------------------
# inject_context — truncation
# ---------------------------------------------------------------------------

def test_inject_context_truncates_at_max_chars():
    db = AgenciaDB(":memory:")
    # Insert 10 long observations (500 chars each) for the same role
    long_content = "análisis financiero " * 25  # ~500 chars, FTS-searchable
    for i in range(10):
        _insert_observation(
            db, f"run-trunc-{i}", f"step-trunc-{i}",
            "strategy", "test_group", long_content.strip()
        )

    memory = ContextMemory(db)
    context = memory.inject_context("strategy", "análisis financiero", max_chars=500)
    assert len(context) <= 500


def test_inject_context_empty_when_no_match():
    db = AgenciaDB(":memory:")
    _insert_observation(
        db, "run-nm-1", "step-nm-1",
        "strategy", "test_group", "marketing digital avanzado"
    )
    memory = ContextMemory(db)
    # FTS query for completely unrelated term
    context = memory.inject_context("strategy", "xyzzy123")
    assert context == ""


def test_inject_context_returns_string():
    db = AgenciaDB(":memory:")
    _insert_observation(
        db, "run-s1", "step-s1",
        "strategy", "grp", "plan estratégico de expansión"
    )
    memory = ContextMemory(db)
    result = memory.inject_context("strategy", "plan estratégico")
    assert isinstance(result, str)
    assert len(result) > 0


# ---------------------------------------------------------------------------
# inject_context — role filter
# ---------------------------------------------------------------------------

def test_inject_context_role_filter_works():
    db = AgenciaDB(":memory:")

    # Insert 5 strategy observations with unique marker
    for i in range(5):
        _insert_observation(
            db, f"run-strat-{i}", f"step-strat-{i}",
            "strategy", "test_group",
            f"STRATEGY_MARKER ventas estratégicas número {i}"
        )

    # Insert 5 finance observations with different marker
    for i in range(5):
        _insert_observation(
            db, f"run-fin-{i}", f"step-fin-{i}",
            "finance", "test_group",
            f"FINANCE_MARKER ventas financieras número {i}"
        )

    memory = ContextMemory(db)
    context = memory.inject_context("strategy", "ventas")

    # strategy results fill the limit of 5 — no fallback to finance
    assert "STRATEGY_MARKER" in context
    assert "FINANCE_MARKER" not in context


# ---------------------------------------------------------------------------
# FTSSearch — search_by_role
# ---------------------------------------------------------------------------

def test_fts_search_by_role_filters_correctly():
    db = AgenciaDB(":memory:")

    # finance observations
    for i in range(3):
        _insert_observation(
            db, f"run-fts-f{i}", f"step-fts-f{i}",
            "finance", "grp", f"análisis de ventas financieras {i}"
        )
    # strategy observations
    for i in range(3):
        _insert_observation(
            db, f"run-fts-s{i}", f"step-fts-s{i}",
            "strategy", "grp", f"análisis de ventas estratégicas {i}"
        )

    results = FTSSearch(db).search_by_role("ventas", "finance", limit=5)
    assert len(results) > 0
    for r in results:
        assert r["agent_role"] == "finance"


def test_fts_search_by_role_empty_query_returns_empty():
    db = AgenciaDB(":memory:")
    results = FTSSearch(db).search_by_role("", "finance", limit=5)
    assert results == []


def test_fts_search_by_role_unknown_role_returns_empty():
    db = AgenciaDB(":memory:")
    _insert_observation(
        db, "run-fts-u1", "step-fts-u1",
        "strategy", "grp", "ventas estratégicas"
    )
    results = FTSSearch(db).search_by_role("ventas", "rol_inexistente", limit=5)
    assert results == []


def test_fts_general_search_returns_all_roles():
    db = AgenciaDB(":memory:")
    _insert_observation(db, "run-a1", "step-a1", "finance", "grp", "ventas financieras")
    _insert_observation(db, "run-b1", "step-b1", "strategy", "grp", "ventas estratégicas")

    results = FTSSearch(db).search("ventas", limit=10)
    roles = {r["agent_role"] for r in results}
    assert "finance" in roles
    assert "strategy" in roles
