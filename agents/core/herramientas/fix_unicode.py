# ARCHIVO: fix_unicode.py
# AREA: HERRAMIENTAS
# DESCRIPCION: Utilidad de mantenimiento. Corrige UnicodeEncodeError en archivos Python de la agencia reemplazando emojis y caracteres especiales por texto ASCII.
# TECNOLOGIA: Python 3

import os
import sys
import json
import datetime
import math
import re
import random

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

ARCHIVOS = [
    "fabrica_agentes.py",
    "noche_total.py",
    "auto_run.py",
    "sistema_maestro.py",
    "api_agencia.py",
    "dashboard_web.py",
    "orquestador_clawbot.py",
]

REEMPLAZOS = [
    ("[FABRICA]", "[FABRICA]"), ("[OK]", "[OK]"), ("[ERROR]", "[ERROR]"),
    ("[WARN]", "[WARN]"), ("[INFO]", "[INFO]"), ("[NOCHE]", "[NOCHE]"),
    ("[RUN]", "[RUN]"), ("[FIX]", "[FIX]"), ("[STOP]", "[STOP]"),
    ("[STATS]", "[STATS]"), ("[LISTA]", "[LISTA]"), ("[DOC]", "[DOC]"), ("[CEREBRO]", "[CEREBRO]"),
    ("[META]", "[META]"), ("[BUSCAR]", "[BUSCAR]"), ("[FAST]", "[FAST]"),
    ("[QA]","[QA]"), ("[PAUSA]", "[PAUSA]"), ("[ALERTA]", "[ALERTA]"),
    ("[OK]",  "[OK]"), ("[FAIL]",  "[FAIL]"), ("->",  "->"), ("<-",  "<-"),
    ("+", "+"), ("-", "-"), ("|", "|"), ("=", "="), (">", ">"), ("<", "<"),
]

PARCHE_VIEJO = """"""

def limpiar(archivo):
    if not os.path.exists(archivo):
        print(f"  No encontrado: {archivo}")
        return

    try:
        with open(archivo, "r", encoding="utf-8", errors="replace") as f:
            texto = f.read()
    except Exception as e:
        print(f"Error al leer {archivo}: {e}")
        return

    # Quitar parche viejo
    texto = texto.replace(PARCHE_VIEJO, "").strip()

    # Aplicar reemplazos
    for orig, remp in REEMPLAZOS:
        texto = texto.replace(orig, remp)

    # Forzar ASCII en cualquier caracter raro restante
    lineas_safe = []
    for linea in texto.split("\n"):
        try:
            linea.encode("cp1252")
            lineas_safe.append(linea)
        except (UnicodeEncodeError):
            linea_safe = ""
            for char in linea:
                try:
                    char.encode("cp1252")
                    linea_safe += char
                except (UnicodeEncodeError):
                    linea_safe += "?"
            lineas_safe.append(linea_safe)

    texto_limpio = "\n".join(lineas_safe)

    # Escribir archivo limpio
    try:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(texto_limpio)
        print(f"  Archivo {archivo} limpio y escrito correctamente")
    except Exception as e:
        print(f"Error al escribir {archivo}: {e}")

def main():
    num_archivos_procesados = 0
    num_archivos_limpios = 0
    for archivo in ARCHIVOS:
        limpiar(archivo)
        num_archivos_procesados += 1
        if os.path.exists(archivo):
            num_archivos_limpios += 1
    print(f"Resumen ejecutivo:")
    print(f"  Archivos procesados: {num_archivos_procesados}")
    print(f"  Archivos limpios: {num_archivos_limpios}")
    print(f"  Fecha de ejecución: {datetime.datetime.now()}")
    print(f"  Versión de Python: {sys.version}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Uso: python fix_unicode.py")
    else:
        main()