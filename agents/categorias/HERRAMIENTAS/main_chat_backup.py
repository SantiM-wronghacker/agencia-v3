"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente de chat mejorado que utiliza la API de Groq para generar respuestas a preguntas del usuario
TECNOLOGÍA: Python, requests, json, Groq API
"""

import requests
import json
import sys
import time
from datetime import datetime
import os
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

MODEL = os.environ.get('MODEL') or sys.argv[1] if len(sys.argv) > 1 else "llama-3.3-70b-versatile"
API_URL = os.environ.get('API_URL') or sys.argv[2] if len(sys.argv) > 2 else "https://api.groq.com/v1/models/" + MODEL + "/generate"
LOG_FILE = os.environ.get('LOG_FILE') or sys.argv[3] if len(sys.argv) > 3 else "log.txt"
DEFAULT_PROMPT = os.environ.get('DEFAULT_PROMPT') or sys.argv[4] if len(sys.argv) > 4 else "Eres un asistente útil, directo y práctico.\nTú: "
API_KEY = os.environ.get('API_KEY') or sys.argv[5] if len(sys.argv) > 5 else "Bearer TU_API_KEY_AQUI"

def get_api_key():
    return API_KEY

def log_message(message_type, content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message_type}: {content}\n"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def generate_response(prompt, api_key):
    payload = {
        "prompt": prompt,
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 0.95,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key,
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload), timeout=30)
        response.raise_for_status()
        return response.json()["text"].strip()
    except requests.exceptions.Timeout:
        log_message("Error", "Tiempo de espera agotado")
        return "Error: Tiempo de espera agotado al conectar con el servicio."
    except requests.exceptions.RequestException as e:
        log_message("Error", str(e))
        return "Error: Ocurrió un error al realizar la solicitud."
    except json.JSONDecodeError:
        log_message("Error", "Error al decodificar la respuesta JSON.")
        return "Error: No se pudo decodificar la respuesta JSON."
    except KeyError:
        log_message("Error", "Error al acceder a la clave 'text' en la respuesta JSON.")
        return "Error: No se encontró la clave 'text' en la respuesta JSON."

def calcular_intereses(p, t, r):
    return p * t * r / 100

def calcular_descuento(p, d):
    return p * (1 - d / 100)

def main():
    print("ÁREA: HERRAMIENTAS")
    print("DESCRIPCIÓN: Agente de chat mejorado que utiliza la API de Groq para generar respuestas a preguntas del usuario")
    print("TECNOLOGÍA: Python, requests, json, Groq API")

    if not WEB:
        print("No hay conexión a internet.")

    print("Modelo:", MODEL)
    print("API URL:", API_URL)
    print("Log file:", LOG_FILE)
    print("Default prompt:", DEFAULT_PROMPT)
    print("API key:", get_api_key())

    prompt = DEFAULT_PROMPT
    api_key = get_api_key()
    response = generate_response(prompt, api_key)

    print("Respuesta:")
    print(response)

    print("Resumen ejecutivo:")
    print("El modelo utilizado es", MODEL)
    print("La API URL utilizada es", API_URL)
    print("El log file utilizado es", LOG_FILE)
    print("El default prompt utilizado es", DEFAULT_PROMPT)
    print("La API key utilizada es", get_api_key())

if __name__ == "__main__":
    main()