"""Roles concretos de la agencia."""

from agencia.agents.builder.role_agent import LegacyRoleAgent
from agencia.agents.builder.roles.strategy_role import StrategyRole
from agencia.agents.builder.roles.finance_role import FinanceRole
from agencia.agents.builder.roles.legal_role import LegalRole
from agencia.agents.builder.roles.marketing_role import MarketingRole
from agencia.agents.builder.roles.tech_role import TechRole
from agencia.agents.builder.roles.operations_role import OperationsRole

ALL_ROLES = [
    StrategyRole,
    FinanceRole,
    LegalRole,
    MarketingRole,
    TechRole,
    OperationsRole,
]

__all__ = [
    "StrategyRole",
    "FinanceRole",
    "LegalRole",
    "MarketingRole",
    "TechRole",
    "OperationsRole",
    "ALL_ROLES",
]
