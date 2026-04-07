"""
ÁREA: CEREBRO
DESCRIPCIÓN: Router inteligente que clasifica órdenes del usuario y las distribuye al agente correcto usando el bus de mensajes. Soporta rutas: CHAT, SAVE, TASK, FINANZAS, REAL_ESTATE, RAG.
TECNOLOGÍA: Groq (Nube)
"""


from llm_router import completar

def _groq_compat_create(**kwargs):
    """Compatibilidad con llamadas antiguas a client.chat.completions.create"""
    messages = kwargs.get('messages', [])
    temperatura = kwargs.get('temperature', 0.5)
    max_tokens = kwargs.get('max_tokens', 1000)

    class _Resp:
        class _Choice:
            class _Msg:
                content = ""
            message = _Msg()
        choices = [_Choice()]

    resultado = completar(messages, temperatura=temperatura, max_tokens=max_tokens)
    resp = _Resp()
    resp.choices[0].message.content = resultado or ""
    return resp

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
# Importar bus de mensajes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bus_mensajes as bus

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

# === CONFIGURACIÓN ===
RUNS_DIR = Path("runs")
KB_DIR = Path("kb")
RUNS_DIR.mkdir(exist_ok=True)
KB_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────
#  SISTEMAS DE PROMPTS POR ROL
# ─────────────────────────────────────────────

SYSTEM_ROUTER = """Eres el Router de la Agencia Santi — un sistema de 64 agentes especializados.
Tu trabajo es clasificar la intención del usuario en UNA de estas rutas:

- CHAT: pregunta simple, conversación general
- SAVE: el usuario quiere guardar una nota, idea o documento
- TASK: quiere un plan + entregable complejo (estrategia, propuesta, checklist)
- FINANZAS: cálculos de ROI, ISR, IVA, balances, contaduría, NIF
- REAL_ESTATE: inmuebles, hipotecas, plusvalía, leads, copywriting inmobiliario
- RAG: pregunta sobre documentos internos de la carpeta kb/

Devuelve SOLO una palabra: CHAT, SAVE, TASK, FINANZAS, REAL_ESTATE o RAG.

Reglas:
- "guardar", "anotar", "nota", "guarda esto" => SAVE
- "plan", "estrategia", "checklist", "pasos", "propuesta" => TASK  
- "ROI", "ISR", "IVA", "balance", "NIF", "impuesto", "contabilidad" => FINANZAS
- "casa", "depa", "hipoteca", "inmueble", "plusvalía", "lead", "cliente comprador" => REAL_ESTATE
- preguntas sobre precios internos, procesos, políticas => RAG
- todo lo demás => CHAT
"""

SYSTEM_CHAT = """Eres un asistente de la Agencia Santi. 
Eres directo, práctico y útil. Responde en español.
Tienes acceso a 64 agentes especializados en finanzas, real estate y herramientas."""

SYSTEM_PLANNER = """Eres el Planner de la Agencia Santi.
Convierte cualquier petición en un plan de acción concreto.
Formato de respuesta:
1) OBJETIVO: (1 línea clara)
2) PLAN: (5-8 pasos numerados y accionables)
3) ENTREGABLES: (qué se producirá)
4) RIESGOS: (2-3 puntos breves)
Sé específico, no genérico."""

SYSTEM_EXECUTOR = """Eres el Executor de la Agencia Santi.
Recibes un objetivo y un plan, y produces el primer entregable real.
Formato Markdown con checklist accionable.
Si faltan datos, márcalos con [DATO REQUERIDO: descripción].
Sé concreto y útil, no teórico."""

SYSTEM_FINANZAS = """Eres el agente de Finanzas de la Agencia Santi, especializado en:
- Cálculos de ISR, IVA, IMSS para México
- Análisis de balances bajo NIF mexicanas
- Cálculos de ROI e indicadores financieros
- Contaduría pública y fiscal mexicana
Usa cifras reales, tasas actuales de México. Sé preciso y muestra las fórmulas."""

