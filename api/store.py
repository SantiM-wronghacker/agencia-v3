"""
SQLite-backed task store for the Dashboard API v2.

Replaces the in-memory dict with a persistent SQLite database.
DB path is configurable via the ``DASHBOARD_DB_PATH`` environment variable
(default: ``./data/dashboard.db``).  The parent directory is created
automatically if it does not exist.
"""
from __future__ import annotations

import json
import os
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .models import TaskSchema, TaskStatus

_DEFAULT_DB_PATH = os.path.join(".", "data", "dashboard.db")
DB_PATH: str = os.environ.get("DASHBOARD_DB_PATH", _DEFAULT_DB_PATH)


def _ensure_dir(path: str) -> None:
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)


class TaskStore:
    """Thread-safe, SQLite-backed task store."""

    def __init__(self, db_path: str | None = None) -> None:
        self._db_path = db_path or DB_PATH
        _ensure_dir(self._db_path)
        self._local = threading.local()
        self._init_db()

    # -- connection helpers --------------------------------------------------

    def _get_conn(self) -> sqlite3.Connection:
        conn = getattr(self._local, "conn", None)
        if conn is None:
            conn = sqlite3.connect(self._db_path)
            conn.row_factory = sqlite3.Row
            self._local.conn = conn
        return conn

    def _init_db(self) -> None:
        conn = self._get_conn()
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id          TEXT PRIMARY KEY,
                name        TEXT NOT NULL,
                description TEXT,
                status      TEXT NOT NULL DEFAULT 'pending',
                created_at  TEXT NOT NULL,
                updated_at  TEXT NOT NULL,
                result      TEXT,
                logs        TEXT NOT NULL DEFAULT '[]'
            )
            """
        )
        conn.commit()

    # -- serialisation helpers -----------------------------------------------

    @staticmethod
    def _row_to_task(row: sqlite3.Row) -> TaskSchema:
        return TaskSchema(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            status=TaskStatus(row["status"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            result=json.loads(row["result"]) if row["result"] else None,
            logs=json.loads(row["logs"]),
        )

    # -- public API (mirrors dict-like behaviour) ----------------------------

    def add(self, task: TaskSchema) -> None:
        conn = self._get_conn()
        conn.execute(
            """
            INSERT INTO tasks (id, name, description, status, created_at, updated_at, result, logs)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task.id,
                task.name,
                task.description,
                task.status.value,
                task.created_at.isoformat(),
                task.updated_at.isoformat(),
                json.dumps(task.result, default=str) if task.result is not None else None,
                json.dumps(task.logs),
            ),
        )
        conn.commit()

    def get(self, task_id: str) -> Optional[TaskSchema]:
        conn = self._get_conn()
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if row is None:
            return None
        return self._row_to_task(row)

    def update(self, task: TaskSchema) -> None:
        conn = self._get_conn()
        conn.execute(
            """
            UPDATE tasks
               SET name = ?, description = ?, status = ?,
                   created_at = ?, updated_at = ?,
                   result = ?, logs = ?
             WHERE id = ?
            """,
            (
                task.name,
                task.description,
                task.status.value,
                task.created_at.isoformat(),
                task.updated_at.isoformat(),
                json.dumps(task.result, default=str) if task.result is not None else None,
                json.dumps(task.logs),
                task.id,
            ),
        )
        conn.commit()

    def list_all(self) -> list[TaskSchema]:
        conn = self._get_conn()
        rows = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC").fetchall()
        return [self._row_to_task(r) for r in rows]

    def clear(self) -> None:
        """Remove all tasks – mainly for testing."""
        conn = self._get_conn()
        conn.execute("DELETE FROM tasks")
        conn.commit()

    def delete(self, task_id: str) -> bool:
        """Delete a task by ID. Returns True if a row was deleted."""
        conn = self._get_conn()
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return cursor.rowcount > 0

    # -- dict-like interface ---------------------------------------------------

    def __setitem__(self, task_id: str, task: TaskSchema) -> None:
        existing = self.get(task_id)
        if existing is None:
            self.add(task)
        else:
            self.update(task)

    def __getitem__(self, task_id: str) -> TaskSchema:
        task = self.get(task_id)
        if task is None:
            raise KeyError(task_id)
        return task

    def __contains__(self, task_id: str) -> bool:
        return self.get(task_id) is not None

    def close(self) -> None:
        conn = getattr(self._local, "conn", None)
        if conn is not None:
            conn.close()
            self._local.conn = None
