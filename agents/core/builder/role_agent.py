"""
RoleAgent - a specialised agent bound to a named role.

Each RoleAgent only has access to its own pre-registered tools/sub-agents.
It **cannot** execute arbitrary scripts or call tools outside its scope.

Modern interface supports both:
- RoleAgent(role, description, handler): Modern handler-based approach
- LegacyRoleAgent subclasses: Class-based with atributos (nombre, dominio, capacidades)
"""
from __future__ import annotations

import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)


class RoleAgent:
    """An agent that is scoped to a single *role* (e.g. ``strategy``, ``tech``).

    Parameters
    ----------
    role:
        Short slug that identifies this role (e.g. ``"strategy"``).
    description:
        Human-readable description of the role's purpose.
    handler:
        Callable that performs the role's work.
        Signature: ``(goal: str, context: dict) -> dict``
    """

    def __init__(
        self,
        role: str,
        description: str,
        handler: Callable[..., dict[str, Any]],
    ) -> None:
        self.role = role
        self.description = description
        self._handler = handler

    def execute(self, goal: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Run the role handler with the given *goal* and optional *context*."""
        ctx = context or {}
        logger.info("RoleAgent[%s] executing goal: %s", self.role, goal)
        return self._handler(goal, ctx)

    def __repr__(self) -> str:
        return f"RoleAgent(role={self.role!r})"


class LegacyRoleAgent:
    """Base class for legacy role-based agents with class attributes.

    Supports:
    - Class-level atributos: nombre, dominio, capacidades
    - ejecutar() method (legacy name)
    - Gap detection and generation via SubAgentFactory
    - Internally compatible with modern handler-based approach

    Subclasses should override ejecutar() to define role-specific behavior.
    """

    nombre: str = "BaseRole"
    dominio: str = "general"
    capacidades: set[str] = set()

    def __init__(self) -> None:
        """Initialize legacy role agent."""
        from agencia.agents.builder.sub_agent_factory import SubAgentFactory

        self._resultados: list[dict[str, Any]] = []
        self.factory = SubAgentFactory(owner_role=self.nombre)

    def detectar_gaps(self, requerimientos: set[str]) -> set[str]:
        """Detect capability gaps versus requirements."""
        caps_actuales = self.capacidades | {s.nombre for s in self.factory.listar()}
        return requerimientos - caps_actuales

    def generar_subagente(self, gap: str) -> None:
        """Generate a sub-agent to cover a gap."""
        def _placeholder(**kwargs: Any) -> dict:
            return {"status": "generated", "gap": gap, "input": kwargs}

        self.factory.crear(
            nombre=gap,
            descripcion=f"Sub-agent generated for: {gap}",
            fn=_placeholder,
        )

    def cubrir_gaps(self, requerimientos: set[str]) -> set[str]:
        """Detect and cover all gaps by generating sub-agents."""
        gaps = self.detectar_gaps(requerimientos)
        for gap in gaps:
            self.generar_subagente(gap)
        return gaps

    def info(self) -> dict[str, Any]:
        """Return public metadata of the role (visible to TeamDirector)."""
        return {
            "nombre": self.nombre,
            "dominio": self.dominio,
            "capacidades": sorted(self.capacidades),
        }

    def execute(self, goal: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Modern interface: execute goal using ejecutar()."""
        return self.ejecutar(goal, context)

    def ejecutar(self, orden: str, contexto: dict[str, Any] | None = None) -> dict[str, Any]:
        """Legacy interface: execute an order within the role's domain.

        Subclasses should override this method with their specific logic.
        """
        resultado = {
            "role": self.nombre,
            "dominio": self.dominio,
            "orden": orden,
            "status": "completado",
            "capacidades_usadas": list(self.capacidades),
        }
        self._resultados.append(resultado)
        return resultado

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(nombre={self.nombre!r}, dominio={self.dominio!r})"
