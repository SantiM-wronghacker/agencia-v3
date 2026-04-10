from tools.base import BaseTool, ToolResult, tool

_BASE = "https://api.webflow.com/v2"


@tool
class WebflowTool(BaseTool):
    name = "webflow"
    description = (
        "Gestiona contenido CMS en Webflow. "
        "Úsala para crear y actualizar items "
        "en colecciones del CMS de Webflow."
    )

    def _get_headers(self) -> dict | None:
        token = self.credentials.get("api_token")
        if not token:
            return None
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "create_item":
            return self._create_item(**kwargs)
        if action == "update_item":
            return self._update_item(**kwargs)
        if action == "list_items":
            return self._list_items(**kwargs)
        if action == "publish_site":
            return self._publish_site()
        return self._error(f"Acción '{action}' no soportada")

    def _create_item(self, collection_id: str = "", fields: dict = None) -> ToolResult:
        headers = self._get_headers()
        if not headers:
            return self._error("Credencial Webflow no configurada: api_token")
        import httpx

        try:
            r = httpx.post(
                f"{_BASE}/collections/{collection_id}/items",
                json={"fieldData": fields or {}},
                headers=headers,
                timeout=30,
            )
            r.raise_for_status()
            data = r.json()
            return self._success(
                f"Item creado en Webflow. ID: {data.get('id', '')}",
                raw_data={"item_id": data.get("id")},
            )
        except Exception as e:
            return self._error(f"Error Webflow: {e}")

    def _update_item(
        self, collection_id: str = "", item_id: str = "", fields: dict = None
    ) -> ToolResult:
        headers = self._get_headers()
        if not headers:
            return self._error("Credencial Webflow no configurada: api_token")
        import httpx

        try:
            r = httpx.patch(
                f"{_BASE}/collections/{collection_id}/items/{item_id}",
                json={"fieldData": fields or {}},
                headers=headers,
                timeout=30,
            )
            r.raise_for_status()
            return self._success(f"Item {item_id} actualizado en Webflow")
        except Exception as e:
            return self._error(f"Error Webflow: {e}")

    def _list_items(self, collection_id: str = "", limit: int = 20) -> ToolResult:
        headers = self._get_headers()
        if not headers:
            return self._error("Credencial Webflow no configurada: api_token")
        import httpx

        try:
            r = httpx.get(
                f"{_BASE}/collections/{collection_id}/items",
                params={"limit": limit},
                headers=headers,
                timeout=30,
            )
            r.raise_for_status()
            items = r.json().get("items", [])
            lines = [
                f"- [{i.get('id', '')}] {i.get('fieldData', {}).get('name', 'sin nombre')}"
                for i in items
            ]
            return self._success(
                "\n".join(lines) if lines else "Sin items",
                raw_data={"items": items},
            )
        except Exception as e:
            return self._error(f"Error Webflow: {e}")

    def _publish_site(self) -> ToolResult:
        headers = self._get_headers()
        site_id = self.credentials.get("site_id")
        if not headers or not site_id:
            return self._error(
                "Credenciales Webflow no configuradas: api_token, site_id"
            )
        import httpx

        try:
            r = httpx.post(
                f"{_BASE}/sites/{site_id}/publish",
                json={"domains": []},
                headers=headers,
                timeout=60,
            )
            r.raise_for_status()
            return self._success("Sitio publicado en Webflow")
        except Exception as e:
            return self._error(f"Error Webflow publish: {e}")
