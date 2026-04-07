"""
AREA: CEREBRO
DESCRIPCION: Gestiona la memoria de conversaciones y actualiza resúmenes.
TECNOLOGIA: Python, json, sys, os, datetime
"""

import json
import os
import sys
import datetime

try:
    MODEL = sys.argv[1] if len(sys.argv) > 1 else "modelo_estandar"
    API_KEY = sys.argv[2] if len(sys.argv) > 2 else 'clave_api_estandar'
    BASE_URL = sys.argv[3] if len(sys.argv) > 3 else "https://api.estandar.com"
except IndexError:
    print("Error: Debe proporcionar los parámetros MODEL, API_KEY y BASE_URL")
    sys.exit(1)

RUNS_DIR = os.path.join("runs")
os.makedirs(RUNS_DIR, exist_ok=True)

STATE_FILE = os.path.join(RUNS_DIR, "state.json")

SUMMARY_SYSTEM = """Eres un compresor de memoria.
Actualiza un resumen vivo de la conversación.
Reglas:
- Mantén el resumen en 10-20 líneas.
- Conserva: objetivos, decisiones, preferencias, datos (precios, nombres), pendientes.
- Elimina: charla repetitiva.
Devuelve SOLO el resumen actualizado.
"""

def load_state():
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r', encoding="utf-8") as file:
                return json.load(file)
    except Exception as e:
        print(f"Error al cargar estado: {e}")
    return {"summary": "", "recent": []}

def save_state(state):
    try:
        with open(STATE_FILE, 'w', encoding="utf-8") as file:
            json.dump(state, file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error al guardar estado: {e}")

def procesar_conversacion(conversacion):
    try:
        # Procesar la conversación para extraer datos útiles
        datos_utiles = []
        for linea in conversacion.splitlines():
            if "objetivo" in linea.lower():
                datos_utiles.append(linea)
            elif "decisión" in linea.lower():
                datos_utiles.append(linea)
            elif "preferencia" in linea.lower():
                datos_utiles.append(linea)
            elif "precio" in linea.lower():
                datos_utiles.append(linea)
            elif "nombre" in linea.lower():
                datos_utiles.append(linea)
            elif "pendiente" in linea.lower():
                datos_utiles.append(linea)
        return "\n".join(datos_utiles)
    except Exception as e:
        print(f"Error al procesar conversación: {e}")
        return ""

def resumen_ejecutivo(summary):
    try:
        # Generar un resumen ejecutivo con los datos más importantes
        resumen = []
        for linea in summary.splitlines():
            if "objetivo" in linea.lower():
                resumen.append(linea)
            elif "decisión" in linea.lower():
                resumen.append(linea)
            elif "preferencia" in linea.lower():
                resumen.append(linea)
        return "\n".join(resumen)
    except Exception as e:
        print(f"Error al generar resumen ejecutivo: {e}")
        return ""

def main():
    estado = load_state()
    conversacion = estado.get("summary", "")
    if len(conversacion.splitlines()) < 20:
        conversacion += "\n" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conversacion += "\n" + "Conversación en progreso..."
    estado["summary"] = procesar_conversacion(conversacion)
    save_state(estado)
    resumen = estado["summary"]
    print("Resumen de la conversación:")
    print(resumen)
    print("\nResumen ejecutivo:")
    print(resumen_ejecutivo(resumen))

if __name__ == "__main__":
    main()