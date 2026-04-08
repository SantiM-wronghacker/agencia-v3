from tools.base import BaseTool, ToolResult, tool
from tools.utils.http import HTTPClient

_BASE = "https://graph.facebook.com/v18.0"


@tool
class InstagramTool(BaseTool):
    name = "instagram"
    description = (
        "Publica contenido en Instagram. "
        "Úsala cuando necesites publicar un post, "
        "imagen o historia en Instagram."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "post_image":
            return self._post_image(**kwargs)
        if action == "get_stats":
            return self._get_stats(**kwargs)
        if action == "get_account":
            return self._get_account()
        return self._error(f"Acción '{action}' no soportada")

    def _post_image(self, caption: str = "", image_url: str = None) -> ToolResult:
        access_token = self.credentials.get("access_token")
        account_id = self.credentials.get("account_id")
        if not access_token:
            return self._error("Credencial access_token no configurada")
        if not account_id:
            return self._error("Credencial account_id no configurada")

        client = HTTPClient(_BASE)
        params: dict = {"caption": caption, "access_token": access_token}
        if image_url:
            params["image_url"] = image_url

        resp = client.post(f"/{account_id}/media", data=params)
        if not resp or "id" not in resp:
            return self._error("Error al crear el contenedor de media en Instagram")

        creation_id = resp["id"]
        publish_resp = client.post(
            f"/{account_id}/media_publish",
            data={"creation_id": creation_id, "access_token": access_token},
        )
        if not publish_resp or "id" not in publish_resp:
            return self._error("Error al publicar el media en Instagram")

        media_id = publish_resp["id"]
        return self._success(
            f"Post publicado en Instagram. ID: {media_id}",
            raw_data={"media_id": media_id},
        )

    def _get_account(self) -> ToolResult:
        access_token = self.credentials.get("access_token")
        account_id = self.credentials.get("account_id")
        if not access_token:
            return self._error("Credencial access_token no configurada")
        if not account_id:
            return self._error("Credencial account_id no configurada")

        client = HTTPClient(_BASE)
        resp = client.get(
            f"/{account_id}",
            params={
                "fields": "followers_count,media_count,name",
                "access_token": access_token,
            },
        )
        if not resp:
            return self._error("Error al obtener datos de la cuenta de Instagram")

        name = resp.get("name", "N/A")
        followers = resp.get("followers_count", 0)
        media = resp.get("media_count", 0)
        output = (
            f"Cuenta Instagram: {name}\n"
            f"Seguidores: {followers}\n"
            f"Publicaciones: {media}"
        )
        return self._success(output, raw_data=resp)

    def _get_stats(self, media_id: str = "") -> ToolResult:
        access_token = self.credentials.get("access_token")
        if not access_token:
            return self._error("Credencial access_token no configurada")
        if not media_id:
            return self._error("Parámetro media_id requerido")

        client = HTTPClient(_BASE)
        resp = client.get(
            f"/{media_id}/insights",
            params={
                "metric": "impressions,reach,likes_count",
                "access_token": access_token,
            },
        )
        if not resp:
            return self._error("Error al obtener métricas de Instagram")

        data = resp.get("data", [])
        lines = [f"Métricas para media {media_id}:"]
        for item in data:
            lines.append(f"  {item.get('name', '?')}: {item.get('values', [{}])[0].get('value', 0)}")
        return self._success("\n".join(lines), raw_data=resp)
