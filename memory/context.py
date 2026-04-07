from memory.db import AgenciaDB
from memory.fts import FTSSearch


class ContextMemory:
    def __init__(self, db: AgenciaDB):
        self.db = db
        self.fts = FTSSearch(db)

    def inject_context(
        self, role: str, task: str, max_chars: int = 1500
    ) -> str:
        results = self.fts.search_by_role(task, role, limit=5)
        if not results:
            results = self.fts.search(task, limit=3)
        if not results:
            return ""

        lines = ["Contexto de trabajos anteriores relevantes:"]
        for obs in results:
            group = obs.get("group_name", "?")
            agent = obs.get("agent_role", "?")
            content = obs.get("content", "")[:300]
            lines.append(f"- [{group} / {agent}]: {content}")

        context = "\n".join(lines)
        if len(context) > max_chars:
            context = context[:max_chars - 3] + "..."
        return context
