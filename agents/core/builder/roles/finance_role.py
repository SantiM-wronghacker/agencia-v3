"""Rol de Finanzas — análisis financiero, ROI, presupuestos."""

from __future__ import annotations

from typing import Any

from agencia.agents.builder.role_agent import LegacyRoleAgent


class FinanceRole(LegacyRoleAgent):
    nombre = "Finanzas"
    dominio = "finanzas"
    capacidades = {
        "analisis_financiero",
        "presupuesto",
        "roi",
        "proyecciones",
        "costos",
    }

    def ejecutar(self, orden: str, contexto: dict[str, Any] | None = None) -> dict[str, Any]:
        resultado = {
            "role": self.nombre,
            "dominio": self.dominio,
            "orden": orden,
            "status": "completado",
            "entregables": ["analisis_roi", "presupuesto", "proyecciones"],
        }
        self._resultados.append(resultado)
        return resultado
