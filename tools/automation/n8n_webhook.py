from tools.base import BaseTool, ToolResult, tool


@tool
class N8NWebhookTool(BaseTool):
    name = "n8n_webhook"
    description = (
        "Envía datos a n8n self-hosted. "
        "Úsala para conectar con workflows de n8n "
        "en instalaciones locales o en la nube."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "send":
            return self._send(**kwargs)
        if action == "trigger":
            return self._trigger(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _send(self, data: dict = None, workflow_name: str = "") -> ToolResult:
        data = data or {}
        url = self.credentials.get("webhook_url")
        if not url:
            return self._error(
                "URL de n8n no configurada. "
                "Configura webhook_url con la URL de tu workflow n8n."
            )
        headers = {}
        if self.credentials.get("n8n_api_key"):
            headers["X-N8N-API-KEY"] = self.credentials["n8n_api_key"]
        import httpx
        try:
            r = httpx.post(url, json=data, headers=headers, timeout=15)
            r.raise_for_status()
            return self._success(
                f"Datos enviados a n8n exitosamente"
                + (f" — workflow: {workflow_name}" if workflow_name else ""),
                raw_data={"sent": data, "status": r.status_code},
            )
        except Exception as e:
            return self._error(f"Error enviando a n8n: {e}")

    def _trigger(self, data: dict = None, workflow_name: str = "") -> ToolResult:
        data = data or {}
        url = self.credentials.get("webhook_url")
        if not url:
            return self._error(
                "URL de n8n no configurada. "
                "Configura webhook_url con la URL de tu workflow n8n."
            )
        headers = {}
        if self.credentials.get("n8n_api_key"):
            headers["X-N8N-API-KEY"] = self.credentials["n8n_api_key"]
        import httpx
        try:
            r = httpx.post(url, json=data, headers=headers, timeout=15)
            r.raise_for_status()
            return self._success(
                f"Workflow n8n '{workflow_name}' disparado",
                raw_data={"sent": data, "workflow_name": workflow_name},
            )
        except Exception as e:
            return self._error(f"Error disparando workflow n8n '{workflow_name}': {e}")
