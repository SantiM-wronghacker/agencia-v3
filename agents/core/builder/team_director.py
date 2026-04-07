"""
TeamDirector - orchestrates a set of registered RoleAgents.

Only roles that have been **explicitly registered** can be executed.
This prevents execution of arbitrary scripts or unregistered code.

Supports both modern and legacy interfaces:
- Modern: register(), run() - for handler-based RoleAgents
- Legacy: registry parameter, ejecutar_equipo(), ejecutar_desde_archivo() - for LegacyRoleAgents
"""
from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any, Optional

from .role_agent import RoleAgent

if TYPE_CHECKING:
    from .role_registry import RoleRegistry

logger = logging.getLogger(__name__)


class TeamDirector:
    """Coordinates a team of RoleAgent instances.

    Supports both modern (handler-based) and legacy (class-based) role agents.

    Parameters
    ----------
    name:
        Human-readable name for this team (default: "default-team").
    registry:
        Optional RoleRegistry for legacy interface support.
    """

    def __init__(
        self, name: str = "default-team", registry: Optional[RoleRegistry] = None
    ) -> None:
        self.name = name
        self._registry = registry
        self._roles: dict[str, RoleAgent] = {}

    # ---- registration (modern interface) ----------------------------------

    def register(self, agent: RoleAgent) -> None:
        """Register a role agent. Raises ValueError on duplicate."""
        if agent.role in self._roles:
            raise ValueError(f"Role '{agent.role}' is already registered")
        self._roles[agent.role] = agent
        logger.info("TeamDirector[%s]: registered role '%s'", self.name, agent.role)

    @property
    def registered_roles(self) -> list[str]:
        """List all registered role slugs."""
        return list(self._roles.keys())

    # ---- execution (modern interface) -----------------------------------

    def run(
        self,
        goal: str,
        roles: list[str] | None = None,
    ) -> dict[str, Any]:
        """Execute goal using specified (or all) registered roles.

        Parameters
        ----------
        goal:
            The objective to accomplish.
        roles:
            Subset of role slugs to use. If None, all registered roles participate.

        Returns
        -------
        dict
            {"goal": str, "results": {role_slug: result_dict, ...}}

        Raises
        ------
        ValueError
            If any requested role is not registered.
        """
        target_roles = roles if roles is not None else list(self._roles.keys())

        # Security gate: reject unknown roles
        unknown = set(target_roles) - set(self._roles.keys())
        if unknown:
            raise ValueError(
                f"Unregistered roles requested: {unknown}. "
                f"Available: {self.registered_roles}"
            )

        results: dict[str, Any] = {}
        for role_slug in target_roles:
            agent = self._roles[role_slug]
            logger.info("TeamDirector[%s]: dispatching to role '%s'", self.name, role_slug)
            results[role_slug] = agent.execute(goal, context={"team": self.name})

        return {"goal": goal, "results": results}

    # ---- legacy interface (class-based RoleAgents) -----------------------

    def assign(self, role: str, task: str) -> dict[str, Any]:
        """Assign a task to a specific role (legacy interface)."""
        if self._registry is None:
            raise ValueError("No registry configured for legacy role assignment")
        role_agent = self._registry.obtener(role)
        if role_agent is None:
            raise ValueError(f"Role '{role}' not found in registry")
        logger.info("TeamDirector: assigning task '%s' to role '%s'", task, role)
        return {
            "role": role,
            "task": task,
            "status": "assigned",
        }

    def seleccionar_roles(self, requerimientos: set[str]) -> list[Any]:
        """Select RoleAgents whose capabilities cover requirements (legacy)."""
        if self._registry is None:
            return []
        seleccionados: list[Any] = []
        cubiertos: set[str] = set()

        for req in sorted(requerimientos):
            if req in cubiertos:
                continue
            candidatos = self._registry.buscar_por_capacidad(req)
            if candidatos:
                role = candidatos[0]
                if role not in seleccionados:
                    seleccionados.append(role)
                cubiertos |= role.capacidades
        return seleccionados

    def armar_equipo(self, brief: dict[str, Any]) -> dict[str, Any]:
        """Assemble a team of roles for the brief (legacy interface)."""
        if self._registry is None:
            return {"equipo": [], "gaps_cubiertos": {}, "requerimientos": []}

        requerimientos = set(brief.get("requerimientos", []))
        equipo = self.seleccionar_roles(requerimientos)
        gaps_cubiertos_total: dict[str, list[str]] = {}

        for role in equipo:
            gaps = role.cubrir_gaps(requerimientos)
            if gaps:
                gaps_cubiertos_total[role.nombre] = sorted(gaps)

        # Find additional roles if needed
        faltantes = requerimientos - {cap for role in equipo for cap in role.capacidades}
        for role in self._registry.listar():
            if role in equipo:
                continue
            overlap = faltantes & role.capacidades
            if overlap:
                equipo.append(role)
                gaps = role.cubrir_gaps(requerimientos)
                if gaps:
                    gaps_cubiertos_total[role.nombre] = sorted(gaps)
                faltantes -= role.capacidades

        return {
            "cliente": brief.get("cliente", "desconocido"),
            "requerimientos": sorted(requerimientos),
            "equipo": [r.info() for r in equipo],
            "gaps_cubiertos": gaps_cubiertos_total,
        }

    def ejecutar_equipo(self, brief: dict[str, Any]) -> dict[str, Any]:
        """Execute complete flow: assemble team, execute roles, synthesize results (legacy)."""
        if self._registry is None:
            return {
                "cliente": brief.get("cliente", "desconocido"),
                "orden": brief.get("orden", ""),
                "equipo": [],
                "gaps_cubiertos": {},
                "resultados": [],
                "status": "error",
            }

        plan = self.armar_equipo(brief)
        orden = brief.get("orden", brief.get("objetivo", ""))
        contexto = brief.get("contexto", {})

        resultados: list[dict[str, Any]] = []
        for role_info in plan["equipo"]:
            role = self._registry.obtener(role_info["nombre"])
            if role is None:
                continue
            resultado = role.ejecutar(orden, contexto)
            resultados.append(resultado)

        return {
            "cliente": plan["cliente"],
            "orden": orden,
            "equipo": plan["equipo"],
            "gaps_cubiertos": plan["gaps_cubiertos"],
            "resultados": resultados,
            "status": "completado",
        }

    @staticmethod
    def cargar_brief(path: str) -> dict[str, Any]:
        """Load a client brief from JSON file (legacy interface)."""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def ejecutar_desde_archivo(self, path: str) -> dict[str, Any]:
        """Load brief JSON and execute team (legacy interface)."""
        brief = self.cargar_brief(path)
        return self.ejecutar_equipo(brief)

    def __repr__(self) -> str:
        return f"TeamDirector(name={self.name!r}, roles={self.registered_roles})"
