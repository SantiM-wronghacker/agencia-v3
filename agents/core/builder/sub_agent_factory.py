"""
SubAgentFactory — Fábrica interna de subagentes (neuronas/tools).

Cada RoleAgent posee su propia instancia de SubAgentFactory.
El TeamDirector NO tiene acceso a esta fábrica; es 100% interna del rol.

Un subagente generado es una función callable con metadata:
  {"nombre": str, "descripcion": str, "fn": Callable}
"""

from __future__ import annotations

import uuid
from typing import Any, Callable


class SubAgent:
    """Neurona / herramienta interna generada por un RoleAgent."""

    def __init__(self, nombre: str, descripcion: str, fn: Callable[..., Any]):
        self.id = uuid.uuid4().hex[:8]
        self.nombre = nombre
        self.descripcion = descripcion
        self._fn = fn

    def ejecutar(self, *args: Any, **kwargs: Any) -> Any:
        return self._fn(*args, **kwargs)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
        }

    def __repr__(self) -> str:
        return f"SubAgent({self.nombre!r})"


class SubAgentFactory:
    """
    Fábrica interna de un RoleAgent.

    Permite crear subagentes (neuronas / tools) dinámicamente para cubrir
    gaps de capacidad detectados por el rol.
    """

    def __init__(self, owner_role: str):
        self.owner_role = owner_role
        self._subagents: dict[str, SubAgent] = {}

    def crear(
        self,
        nombre: str,
        descripcion: str,
        fn: Callable[..., Any],
    ) -> SubAgent:
        """Crea y registra un nuevo subagente interno."""
        sub = SubAgent(nombre=nombre, descripcion=descripcion, fn=fn)
        self._subagents[sub.id] = sub
        return sub

    def obtener(self, sub_id: str) -> SubAgent | None:
        return self._subagents.get(sub_id)

    def listar(self) -> list[SubAgent]:
        return list(self._subagents.values())

    def eliminar(self, sub_id: str) -> bool:
        return self._subagents.pop(sub_id, None) is not None

    def buscar_por_nombre(self, nombre: str) -> SubAgent | None:
        for sub in self._subagents.values():
            if sub.nombre == nombre:
                return sub
        return None

    def to_dict(self) -> dict:
        return {
            "owner_role": self.owner_role,
            "subagents": [s.to_dict() for s in self._subagents.values()],
        }

    def __len__(self) -> int:
        return len(self._subagents)
