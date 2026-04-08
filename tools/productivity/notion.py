from tools.base import BaseTool, ToolResult, tool
from tools.utils.http import HTTPClient

_BASE = "https://api.notion.com/v1"
_NOTION_VERSION = "2022-06-28"


@tool
class NotionTool(BaseTool):
    name = "notion"
    description = (
        "Crea y consulta páginas en Notion. "
        "Úsala para documentar procesos, crear tareas "
        "o guardar información estructurada."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "create_page":
            return self._create_page(**kwargs)
        if action == "update_page":
            return self._update_page(**kwargs)
        if action == "query_database":
            return self._query_database(**kwargs)
        if action == "get_page":
            return self._get_page(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _get_auth_headers(self) -> dict | None:
        token = self.credentials.get("token")
        if not token:
            return None
        return {
            "Authorization": f"Bearer {token}",
            "Notion-Version": _NOTION_VERSION,
            "Content-Type": "application/json",
        }

    def _client(self) -> HTTPClient:
        return HTTPClient(_BASE, headers=self._get_auth_headers() or {})

    def _create_page(
        self,
        title: str = "",
        content: str = "",
        database_id: str = None,
        properties: dict = None,
    ) -> ToolResult:
        headers = self._get_auth_headers()
        if not headers:
            return self._error("Credencial token no configurada")

        db_id = database_id or self.credentials.get("default_database_id")
        if not db_id:
            return self._error("database_id no especificado y default_database_id no configurado")

        body = {
            "parent": {"database_id": db_id},
            "properties": {
                "Name": {
                    "title": [{"text": {"content": title}}]
                }
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"text": {"content": content[:2000]}}]
                    },
                }
            ],
        }
        if properties:
            body["properties"].update(properties)

        resp = HTTPClient(_BASE, headers=headers).post("/pages", json=body)
        if not resp or "id" not in resp:
            return self._error("Error al crear la página en Notion")

        page_id = resp["id"]
        return self._success(
            f"Página '{title}' creada en Notion",
            raw_data={"page_id": page_id},
        )

    def _query_database(
        self,
        database_id: str = None,
        filter_property: str = None,
        filter_value: str = None,
    ) -> ToolResult:
        headers = self._get_auth_headers()
        if not headers:
            return self._error("Credencial token no configurada")

        db_id = database_id or self.credentials.get("default_database_id")
        if not db_id:
            return self._error("database_id no especificado")

        body: dict = {}
        if filter_property and filter_value:
            body["filter"] = {
                "property": filter_property,
                "rich_text": {"contains": filter_value},
            }

        resp = HTTPClient(_BASE, headers=headers).post(
            f"/databases/{db_id}/query", json=body
        )
        if not resp:
            return self._error("Error al consultar la base de datos de Notion")

        results = resp.get("results", [])
        lines = [f"Resultados en Notion ({len(results)}):"]
        for page in results:
            props = page.get("properties", {})
            # Extract title from Name or first title property
            title = "Sin título"
            for prop_val in props.values():
                if prop_val.get("type") == "title":
                    texts = prop_val.get("title", [])
                    if texts:
                        title = texts[0].get("text", {}).get("content", "Sin título")
                    break
            lines.append(f"  - {title} (ID: {page['id'][:8]}...)")

        return self._success("\n".join(lines), raw_data={"results": results})

    def _update_page(self, page_id: str = "", properties: dict = None) -> ToolResult:
        headers = self._get_auth_headers()
        if not headers:
            return self._error("Credencial token no configurada")
        if not page_id:
            return self._error("Parámetro page_id requerido")

        resp = HTTPClient(_BASE, headers=headers).post(
            f"/pages/{page_id}", json={"properties": properties or {}}
        )
        if not resp:
            return self._error(f"Error al actualizar página {page_id} en Notion")

        return self._success(
            f"Página {page_id} actualizada",
            raw_data={"page_id": page_id},
        )

    def _get_page(self, page_id: str = "") -> ToolResult:
        headers = self._get_auth_headers()
        if not headers:
            return self._error("Credencial token no configurada")
        if not page_id:
            return self._error("Parámetro page_id requerido")

        resp = HTTPClient(_BASE, headers=headers).get(f"/pages/{page_id}")
        if not resp:
            return self._error(f"Error al obtener página {page_id} de Notion")

        props = resp.get("properties", {})
        lines = [f"Página {page_id}:"]
        for key, val in props.items():
            vtype = val.get("type", "")
            if vtype == "title":
                texts = val.get("title", [])
                text_val = texts[0].get("text", {}).get("content", "") if texts else ""
                lines.append(f"  {key}: {text_val}")
            elif vtype == "rich_text":
                texts = val.get("rich_text", [])
                text_val = texts[0].get("text", {}).get("content", "") if texts else ""
                lines.append(f"  {key}: {text_val}")
            elif vtype in ("number", "select", "checkbox", "date"):
                lines.append(f"  {key}: {val.get(vtype, '')}")

        return self._success("\n".join(lines), raw_data=resp)
