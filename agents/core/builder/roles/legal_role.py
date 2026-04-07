"""Rol Legal — contratos, compliance, documentos legales."""

from __future__ import annotations

from typing import Any

from agencia.agents.builder.role_agent import LegacyRoleAgent


class LegalRole(LegacyRoleAgent):
    nombre = "Legal"
    dominio = "legal"
    capacidades = {
        "contratos",
        "compliance",
        "documentos_legales",
        "regulacion",
        "revision_legal",
    }

    def ejecutar(self, orden: str, contexto: dict[str, Any] | None = None) -> dict[str, Any]:
        resultado = {
            "role": self.nombre,
            "dominio": self.dominio,
            "orden": orden,
            "status": "completado",
            "entregables": ["contrato_borrador", "checklist_compliance"],
        }
        self._resultados.append(resultado)
        return resultado
