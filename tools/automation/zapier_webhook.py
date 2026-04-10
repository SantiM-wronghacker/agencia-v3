from tools.base import BaseTool, ToolResult, tool


@tool
class ZapierWebhookTool(BaseTool):
    name = "zapier_webhook"
    description = (
        "Envía y recibe datos de Zapier. "
        "Úsala para conectar con miles de apps "
        "via Zapier sin código adicional."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "send":
            return self._send(**kwargs)
        if action == "trigger":
            return self._trigger(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _send(self, data: dict = None, webhook_url: str = None) -> ToolResult:
        data = data or {}
        url = webhook_url or self.credentials.get("webhook_url")
        if not url:
            return self._error(
                "URL de Zapier no configurada. "
                "Proporciona webhook_url como parámetro "
                "o configúralo en las credenciales."
            )
        import httpx
        try:
            r = httpx.post(url, json=data, timeout=15)
            r.raise_for_status()
            return self._success(
                f"Datos enviados a Zapier exitosamente.\n"
                f"Campos enviados: {list(data.keys())}",
                raw_data={"sent": data, "status": r.status_code},
            )
        except Exception as e:
            return self._error(f"Error enviando a Zapier: {e}")

    def _trigger(
        self,
        zap_name: str = "",
        payload: dict = None,
        webhook_url: str = None,
    ) -> ToolResult:
        payload = payload or {}
        url = webhook_url or self.credentials.get("webhook_url")
        if not url:
            return self._error(
                "URL de Zapier no configurada. "
                "Proporciona webhook_url como parámetro "
                "o configúralo en las credenciales."
            )
        import httpx
        try:
            r = httpx.post(url, json=payload, timeout=15)
            r.raise_for_status()
            return self._success(
                f"Zap '{zap_name}' disparado exitosamente",
                raw_data={"zap_name": zap_name, "sent": payload, "status": r.status_code},
            )
        except Exception as e:
            return self._error(f"Error disparando Zap '{zap_name}': {e}")
