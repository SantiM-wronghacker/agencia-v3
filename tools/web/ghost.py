from tools.base import BaseTool, ToolResult, tool


@tool
class GhostTool(BaseTool):
    name = "ghost"
    description = (
        "Publica contenido en Ghost CMS. "
        "Úsala para crear y gestionar posts "
        "en blogs basados en Ghost."
    )

    def _get_jwt(self) -> str | None:
        key = self.credentials.get("admin_api_key", "")
        if ":" not in key:
            return None
        try:
            import jwt
            import time

            key_id, secret = key.split(":", 1)
            payload = {
                "iat": int(time.time()),
                "exp": int(time.time()) + 300,
                "aud": "/admin/",
            }
            token = jwt.encode(
                payload,
                bytes.fromhex(secret),
                algorithm="HS256",
                headers={"kid": key_id},
            )
            return token if isinstance(token, str) else token.decode()
        except ImportError:
            return None
        except Exception:
            return None

    def _get_base_url(self) -> str | None:
        url = self.credentials.get("url")
        if not url:
            return None
        return url.rstrip("/") + "/ghost/api/admin"

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "create_post":
            return self._create_post(**kwargs)
        if action == "update_post":
            return self._update_post(**kwargs)
        if action == "get_posts":
            return self._get_posts(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _create_post(
        self,
        title: str = "",
        html: str = "",
        status: str = "draft",
        tags: list = None,
    ) -> ToolResult:
        base = self._get_base_url()
        if not base:
            return self._error("Credencial Ghost no configurada: url")
        try:
            import jwt  # noqa: F401
        except ImportError:
            return self._error("PyJWT no instalado. Ejecuta: pip install PyJWT")
        token = self._get_jwt()
        if not token:
            return self._error(
                "Credencial Ghost inválida: admin_api_key debe tener formato 'key_id:secret'"
            )
        import httpx

        try:
            r = httpx.post(
                f"{base}/posts/",
                json={
                    "posts": [
                        {
                            "title": title,
                            "html": html,
                            "status": status,
                            "tags": [{"name": t} for t in (tags or [])],
                        }
                    ]
                },
                headers={"Authorization": f"Ghost {token}"},
                timeout=30,
            )
            r.raise_for_status()
            post = r.json()["posts"][0]
            return self._success(
                f"Post '{title}' creado en Ghost. URL: {post.get('url', '')}",
                raw_data={"post_id": post.get("id"), "url": post.get("url")},
            )
        except Exception as e:
            return self._error(f"Error Ghost: {e}")

    def _update_post(
        self, post_id: str = "", html: str = None, status: str = None
    ) -> ToolResult:
        base = self._get_base_url()
        if not base:
            return self._error("Credencial Ghost no configurada: url")
        token = self._get_jwt()
        if not token:
            return self._error("Credencial Ghost inválida")
        body: dict = {}
        if html:
            body["html"] = html
        if status:
            body["status"] = status
        if not body:
            return self._error("Nada que actualizar")
        from tools.utils.dates import now_iso

        body["updated_at"] = now_iso()
        import httpx

        try:
            r = httpx.put(
                f"{base}/posts/{post_id}/",
                json={"posts": [body]},
                headers={"Authorization": f"Ghost {token}"},
                timeout=30,
            )
            r.raise_for_status()
            return self._success(f"Post {post_id} actualizado en Ghost")
        except Exception as e:
            return self._error(f"Error Ghost: {e}")

    def _get_posts(self, status: str = "published", limit: int = 10) -> ToolResult:
        base = self._get_base_url()
        if not base:
            return self._error("Credencial Ghost no configurada: url")
        token = self._get_jwt()
        if not token:
            return self._error("Credencial Ghost inválida")
        import httpx

        try:
            r = httpx.get(
                f"{base}/posts/",
                params={"limit": limit, "filter": f"status:{status}"},
                headers={"Authorization": f"Ghost {token}"},
                timeout=30,
            )
            r.raise_for_status()
            posts = r.json().get("posts", [])
            lines = [f"- [{p['id']}] {p['title']} ({p['status']})" for p in posts]
            return self._success(
                "\n".join(lines) if lines else "Sin posts",
                raw_data={"posts": posts},
            )
        except Exception as e:
            return self._error(f"Error Ghost: {e}")
