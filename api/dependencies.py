from fastapi import Depends

from core.group import AgentGroup
from core.orchestrator import Orchestrator
from memory.db import AgenciaDB

# ---------------------------------------------------------------------------
# DB singleton
# ---------------------------------------------------------------------------

_db: AgenciaDB | None = None


def get_db() -> AgenciaDB:
    global _db
    if _db is None:
        _db = AgenciaDB()
    return _db


# ---------------------------------------------------------------------------
# Orchestrator singleton
# ---------------------------------------------------------------------------

_orchestrator: Orchestrator | None = None


def _register_default_groups(orchestrator: Orchestrator) -> None:
    for name in ("content_pipeline", "business_analysis", "legal_review", "ops_automation"):
        orchestrator.register(
            AgentGroup(name, [], mode="pipeline", db=orchestrator.db)
        )


def get_orchestrator(db: AgenciaDB = Depends(get_db)) -> Orchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = Orchestrator(db=db)
        _register_default_groups(_orchestrator)
    return _orchestrator
