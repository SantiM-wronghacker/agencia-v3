from memory.db import AgenciaDB


class FTSSearch:
    def __init__(self, db: AgenciaDB):
        self.db = db

    def search(self, query: str, limit: int = 10) -> list[dict]:
        if not query.strip():
            return []
        try:
            with self.db._connect() as conn:
                cur = conn.execute(
                    """
                    SELECT o.content, o.run_id, o.timestamp,
                           s.agent_role, r.group_name
                    FROM observations_fts f
                    JOIN observations o ON o.rowid = f.rowid
                    JOIN steps s ON s.id = o.step_id
                    JOIN runs r ON r.id = o.run_id
                    WHERE observations_fts MATCH ?
                    ORDER BY rank
                    LIMIT ?
                    """,
                    (query, limit),
                )
                cols = [col[0] for col in cur.description]
                return [dict(zip(cols, row)) for row in cur.fetchall()]
        except Exception:
            return []

    def search_by_role(self, query: str, role: str, limit: int = 5) -> list[dict]:
        if not query.strip():
            return []
        try:
            with self.db._connect() as conn:
                cur = conn.execute(
                    """
                    SELECT o.content, o.run_id, o.timestamp,
                           s.agent_role, r.group_name
                    FROM observations_fts f
                    JOIN observations o ON o.rowid = f.rowid
                    JOIN steps s ON s.id = o.step_id
                    JOIN runs r ON r.id = o.run_id
                    WHERE observations_fts MATCH ?
                      AND s.agent_role = ?
                    ORDER BY rank
                    LIMIT ?
                    """,
                    (query, role, limit),
                )
                cols = [col[0] for col in cur.description]
                return [dict(zip(cols, row)) for row in cur.fetchall()]
        except Exception:
            return []
