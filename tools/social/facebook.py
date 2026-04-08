from tools.base import BaseTool, ToolResult, tool
from tools.utils.http import HTTPClient

_BASE = "https://graph.facebook.com"


@tool
class FacebookTool(BaseTool):
    name = "facebook"
    description = (
        "Publica y gestiona contenido en Facebook. "
        "Úsala para posts en página de Facebook."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "post_text":
            return self._post_text(**kwargs)
        if action == "post_image":
            return self._post_image(**kwargs)
        if action == "get_insights":
            return self._get_insights()
        return self._error(f"Acción '{action}' no soportada")

    def _post_text(self, message: str = "") -> ToolResult:
        page_token = self.credentials.get("page_token")
        page_id = self.credentials.get("page_id")
        if not page_token:
            return self._error("Credencial page_token no configurada")
        if not page_id:
            return self._error("Credencial page_id no configurada")

        client = HTTPClient(_BASE)
        resp = client.post(
            f"/v18.0/{page_id}/feed",
            data={"message": message, "access_token": page_token},
        )
        if not resp or "id" not in resp:
            return self._error("Error al publicar el post en Facebook")

        post_id = resp["id"]
        return self._success(f"Post publicado. ID: {post_id}", raw_data={"post_id": post_id})

    def _post_image(self, message: str = "", image_url: str = "") -> ToolResult:
        page_token = self.credentials.get("page_token")
        page_id = self.credentials.get("page_id")
        if not page_token:
            return self._error("Credencial page_token no configurada")
        if not page_id:
            return self._error("Credencial page_id no configurada")

        client = HTTPClient(_BASE)
        resp = client.post(
            f"/v18.0/{page_id}/photos",
            data={"message": message, "url": image_url, "access_token": page_token},
        )
        if not resp or "id" not in resp:
            return self._error("Error al publicar la imagen en Facebook")

        photo_id = resp["id"]
        return self._success(f"Imagen publicada. ID: {photo_id}", raw_data={"photo_id": photo_id})

    def _get_insights(self) -> ToolResult:
        page_token = self.credentials.get("page_token")
        page_id = self.credentials.get("page_id")
        if not page_token:
            return self._error("Credencial page_token no configurada")
        if not page_id:
            return self._error("Credencial page_id no configurada")

        client = HTTPClient(_BASE)
        resp = client.get(
            f"/v18.0/{page_id}/insights",
            params={
                "metric": "page_fans,page_views_total",
                "access_token": page_token,
            },
        )
        if not resp:
            return self._error("Error al obtener insights de Facebook")

        data = resp.get("data", [])
        lines = [f"Insights de página {page_id}:"]
        for item in data:
            values = item.get("values", [{}])
            latest = values[-1].get("value", 0) if values else 0
            lines.append(f"  {item.get('name', '?')}: {latest}")
        return self._success("\n".join(lines), raw_data=resp)
