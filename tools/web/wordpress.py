from tools.base import BaseTool, ToolResult, tool


@tool
class WordPressTool(BaseTool):
    name = "wordpress"
    description = (
        "Crea y gestiona contenido en WordPress. "
        "Úsala para publicar artículos, páginas "
        "y gestionar el sitio web del cliente."
    )

    BASE_PATH = "/wp-json/wp/v2"

    def _get_base_url(self) -> str | None:
        url = self.credentials.get("url")
        if not url:
            return None
        return url.rstrip("/") + self.BASE_PATH

    def _get_auth(self) -> tuple | None:
        u = self.credentials.get("username")
        p = self.credentials.get("app_password")
        if not u or not p:
            return None
        return (u, p)

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "create_post":
            return self._create_post(**kwargs)
        if action == "update_post":
            return self._update_post(**kwargs)
        if action == "get_posts":
            return self._get_posts(**kwargs)
        if action == "upload_media":
            return self._upload_media(**kwargs)
        if action == "get_categories":
            return self._get_categories()
        return self._error(f"Acción '{action}' no soportada")

    def _create_post(
        self,
        title: str = "",
        content: str = "",
        status: str = "draft",
        categories: list = None,
        tags: list = None,
        excerpt: str = "",
    ) -> ToolResult:
        base = self._get_base_url()
        auth = self._get_auth()
        if not base or not auth:
            return self._error(
                "Credenciales WordPress no configuradas: url, username, app_password"
            )
        import httpx

        try:
            r = httpx.post(
                f"{base}/posts",
                json={
                    "title": title,
                    "content": content,
                    "status": status,
                    "excerpt": excerpt,
                    "categories": categories or [],
                    "tags": tags or [],
                },
                auth=auth,
                timeout=30,
            )
            r.raise_for_status()
            data = r.json()
            return self._success(
                f"Post '{title}' creado en WordPress. ID: {data['id']}. Status: {status}",
                raw_data={"post_id": data["id"], "link": data.get("link", "")},
            )
        except Exception as e:
            return self._error(f"Error WordPress: {e}")

    def _update_post(
        self,
        post_id: int = 0,
        content: str = None,
        title: str = None,
        status: str = None,
    ) -> ToolResult:
        base = self._get_base_url()
        auth = self._get_auth()
        if not base or not auth:
            return self._error("Credenciales WordPress no configuradas")
        body = {}
        if content:
            body["content"] = content
        if title:
            body["title"] = title
        if status:
            body["status"] = status
        if not body:
            return self._error("Nada que actualizar — todos los campos son None")
        import httpx

        try:
            r = httpx.patch(
                f"{base}/posts/{post_id}",
                json=body,
                auth=auth,
                timeout=30,
            )
            r.raise_for_status()
            return self._success(f"Post {post_id} actualizado en WordPress")
        except Exception as e:
            return self._error(f"Error WordPress: {e}")

    def _get_posts(self, status: str = "publish", limit: int = 10) -> ToolResult:
        base = self._get_base_url()
        auth = self._get_auth()
        if not base or not auth:
            return self._error("Credenciales WordPress no configuradas")
        import httpx

        try:
            r = httpx.get(
                f"{base}/posts",
                params={"status": status, "per_page": limit},
                auth=auth,
                timeout=30,
            )
            r.raise_for_status()
            posts = r.json()
            lines = [
                f"- [{p['id']}] {p['title']['rendered']} ({p['status']})"
                for p in posts
            ]
            return self._success(
                "\n".join(lines) if lines else "Sin posts",
                raw_data={"posts": posts},
            )
        except Exception as e:
            return self._error(f"Error WordPress: {e}")

    def _upload_media(self, file_path: str = "", alt_text: str = "") -> ToolResult:
        from pathlib import Path

        base = self._get_base_url()
        auth = self._get_auth()
        if not base or not auth:
            return self._error("Credenciales WordPress no configuradas")
        p = Path(file_path)
        if not p.exists():
            return self._error(f"Archivo no encontrado: {file_path}")
        import httpx
        import mimetypes

        ct = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        try:
            with open(file_path, "rb") as f:
                r = httpx.post(
                    f"{base}/media",
                    content=f.read(),
                    headers={
                        "Content-Disposition": f'attachment; filename="{p.name}"',
                        "Content-Type": ct,
                    },
                    auth=auth,
                    timeout=60,
                )
            r.raise_for_status()
            data = r.json()
            return self._success(
                f"Media subida. ID: {data['id']}. URL: {data.get('source_url', '')}",
                raw_data={
                    "media_id": data["id"],
                    "url": data.get("source_url", ""),
                },
            )
        except Exception as e:
            return self._error(f"Error WordPress upload: {e}")

    def _get_categories(self) -> ToolResult:
        base = self._get_base_url()
        auth = self._get_auth()
        if not base or not auth:
            return self._error("Credenciales WordPress no configuradas")
        import httpx

        try:
            r = httpx.get(
                f"{base}/categories",
                params={"per_page": 100},
                auth=auth,
                timeout=30,
            )
            r.raise_for_status()
            cats = r.json()
            lines = [f"- [{c['id']}] {c['name']}" for c in cats]
            return self._success(
                "\n".join(lines) if lines else "Sin categorías",
                raw_data={"categories": cats},
            )
        except Exception as e:
            return self._error(f"Error WordPress: {e}")
