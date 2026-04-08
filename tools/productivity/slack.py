from tools.base import BaseTool, ToolResult, tool
from tools.utils.http import HTTPClient

_BASE = "https://slack.com/api"


@tool
class SlackTool(BaseTool):
    name = "slack"
    description = (
        "Envía mensajes en Slack. "
        "Úsala para notificar al equipo, "
        "enviar reportes o alertas internas."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "send_message":
            return self._send_message(**kwargs)
        if action == "send_dm":
            return self._send_dm(**kwargs)
        if action == "list_channels":
            return self._list_channels()
        return self._error(f"Acción '{action}' no soportada")

    def _check_token(self) -> ToolResult | None:
        if not self.credentials.get("bot_token"):
            return self._error("Credencial bot_token no configurada")
        return None

    def _client(self) -> HTTPClient:
        return HTTPClient(
            _BASE,
            headers={
                "Authorization": f"Bearer {self.credentials['bot_token']}",
                "Content-Type": "application/json",
            },
        )

    def _send_message(
        self, channel: str = "", text: str = "", blocks: list = None
    ) -> ToolResult:
        err = self._check_token()
        if err:
            return err

        body: dict = {"channel": channel, "text": text}
        if blocks:
            body["blocks"] = blocks

        resp = self._client().post("/chat.postMessage", json=body)
        if not resp or not resp.get("ok"):
            error_msg = resp.get("error", "desconocido") if resp else "sin respuesta"
            return self._error(f"Error al enviar mensaje a Slack: {error_msg}")

        return self._success(
            f"Mensaje enviado a #{channel}",
            raw_data={"ts": resp.get("ts", ""), "channel": channel},
        )

    def _send_dm(self, user_id: str = "", text: str = "") -> ToolResult:
        err = self._check_token()
        if err:
            return err

        client = self._client()

        # Open DM channel
        dm_resp = client.post("/conversations.open", json={"users": [user_id]})
        if not dm_resp or not dm_resp.get("ok"):
            error_msg = dm_resp.get("error", "desconocido") if dm_resp else "sin respuesta"
            return self._error(f"Error al abrir DM con {user_id}: {error_msg}")

        dm_channel = dm_resp["channel"]["id"]

        # Send message to DM channel
        msg_resp = client.post(
            "/chat.postMessage",
            json={"channel": dm_channel, "text": text},
        )
        if not msg_resp or not msg_resp.get("ok"):
            error_msg = msg_resp.get("error", "desconocido") if msg_resp else "sin respuesta"
            return self._error(f"Error al enviar DM a {user_id}: {error_msg}")

        return self._success(
            f"DM enviado a {user_id}",
            raw_data={"ts": msg_resp.get("ts", ""), "channel": dm_channel},
        )

    def _list_channels(self) -> ToolResult:
        err = self._check_token()
        if err:
            return err

        resp = HTTPClient(
            _BASE,
            headers={"Authorization": f"Bearer {self.credentials['bot_token']}"},
        ).get(
            "/conversations.list",
            params={"types": "public_channel,private_channel", "limit": 200},
        )
        if not resp or not resp.get("ok"):
            error_msg = resp.get("error", "desconocido") if resp else "sin respuesta"
            return self._error(f"Error al listar canales de Slack: {error_msg}")

        channels = resp.get("channels", [])
        lines = [f"Canales en Slack ({len(channels)}):"]
        for ch in channels:
            prefix = "#" if not ch.get("is_private") else "🔒"
            lines.append(f"  {prefix}{ch.get('name', '?')} (ID: {ch.get('id', '?')})")

        return self._success("\n".join(lines), raw_data={"channels": channels})
