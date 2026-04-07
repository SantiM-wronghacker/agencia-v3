"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Ejecuta una misión de mejora en el Dashboard con validaciones avanzadas
TECNOLOGÍA: Python, patcher_pro
"""
from agencia.agents.cerebro.patcher_pro import aplicar_mejora
import os
import time
import sys
import json
import datetime
import re

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def validar_archivo(archivo):
    if not os.path.exists(archivo):
        raise FileNotFoundError(f"Archivo no encontrado: {archivo}")
    if not os.path.isfile(archivo):
        raise ValueError(f"El path no es un archivo: {archivo}")
    if os.path.getsize(archivo) == 0:
        raise ValueError(f"Archivo vacío: {archivo}")

def procesar(archivo_mision='mision_del_arquitecto.txt', archivo_dashboard='app_dashboard.py'):
    try:
        validar_archivo(archivo_mision)
        validar_archivo(archivo_dashboard)

        with open(archivo_mision, 'r', encoding='utf-8') as f:
            mision = f.read().strip()

        if not mision:
            raise ValueError("El archivo de misión está vacío")

        if len(mision) > 1000:
            print(f"Advertencia: La misión tiene {len(mision)} caracteres (límite recomendado: 1000)")

        print(f"Ejecutando misión: {mision[:100]}...")
        inicio = datetime.datetime.now()
        aplicar_mejora(archivo_dashboard, mision)
        fin = datetime.datetime.now()

        duracion = (fin - inicio).total_seconds()
        print(f"Tiempo de ejecución: {duracion:.2f} segundos")
        print(f"Fecha de ejecución: {fin.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Archivo de misión: {archivo_mision} (Tamaño: {os.path.getsize(archivo_mision)} bytes)")
        print(f"Archivo de dashboard: {archivo_dashboard} (Tamaño: {os.path.getsize(archivo_dashboard)} bytes)")
        print(f"Estado de la misión: Exitosa")
        print(f"Versión del sistema: {sys.version.split()[0]}")
        print(f"Directorio de trabajo: {os.getcwd()}")

        resumen = {
            "fecha": fin.strftime('%Y-%m-%d %H:%M:%S'),
            "archivo_mision": archivo_mision,
            "archivo_dashboard": archivo_dashboard,
            "estado": "Exitosa",
            "duracion": f"{duracion:.2f} segundos",
            "tamano_mision": f"{os.path.getsize(archivo_mision)} bytes",
            "tamano_dashboard": f"{os.path.getsize(archivo_dashboard)} bytes",
            "version_python": sys.version.split()[0],
            "directorio": os.getcwd()
        }

        print("\nResumen Ejecutivo:")
        print(json.dumps(resumen, indent=4, ensure_ascii=False))

    except Exception as e:
        print(f"Error: {str(e)}")
        print(f"Fecha de error: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Archivo de misión: {archivo_mision}")
        print(f"Archivo de dashboard: {archivo_dashboard}")
        print(f"Estado de la misión: Fallida")
        print(f"Tipo de error: {type(e).__name__}")

        resumen = {
            "fecha": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "archivo_mision": archivo_mision,
            "archivo_dashboard": archivo_dashboard,
            "estado": "Fallida",
            "error": str(e),
            "tipo_error": type(e).__name__
        }

        print("\nResumen Ejecutivo:")
        print(json.dumps(resumen, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        procesar(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'app_dashboard.py')
    else:
        print("Ejecutando con valores por defecto...")
        procesar()