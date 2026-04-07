from fastapi import Depends

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
    from groups import (
        create_content_pipeline,
        create_business_analysis,
        create_legal_review,
        create_ops_automation,
    )
    db = orchestrator.db
    orchestrator.register(create_content_pipeline(db))
    orchestrator.register(create_business_analysis(db))
    orchestrator.register(create_legal_review(db))
    orchestrator.register(create_ops_automation(db))


def get_orchestrator(db: AgenciaDB = Depends(get_db)) -> Orchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = Orchestrator(db=db)
        _register_default_groups(_orchestrator)
    return _orchestrator
