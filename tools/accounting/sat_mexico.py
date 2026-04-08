import re
from datetime import datetime

from tools.base import BaseTool, ToolResult, tool

# ISR 2024 monthly table for physical persons (actividad empresarial)
_ISR_TABLE = [
    (0.01,      746.04,     0.00,       0.0192),
    (746.05,    6332.05,    14.32,      0.064),
    (6332.06,   11128.01,   371.83,     0.1088),
    (11128.02,  12935.82,   893.63,     0.16),
    (12935.83,  15487.71,   1182.88,    0.1792),
    (15487.72,  31236.49,   1640.18,    0.2136),
    (31236.50,  49233.00,   5004.12,    0.2352),
    (49233.01,  93993.90,   9236.89,    0.30),
    (93993.91,  125325.20,  22665.17,   0.32),
    (125325.21, 375975.61,  32691.18,   0.34),
    (375975.62, float("inf"), 117912.32, 0.35),
]


@tool
class SATMexicoTool(BaseTool):
    name = "sat_mexico"
    description = (
        "Herramientas fiscales para México. "
        "Úsala para validar RFC, calcular impuestos "
        "IVA e ISR, y generar XML de CFDI."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "validate_rfc":
            return self._validate_rfc(**kwargs)
        if action == "calculate_iva":
            return self._calculate_iva(**kwargs)
        if action == "calculate_isr":
            return self._calculate_isr(**kwargs)
        if action == "calculate_retenciones":
            return self._calculate_retenciones(**kwargs)
        if action == "generate_cfdi_data":
            return self._generate_cfdi_data(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _validate_rfc(self, rfc: str = "") -> ToolResult:
        rfc = rfc.strip().upper()
        pattern = r"^[A-ZÑ&]{3,4}\d{6}[A-Z\d]{3}$"
        if not re.match(pattern, rfc):
            return self._error(f"RFC {rfc} inválido")

        tipo = "Física" if len(rfc) == 13 else "Moral"
        return self._success(
            f"RFC {rfc} válido. Tipo: Persona {tipo}",
            raw_data={"rfc": rfc, "tipo": tipo},
        )

    def _calculate_iva(self, subtotal: float = 0.0, rate: float = 0.16) -> ToolResult:
        subtotal = float(subtotal)
        iva = round(subtotal * rate, 2)
        total = round(subtotal + iva, 2)
        return self._success(
            f"Subtotal: ${subtotal:,.2f}\n"
            f"IVA ({rate * 100:.0f}%): ${iva:,.2f}\n"
            f"Total: ${total:,.2f}",
            raw_data={"subtotal": subtotal, "iva": iva, "total": total, "rate": rate},
        )

    def _calculate_isr(self, ingreso_mensual: float = 0.0) -> ToolResult:
        ingreso = float(ingreso_mensual)
        isr_mensual = 0.0

        for lim_inf, lim_sup, cuota_fija, porcentaje in _ISR_TABLE:
            if lim_inf <= ingreso <= lim_sup:
                excedente = ingreso - lim_inf
                isr_mensual = round(cuota_fija + excedente * porcentaje, 2)
                break

        isr_anual = round(isr_mensual * 12, 2)
        tasa_efectiva = round((isr_mensual / ingreso * 100) if ingreso > 0 else 0, 2)

        return self._success(
            f"Cálculo ISR 2024:\n"
            f"  Ingreso mensual: ${ingreso:,.2f}\n"
            f"  ISR mensual: ${isr_mensual:,.2f}\n"
            f"  ISR anual estimado: ${isr_anual:,.2f}\n"
            f"  Tasa efectiva: {tasa_efectiva}%",
            raw_data={
                "ingreso_mensual": ingreso,
                "isr_mensual": isr_mensual,
                "isr_anual": isr_anual,
                "tasa_efectiva": tasa_efectiva,
            },
        )

    def _calculate_retenciones(
        self, monto: float = 0.0, tipo: str = "honorarios"
    ) -> ToolResult:
        monto = float(monto)
        tipo = tipo.lower()

        if tipo == "honorarios":
            iva = round(monto * 0.16, 2)
            isr_retenido = round(monto * 0.10, 2)
            iva_retenido = round(iva * (2 / 3), 2)  # 10.67% del total ≈ 2/3 del IVA
            neto = round(monto + iva - isr_retenido - iva_retenido, 2)
            output = (
                f"Retenciones para Honorarios:\n"
                f"  Monto base: ${monto:,.2f}\n"
                f"  IVA (16%): ${iva:,.2f}\n"
                f"  ISR retenido (10%): ${isr_retenido:,.2f}\n"
                f"  IVA retenido (2/3): ${iva_retenido:,.2f}\n"
                f"  Neto a pagar: ${neto:,.2f}"
            )
            raw = {
                "monto": monto, "iva": iva,
                "isr_retenido": isr_retenido, "iva_retenido": iva_retenido,
                "neto": neto,
            }
        elif tipo == "arrendamiento":
            iva = round(monto * 0.16, 2)
            isr_retenido = round(monto * 0.10, 2)
            neto = round(monto + iva - isr_retenido, 2)
            output = (
                f"Retenciones para Arrendamiento:\n"
                f"  Monto base: ${monto:,.2f}\n"
                f"  IVA (16%): ${iva:,.2f}\n"
                f"  ISR retenido (10%): ${isr_retenido:,.2f}\n"
                f"  Neto a pagar: ${neto:,.2f}"
            )
            raw = {
                "monto": monto, "iva": iva,
                "isr_retenido": isr_retenido, "neto": neto,
            }
        else:
            return self._error(
                f"Tipo '{tipo}' no soportado. Usa 'honorarios' o 'arrendamiento'"
            )

        return self._success(output, raw_data=raw)

    def _generate_cfdi_data(
        self,
        emisor_rfc: str = "",
        receptor_rfc: str = "",
        concepto: str = "",
        subtotal: float = 0.0,
        forma_pago: str = "99",
    ) -> ToolResult:
        subtotal = float(subtotal)
        iva = round(subtotal * 0.16, 2)
        total = round(subtotal + iva, 2)
        fecha = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        cfdi = {
            "Version": "4.0",
            "Fecha": fecha,
            "FormaPago": forma_pago,
            "SubTotal": subtotal,
            "Descuento": 0,
            "Moneda": "MXN",
            "Total": total,
            "TipoDeComprobante": "I",
            "Exportacion": "01",
            "MetodoPago": "PUE",
            "LugarExpedicion": "06600",
            "Emisor": {
                "Rfc": emisor_rfc.upper(),
                "RegimenFiscal": "612",
            },
            "Receptor": {
                "Rfc": receptor_rfc.upper(),
                "UsoCFDI": "G03",
            },
            "Conceptos": [
                {
                    "ClaveProdServ": "84111506",
                    "Cantidad": 1,
                    "ClaveUnidad": "E48",
                    "Descripcion": concepto,
                    "ValorUnitario": subtotal,
                    "Importe": subtotal,
                }
            ],
            "Impuestos": {
                "TotalImpuestosTrasladados": iva,
            },
        }

        return self._success(
            "Datos CFDI generados. Lleva este JSON a tu PAC para timbrar.",
            raw_data=cfdi,
        )
