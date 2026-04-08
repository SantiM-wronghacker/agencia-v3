import re

from tools.base import BaseTool, ToolResult, tool
from tools.utils.http import HTTPClient

_BASE = "https://graph.facebook.com/v18.0"


@tool
class WhatsAppTool(BaseTool):
    name = "whatsapp"
    description = (
        "Envía mensajes de WhatsApp Business. "
        "Úsala para contactar clientes, "
        "enviar cotizaciones o confirmaciones."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "send_message":
            return self._send_message(**kwargs)
        if action == "send_template":
            return self._send_template(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _check_credentials(self) -> ToolResult | None:
        if not self.credentials.get("token"):
            return self._error("Credencial token no configurada")
        if not self.credentials.get("phone_number_id"):
            return self._error("Credencial phone_number_id no configurada")
        return None

    def _clean_phone(self, number: str) -> str:
        """Strip non-digits; prepend 52 (Mexico) if no country code present."""
        digits = re.sub(r"\D", "", number)
        # If it starts with 52 and has 12 digits it already has country code
        # Mexican numbers without country code have 10 digits
        if len(digits) == 10:
            digits = "52" + digits
        return digits

    def _client(self) -> HTTPClient:
        return HTTPClient(
            _BASE,
            headers={
                "Authorization": f"Bearer {self.credentials['token']}",
                "Content-Type": "application/json",
            },
        )

    def _send_message(self, to: str = "", message: str = "") -> ToolResult:
        err = self._check_credentials()
        if err:
            return err

        phone_number_id = self.credentials["phone_number_id"]
        to_clean = self._clean_phone(to)

        resp = self._client().post(
            f"/{phone_number_id}/messages",
            json={
                "messaging_product": "whatsapp",
                "to": to_clean,
                "type": "text",
                "text": {"body": message},
            },
        )
        if not resp:
            return self._error(f"Error al enviar WhatsApp a {to}")

        return self._success(
            f"WhatsApp enviado a {to}",
            raw_data={"to": to_clean, "message_id": resp.get("messages", [{}])[0].get("id", "")},
        )

    def _send_template(
        self,
        to: str = "",
        template_name: str = "",
        variables: list = None,
    ) -> ToolResult:
        err = self._check_credentials()
        if err:
            return err

        phone_number_id = self.credentials["phone_number_id"]

        resp = self._client().post(
            f"/{phone_number_id}/messages",
            json={
                "messaging_product": "whatsapp",
                "to": to,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {"code": "es_MX"},
                    "components": [
                        {
                            "type": "body",
                            "parameters": variables or [],
                        }
                    ],
                },
            },
        )
        if not resp:
            return self._error(f"Error al enviar template WhatsApp a {to}")

        return self._success(
            f"Template '{template_name}' enviado a {to}",
            raw_data={"to": to, "template": template_name},
        )
