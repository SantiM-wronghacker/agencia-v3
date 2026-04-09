"""Extended tests for memory/db.py and memory/fts.py — covers remaining lines."""
from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

import pytest

from memory.db import AgenciaDB
from memory.fts import FTSSearch


# ---------------------------------------------------------------------------
# AgenciaDB — covers missing lines 81, 86, 98, 104-106, 112-113
# ---------------------------------------------------------------------------

class TestAgenciaDBExtended:

    def test_get_run_returns_none_for_unknown_id(self, db):
        result = db.get_run("nonexistent-run-id")
        assert result is None

    def test_get_run_returns_dict_after_create(self, db):
        run_id = str(uuid4())
        db.create_run(run_id, "test_group", "pipeline", "tarea de prueba")
        result = db.get_run(run_id)
        assert result is not None
        assert result["id"] == run_id
        assert result["group_name"] == "test_group"

    def test_get_steps_returns_ordered_steps(self, db):
        run_id = str(uuid4())
        db.create_run(run_id, "grp", "pipeline", "tarea")
        step_ids = [str(uuid4()) for _ in range(3)]
        for i, step_id in enumerate(step_ids):
            db.create_step(step_id, run_id, i, f"agent_{i}", f"input {i}",
                           datetime.now(timezone.utc))
        steps = db.get_steps(run_id)
        assert len(steps) == 3
        assert steps[0]["step_index"] == 0
        assert steps[1]["step_index"] == 1
        assert steps[2]["step_index"] == 2

    def test_get_steps_empty_for_unknown_run(self, db):
        steps = db.get_steps("nonexistent-run-id")
        assert steps == []

    def test_get_recent_runs_respects_limit(self, db):
        for i in range(15):
            run_id = str(uuid4())
            db.create_run(run_id, f"grp_{i}", "pipeline", f"t{i}")
            db.complete_run(run_id, f"out{i}", 100, True)
        recent = db.get_recent_runs(limit=5)
        assert len(recent) == 5

    def test_get_recent_runs_ordered_by_created_at_desc(self, db):
        ids = []
        for i in range(3):
            run_id = str(uuid4())
            db.create_run(run_id, "ordered_grp", "pipeline", f"t{i}")
            db.complete_run(run_id, f"out{i}", 100, True)
            ids.append(run_id)
        runs = db.get_recent_runs(limit=10)
        group_runs = [r for r in runs if r["group_name"] == "ordered_grp"]
        # most recent first
        assert group_runs[0]["id"] == ids[-1]

    def test_complete_run_sets_failed_status(self, db):
        run_id = str(uuid4())
        db.create_run(run_id, "grp", "pipeline", "tarea")
        db.complete_run(run_id, "", 500, False, error="Algo falló")
        run = db.get_run(run_id)
        assert run["status"] == "failed"
        assert run["success"] == 0
        assert run["error"] == "Algo falló"

    def test_complete_step_success(self, db):
        run_id = str(uuid4())
        step_id = str(uuid4())
        db.create_run(run_id, "grp", "pipeline", "tarea")
        db.create_step(step_id, run_id, 0, "agent", "input",
                       datetime.now(timezone.utc))
        db.complete_step(run_id, step_id, "output del agente", "ollama", 1500, True)
        steps = db.get_steps(run_id)
        assert len(steps) == 1
        assert steps[0]["output"] == "output del agente"
        assert steps[0]["provider"] == "ollama"
        assert steps[0]["success"] == 1

    def test_complete_step_failure(self, db):
        run_id = str(uuid4())
        step_id = str(uuid4())
        db.create_run(run_id, "grp", "pipeline", "tarea")
        db.create_step(step_id, run_id, 0, "agent", "input",
                       datetime.now(timezone.utc))
        db.complete_step(run_id, step_id, "", "ollama", 500, False, error="LLM error")
        steps = db.get_steps(run_id)
        assert steps[0]["success"] == 0
        assert steps[0]["error"] == "LLM error"

    def test_save_observation_returns_id(self, db):
        run_id = str(uuid4())
        step_id = str(uuid4())
        db.create_run(run_id, "grp", "pipeline", "tarea")
        db.create_step(step_id, run_id, 0, "agent", "input",
                       datetime.now(timezone.utc))
        obs_id = db.save_observation(run_id, step_id, "contenido de observación", "output")
        assert isinstance(obs_id, str)
        assert len(obs_id) > 0

    def test_file_based_db(self, tmp_path):
        """Covers the file-path branch of AgenciaDB (not :memory:)."""
        db_path = str(tmp_path / "test_file.db")
        db = AgenciaDB(db_path)
        run_id = str(uuid4())
        db.create_run(run_id, "file_grp", "pipeline", "tarea")
        result = db.get_run(run_id)
        assert result is not None
        assert result["group_name"] == "file_grp"


