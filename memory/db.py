import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

from config.settings import settings

_SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
  id TEXT PRIMARY KEY,
  group_name TEXT NOT NULL,
  mode TEXT,
  status TEXT NOT NULL DEFAULT 'running',
  input_summary TEXT,
  final_output TEXT,
  total_duration_ms INTEGER,
  success INTEGER,
  error TEXT,
  created_at TEXT NOT NULL,
  completed_at TEXT
);

CREATE TABLE IF NOT EXISTS steps (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(id),
  step_index INTEGER NOT NULL,
  agent_role TEXT NOT NULL,
  input TEXT NOT NULL,
  output TEXT,
  provider TEXT,
  duration_ms INTEGER,
  success INTEGER NOT NULL,
  error TEXT,
  timestamp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS observations (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(id),
  step_id TEXT REFERENCES steps(id),
  content TEXT NOT NULL,
  type TEXT NOT NULL DEFAULT 'output',
  timestamp TEXT NOT NULL
);

CREATE VIRTUAL TABLE IF NOT EXISTS observations_fts
USING fts5(content, content='observations', content_rowid='rowid');

CREATE TRIGGER IF NOT EXISTS obs_ai AFTER INSERT ON observations BEGIN
  INSERT INTO observations_fts(rowid, content) VALUES (new.rowid, new.content);
END;

CREATE TRIGGER IF NOT EXISTS obs_ad AFTER DELETE ON observations BEGIN
  INSERT INTO observations_fts(observations_fts, rowid, content)
  VALUES('delete', old.rowid, old.content);
END;
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _row_to_dict(cursor: sqlite3.Cursor, row: tuple) -> dict:
    return {col[0]: val for col, val in zip(cursor.description, row)}


class _NoCloseConnection:
    """Wraps a persistent connection so `with` blocks commit but don't close it."""

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def __enter__(self) -> sqlite3.Connection:
        return self._conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._conn.commit()
        else:
            self._conn.rollback()
        return False

    # Forward attribute access so callers can use execute/executescript directly
    def __getattr__(self, name):
        return getattr(self._conn, name)


class AgenciaDB:
    def __init__(self, db_path: str = None):
        self.db_path = db_path if db_path is not None else settings.DB_PATH
        self._persistent_conn: sqlite3.Connection | None = None
        if self.db_path == ":memory:":
            # Keep a single connection so the in-memory DB survives across calls
            self._persistent_conn = sqlite3.connect(":memory:", check_same_thread=False)
            self._persistent_conn.execute("PRAGMA foreign_keys = ON")
        else:
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        if self._persistent_conn is not None:
            return _NoCloseConnection(self._persistent_conn)
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_schema(self):
        if self._persistent_conn is not None:
            self._persistent_conn.executescript(_SCHEMA)
        else:
            with self._connect() as conn:
                conn.executescript(_SCHEMA)

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def create_run(
        self, run_id: str, group_name: str, mode: str, input_summary: str
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO runs (id, group_name, mode, status, input_summary, created_at)
                VALUES (?, ?, ?, 'running', ?, ?)
                """,
                (run_id, group_name, mode, input_summary, _now()),
            )

    def complete_run(
        self,
        run_id: str,
        final_output: str,
        total_duration_ms: int,
        success: bool,
        error: str = None,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE runs
                SET status = ?,
                    final_output = ?,
                    total_duration_ms = ?,
                    success = ?,
                    error = ?,
                    completed_at = ?
                WHERE id = ?
                """,
                (
                    "completed" if success else "failed",
                    final_output,
                    total_duration_ms,
                    1 if success else 0,
                    error,
                    _now(),
                    run_id,
                ),
            )

    def create_step(
        self,
        step_id: str,
        run_id: str,
        step_index: int,
        agent_role: str,
        input: str,
        timestamp: datetime,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO steps
                  (id, run_id, step_index, agent_role, input, success, timestamp)
                VALUES (?, ?, ?, ?, ?, 0, ?)
                """,
                (
                    step_id,
                    run_id,
                    step_index,
                    agent_role,
                    input,
                    timestamp.isoformat() if hasattr(timestamp, "isoformat") else str(timestamp),
                ),
            )

    def complete_step(
        self,
        run_id: str,
        step_id: str,
        output: str,
        provider: str,
        duration_ms: int,
        success: bool,
        error: str = None,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE steps
                SET output = ?,
                    provider = ?,
                    duration_ms = ?,
                    success = ?,
                    error = ?
                WHERE id = ? AND run_id = ?
                """,
                (output, provider, duration_ms, 1 if success else 0, error, step_id, run_id),
            )

    def save_observation(
        self,
        run_id: str,
        step_id: str,
        content: str,
        obs_type: str = "output",
    ) -> str:
        obs_id = str(uuid.uuid4())
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO observations (id, run_id, step_id, content, type, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (obs_id, run_id, step_id, content, obs_type, _now()),
            )
        return obs_id

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def get_run(self, run_id: str) -> dict | None:
        with self._connect() as conn:
            cur = conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,))
            row = cur.fetchone()
            return _row_to_dict(cur, row) if row else None

    def get_steps(self, run_id: str) -> list[dict]:
        with self._connect() as conn:
            cur = conn.execute(
                "SELECT * FROM steps WHERE run_id = ? ORDER BY step_index", (run_id,)
            )
            return [_row_to_dict(cur, row) for row in cur.fetchall()]

    def get_recent_runs(self, limit: int = 10) -> list[dict]:
        with self._connect() as conn:
            cur = conn.execute(
                "SELECT * FROM runs ORDER BY created_at DESC LIMIT ?", (limit,)
            )
            return [_row_to_dict(cur, row) for row in cur.fetchall()]
