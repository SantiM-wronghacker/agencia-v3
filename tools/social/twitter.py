from tools.base import BaseTool, ToolResult, tool
from tools.utils.http import HTTPClient

_BASE = "https://api.twitter.com"


@tool
class TwitterTool(BaseTool):
    name = "twitter"
    description = (
        "Publica tweets en X (Twitter). "
        "Úsala para posts de texto corto."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "post_tweet":
            return self._post_tweet(**kwargs)
        if action == "get_stats":
            return self._get_stats(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _post_tweet(self, text: str = "") -> ToolResult:
        bearer_token = self.credentials.get("bearer_token")
        if not bearer_token:
            return self._error("Credencial bearer_token no configurada")

        if len(text) > 280:
            return self._error(
                f"El tweet supera los 280 caracteres ({len(text)} caracteres)"
            )

        client = HTTPClient(
            _BASE,
            headers={
                "Authorization": f"Bearer {bearer_token}",
                "Content-Type": "application/json",
            },
        )
        resp = client.post("/2/tweets", json={"text": text})
        if not resp or "data" not in resp:
            return self._error("Error al publicar el tweet")

        tweet_id = resp["data"].get("id", "")
        return self._success(
            f"Tweet publicado. ID: {tweet_id}",
            raw_data={"tweet_id": tweet_id},
        )

    def _get_stats(self, tweet_id: str = "") -> ToolResult:
        bearer_token = self.credentials.get("bearer_token")
        if not bearer_token:
            return self._error("Credencial bearer_token no configurada")
        if not tweet_id:
            return self._error("Parámetro tweet_id requerido")

        client = HTTPClient(
            _BASE,
            headers={"Authorization": f"Bearer {bearer_token}"},
        )
        resp = client.get(
            f"/2/tweets/{tweet_id}",
            params={"tweet.fields": "public_metrics"},
        )
        if not resp or "data" not in resp:
            return self._error("Error al obtener estadísticas del tweet")

        metrics = resp["data"].get("public_metrics", {})
        output = (
            f"Estadísticas tweet {tweet_id}:\n"
            f"  Likes: {metrics.get('like_count', 0)}\n"
            f"  Retweets: {metrics.get('retweet_count', 0)}\n"
            f"  Respuestas: {metrics.get('reply_count', 0)}\n"
            f"  Impresiones: {metrics.get('impression_count', 0)}"
        )
        return self._success(output, raw_data=metrics)
