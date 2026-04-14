import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

_SCHEMA = """
CREATE TABLE IF NOT EXISTS clients (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  license_key TEXT UNIQUE NOT NULL,
  package_type TEXT NOT NULL DEFAULT 'basic',
  status TEXT NOT NULL DEFAULT 'active',
  agentes TEXT NOT NULL DEFAULT '[]',
  notes TEXT DEFAULT '',
  active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL,
  paid_until TEXT NOT NULL,
  last_heartbeat TEXT
);

CREATE TABLE IF NOT EXISTS heartbeats (
  id TEXT PRIMARY KEY,
  client_id TEXT NOT NULL REFERENCES clients(id),
  timestamp TEXT NOT NULL,
  ip_address TEXT,
  package_type TEXT,
  status_given TEXT
);
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

    def __getattr__(self, name):
        return getattr(self._conn, name)


class LicenseDB:
    def __init__(self, db_path: str = None):
        import os
        self.db_path = db_path if db_path is not None else os.getenv("DB_PATH", "data/licenses.db")
        self._persistent_conn: sqlite3.Connection | None = None
        if self.db_path == ":memory:":
            self._persistent_conn = sqlite3.connect(":memory:", check_same_thread=False)
            self._persistent_conn.execute("PRAGMA foreign_keys = ON")
        else:
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self):
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
    # Client operations
    # ------------------------------------------------------------------

    def create_client(
        self,
        name: str,
        email: str,
        license_key: str,
        package_type: str,
        paid_until: str,
        agentes: str = None,
    ) -> str:
        client_id = str(uuid.uuid4())
        agentes = agentes or "[]"
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO clients (id, name, email, license_key, package_type, status, agentes, active, created_at, paid_until)
                VALUES (?, ?, ?, ?, ?, 'active', ?, 1, ?, ?)
                """,
                (client_id, name, email, license_key, package_type, agentes, _now(), paid_until),
            )
        return client_id

    def get_client_by_key(self, license_key: str) -> dict | None:
        with self._connect() as conn:
            cur = conn.execute(
                "SELECT * FROM clients WHERE license_key = ?", (license_key,)
            )
            row = cur.fetchone()
            return _row_to_dict(cur, row) if row else None

    def get_client(self, client_id: str) -> dict | None:
        with self._connect() as conn:
            cur = conn.execute(
                "SELECT * FROM clients WHERE id = ?", (client_id,)
            )
            row = cur.fetchone()
            return _row_to_dict(cur, row) if row else None

    def update_client(self, client_id: str, **kwargs) -> None:
        allowed = {"active", "paid_until", "package_type", "status", "agentes", "notes"}
        fields = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
        if not fields:
            return
        set_clause = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [client_id]
        with self._connect() as conn:
            conn.execute(
                f"UPDATE clients SET {set_clause} WHERE id = ?", values
            )

    def get_all_clients(self) -> list[dict]:
        with self._connect() as conn:
            cur = conn.execute("SELECT * FROM clients ORDER BY created_at DESC")
            return [_row_to_dict(cur, row) for row in cur.fetchall()]

    # ------------------------------------------------------------------
    # Heartbeat operations
    # ------------------------------------------------------------------

    def record_heartbeat(
        self,
        client_id: str,
        ip_address: str,
        package_type: str,
        status_given: str,
    ) -> None:
        hb_id = str(uuid.uuid4())
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO heartbeats (id, client_id, timestamp, ip_address, package_type, status_given)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (hb_id, client_id, _now(), ip_address, package_type, status_given),
            )

    def get_last_heartbeat(self, client_id: str) -> dict | None:
        with self._connect() as conn:
            cur = conn.execute(
                """
                SELECT * FROM heartbeats
                WHERE client_id = ?
                ORDER BY timestamp DESC
                LIMIT 1
                """,
                (client_id,),
            )
            row = cur.fetchone()
            return _row_to_dict(cur, row) if row else None

    def get_client_heartbeats(self, client_id: str, limit: int = 10) -> list[dict]:
        with self._connect() as conn:
            cur = conn.execute(
                """
                SELECT * FROM heartbeats
                WHERE client_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (client_id, limit),
            )
            return [_row_to_dict(cur, row) for row in cur.fetchall()]

    def update_last_heartbeat(self, client_id: str, timestamp: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE clients SET last_heartbeat = ? WHERE id = ?",
                (timestamp, client_id),
            )
