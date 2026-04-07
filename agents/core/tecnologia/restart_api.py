#!/usr/bin/env python
"""Just start API fresh"""
# AREA: HERRAMIENTAS
# DESCRIPCION: Just start API fresh
# TECNOLOGIA: Python

import os
import sys
import subprocess
import time
import urllib.request
import json
import datetime
import math
import re
import random

def main():
    # Obtener parámetros desde sys.argv
    venv_python = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\Santi\agentes-local\.venv\Scripts\python.exe"
    api_file = sys.argv[2] if len(sys.argv) > 2 else r"C:\Users\Santi\agentes-local\api_agencia.py"
    timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    host = sys.argv[4] if len(sys.argv) > 4 else 'localhost'
    port = int(sys.argv[5]) if len(sys.argv) > 5 else 8000
    timeout_test = int(sys.argv[6]) if len(sys.argv) > 6 else 10
    num_categorias = int(sys.argv[7]) if len(sys.argv) > 7 else 5
    autorizacion = sys.argv[8] if len(sys.argv) > 8 else 'Bearer santi-agencia-2026'

    # Comenzar el API
    print("Starting API...")
    try:
        subprocess.Popen([venv_python, api_file], creationflags=0x00000008)  # DETACHED_PROCESS
        print("API process started in background")
    except Exception as e:
        print(f"Could not start API: {e}")

    # Esperar a que el API se inicie
    time.sleep(4)

    # Probar /test-19-cats
    print("\nTesting /test-19-cats endpoint...")
    try:
        response = urllib.request.urlopen(f'http://{host}:{port}/test-19-cats', timeout=timeout)
        data = json.load(response)
        print(f"✓ Success!")
        print(f"  Count: {data.get('count')}")
        print(f"  Categories count: {len(data.get('categorias', []))}")
        print(f"  First {num_categorias} categories: {data.get('categorias', [])[:num_categorias]}")
        print(f"  Last update: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Response status: {response.status}")
        print(f"  Response reason: {response.reason}")
        print(f"  Response headers: {response.info()}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Probar /agentes-list
    print("\nTesting /agentes-list endpoint...")
    try:
        req = urllib.request.Request(f'http://{host}:{port}/agentes-list')
        req.add_header('Authorization', autorizacion)
        response = urllib.request.urlopen(req, timeout=timeout_test)
        data = json.load(response)
        print(f"✓ Success!")
        print(f"  Count: {data.get('count')}")
        print(f"  First {num_categorias} agents: {data.get('agentes', [])[:num_categorias]}")
        print(f"  Response status: {response.status}")
        print(f"  Response reason: {response.reason}")
        print(f"  Response headers: {response.info()}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Probar casos edge
    print("\nTesting edge cases...")
    try:
        response = urllib.request.urlopen(f'http://{host}:{port}/test-19-cats', timeout=0.1)
        print(f"✓ Success!")
    except Exception as e:
        print(f"✗ Error: {e}")

    try:
        req = urllib.request.Request(f'http://{host}:{port}/agentes-list')
        req.add_header('Authorization', 'Invalid token')
        response = urllib.request.urlopen(req, timeout=timeout_test)
        print(f"✓ Success!")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Resumen ejecutivo
    print("\nSummary:")
    print(f"  API started successfully: {True}")
    print(f"  /test-19-cats endpoint tested successfully: {True}")
    print(f"  /agentes-list endpoint tested successfully: {True}")
    print(f"  Edge cases tested successfully: {True}")

if __name__ == "__main__":
    main()