SYSTEM_REAL_ESTATE = """Eres el agente de Real Estate de la Agencia Santi, especializado en:
- Mercado inmobiliario mexicano
- Simuladores hipotecarios (tasas INFONAVIT, FOVISSSTE, bancarias)
- Análisis de plusvalía por zona
- Generación de copies y propuestas para leads
- Seguimiento de clientes compradores
Usa datos del mercado mexicano. Sé específico con zonas y precios reales."""

# ─────────────────────────────────────────────
#  FUNCIONES CORE
# ─────────────────────────────────────────────

def llamar_groq(system, user, temperatura=0.7, max_tokens=2048):
    """Llamada robusta a Groq con reintentos."""
    for intento in range(3):
        try:
            completion = _groq_compat_create(
                model=MODELO,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                temperature=temperatura,
                max_tokens=max_tokens,
                top_p=1,
                stream=False
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            err = str(e).lower()
            if "rate_limit" in err:
                time.sleep(10 * (intento + 1))
            elif intento < 2:
                time.sleep(3)
            else:
                return f"[ERROR Groq]: {e}"

def clasificar_ruta(orden):
    """Clasifica la orden en una ruta usando Groq."""
    ruta = llamar_groq(SYSTEM_ROUTER, orden, temperatura=0.0, max_tokens=10)
    ruta = ruta.upper().split()[0] if ruta else "CHAT"
    rutas_validas = {"CHAT", "SAVE", "TASK", "FINANZAS", "REAL_ESTATE", "RAG"}
    return ruta if ruta in rutas_validas else "CHAT"

def guardar_md(titulo, contenido):
    """Guarda un archivo markdown en runs/."""
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe = "".join(c for c in titulo if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "_")
    path = RUNS_DIR / f"{ts}_{safe or 'run'}.md"
    path.write_text(contenido, encoding="utf-8")
    return str(path)

def rag_buscar(query, top_k=3):
    """RAG simple por coincidencia de palabras en kb/."""
    archivos = list(KB_DIR.glob("*"))
    if not archivos:
        return "KB vacía. Agrega documentos a la carpeta kb/ para usar RAG."

    scored = []
    q = query.lower()
    for f in archivos:
        try:
            txt = f.read_text(encoding="utf-8", errors="ignore")
            score = sum(1 for w in q.split() if w in txt.lower())
            scored.append((score, f.name, txt))
        except Exception:
            continue

    scored.sort(reverse=True, key=lambda x: x[0])
    top = scored[:top_k]
    contexto = []
    for score, nombre, txt in top:
        contexto.append(f"[Fuente: {nombre} | relevancia:{score}]\n{txt[:2000]}")
    return "\n\n---\n\n".join(contexto)

# ─────────────────────────────────────────────
#  MANEJADORES POR RUTA
# ─────────────────────────────────────────────

def manejar_chat(orden, id_mensaje=None):
    respuesta = llamar_groq(SYSTEM_CHAT, orden)
    if id_mensaje:
        bus.depositar("agent_router", "maestro_ceo", "resultado", respuesta, respuesta_a=id_mensaje)
    return respuesta

def manejar_save(orden, id_mensaje=None):
    if "|" in orden and orden.lower().startswith("guardar:"):
        payload = orden[len("guardar:"):].strip()
        titulo, texto = [x.strip() for x in payload.split("|", 1)]
    else:
        titulo = "nota"
        texto = orden
    
    md = f"# {titulo}\n\n{texto}\n"
    ruta = guardar_md(titulo, md)
    respuesta = f"Guardado en: {ruta}"
    
    if id_mensaje:
        bus.depositar("agent_router", "maestro_ceo", "resultado", respuesta, respuesta_a=id_mensaje)
    return respuesta

def manejar_task(orden, id_mensaje=None):
    plan = llamar_groq(SYSTEM_PLANNER, orden)
    entregable = llamar_groq(SYSTEM_EXECUTOR, f"Petición:\n{orden}\n\nPlan:\n{plan}")
    reporte = f"# Tarea\n{orden}\n\n# Plan\n{plan}\n\n# Entregable\n{entregable}\n"
    ruta = guardar_md("tarea", reporte)
    respuesta = f"Tarea completada. Guardada en: {ruta}\n\n{entregable[:500]}..."
    
    if id_mensaje:
        bus.depositar("agent_router", "maestro_ceo", "resultado", respuesta, respuesta_a=id_mensaje)
    return respuesta

def manejar_finanzas(orden, id_mensaje=None):
    respuesta = llamar_groq(SYSTEM_FINANZAS, orden, max_tokens=3000)
    ruta = guardar_md("finanzas", f"# Consulta Financiera\n{orden}\n\n# Análisis\n{respuesta}")
    
    resultado = f"{respuesta}\n\n[Reporte guardado: {ruta}]"
    if id_mensaje:
        bus.depositar("agent_router", "maestro_ceo", "resultado", resultado, respuesta_a=id_mensaje)
    return resultado

def manejar_real_estate(orden, id_mensaje=None):
    respuesta = llamar_groq(SYSTEM_REAL_ESTATE, orden, max_tokens=3000)
    ruta = guardar_md("real_estate", f"# Consulta Inmobiliaria\n{orden}\n\n# Análisis\n{respuesta}")
    
    resultado = f"{respuesta}\n\n[Reporte guardado: {ruta}]"
    if id_mensaje:
        bus.depositar("agent_router", "maestro_ceo", "resultado", resultado, respuesta_a=id_mensaje)
    return resultado

def manejar_rag(orden, id_mensaje=None):
    contexto = rag_buscar(orden)
    respuesta = llamar_groq(
        SYSTEM_CHAT,
        f"Responde usando SOLO el contexto. Si no está ahí, dilo.\n\nCONTEXTO:\n{contexto}\n\nPREGUNTA:\n{orden}",
        max_tokens=1500
    )
    if id_mensaje:
        bus.depositar("agent_router", "maestro_ceo", "resultado", respuesta, respuesta_a=id_mensaje)
    return respuesta

# ─────────────────────────────────────────────
#  FUNCIÓN PRINCIPAL — usada por maestro_ceo
# ─────────────────────────────────────────────

MANEJADORES = {
    "CHAT": manejar_chat,
    "SAVE": manejar_save,
    "TASK": manejar_task,
    "FINANZAS": manejar_finanzas,
    "REAL_ESTATE": manejar_real_estate,
    "RAG": manejar_rag
}

def procesar_orden(orden, id_mensaje=None):
    """
    Punto de entrada principal.
    Clasifica la orden y la despacha al manejador correcto.
    """
    ruta = clasificar_ruta(orden)
    print(f"   Router → {ruta}")
    
    manejador = MANEJADORES.get(ruta, manejar_chat)
    return manejador(orden, id_mensaje)

# ─────────────────────────────────────────────
#  MODO STANDALONE — escucha el bus
# ─────────────────────────────────────────────

def modo_bus():
    """Escucha el bus de mensajes y procesa órdenes dirigidas al router."""
    print("📡 Agent Router escuchando el bus...")
    while True:
        mensajes = bus.recoger("agent_router", tipo="orden")
        for m in mensajes:
            print(f"   Procesando: {m['contenido'][:60]}...")
            procesar_orden(m["contenido"], id_mensaje=m["id"])
        time.sleep(2)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--bus":
        modo_bus()
    elif len(sys.argv) > 1:
        orden = " ".join(sys.argv[1:])
        print(procesar_orden(orden))
    else:
        # Modo interactivo
        print("Router listo. 'salir' para terminar.\n")
        while True:
            orden = input("Tú: ").strip()
            if orden.lower() in ("salir", "exit", "quit"):
                break
            print(f"\n{procesar_orden(orden)}\n")