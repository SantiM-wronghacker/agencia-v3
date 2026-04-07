from agencia.agents.cerebro.llm_router import completar
from datetime import datetime
from pathlib import Path
import sys
import time
import re
import os
import json

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

MODEL = sys.argv[1] if len(sys.argv) > 1 else "llama-3.3-70b-versatile"
RUNS_DIR = Path(sys.argv[2] if len(sys.argv) > 2 else "runs")
RUNS_DIR.mkdir(exist_ok=True)

SYSTEM = """Eres un asistente útil y directo.
Si el usuario te pide guardar algo, crea una nota clara y estructurada.
"""

def save_note(title: str, content: str) -> str:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "_")
    filename = RUNS_DIR / f"{ts}_{safe_title or 'nota'}.md"
    filename.write_text(content, encoding="utf-8")
    return str(filename)

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

def main():
    if len(sys.argv) < 3:
        print("Usando valores por defecto.")
        user_input = "guardar: Nota de ejemplo | Este es un ejemplo de nota."
    else:
        user_input = " ".join(sys.argv[3:])

    print("Agente con archivos listo.")
    print("Formato para guardar:")
    print("  guardar: Titulo | Texto")
    print("Escribe 'salir' para terminar.\n")
    print(f"Fecha y hora actual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Directorio de runs: {RUNS_DIR}")
    print(f"Modelo de lenguaje: {MODEL}")
    print(f"Conexión a internet: {WEB}")
    print(f"Sistema operativo: {os.name}")
    print(f"Versión de Python: {sys.version}")
    print(f"Directorio de trabajo: {os.getcwd()}")
    print(f"Lista de archivos en el directorio de runs: {os.listdir(RUNS_DIR)}")

    if user_input.lower() in ("salir", "exit"):
        print("Saliendo...")
    elif user_input.startswith("guardar:"):
        try:
            title, content = user_input[8:].split(" | ", 1)
            filename = save_note(title, content)
            print(f"Nota guardada en: {filename}")
        except Exception as e:
            print(f"Error al guardar nota: {e}")
    else:
        try:
            resultado = _groq_compat_create(messages=[user_input])
            print(f"Resultado: {resultado.choices[0].message.content}")
        except Exception as e:
            print(f"Error: {e}")

    print("\nResumen ejecutivo:")
    print(f"Fecha y hora actual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Directorio de runs: {RUNS_DIR}")
    print(f"Modelo de lenguaje: {MODEL}")
    print(f"Conexión a internet: {WEB}")

if __name__ == "__main__":
    main()