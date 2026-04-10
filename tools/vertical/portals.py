from tools.base import BaseTool, ToolResult, tool

_INMUEBLES24_API = "https://api.inmuebles24.com/v1/properties"
_LAMUDI_API = "https://api.lamudi.com.mx/v1/listings"


@tool
class PortalsTool(BaseTool):
    name = "portals"
    description = (
        "Publica propiedades en portales inmobiliarios. "
        "Úsala para publicar en Inmuebles24, "
        "Lamudi u otros portales."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "post_inmuebles24":
            return self._post_inmuebles24(**kwargs)
        if action == "post_lamudi":
            return self._post_lamudi(**kwargs)
        if action == "list_active":
            return self._list_active()
        return self._error(f"Acción '{action}' no soportada")

    def _post_inmuebles24(self, property_data: dict = None) -> ToolResult:
        api_key = self.credentials.get("inmuebles24_api_key")
        if not api_key:
            return self._error("Credencial no configurada: inmuebles24_api_key")
        import httpx

        try:
            r = httpx.post(
                _INMUEBLES24_API,
                json=property_data or {},
                headers={"Authorization": f"Bearer {api_key}",
                         "Content-Type": "application/json"},
                timeout=30,
            )
            r.raise_for_status()
            data = r.json()
            listing_id = data.get("id", "N/A")
            return self._success(
                f"Propiedad publicada en Inmuebles24. ID: {listing_id}",
                raw_data={"listing_id": listing_id, "portal": "inmuebles24"},
            )
        except Exception as e:
            return self._error(f"Error al publicar en Inmuebles24: {e}")

    def _post_lamudi(self, property_data: dict = None) -> ToolResult:
        api_key = self.credentials.get("lamudi_api_key")
        if not api_key:
            return self._error("Credencial no configurada: lamudi_api_key")
        import httpx

        try:
            r = httpx.post(
                _LAMUDI_API,
                json=property_data or {},
                headers={"Authorization": f"Bearer {api_key}",
                         "Content-Type": "application/json"},
                timeout=30,
            )
            r.raise_for_status()
            data = r.json()
            listing_id = data.get("id", "N/A")
            return self._success(
                f"Propiedad publicada en Lamudi. ID: {listing_id}",
                raw_data={"listing_id": listing_id, "portal": "lamudi"},
            )
        except Exception as e:
            return self._error(f"Error al publicar en Lamudi: {e}")

    def _list_active(self) -> ToolResult:
        portals = []
        if self.credentials.get("inmuebles24_api_key"):
            portals.append("Inmuebles24")
        if self.credentials.get("lamudi_api_key"):
            portals.append("Lamudi")
        if not portals:
            return self._success(
                "Sin portales configurados. Proporciona inmuebles24_api_key o lamudi_api_key."
            )
        return self._success(
            f"Portales activos: {', '.join(portals)}",
            raw_data={"portals": portals},
        )
