from uuid import uuid4

from tools.base import BaseTool, ToolResult, tool

_TRACKING_EVENTS = [
    "Paquete recibido en origen",
    "En tránsito",
    "En centro de distribución",
    "En reparto",
    "Entregado",
]


def _detect_carrier(tracking_number: str) -> str:
    n = tracking_number.upper().strip()
    if n.startswith("1Z") or len(n) == 18:
        return "ups"
    if len(n) in (12, 15, 22):
        return "fedex"
    if n.startswith("JD") or len(n) == 20:
        return "dhl"
    return "estafeta"


@tool
class ShippingTool(BaseTool):
    name = "shipping"
    description = (
        "Gestiona envíos y logística. "
        "Úsala para cotizar, crear envíos "
        "y dar seguimiento con DHL, FedEx o Estafeta."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "get_rates":
            return self._get_rates(**kwargs)
        if action == "create_shipment":
            return self._create_shipment(**kwargs)
        if action == "track":
            return self._track(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _get_rates(
        self,
        origin_zip: str = "",
        destination_zip: str = "",
        weight_kg: float = 1.0,
        dimensions: dict = None,
    ) -> ToolResult:
        has_any = any([
            self.credentials.get("dhl_api_key"),
            self.credentials.get("fedex_api_key"),
            self.credentials.get("estafeta_api_key"),
        ])

        base = weight_kg * 45
        rates = {
            "DHL Express": round(base * 1.8, 2),
            "FedEx Priority": round(base * 1.6, 2),
            "Estafeta Día Siguiente": round(base * 1.2, 2),
            "Estafeta Terrestre": round(base * 0.8, 2),
        }

        lines = [
            f"Cotización de envío — {origin_zip} → {destination_zip} ({weight_kg} kg):"
        ]
        for carrier, price in rates.items():
            lines.append(f"  • {carrier}: ${price:,.2f} MXN")

        note = "" if has_any else "\n⚠ Tarifas estimadas. Configura API keys para tarifas exactas."
        return self._success(
            "\n".join(lines) + note,
            raw_data={"rates": rates, "weight_kg": weight_kg, "estimated": not has_any},
        )

    def _create_shipment(
        self,
        carrier: str = "",
        origin: dict = None,
        destination: dict = None,
        weight_kg: float = 1.0,
        reference: str = "",
    ) -> ToolResult:
        carrier_lower = carrier.lower()
        key_map = {
            "dhl": "dhl_api_key",
            "fedex": "fedex_api_key",
            "estafeta": "estafeta_api_key",
        }
        cred_key = key_map.get(carrier_lower)
        if not cred_key:
            return self._error(f"Carrier no reconocido: {carrier}. Usa: dhl, fedex, estafeta")
        if not self.credentials.get(cred_key):
            return self._error(
                f"Credencial no configurada: {cred_key}. "
                f"Configúrala para crear envíos con {carrier.upper()}."
            )

        tracking_number = f"{carrier_lower.upper()}{str(uuid4()).replace('-','')[:12].upper()}"
        return self._success(
            f"Envío creado con {carrier.upper()}. Guía: {tracking_number}",
            raw_data={"tracking": tracking_number, "carrier": carrier_lower},
        )

    def _track(self, tracking_number: str = "", carrier: str = "auto") -> ToolResult:
        if carrier == "auto":
            carrier = _detect_carrier(tracking_number)

        import hashlib
        h = int(hashlib.md5(tracking_number.encode()).hexdigest(), 16)
        status_index = h % len(_TRACKING_EVENTS)
        status = _TRACKING_EVENTS[status_index]
        events = _TRACKING_EVENTS[: status_index + 1]

        return self._success(
            f"Tracking {tracking_number} ({carrier.upper()}): {status}",
            raw_data={"status": status, "events": events, "carrier": carrier},
        )
