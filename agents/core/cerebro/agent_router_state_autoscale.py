"""
Router CLI with hybrid memory + RAG PRO + auto-escalation (FAST -> STRONG).
Refactored to use core.py and config.py.
"""
import logging

from agencia.agents.herramientas.config import MODEL_FAST, MODEL_STRONG
from agencia.agents.herramientas.core import (
    llm, save_md, load_state, save_state, add_recent, format_recent,
    build_context_prefix, update_summary,
    SYSTEM_ROUTER, SYSTEM_CHAT, SYSTEM_PLANNER, SYSTEM_EXEC,
)
from agencia.agents.cerebro.rag_pro import search_kb
from agencia.agents.herramientas.logging_config import setup_logging

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

logger = logging.getLogger(__name__)


# =========================
# Auto-escalation
# =========================
def needs_escalation(answer: str, route: str = "CHAT") -> bool:
    """Heuristic to decide whether to retry with MODEL_STRONG.
    Length check only applies to TASK/RAG, not CHAT."""
    a = (answer or "").strip().lower()
    if not a:
        return True

    red_flags = [
        "no sé", "no estoy seguro", "no tengo información", "no puedo",
        "no cuento con", "no encontré", "no aparece", "no está en el contexto"
    ]
    if any(x in a for x in red_flags):
        return True

    if route in ("TASK", "RAG") and len(a) < 60:
        return True

    return False


def answer_with_autoscale(system: str, prompt: str, route: str = "CHAT",
                          allow_strong_retry: bool = True) -> str:
    ans_fast = llm(system, prompt, model=MODEL_FAST)
    if allow_strong_retry and needs_escalation(ans_fast, route=route):
        logger.info("Escalating from %s to %s (route=%s)", MODEL_FAST, MODEL_STRONG, route)
        ans_strong = llm(system, prompt, model=MODEL_STRONG)
        return ans_strong.strip() or ans_fast
    return ans_fast


# =========================
# State helpers
# =========================
def reset_state():
    s = {"summary": "", "recent": []}
    save_state(s)
    return s


# =========================
# Router + Handlers
# =========================
def route_intent(state, user_text) -> str:
    prefix = build_context_prefix(state)
    recent = format_recent(state, n_msgs=6)
    prompt = f"""{prefix}
CONVERSACIÓN RECIENTE:
{recent}

MENSAJE ACTUAL:
{user_text}
"""
    out = llm(SYSTEM_ROUTER, prompt, model=MODEL_FAST).upper().split()[0]
    return out if out in ("CHAT", "SAVE", "TASK", "RAG") else "CHAT"


def handle_save(user_text) -> str:
    if user_text.lower().startswith("guardar:") and "|" in user_text:
        payload = user_text[len("guardar:"):].strip()
        title, text = [x.strip() for x in payload.split("|", 1)]
    else:
        title, text = "nota", user_text

    md = f"# {title}\n\n{text}\n"
    path = save_md(title, md)
    return f"Guardado en: {path}"


def handle_task(state, user_text) -> str:
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
    path = save_md("tarea_autoscale", report)
    return f"TASK ({MODEL_STRONG}) listo y guardado en: {path}"


def handle_rag(state, user_text) -> str:
    context = search_kb(user_text, k=3)
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
    return answer_with_autoscale(SYSTEM_CHAT, prompt, route="RAG", allow_strong_retry=True)


def handle_chat(state, user_text) -> str:
    prefix = build_context_prefix(state)
    recent = format_recent(state, n_msgs=10)
    prompt = f"""{prefix}
CONVERSACIÓN RECIENTE:
{recent}

MENSAJE:
{user_text}
"""
    return answer_with_autoscale(SYSTEM_CHAT, prompt, route="CHAT", allow_strong_retry=True)


def main():
    setup_logging()
    state = load_state()
    print("Router: Memoria híbrida + RAG PRO + routing + auto-escalado (FAST->STRONG si hace falta).")
    print(f"FAST:   {MODEL_FAST}")
    print(f"STRONG: {MODEL_STRONG}")
    print("Comandos: salir | reset\n")

    while True:
        user = input("Tú: ").strip()
        if user.lower() in ("salir", "exit", "quit"):
            break

        if user.lower() == "reset":
            state = reset_state()
            print("Memoria borrada.\n")
            continue

        state = add_recent(state, "user", user)

        route = route_intent(state, user)
        print(f"\nRouter -> {route}")

        if route == "SAVE":
            out = handle_save(user)
        elif route == "TASK":
            out = handle_task(state, user)
        elif route == "RAG":
            out = handle_rag(state, user)
        else:
            out = handle_chat(state, user)

        state = add_recent(state, "assistant", out)
        state = update_summary(state)
        save_state(state)

        print("\nAgente:", out, "\n")


if __name__ == "__main__":
    main()
