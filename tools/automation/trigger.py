import uuid
from pathlib import Path

from tools.base import BaseTool, ToolResult, tool
from tools.utils.dates import now_iso

_DATA_FILE = Path("data/triggers.json")
_VALID_EVENT_TYPES = {"webhook", "schedule", "email", "file_created"}


@tool
class TriggerTool(BaseTool):
    name = "trigger"
    description = (
        "Configura disparadores basados en eventos. "
        "Úsala para ejecutar grupos de agentes "
        "cuando ocurren eventos específicos."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "register":
            return self._register(**kwargs)
        if action == "list":
            return self._list()
        if action == "deactivate":
            return self._deactivate(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _load(self) -> list:
        if _DATA_FILE.exists():
            import json
            try:
                return json.loads(_DATA_FILE.read_text(encoding="utf-8"))
            except Exception:
                return []
        return []

    def _save(self, triggers: list) -> None:
        import json
        _DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        _DATA_FILE.write_text(json.dumps(triggers, indent=2, ensure_ascii=False), encoding="utf-8")

    def _register(
        self,
        trigger_name: str = "",
        group_name: str = "",
        event_type: str = "",
        task_template: str = "",
    ) -> ToolResult:
        if event_type not in _VALID_EVENT_TYPES:
            return self._error(
                f"Tipo de evento inválido: '{event_type}'. "
                f"Válidos: {', '.join(sorted(_VALID_EVENT_TYPES))}"
            )
        tid = str(uuid.uuid4())
        entry = {
            "id": tid,
            "name": trigger_name,
            "group_name": group_name,
            "event_type": event_type,
            "task_template": task_template,
            "active": True,
            "created_at": now_iso(),
        }
        if event_type == "webhook":
            entry["webhook_url"] = f"/webhooks/agencia/{trigger_name}"
        triggers = self._load()
        triggers.append(entry)
        self._save(triggers)
        msg = (
            f"Trigger '{trigger_name}' registrado.\n"
            f"Tipo: {event_type}\n"
            f"Grupo: {group_name}"
        )
        if event_type == "webhook":
            msg += f"\nWebhook: /webhooks/agencia/{trigger_name}"
        return self._success(msg, raw_data=entry)

    def _list(self) -> ToolResult:
        triggers = self._load()
        if not triggers:
            return self._success("No hay triggers registrados.", raw_data={"triggers": []})
        lines = ["ID       | Nombre              | Tipo         | Estado",
                 "-" * 60]
        for t in triggers:
            lines.append(
                f"{t['id'][:8]:<9}| {t['name'][:20]:<21}| "
                f"{t['event_type']:<14}| {'Activo' if t['active'] else 'Inactivo'}"
            )
        return self._success("\n".join(lines), raw_data={"triggers": triggers})

    def _deactivate(self, trigger_id: str = "") -> ToolResult:
        triggers = self._load()
        found = False
        for t in triggers:
            if t["id"] == trigger_id:
                t["active"] = False
                found = True
                break
        if not found:
            return self._error(f"Trigger '{trigger_id}' no encontrado")
        self._save(triggers)
        return self._success(f"Trigger {trigger_id} desactivado", raw_data={"id": trigger_id})
