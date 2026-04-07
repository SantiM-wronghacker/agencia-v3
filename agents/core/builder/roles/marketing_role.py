"""Rol de Marketing — campañas, branding, contenido."""

from __future__ import annotations

from typing import Any

from agencia.agents.builder.role_agent import LegacyRoleAgent


class MarketingRole(LegacyRoleAgent):
    nombre = "Marketing"
    dominio = "marketing"
    capacidades = {
        "campanas",
        "branding",
        "contenido",
        "redes_sociales",
        "seo",
    }

    def ejecutar(self, orden: str, contexto: dict[str, Any] | None = None) -> dict[str, Any]:
        resultado = {
            "role": self.nombre,
            "dominio": self.dominio,
            "orden": orden,
            "status": "completado",
            "entregables": ["plan_campana", "calendario_contenido", "estrategia_seo"],
        }
        self._resultados.append(resultado)
        return resultado
