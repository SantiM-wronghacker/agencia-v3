import json
import requests
from datetime import datetime
from pathlib import Path
import sys
import time

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

MODEL_MAIN = "llama-3.3-70b-versatile"  
MODEL_SUMMARY = "llama-3.3-70b-versatile"  
RUNS_DIR = Path("runs")
KB_DIR = Path("kb")
RUNS_DIR.mkdir(exist_ok=True)
KB_DIR.mkdir(exist_ok=True)

STATE_FILE = RUNS_DIR / "state.json"
MAX_RECENT_TURNS = 10  

SYSTEM_ROUTER = """Eres un Router (director) de un sistema de agentes.
Clasifica la intención en UNA ruta:

- CHAT: conversación o pregunta simple
- SAVE: guardar nota/idea
- TASK: plan + entregable
- RAG: responder usando kb/ (memoria documental)

Devuelve SOLO una palabra: CHAT, SAVE, TASK o RAG.
Reglas:
- Si menciona "guardar", "anotar", "nota", "guardar:" => SAVE
- Si pide plan, estrategia, checklist, pasos, propuesta, documento => TASK
- Si pregunta precios/políticas/procesos internos => RAG
- Si no estás seguro => CHAT
"""

SYSTEM_CHAT = "Eres un asistente útil, directo y práctico."
SYSTEM_PLANNER = """Eres un Planner. Convierte la petición en un plan accionable.
Devuelve:
1) Objetivo (1 línea)
2) Plan (5-10 pasos numerados)
3) Entregables
4) Riesgos y supuestos (breve)
"""
SYSTEM_EXEC = """Eres un Executor. Toma la petición y el plan y genera un primer entregable real.
Entrega en Markdown con checklist. Marca supuestos si faltan datos.
"""

SUMMARY_SYSTEM = """Eres un compresor de memoria.
Actualiza un resumen vivo de la conversación.
Reglas:
- Mantén el resumen en 10-20 líneas máximo.
- Conserva: objetivos, decisiones, preferencias, datos (precios, nombres), pendientes.
- Elimina: repetición, relleno, saludos.
Devuelve SOLO el resumen actualizado (sin títulos).
"""

def llm(system: str, user: str, model: str = MODEL_MAIN) -> str:
    try:
        response = requests.post(
            "https://api.groq.com/v1-alpha/completions",
            json={
                "model": model,
                "prompt": f"{system}\n{user}",
                "max_tokens": 2048,
                "temperature": 0.7,
            },
        )
        response.raise_for_status()
        return response.json()["completion"].strip()
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return ""

def llm_messages(messages, model: str = MODEL_MAIN) -> str:
    try:
        response = requests.post(
            "https://api.groq.com/v1-alpha/completions",
            json={
                "model": model,
                "prompt": messages,
                "max_tokens": 2048,
                "temperature": 0.7,
            },
        )
        response.raise_for_status()
        return response.json()["completion"].strip()
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return ""

def save_md(title: str, content: str) -> str:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "_")
    path = RUNS_DIR / f"{ts}_{safe or 'run'}.md"
    path.write_text(content, encoding="utf-8")
    return str(path)

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"summary": "", "recent": []}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def add_recent(state, role, content):
    state["recent"].append({"role": role, "content": content})
    state["recent"] = state["recent"][-(MAX_RECENT_TURNS * 2):]
    return state

def format_recent(state, n_msgs=8):
    msgs = state["recent"][-n_msgs:]
    return "\n".join([f"{m['role']}: {m['content']}" for m in msgs])

def update_summary(state):
    recent_text = format_recent(state, n_msgs=8)
    prompt = f"""Resumen anterior:
{state.get("summary","")}

Nuevos mensajes recientes:
{recent_text}
"""
    state["summary"] = llm(SUMMARY_SYSTEM, prompt, model=MODEL_SUMMARY)
    return state

def reset_state():
    s = {"summary": "", "recent": []}
    save_state(s)
    return s

def build_context_prefix(state) -> str:
    summary = state.get("summary", "").strip()
    if not summary:
        return ""
    return f"MEMORIA (resumen de la conversación):\n{summary}\n"

def route_intent(state, user_text) -> str:
    prefix = build_context_prefix(state)
    recent = format_recent(state, n_msgs=6)

    prompt = f"""{prefix}
CONVERSACIÓN RECIENTE:
{recent}

MENSAJE ACTUAL:
{user_text}
"""
    out = llm(SYSTEM_ROUTER, prompt).upper().split()[0]
    return out if out in ("CHAT", "SAVE", "TASK", "RAG") else "CHAT"

def handle_save(user_text) -> str:
    if user_text.lower().startswith("guardar:") and "|" in user_text:
        payload = user_text[len("guardar:"):].strip()
        title, text = [x.strip() for x in payload.split("|", 1)]
    else:
        title, text = "nota", user_text

    md = f"# {title}\n\n{text}\n"
    path = save_md(title, md)
    return f" Guardado en: {path}"

def handle_task(state, user_text) -> str:
    prefix = build_context_prefix(state)
    recent = format_recent(state, n_msgs=8)

    planner_prompt = f"""{prefix}
CONVERSACIÓN RECIENTE:
{recent}

TAREA:
{user_text}
"""
    plan = llm(SYSTEM_PLANNER, planner_prompt)

    deliverable = llm(
        SYSTEM_EXEC,
        f"Petición:\n{user_text}\n\nPlan:\n{plan}"
    )

    report = f"# Tarea\n{user_text}\n\n# Memoria (resumen)\n{state.get('summary','')}\n\n# Plan (Planner)\n{plan}\n\n# Entregable (Executor)\n{deliverable}\n"
    path = save_md("tarea_state_memoria", report)
    return f" Tarea resuelta y guardada en: {path}"

def handle_rag(state, user_text) -> str:
    context = "No hay contexto disponible"
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
    return llm(SYSTEM_CHAT, prompt)

def handle_chat(state, user_text) -> str:
    prefix = build_context_prefix(state)
    recent = format_recent(state, n_msgs=10)

    prompt = f"""{prefix}
CONVERSACIÓN RECIENTE:
{recent}

MENSAJE:
{user_text}
"""
    return llm(SYSTEM_CHAT, prompt)

def main():
    state = load_state()
    print("Router FINAL: Memoria híbrida (state.json) + RAG PRO.")
    print("Comandos:")
    print("- salir")
    print("- reset  (borra memoria de conversación)")
    print("- Para guardar: guardar: Titulo | Texto")
    print("- RAG documental: kb/  (reindexa con rag_index.py)\n")

    if len(sys.argv) > 1:
        user_text = sys.argv[1]
    else:
        user_text = "Hola, ¿cómo puedo ayudarte?"

    while True:
        if user_text.lower() in ("salir", "exit", "quit"):
            break

        if user_text.lower() == "reset":
            state = reset_state()
            print(" Memoria borrada.\n")
            continue

        state = add_recent(state, "user", user_text)

        route = route_intent(state, user_text)
        print(f"\nRouter → {route}")

        if route == "SAVE":
            out = handle_save(user_text)
        elif route == "TASK":
            out = handle_task(state, user_text)
        elif route == "RAG":
            out = handle_rag(state, user_text)
        else:
            out = handle_chat(state, user_text)

        state = add_recent(state, "assistant", out)

        state = update_summary(state)
        save_state(state)

        print("\nAgente:", out, "\n")
        time.sleep(2)

if __name__ == "__main__":
    main()