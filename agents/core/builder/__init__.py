"""
Agencia Builder — Sistema de roles inteligentes.

El TeamDirector SOLO selecciona y coordina RoleAgents (roles superiores).
Cada RoleAgent encapsula sus propios subagentes/neuronas internamente
y puede generar nuevos mediante SubAgentFactory cuando detecta gaps.
"""

from agencia.agents.builder.role_agent import RoleAgent, LegacyRoleAgent
from agencia.agents.builder.sub_agent_factory import SubAgentFactory
from agencia.agents.builder.team_director import TeamDirector
from agencia.agents.builder.role_registry import RoleRegistry

__all__ = ["RoleAgent", "LegacyRoleAgent", "SubAgentFactory", "TeamDirector", "RoleRegistry"]
