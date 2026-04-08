from tools.base import BaseTool, ToolResult, tool
from tools.utils.http import HTTPClient

_BASE = "https://api.hubapi.com"


@tool
class HubSpotTool(BaseTool):
    name = "hubspot"
    description = (
        "Gestiona contactos y deals en HubSpot CRM. "
        "Úsala para crear contactos, actualizar deals "
        "y consultar el pipeline de ventas."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "create_contact":
            return self._create_contact(**kwargs)
        if action == "update_deal":
            return self._update_deal(**kwargs)
        if action == "get_pipeline":
            return self._get_pipeline()
        if action == "create_task":
            return self._create_task(**kwargs)
        if action == "get_contacts":
            return self._get_contacts(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _client(self) -> HTTPClient:
        return HTTPClient(
            _BASE,
            headers={
                "Authorization": f"Bearer {self.credentials['api_key']}",
                "Content-Type": "application/json",
            },
        )

    def _check_key(self) -> ToolResult | None:
        if not self.credentials.get("api_key"):
            return self._error("Credencial api_key no configurada")
        return None

    def _create_contact(
        self,
        name: str = "",
        email: str = "",
        phone: str = "",
        company: str = "",
    ) -> ToolResult:
        err = self._check_key()
        if err:
            return err

        parts = name.split(" ", 1)
        firstname = parts[0]
        lastname = parts[1] if len(parts) > 1 else ""

        resp = self._client().post(
            "/crm/v3/objects/contacts",
            json={
                "properties": {
                    "firstname": firstname,
                    "lastname": lastname,
                    "email": email,
                    "phone": phone,
                    "company": company,
                }
            },
        )
        if not resp or "id" not in resp:
            return self._error("Error al crear el contacto en HubSpot")

        contact_id = resp["id"]
        return self._success(
            f"Contacto {name} creado en HubSpot. ID: {contact_id}",
            raw_data={"contact_id": contact_id},
        )

    def _update_deal(
        self,
        deal_id: str = "",
        stage: str = None,
        amount: float = None,
    ) -> ToolResult:
        err = self._check_key()
        if err:
            return err

        properties: dict = {}
        if stage is not None:
            properties["dealstage"] = stage
        if amount is not None:
            properties["amount"] = str(amount)

        resp = self._client().post(
            f"/crm/v3/objects/deals/{deal_id}",
            json={"properties": properties},
        )
        # HubSpot PATCH returns the updated object; we use post() which wraps the call
        # A None response means HTTP error
        if resp is None:
            return self._error(f"Error al actualizar el deal {deal_id} en HubSpot")

        return self._success(
            f"Deal {deal_id} actualizado",
            raw_data={"deal_id": deal_id, "properties": properties},
        )

    def _get_pipeline(self) -> ToolResult:
        err = self._check_key()
        if err:
            return err

        resp = self._client().get(
            "/crm/v3/objects/deals",
            params={"properties": "dealname,dealstage,amount", "limit": 100},
        )
        if not resp:
            return self._error("Error al obtener el pipeline de HubSpot")

        results = resp.get("results", [])
        if not results:
            return self._success("Pipeline vacío — sin deals registrados")

        lines = [f"Pipeline de ventas ({len(results)} deals):"]
        for deal in results:
            props = deal.get("properties", {})
            name = props.get("dealname", "Sin nombre")
            stage = props.get("dealstage", "N/A")
            amount = props.get("amount", "0")
            lines.append(f"  - {name} | Etapa: {stage} | Monto: ${amount}")

        return self._success("\n".join(lines), raw_data={"deals": results})

    def _create_task(
        self,
        contact_id: str = "",
        title: str = "",
        due_date: str = None,
    ) -> ToolResult:
        err = self._check_key()
        if err:
            return err

        properties: dict = {
            "hs_task_subject": title,
            "hs_task_status": "NOT_STARTED",
        }
        if due_date:
            properties["hs_timestamp"] = due_date

        resp = self._client().post(
            "/crm/v3/objects/tasks",
            json={"properties": properties},
        )
        if not resp or "id" not in resp:
            return self._error(f"Error al crear la tarea en HubSpot")

        task_id = resp["id"]
        return self._success(
            f"Tarea '{title}' creada",
            raw_data={"task_id": task_id, "contact_id": contact_id},
        )

    def _get_contacts(self, limit: int = 50) -> ToolResult:
        err = self._check_key()
        if err:
            return err

        resp = self._client().get(
            "/crm/v3/objects/contacts",
            params={"limit": limit, "properties": "firstname,lastname,email"},
        )
        if not resp:
            return self._error("Error al obtener contactos de HubSpot")

        results = resp.get("results", [])
        lines = [f"Contactos en HubSpot ({len(results)}):"]
        for c in results:
            props = c.get("properties", {})
            name = f"{props.get('firstname', '')} {props.get('lastname', '')}".strip()
            email = props.get("email", "sin email")
            lines.append(f"  - {name or 'Sin nombre'} <{email}>")

        return self._success("\n".join(lines), raw_data={"contacts": results})
