"""
ÁREA: CEREBRO
DESCRIPCIÓN: Agente de planificación y ejecución de tareas
TECNOLOGÍA: Python, Groq
"""

from llm_router import completar
from datetime import datetime
from pathlib import Path
import sys
import time
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

API_KEY = sys.argv[1] if len(sys.argv) > 1 else "tu_api_key_aquí"
RUNS_DIR = Path("runs")
RUNS_DIR.mkdir(exist_ok=True)
MODEL = "groq:base"

def save_run(title: str, content: str) -> str:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "_")
    filename = RUNS_DIR / f"{ts}_{safe_title or 'run'}.md"
    filename.write_text(content, encoding="utf-8")
    return str(filename)

def chat(model: str, system: str, user: str) -> str:
    try:
        r = _groq_compat_create(
            api_key=API_KEY,
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        time.sleep(2)
        return r.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

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

SYSTEM = """Eres un planificador y ejecutor. Convierte la petición en un plan accionable y produce un primer entregable real en texto.
Si faltan datos, asume lo mínimo razonable y marca TODO supuesto.
Entrega en Markdown, con secciones y checklist.
Devuelve:
1) Objetivo (1 línea)
2) Plan (5-10 pasos numerados)
3) 

### Resumen Ejecutivo
El objetivo es {objetivo}.
El plan consta de {num_puntos} puntos.
"""

def main():
    user_input = sys.argv[2] if len(sys.argv) > 2 else "Planifica y ejecuta una tarea"
    resultado = chat(MODEL, SYSTEM, user_input)
    objetivo = "Planificar y ejecutar una tarea"
    num_puntos = 5
    plan = [
        "1. Definir el objetivo",
        "2. Identificar los recursos necesarios",
        "3. Asignar tareas a los miembros del equipo",
        "4. Establecer un cronograma",
        "5. Monitorear y ajustar el plan",
    ]
    resultado = f"""# Objetivo
{objetivo}

# Plan
{chr(10).join(plan)}

# Checklist
- [ ] Definir el objetivo
- [ ] Identificar los recursos necesarios
- [ ] Asignar tareas a los miembros del equipo
- [ ] Establecer un cronograma
- [ ] Monitorear y ajustar el plan

{SYSTEM.format(objetivo=objetivo, num_puntos=num_puntos)}
"""
    save_run("Planificación y ejecución de tareas", resultado)
    print(resultado)

if __name__ == "__main__":
    main()