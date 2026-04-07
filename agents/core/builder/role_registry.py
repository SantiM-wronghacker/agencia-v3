"""
RoleRegistry — Registro centralizado de RoleAgents disponibles.

Permite al TeamDirector descubrir roles por dominio o capacidad
sin necesidad de conocer detalles internos.
"""

from __future__ import annotations

from typing import Type

from agencia.agents.builder.role_agent import RoleAgent


class RoleRegistry:
    """Registro singleton de roles disponibles para el Director."""

    def __init__(self) -> None:
        self._roles: dict[str, RoleAgent] = {}

    def registrar(self, role: RoleAgent) -> None:
        """Registra una instancia de RoleAgent."""
        self._roles[role.nombre] = role

    def registrar_clase(self, cls: Type[RoleAgent]) -> None:
        """Instancia y registra un RoleAgent a partir de su clase."""
        instance = cls()
        self.registrar(instance)

    def obtener(self, nombre: str) -> RoleAgent | None:
        return self._roles.get(nombre)

    def listar(self) -> list[RoleAgent]:
        return list(self._roles.values())

    def buscar_por_dominio(self, dominio: str) -> list[RoleAgent]:
        return [r for r in self._roles.values() if r.dominio == dominio]

    def buscar_por_capacidad(self, capacidad: str) -> list[RoleAgent]:
        """Devuelve roles que tienen la capacidad solicitada."""
        return [
            r for r in self._roles.values() if capacidad in r.capacidades
        ]

    def dominios_disponibles(self) -> list[str]:
        return sorted({r.dominio for r in self._roles.values()})

    def to_dict(self) -> dict:
        return {
            "roles": [r.info() for r in self._roles.values()],
            "dominios": self.dominios_disponibles(),
        }

    def __len__(self) -> int:
        return len(self._roles)

    def __contains__(self, nombre: str) -> bool:
        return nombre in self._roles
