#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script para verificar el endpoint /agentes-list
AREA: CEREBRO
DESCRIPCION: Test script para verificar el endpoint /agentes-list
TECNOLOGIA: Python 3.x
"""

import sys
import os
import json
import urllib.request
import urllib.error
import datetime

def main():
    # Fix encoding
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    # Asegurar que estamos usando el archivo correcto
    api_path = os.path.join(os.path.dirname(__file__), 'api_agencia.py')
    print("[INFO] Using API file: {}".format(api_path))
    print("[INFO] File exists: {}".format(os.path.exists(api_path)))

    # Leer el archivo y verificar que contiene el código correcto
    try:
        with open(api_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("[ERROR] El archivo no existe")
        return

    # Buscar el endpoint /agentes-list
    if '/agentes-list' in content:
        print("[OK] Found /agentes-list endpoint in code")

        # Encontrar la sección de TODAS_LAS_CATEGORIAS
        start_idx = content.find('elif ruta == "/agentes-list"')
        section = content[start_idx:start_idx+1500]

        # Contar MICRO_TAREAS
        if 'MICRO_TAREAS' in section:
            print("[OK] Found MICRO_TAREAS in /agentes-list endpoint")

        # Verificar que sorted(TODAS_LAS_CATEGORIAS) está en la respuesta
        if 'sorted(TODAS_LAS_CATEGORIAS)' in section:
            print("[OK] Using sorted(TODAS_LAS_CATEGORIAS) in response")
        else:
            print("[ERROR] NOT using sorted(TODAS_LAS_CATEGORIAS)")
    else:
        print("[ERROR] /agentes-list endpoint NOT found in code!")
        return

    # Ahora hacer una prueba real del endpoint
    print("\n" + "="*50)
    print("[INFO] Testing actual endpoint...")
    url = 'http://localhost:8000/agentes-list'
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'Bearer santi-agencia-2026')

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.load(response)
            print("[OK] Connected to API")
            print("[INFO] Agentes: {}".format(len(data.get('agentes', {}))))
            print("[INFO] Categorias: {}".format(len(data.get('categorias', []))))
            print("[INFO] Categorias list: {}".format(data.get('categorias', [])))
            print("[INFO] Fecha de respuesta: {}".format(datetime.datetime.now()))
            print("[INFO] Tiempo de respuesta: {} segundos".format(response.headers.get('response-time', 'No disponible')))
    except urllib.error.URLError as e:
        print("[ERROR] Error al conectar al API: {}".format(e))
    except json.JSONDecodeError as e:
        print("[ERROR] Error al parsear la respuesta: {}".format(e))

    # Resumen ejecutivo
    print("\n" + "="*50)
    print("[RESUMEN EJECUTIVO]")
    print("Fecha de ejecución: {}".format(datetime.datetime.now()))
    print("Resultado de la prueba: {}".format("EXITOSO" if '/agentes-list' in content else "FALLIDO"))
    print("Cantidad de agentes: {}".format(len(data.get('agentes', {})) if 'data' in locals() else 'No disponible'))
    print("Cantidad de categorias: {}".format(len(data.get('categorias', [])) if 'data' in locals() else 'No disponible'))

if __name__ == "__main__":
    main()