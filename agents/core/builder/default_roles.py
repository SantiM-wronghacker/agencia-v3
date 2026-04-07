"""
Built-in default roles for the TeamDirector.

Each role has a simple handler that can be replaced with real LLM-backed
logic later.  For now they return structured dicts so the system is
functional end-to-end.
"""
from __future__ import annotations

from typing import Any

from .role_agent import RoleAgent


# ---- handler implementations ------------------------------------------------


def _strategy_handler(goal: str, context: dict[str, Any]) -> dict[str, Any]:
    return {
        "role": "strategy",
        "analysis": f"Strategic analysis for: {goal}",
        "recommendations": ["Define KPIs", "Identify target market", "Set timeline"],
    }


def _tech_handler(goal: str, context: dict[str, Any]) -> dict[str, Any]:
    return {
        "role": "tech",
        "analysis": f"Technical feasibility for: {goal}",
        "stack": ["Python", "FastAPI", "React"],
        "risks": ["Integration complexity"],
    }


def _marketing_handler(goal: str, context: dict[str, Any]) -> dict[str, Any]:
    return {
        "role": "marketing",
        "analysis": f"Marketing plan for: {goal}",
        "channels": ["social", "email", "content"],
    }


def _finance_handler(goal: str, context: dict[str, Any]) -> dict[str, Any]:
    return {
        "role": "finance",
        "analysis": f"Financial projection for: {goal}",
        "budget_estimate": "TBD",
    }


# ---- registry ---------------------------------------------------------------

BUILTIN_ROLES: dict[str, RoleAgent] = {
    "strategy": RoleAgent("strategy", "Strategic planning and analysis", _strategy_handler),
    "tech": RoleAgent("tech", "Technical feasibility and architecture", _tech_handler),
    "marketing": RoleAgent("marketing", "Marketing strategy and channels", _marketing_handler),
    "finance": RoleAgent("finance", "Financial planning and projections", _finance_handler),
}
