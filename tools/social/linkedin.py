from tools.base import BaseTool, ToolResult, tool
from tools.utils.http import HTTPClient

_BASE = "https://api.linkedin.com"


@tool
class LinkedInTool(BaseTool):
    name = "linkedin"
    description = (
        "Publica contenido profesional en LinkedIn. "
        "Úsala para posts en perfil o página de empresa."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "post_text":
            return self._post_text(**kwargs)
        if action == "post_image":
            return self._post_image(**kwargs)
        if action == "get_stats":
            return self._get_stats()
        return self._error(f"Acción '{action}' no soportada")

    def _get_author(self) -> tuple[str | None, ToolResult | None]:
        """Returns (author_urn, error_result). error_result is None on success."""
        access_token = self.credentials.get("access_token")
        org_id = self.credentials.get("org_id")

        if org_id:
            return f"urn:li:organization:{org_id}", None

        client = HTTPClient(_BASE, headers={"Authorization": f"Bearer {access_token}"})
        resp = client.get("/v2/me")
        if not resp or "id" not in resp:
            return None, self._error("No se pudo obtener el URN del usuario de LinkedIn")
        return f"urn:li:person:{resp['id']}", None

    def _post_text(self, text: str = "") -> ToolResult:
        access_token = self.credentials.get("access_token")
        if not access_token:
            return self._error("Credencial access_token no configurada")

        author, err = self._get_author()
        if err:
            return err

        client = HTTPClient(
            _BASE,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        )
        body = {
            "author": author,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            },
        }
        resp = client.post("/v2/ugcPosts", json=body)
        if not resp:
            return self._error("Error al publicar el post en LinkedIn")

        post_id = resp.get("id", "")
        return self._success(f"Post publicado en LinkedIn", raw_data={"post_id": post_id})

    def _post_image(self, text: str = "", image_url: str = "") -> ToolResult:
        access_token = self.credentials.get("access_token")
        if not access_token:
            return self._error("Credencial access_token no configurada")

        author, err = self._get_author()
        if err:
            return err

        client = HTTPClient(
            _BASE,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        )
        body = {
            "author": author,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "ARTICLE",
                    "media": [
                        {
                            "status": "READY",
                            "originalUrl": image_url,
                        }
                    ],
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            },
        }
        resp = client.post("/v2/ugcPosts", json=body)
        if not resp:
            return self._error("Error al publicar imagen en LinkedIn")

        post_id = resp.get("id", "")
        return self._success(f"Post con imagen publicado en LinkedIn", raw_data={"post_id": post_id})

    def _get_stats(self) -> ToolResult:
        access_token = self.credentials.get("access_token")
        org_id = self.credentials.get("org_id")
        if not access_token:
            return self._error("Credencial access_token no configurada")
        if not org_id:
            return self._error("Credencial org_id no configurada para obtener estadísticas")

        client = HTTPClient(
            _BASE,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        resp = client.get(
            "/v2/organizationalEntityFollowerStatistics",
            params={"q": "organizationalEntity", "organizationalEntity": f"urn:li:organization:{org_id}"},
        )
        if not resp:
            return self._error("Error al obtener estadísticas de LinkedIn")

        elements = resp.get("elements", [{}])
        el = elements[0] if elements else {}
        total = el.get("totalFollowerCount", 0)
        organic = el.get("organicFollowerCount", 0)
        output = (
            f"Estadísticas LinkedIn (org {org_id}):\n"
            f"  Seguidores totales: {total}\n"
            f"  Seguidores orgánicos: {organic}"
        )
        return self._success(output, raw_data=resp)
