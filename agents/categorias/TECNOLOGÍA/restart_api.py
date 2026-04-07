#!/usr/bin/env python
"""Just start API fresh"""
import os
import sys
import subprocess
import time
import urllib.request
import json

# Start new API
print("Starting API...")
venv_python = r"C:\Users\Santi\agentes-local\.venv\Scripts\python.exe"
api_file = r"C:\Users\Santi\agentes-local\api_agencia.py"

# Try to start it (may fail if already running, that's ok)
try:
    subprocess.Popen([venv_python, api_file], creationflags=0x00000008)  # DETACHED_PROCESS
    print("API process started in background")
except Exception as e:
    print(f"Could not start API: {e}")

# Wait for it to start
time.sleep(4)

# Test /test-19-cats
print("\nTesting /test-19-cats endpoint...")
try:
    response = urllib.request.urlopen('http://localhost:8000/test-19-cats', timeout=5)
    data = json.load(response)
    print(f"✓ Success!")
    print(f"  Count: {data.get('count')}")
    print(f"  Categories count: {len(data.get('categorias', []))}")
    print(f"  First 3 categories: {data.get('categorias', [])[:3]}")
except Exception as e:
    print(f"✗ Error: {e}")

# Also test /agentes-list
print("\nTesting /agentes-list endpoint...")
try:
    req = urllib.request.Request('http://localhost:8000/agentes-list')
    req.add_header('Authorization', 'Bearer santi-agencia-2026')
    response = urllib.request.urlopen(req, timeout=5)
    data = json.load(response)
    print(f"✓ Success!")
    print(f"  Agentes: {len(data.get('agentes', {}))}")
    print(f"  Categories: {len(data.get('categorias', []))}")
    print(f"  Categories list: {data.get('categorias', [])}")
except Exception as e:
    print(f"✗ Error: {e}")
