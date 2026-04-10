from tools.base import BaseTool, ToolResult, tool


@tool
class MakeWebhookTool(BaseTool):
    name = "make_webhook"
    description = (
        "Envía datos a Make (ex-Integromat). "
        "Úsala para conectar con scenarios de Make "
        "y automatizar flujos de trabajo complejos."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "send":
            return self._send(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _send(self, data: dict = None, webhook_url: str = None) -> ToolResult:
        data = data or {}
        url = webhook_url or self.credentials.get("webhook_url")
        if not url:
            return self._error(
                "URL de Make no configurada. "
                "Obtén el webhook URL desde tu scenario en Make.com"
            )
        import httpx
        try:
            r = httpx.post(url, json=data, timeout=15)
            return self._success(
                f"Datos enviados a Make exitosamente.\n"
                f"Status: {r.status_code}",
                raw_data={"sent": data},
            )
        except Exception as e:
            return self._error(f"Error enviando a Make: {e}")