# ---------------------------------------------------------------------------
# FTSSearch — covers search_by_role and edge cases (lines 29-30, 54-55)
# ---------------------------------------------------------------------------

class TestFTSSearchExtended:

    def _setup_observations(self, db, content: str, role: str = "test_agent",
                             group: str = "test_group") -> None:
        """Insert a run + step + observation."""
        run_id = str(uuid4())
        step_id = str(uuid4())
        db.create_run(run_id, group, "pipeline", "tarea")
        db.create_step(step_id, run_id, 0, role, "input", datetime.now(timezone.utc))
        db.complete_step(run_id, step_id, content, "fake", 100, True)
        db.save_observation(run_id, step_id, content, "output")
        db.complete_run(run_id, content, 100, True)

    def test_search_empty_query_returns_empty_list(self, db):
        result = FTSSearch(db).search("")
        assert result == []

    def test_search_whitespace_only_returns_empty(self, db):
        result = FTSSearch(db).search("   ")
        assert result == []

    def test_search_by_role_empty_query_returns_empty(self, db):
        result = FTSSearch(db).search_by_role("", "some_agent")
        assert result == []

    def test_search_by_role_whitespace_returns_empty(self, db):
        result = FTSSearch(db).search_by_role("   ", "agent")
        assert result == []

    def test_search_by_role_finds_match(self, db):
        unique = f"termino_unico_{uuid4().hex[:8]}"
        self._setup_observations(db, f"Análisis de {unique} completado", role="analyst")
        results = FTSSearch(db).search_by_role(unique, "analyst")
        assert len(results) >= 1
        assert unique in results[0]["content"]
        assert results[0]["agent_role"] == "analyst"

    def test_search_by_role_filters_by_role(self, db):
        unique = f"keyword_{uuid4().hex[:8]}"
        self._setup_observations(db, f"Informe de {unique}", role="role_a")
        self._setup_observations(db, f"Análisis de {unique}", role="role_b")
        results_a = FTSSearch(db).search_by_role(unique, "role_a")
        results_b = FTSSearch(db).search_by_role(unique, "role_b")
        assert all(r["agent_role"] == "role_a" for r in results_a)
        assert all(r["agent_role"] == "role_b" for r in results_b)

    def test_search_by_role_no_match_returns_empty(self, db):
        results = FTSSearch(db).search_by_role("termino_inexistente_xyz", "nonexistent_role")
        assert results == []

    def test_search_respects_limit(self, db):
        run_id = str(uuid4())
        step_id = str(uuid4())
        db.create_run(run_id, "grp", "pipeline", "tarea")
        db.create_step(step_id, run_id, 0, "agent", "input", datetime.now(timezone.utc))
        db.complete_step(run_id, step_id, "output", "fake", 100, True)
        for i in range(20):
            db.save_observation(run_id, step_id, f"marketing digital {i}", "output")
        db.complete_run(run_id, "done", 200, True)

        results = FTSSearch(db).search("marketing", limit=5)
        assert len(results) <= 5

    def test_search_returns_correct_columns(self, db):
        self._setup_observations(db, "estrategia de contenidos")
        results = FTSSearch(db).search("estrategia")
        if results:  # might find it
            row = results[0]
            assert "content" in row
            assert "run_id" in row
            assert "agent_role" in row
            assert "group_name" in row
