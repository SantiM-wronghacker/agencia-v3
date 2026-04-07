#!/usr/bin/env python3
"""
Wrapper: ejecuta dashboard_web.py desde su ubicación real en herramientas/
"""
import sys
import os
import runpy

# El script real está en herramientas/
real_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "herramientas", "dashboard_web.py"
)

if not os.path.exists(real_path):
    print(f"ERROR: No se encontró {real_path}", file=sys.stderr)
    sys.exit(1)

# Cambiar al directorio del script real para rutas relativas
os.chdir(os.path.dirname(real_path))
sys.path.insert(0, os.path.dirname(real_path))

runpy.run_path(real_path, run_name="__main__")
