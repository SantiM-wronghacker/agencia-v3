from typing import TYPE_CHECKING

from core.base import GroupResult
from core.group import AgentGroup

if TYPE_CHECKING:
    from memory.db import AgenciaDB


class Orchestrator:
    def __init__(self, db: "AgenciaDB | None" = None):
        self.db = db
        self._groups: dict[str, AgentGroup] = {}

    def register(self, group: AgentGroup) -> None:
        if group.db is None and self.db is not None:
            group.db = self.db
        self._groups[group.name] = group

    def run(self, group_name: str, task: str, run_id: str = None) -> GroupResult:
        if group_name not in self._groups:
            raise ValueError(
                f"Grupo '{group_name}' no registrado. "
                f"Disponibles: {', '.join(self._groups) or 'ninguno'}"
            )
        return self._groups[group_name].execute(task, run_id=run_id)

    def list_groups(self) -> list[dict]:
        return [
            {
                "name": g.name,
                "mode": g.mode,
                "agent_count": len(g.agents),
                "agent_roles": [a.role for a in g.agents],
            }
            for g in self._groups.values()
        ]

    def get_group(self, group_name: str) -> AgentGroup | None:
        return self._groups.get(group_name)
