"""
ÁREA: CEREBRO
DESCRIPCIÓN: Agente de router con memoria que clasifica intenciones y responde según el contexto.
TECNOLOGÍA: Python, LLaMA, json, pathlib
"""

import json
from datetime import datetime
from pathlib import Path
import ollama
import sys
import time

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

# === Config ===
MODEL = "llama-3.3-70b-versatile"
RUNS_DIR = Path("runs")
KB_DIR = Path("kb")
RUNS_DIR.mkdir(exist_ok=True)
KB_DIR.mkdir(exist_ok=True)

SESSION_FILE = RUNS_DIR / "session.json"
MAX_TURNS = 12  # cuántos turnos recientes guardamos (para no inflar el contexto)

SYSTEM_ROUTER = """Eres un Router (director) de un sistema de agentes.
Clasifica la intención en UNA ruta:

- CHAT: conversación o pregunta simple
- SAVE: guardar nota/idea
- TASK: plan + entregable
- RAG: responder usando kb/

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

# ---------- Session helpers ----------
def load_session():
    if SESSION_FILE.exists():
        try:
            return json.loads(SESSION_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

def save_session(history):
    SESSION_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")

def add_turn(history, role, content):
    history.append({"role": role, "content": content})
    # Recortamos a los últimos MAX_TURNS*2 mensajes (user+assistant)
    history = history[-(MAX_TURNS * 2):]
    return history

# ---------- LLM helpers ----------
def llm(messages, model=MODEL) -> str:
    r = ollama.chat(model=model, messages=messages)
    return r["message"]["content"].strip()

def save_md(title: str, content: str) -> str:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "_")
    path = RUNS_DIR / f"{ts}_{safe or 'run'}.md"
    path.write_text(content, encoding="utf-8")
    return str(path)

def rag_search(query: str, top_k: int = 2) -> str:
    files = list(KB_DIR.glob("*"))
    if not files:
        return "KB vacía: no hay archivos en kb/. Agrega docs (precios, procesos, etc.)."

    scored = []
    q = query.lower()
    for f in files:
        try:
            txt = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        score = sum(1 for w in q.split() if w in txt.lower())
        scored.append((score, f.name, txt))

    scored.sort(reverse=True, key=lambda x: x[0])
    top = scored[:top_k]
    context = []
    for score, name, txt in top:
        snippet = txt[:1500]
        context.append(f"[Fuente: {name} | score={score}]\n{snippet}")
    return "\n\n---\n\n".join(context)

# ---------- Handlers ----------
def route_intent(history, user_text) -> str:
    # Router ve el último contexto de la conversación (últimos mensajes)
    recent = history[-6:]  # pequeño contexto para clasificar
    router_msgs = [{"role": "system", "content": SYSTEM_ROUTER}]
    router_msgs.extend(recent)
    router_msgs.append({"role": "user", "content": user_text})
    out = llm(router_msgs).upper().split()[0]
    return out if out in ("CHAT", "SAVE", "TASK", "RAG") else "CHAT"

def handle_save(history, user_text) -> str:
    if user_text.lower().startswith("guardar:") and "|" in user_text:
        payload = user_text[len("guardar:"):].strip()
        title, text = [x.strip() for x in payload.split("|", 1)]
    else:
        title, text = "nota", user_text

    md = f"# {title}\n\n{text}\n"
    path = save_md(title, md)
    return f" Guardado en: {path}"

def handle_task(history, user_text) -> str:
    recent = history[-8:]
    plan = llm([{"role": "system", "content": SYSTEM_PLANNER}, *recent, {"role": "user", "content": user_text}])
    deliverable = llm([{"role": "system", "content": SYSTEM_EXEC}, {"role": "user", "content": f"Petición:\n{user_text}\n\nPlan:\n{plan}"}])

    report = f"# Tarea\n{user_text}\n\n# Plan (Planner)\n{plan}\n\n# Entregable (Executor)\n{deliverable}\n"
    path = save_md("tarea_router_memoria", report)
    return f" Tarea resuelta y guardada en: {path}"

def handle_rag(history, user_text) -> str:
    context = rag_search(user_text, top_k=2)
    recent = history[-8:]
    msgs = [{"role": "system", "content": SYSTEM_CHAT}]
    msgs.extend(recent)
    msgs.append({"role": "user", "content": f"Responde usando SOLO el contexto. Si no está, dilo.\n\nCONTEXTO:\n{context}\n\nPREGUNTA:\n{user_text}"})
    return llm(msgs)

def handle_chat(history, user_text) -> str:
    recent = history[-10:]
    msgs = [{"role": "system", "content": SYSTEM_CHAT}]
    msgs.extend(recent)
    msgs.append({"role": "user", "content": user_text})
    return llm(msgs)

def main():
    history = load_session()
    print("Router con memoria listo.")
    print("Comandos:")
    print("- salir")
    print("- reset (borra la memoria de sesión)")
    print("- Para guardar: guardar: Titulo | Texto")
    print("- Memoria documental: kb/\n")

    if len(sys.argv) > 1:
        user_text = sys.argv[1]
    else:
        user_text = "Hola, ¿cómo puedo ayudarte?"

    print(f"Tú: {user_text}")

    # Guardamos el mensaje del usuario en memoria
    history = add_turn(history, "user", user_text)

    route = route_intent(history, user_text)
    print(f"\nRouter → {route}")

    if route == "SAVE":
        out = handle_save(history, user_text)
    elif route == "TASK":
        out = handle_task(history, user_text)
    elif route == "RAG":
        out = handle_rag(history, user_text)
    else:
        out = handle_chat(history, user_text)

    # Guardamos respuesta en memoria
    history = add_turn(history, "assistant", out)
    save_session(history)

    print("\nAgente:", out, "\n")

if __name__ == "__main__":
    main()