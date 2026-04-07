"""Rol de Estrategia — planificación y dirección de proyectos."""

from __future__ import annotations

from typing import Any

from agencia.agents.builder.role_agent import LegacyRoleAgent


class StrategyRole(LegacyRoleAgent):
    nombre = "Estrategia"
    dominio = "estrategia"
    capacidades = {
        "planificacion",
        "analisis_mercado",
        "definicion_objetivos",
        "roadmap",
        "kpi",
    }

    def ejecutar(self, orden: str, contexto: dict[str, Any] | None = None) -> dict[str, Any]:
        resultado = {
            "role": self.nombre,
            "dominio": self.dominio,
            "orden": orden,
            "status": "completado",
            "entregables": ["plan_estrategico", "roadmap", "kpis"],
        }
        self._resultados.append(resultado)
        return resultado
