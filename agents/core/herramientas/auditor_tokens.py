"""
AREA: HERRAMIENTAS
DESCRIPCION: Auditor de tokens para agentes de IA
TECNOLOGIA: Python, re, datetime, sys
"""

import os
import re
from datetime import datetime
import sys

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def leer_logs(ruta_log):
    try:
        with open(ruta_log, 'r', encoding='utf-8') as archivo_log:
            logs = archivo_log.readlines()
            return logs
    except FileNotFoundError:
        print(f"No se encontró el archivo de log en la ruta: {ruta_log}")
        return []
    except Exception as e:
        print(f"Error al leer el archivo de log: {e}")
        return []

def contar_tokens(logs):
    contador = {'Gemini': 0, 'Groq': 0}
    patron_gemini = re.compile(r'gemini')
    patron_groq = re.compile(r'groq')

    for linea in logs:
        if patron_gemini.search(linea):
            contador['Gemini'] += 1
        if patron_groq.search(linea):
            contador['Groq'] += 1

    return contador

def filtrar_por_fecha(logs, fecha_hoy):
    logs_filtrados = []
    patron_fecha = re.compile(r'\d{4}-\d{2}-\d{2}')

    for linea in logs:
        fecha_log = patron_fecha.search(linea)
        if fecha_log and fecha_log.group() == fecha_hoy:
            logs_filtrados.append(linea)

    return logs_filtrados

def calcular_promedio(contador_tokens, logs_filtrados):
    try:
        promedio_gemini = contador_tokens['Gemini'] / len(logs_filtrados) if logs_filtrados else 0
        promedio_groq = contador_tokens['Groq'] / len(logs_filtrados) if logs_filtrados else 0
        return promedio_gemini, promedio_groq
    except ZeroDivisionError:
        return 0, 0

def calcular_porcentaje(contador_tokens, logs_filtrados):
    try:
        total_tokens = contador_tokens['Gemini'] + contador_tokens['Groq']
        porcentaje_gemini = (contador_tokens['Gemini'] / total_tokens) * 100 if total_tokens else 0
        porcentaje_groq = (contador_tokens['Groq'] / total_tokens) * 100 if total_tokens else 0
        return porcentaje_gemini, porcentaje_groq
    except ZeroDivisionError:
        return 0, 0

def main():
    if len(sys.argv) > 1:
        ruta_log = sys.argv[1]
    else:
        ruta_log = 'path_a_tu_log.txt'
    logs = leer_logs(ruta_log)
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    logs_filtrados = filtrar_por_fecha(logs, fecha_hoy)
    contador_tokens = contar_tokens(logs)
    promedio_gemini, promedio_groq = calcular_promedio(contador_tokens, logs_filtrados)
    porcentaje_gemini, porcentaje_groq = calcular_porcentaje(contador_tokens, logs_filtrados)

    print(f"Fecha de hoy: {fecha_hoy}")
    print(f"Total de logs: {len(logs)}")
    print(f"Total de logs filtrados: {len(logs_filtrados)}")
    print(f"Tokens Gemini: {contador_tokens['Gemini']}")
    print(f"Tokens Groq: {contador_tokens['Groq']}")
    print(f"Promedio de tokens Gemini: {promedio_gemini:.2f}")
    print(f"Promedio de tokens Groq: {promedio_groq:.2f}")
    print(f"Porcentaje de tokens Gemini: {porcentaje_gemini:.2f}%")
    print(f"Porcentaje de tokens Groq: {porcentaje_groq:.2f}%")

    print("\nResumen ejecutivo:")
    print(f"El {fecha_hoy} se registraron {len(logs)} logs en total, de los cuales {len(logs_filtrados)} fueron filtrados.")
    print(f"Los tokens Gemini representan {porcentaje_gemini:.2f}% del total, mientras que los tokens Groq representan {porcentaje_groq:.2f}%.")

if __name__ == "__main__":
    main()