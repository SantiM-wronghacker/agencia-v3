"""
Multi-project router for the FastAPI backend.
Refactored to use core.py and config.py. Stubs fully implemented.
"""
import json
import logging
from pathlib import Path

from config import MODEL_FAST, MODEL_STRONG, PROJECTS_DIR
from core import (
    llm,
    load_state as _load_state,
    save_state as _save_state,
    add_recent,
    format_recent,
    build_context_prefix,
    update_summary,
    save_md,
    SYSTEM_ROUTER, SYSTEM_CHAT, SYSTEM_PLANNER, SYSTEM_EXEC,
)
from rag_pro import search_kb

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

logger = logging.getLogger(__name__)

PROJECTS_DIR.mkdir(exist_ok=True)

DEFAULT_AGENTS = [
    {"id": "chat", "name": "Chat", "enabled": True},
    {"id": "rag", "name": "RAG PRO", "enabled": True},
    {"id": "save", "name": "Save (notes)", "enabled": True},
    {"id": "task", "name": "Task (Planner+Executor)", "enabled": True},
    {"id": "router", "name": "Router", "enabled": True},
]


def ensure_project(company: str, project: str) -> Path:
    """Create project directory structure and initialize state + config if needed."""
    p = PROJECTS_DIR / company / project
    (p / "kb").mkdir(parents=True, exist_ok=True)
    (p / "runs").mkdir(parents=True, exist_ok=True)
    (p / "memory_db").mkdir(parents=True, exist_ok=True)

    state = p / "runs" / "state.json"
    if not state.exists():
        _save_state({"summary": "", "recent": []}, state_file=state)

    cfg = p / "config.json"
    if not cfg.exists():
        cfg.write_text(
            json.dumps({"agents": DEFAULT_AGENTS}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    return p


def load_state(project_path: Path) -> dict:
    return _load_state(state_file=project_path / "runs" / "state.json")


def save_state(project_path: Path, state: dict):
    _save_state(state, state_file=project_path / "runs" / "state.json")


def route_intent(state, user_text) -> str:
    prompt = f"{build_context_prefix(state)}\nRECENTE:\n{format_recent(state, 6)}\n\nMENSAJE:\n{user_text}"
    out = llm(SYSTEM_ROUTER, prompt, model=MODEL_FAST).upper().split()[0]
    return out if out in ("CHAT", "SAVE", "TASK", "RAG") else "CHAT"


def handle_chat(state, user_text: str) -> str:
    prompt = f"{build_context_prefix(state)}\nRECENTE:\n{format_recent(state, 10)}\n\nMENSAJE:\n{user_text}"
    return llm(SYSTEM_CHAT, prompt, model=MODEL_FAST)


def handle_save(project_path: Path, user_text: str) -> str:
    runs_dir = project_path / "runs"
    md_content = f"# Nota\n\n{user_text}\n"
    path = save_md("nota", md_content, runs_dir=runs_dir)
    return f"Guardado en: {path}"


def handle_task(project_path: Path, state, user_text: str) -> str:
    """Full Planner -> Executor pipeline per project."""
    prefix = build_context_prefix(state)
    recent = format_recent(state, n_msgs=8)

    planner_prompt = f"""{prefix}
CONVERSACIÓN RECIENTE:
{recent}

TAREA:
{user_text}
"""
    plan = llm(SYSTEM_PLANNER, planner_prompt, model=MODEL_STRONG)
    deliverable = llm(SYSTEM_EXEC, f"Petición:\n{user_text}\n\nPlan:\n{plan}", model=MODEL_STRONG)

    report = (
        f"# Tarea\n{user_text}\n\n"
        f"# Memoria (resumen)\n{state.get('summary', '')}\n\n"
        f"# Plan\n{plan}\n\n"
        f"# Entregable\n{deliverable}\n"
    )
    runs_dir = project_path / "runs"
    path = save_md("tarea_proyecto", report, runs_dir=runs_dir)
    return f"TASK completado y guardado en: {path}"


def handle_rag(project_path: Path, state, user_text: str) -> str:
    """RAG search using the project's own ChromaDB."""
    db_dir = project_path / "memory_db"
    context = search_kb(user_text, k=3, db_dir=db_dir)
    prefix = build_context_prefix(state)
    recent = format_recent(state, n_msgs=8)

    prompt = f"""{prefix}
CONVERSACIÓN RECIENTE:
{recent}

INSTRUCCIÓN:
Responde usando SOLO el contexto (KB). Si no está en el contexto, dilo.

CONTEXTO (KB):
{context}

PREGUNTA:
{user_text}
"""
    return llm(SYSTEM_CHAT, prompt, model=MODEL_FAST)
