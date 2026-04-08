from pathlib import Path

from tools.base import BaseTool, ToolResult, tool
from tools.utils.http import HTTPClient

_BASE = "https://open.tiktokapis.com"


@tool
class TikTokTool(BaseTool):
    name = "tiktok"
    description = (
        "Publica videos en TikTok Business. "
        "Úsala para subir videos cortos."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "upload_video":
            return self._upload_video(**kwargs)
        if action == "get_stats":
            return self._get_stats(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _upload_video(
        self,
        video_path: str = "",
        caption: str = "",
        hashtags: list = None,
    ) -> ToolResult:
        access_token = self.credentials.get("access_token")
        open_id = self.credentials.get("open_id")
        if not access_token:
            return self._error("Credencial access_token no configurada")
        if not open_id:
            return self._error("Credencial open_id no configurada")
        if not video_path or not Path(video_path).exists():
            return self._error(f"El archivo de video no existe: {video_path}")

        title = caption
        if hashtags:
            title += " " + " ".join(f"#{tag}" for tag in hashtags)

        client = HTTPClient(
            _BASE,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        )
        body = {
            "post_info": {
                "title": title,
                "privacy_level": "PUBLIC_TO_EVERYONE",
            },
            "source_info": {
                "source": "FILE_UPLOAD",
            },
        }
        resp = client.post("/v2/post/publish/video/init/", json=body)
        if not resp or "data" not in resp:
            return self._error("Error al iniciar la subida del video en TikTok")

        publish_id = resp["data"].get("publish_id", "")
        return self._success(
            f"Video subido a TikTok. ID: {publish_id}",
            raw_data={"publish_id": publish_id},
        )

    def _get_stats(self, video_id: str = "") -> ToolResult:
        access_token = self.credentials.get("access_token")
        if not access_token:
            return self._error("Credencial access_token no configurada")
        if not video_id:
            return self._error("Parámetro video_id requerido")

        client = HTTPClient(
            _BASE,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        )
        resp = client.post(
            "/v2/video/list/",
            json={"filters": {"video_ids": [video_id]}},
        )
        if not resp or "data" not in resp:
            return self._error("Error al obtener estadísticas del video en TikTok")

        videos = resp["data"].get("videos", [{}])
        v = videos[0] if videos else {}
        views = v.get("view_count", 0)
        likes = v.get("like_count", 0)
        comments = v.get("comment_count", 0)
        output = (
            f"Estadísticas video TikTok {video_id}:\n"
            f"  Vistas: {views}\n"
            f"  Likes: {likes}\n"
            f"  Comentarios: {comments}"
        )
        return self._success(output, raw_data=resp)
