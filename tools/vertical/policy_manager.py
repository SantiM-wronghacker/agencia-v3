import json
from pathlib import Path
from uuid import uuid4

from tools.base import BaseTool, ToolResult, tool
from tools.utils.dates import now_iso, days_from_now

_DATA_FILE = Path("data/policies.json")

_RATES = {
    "auto": 0.03,
    "hogar": 0.005,
    "vida": 0.01,
    "gmm": 0.08,
    "negocio": 0.02,
}


def _load() -> list:
    if not _DATA_FILE.exists():
        return []
    try:
        return json.loads(_DATA_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def _save(data: list) -> None:
    _DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    _DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


@tool
class PolicyManagerTool(BaseTool):
    name = "policy_manager"
    description = (
        "Gestiona pólizas de seguros. "
        "Úsala para generar cotizaciones, "
        "gestionar renovaciones y crear reportes de siniestros."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "generate_quote":
            return self._generate_quote(**kwargs)
        if action == "create_policy":
            return self._create_policy(**kwargs)
        if action == "renewal_reminder":
            return self._renewal_reminder(**kwargs)
        if action == "create_claim":
            return self._create_claim(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _generate_quote(
        self,
        coverage_type: str = "auto",
        client_data: dict = None,
        sum_insured: float = 0.0,
    ) -> ToolResult:
        rate = _RATES.get(coverage_type)
        if rate is None:
            return self._error(
                f"Tipo de cobertura no válido: {coverage_type}. "
                f"Usa: {', '.join(_RATES.keys())}"
            )

        prima_neta = sum_insured * rate
        derechos = prima_neta * 0.05
        subtotal = prima_neta + derechos
        iva = subtotal * 0.16
        prima_total = subtotal + iva
        vigencia_desde = now_iso()[:10]
        vigencia_hasta = days_from_now(365)

        client_name = (client_data or {}).get("name", "Cliente")
        lines = [
            f"COTIZACIÓN DE SEGURO — {coverage_type.upper()}",
            f"Cliente: {client_name}",
            f"Suma asegurada: ${sum_insured:,.2f}",
            f"Prima neta: ${prima_neta:,.2f}",
            f"Derechos: ${derechos:,.2f}",
            f"Subtotal: ${subtotal:,.2f}",
            f"IVA (16%): ${iva:,.2f}",
            f"Prima total: ${prima_total:,.2f}",
            f"Vigencia: {vigencia_desde} al {vigencia_hasta}",
        ]
        quote_data = {
            "coverage_type": coverage_type,
            "sum_insured": sum_insured,
            "prima_neta": prima_neta,
            "prima_total": prima_total,
            "vigencia_hasta": vigencia_hasta,
            "client_data": client_data or {},
        }
        return self._success("\n".join(lines), raw_data=quote_data)

    def _create_policy(
        self,
        quote_data: dict = None,
        policy_number: str = None,
    ) -> ToolResult:
        if not policy_number:
            policy_number = f"POL-{str(uuid4())[:8].upper()}"
        expiry = days_from_now(365)
        policy = {
            "policy_number": policy_number,
            "quote_data": quote_data or {},
            "status": "active",
            "issued_at": now_iso(),
            "expires_at": expiry,
        }
        data = _load()
        data.append(policy)
        _save(data)
        return self._success(
            f"Póliza {policy_number} creada. Vigencia hasta {expiry}",
            raw_data=policy,
        )

    def _renewal_reminder(
        self,
        policy_id: str = "",
        days_before: int = 30,
    ) -> ToolResult:
        data = _load()
        policy = next(
            (p for p in data if p.get("policy_number") == policy_id),
            None,
        )
        if not policy:
            return self._error(f"Póliza '{policy_id}' no encontrada")

        expires_at = policy.get("expires_at", "")
        coverage = policy.get("quote_data", {}).get("coverage_type", "seguro")
        client_name = policy.get("quote_data", {}).get("client_data", {}).get("name", "Cliente")
        prima = policy.get("quote_data", {}).get("prima_total", 0)

        message = (
            f"Estimado/a {client_name},\n\n"
            f"Le informamos que su póliza de {coverage} (No. {policy_id}) "
            f"vence el {expires_at}.\n\n"
            f"Para renovarla, contacte a su asesor. Prima estimada de renovación: ${prima:,.2f}\n\n"
            f"¡No deje vencer su cobertura!"
        )
        return self._success(
            f"Mensaje de renovación para póliza {policy_id}:\n\n{message}",
            raw_data={"policy_id": policy_id, "expires_at": expires_at, "message": message},
        )

    def _create_claim(
        self,
        policy_id: str = "",
        incident_date: str = "",
        description: str = "",
        estimated_loss: float = 0.0,
    ) -> ToolResult:
        folio = f"SIN-{str(uuid4())[:8].upper()}"
        claim = {
            "folio": folio,
            "policy_id": policy_id,
            "incident_date": incident_date,
            "description": description,
            "estimated_loss": estimated_loss,
            "status": "reported",
            "reported_at": now_iso(),
        }

        claims_file = Path("data/claims.json")
        claims = []
        if claims_file.exists():
            try:
                claims = json.loads(claims_file.read_text(encoding="utf-8"))
            except Exception:
                claims = []
        claims.append(claim)
        claims_file.parent.mkdir(parents=True, exist_ok=True)
        claims_file.write_text(json.dumps(claims, indent=2, ensure_ascii=False), encoding="utf-8")

        return self._success(
            f"Siniestro reportado. Folio: {folio}. Póliza: {policy_id}",
            raw_data=claim,
        )
