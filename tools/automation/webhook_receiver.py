import uuid
from pathlib import Path

from tools.base import BaseTool, ToolResult, tool
from tools.utils.dates import now_iso

_ENDPOINTS_FILE = Path("data/webhook_endpoints.json")
_EVENTS_FILE = Path("data/webhook_events.json")


@tool
class WebhookReceiverTool(BaseTool):
    name = "webhook_receiver"
    description = (
        "Gestiona endpoints de webhooks para recibir datos externos. "
        "Úsala para configurar URLs que disparan agentes "
        "cuando llegan datos de formularios, e-commerce u otros sistemas."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "create_endpoint":
            return self._create_endpoint(**kwargs)
        if action == "list_endpoints":
            return self._list_endpoints()
        if action == "get_recent_events":
            return self._get_recent_events(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _load(self, path: Path) -> list:
        if path.exists():
            import json
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                return []
        return []

    def _save(self, data: list, path: Path) -> None:
        import json
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def _create_endpoint(
        self,
        name: str = "",
        group_name: str = "",
        description: str = "",
    ) -> ToolResult:
        if not name:
            return self._error("El parámetro 'name' es obligatorio")
        eid = str(uuid.uuid4())[:8]
        secret = uuid.uuid4().hex[:16]
        entry = {
            "id": eid,
            "name": name,
            "group_name": group_name,
            "description": description,
            "url": f"/webhooks/agencia/{name}",
            "secret": secret,
            "active": True,
            "events_count": 0,
            "created_at": now_iso(),
        }
        endpoints = self._load(_ENDPOINTS_FILE)
        endpoints.append(entry)
        self._save(endpoints, _ENDPOINTS_FILE)
        return self._success(
            f"Webhook creado: {name}\n"
            f"URL: /webhooks/agencia/{name}\n"
            f"Secret: {secret}\n"
            f"Grupo que se ejecuta: {group_name}",
            raw_data=entry,
        )

    def _list_endpoints(self) -> ToolResult:
        endpoints = self._load(_ENDPOINTS_FILE)
        if not endpoints:
            return self._success("No hay endpoints registrados.", raw_data={"endpoints": []})
        lines = ["URL                           | Grupo               | Eventos | Estado",
                 "-" * 70]
        for e in endpoints:
            lines.append(
                f"{e['url'][:30]:<31}| {e['group_name'][:20]:<21}| "
                f"{e.get('events_count', 0):<9}| "
                f"{'Activo' if e['active'] else 'Inactivo'}"
            )
        return self._success("\n".join(lines), raw_data={"endpoints": endpoints})

    def _get_recent_events(
        self,
        endpoint_name: str = "",
        limit: int = 10,
    ) -> ToolResult:
        events = self._load(_EVENTS_FILE)
        filtered = [e for e in events if e.get("endpoint_name") == endpoint_name]
        recent = filtered[-limit:]
        if not recent:
            return self._success(
                f"Sin eventos para '{endpoint_name}'",
                raw_data={"events": []},
            )
        lines = [f"Últimos {len(recent)} eventos para '{endpoint_name}':"]
        for ev in recent:
            lines.append(f"  [{ev.get('received_at', '?')}] {ev.get('summary', '(sin resumen)')}")
        return self._success("\n".join(lines), raw_data={"events": recent})
