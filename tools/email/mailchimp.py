from tools.base import BaseTool, ToolResult, tool


@tool
class MailchimpTool(BaseTool):
    name = "mailchimp"
    description = (
        "Gestiona campañas de email con Mailchimp. "
        "Úsala para crear campañas, gestionar listas y "
        "enviar newsletters a suscriptores."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "create_campaign":
            return self._create_campaign(**kwargs)
        if action == "send_campaign":
            return self._send_campaign(**kwargs)
        if action == "list_campaigns":
            return self._list_campaigns(**kwargs)
        if action == "add_subscriber":
            return self._add_subscriber(**kwargs)
        if action == "get_stats":
            return self._get_stats(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _get_client(self):
        import httpx

        api_key = self.credentials.get("api_key", "")
        if not api_key:
            return None, self._error("Credencial api_key no configurada")
        server = api_key.split("-")[-1] if "-" in api_key else "us1"
        base_url = f"https://{server}.api.mailchimp.com/3.0"
        client = httpx.Client(
            base_url=base_url,
            auth=("anystring", api_key),
            timeout=30,
        )
        return client, None

    def _create_campaign(
        self,
        list_id: str = "",
        subject: str = "",
        from_name: str = "",
        reply_to: str = "",
        html_content: str = "",
    ) -> ToolResult:
        if not list_id or not subject:
            return self._error("Parámetros list_id y subject son obligatorios")
        client, err = self._get_client()
        if err:
            return err
        try:
            payload = {
                "type": "regular",
                "recipients": {"list_id": list_id},
                "settings": {
                    "subject_line": subject,
                    "from_name": from_name or "Agencia",
                    "reply_to": reply_to,
                },
            }
            r = client.post("/campaigns", json=payload)
            r.raise_for_status()
            campaign = r.json()
            campaign_id = campaign.get("id", "")

            if html_content and campaign_id:
                client.put(
                    f"/campaigns/{campaign_id}/content",
                    json={"html": html_content},
                )

            return self._success(
                f"Campaña creada: {campaign_id} — {subject}",
                raw_data={"campaign_id": campaign_id, "subject": subject},
            )
        except Exception as e:
            return self._error(f"Error al crear campaña: {e}")

    def _send_campaign(self, campaign_id: str = "") -> ToolResult:
        if not campaign_id:
            return self._error("Parámetro campaign_id es obligatorio")
        client, err = self._get_client()
        if err:
            return err
        try:
            r = client.post(f"/campaigns/{campaign_id}/actions/send")
            r.raise_for_status()
            return self._success(
                f"Campaña {campaign_id} enviada correctamente",
                raw_data={"campaign_id": campaign_id},
            )
        except Exception as e:
            return self._error(f"Error al enviar campaña: {e}")

    def _list_campaigns(self, count: int = 10) -> ToolResult:
        client, err = self._get_client()
        if err:
            return err
        try:
            r = client.get("/campaigns", params={"count": count})
            r.raise_for_status()
            campaigns = r.json().get("campaigns", [])
            names = [
                f"{c.get('id')} — {c.get('settings', {}).get('subject_line', '')}"
                for c in campaigns
            ]
            return self._success(
                f"{len(campaigns)} campañas encontradas",
                raw_data={"campaigns": names},
            )
        except Exception as e:
            return self._error(f"Error al listar campañas: {e}")

    def _add_subscriber(
        self,
        list_id: str = "",
        email: str = "",
        first_name: str = "",
        last_name: str = "",
    ) -> ToolResult:
        if not list_id or not email:
            return self._error("Parámetros list_id y email son obligatorios")
        client, err = self._get_client()
        if err:
            return err
        try:
            payload = {
                "email_address": email,
                "status": "subscribed",
                "merge_fields": {"FNAME": first_name, "LNAME": last_name},
            }
            r = client.post(f"/lists/{list_id}/members", json=payload)
            r.raise_for_status()
            return self._success(
                f"Suscriptor {email} añadido a lista {list_id}",
                raw_data={"email": email, "list_id": list_id},
            )
        except Exception as e:
            return self._error(f"Error al añadir suscriptor: {e}")

    def _get_stats(self, campaign_id: str = "") -> ToolResult:
        if not campaign_id:
            return self._error("Parámetro campaign_id es obligatorio")
        client, err = self._get_client()
        if err:
            return err
        try:
            r = client.get(f"/reports/{campaign_id}")
            r.raise_for_status()
            data = r.json()
            opens = data.get("opens", {})
            clicks = data.get("clicks", {})
            return self._success(
                f"Stats — Abiertos: {opens.get('opens_total', 0)}, "
                f"Clicks: {clicks.get('clicks_total', 0)}",
                raw_data=data,
            )
        except Exception as e:
            return self._error(f"Error al obtener stats: {e}")
