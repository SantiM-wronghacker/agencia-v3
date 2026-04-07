# HERRAMIENTAS/MONITOR DE CAMBIOS EN DIRECTORIO/PYTHON
# AREA: HERRAMIENTAS
# DESCRIPCION: Agente que realiza monitor cambios directorio
# TECNOLOGIA: Python

import os
import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def obtener_directorio_actual():
    return os.getcwd()

def obtener_contenido_directorio(directorio):
    try:
        return os.listdir(directorio)
    except FileNotFoundError:
        print(f"Error: Directorio '{directorio}' no encontrado.")
        return []
    except PermissionError:
        print(f"Error: No tiene permiso para acceder al directorio '{directorio}'.")
        return []
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return []

def obtenerInformacionArchivo(archivo):
    try:
        estadisticas = os.stat(archivo)
        return {
            'nombre': archivo,
            'tamaño': estadisticas.st_size,
            'fecha_modificacion': datetime.datetime.fromtimestamp(estadisticas.st_mtime),
            'fecha_creacion': datetime.datetime.fromtimestamp(estadisticas.st_ctime),
            'tipo': 'Archivo' if os.path.isfile(archivo) else 'Directorio'
        }
    except OSError as e:
        print(f"Error: No se puede obtener información del archivo '{archivo}'. {str(e)}")
        return None
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return None

def calcular_tamaño_total(archivos, directorio):
    tamaño_total = 0
    for archivo in archivos:
        archivo_path = os.path.join(directorio, archivo)
        if os.path.isfile(archivo_path):
            tamaño_total += os.path.getsize(archivo_path)
    return tamaño_total

def calcular_tamaño_promedio(archivos, directorio):
    tamaño_total = 0
    cantidad_archivos = 0
    for archivo in archivos:
        archivo_path = os.path.join(directorio, archivo)
        if os.path.isfile(archivo_path):
            tamaño_total += os.path.getsize(archivo_path)
            cantidad_archivos += 1
    if cantidad_archivos > 0:
        return tamaño_total / cantidad_archivos
    else:
        return 0

def main():
    try:
        directorio = sys.argv[1] if len(sys.argv) > 1 else '/home'
        print("Directorio actual:", obtener_directorio_actual())
        print("Directorio a monitorear:", directorio)
        archivos = obtener_contenido_directorio(directorio)
        print("Cantidad de archivos y directorios:", len(archivos))
        print("Lista de archivos y directorios:")
        for archivo in archivos:
            informacion = obtenerInformacionArchivo(os.path.join(directorio, archivo))
            if informacion:
                print(f"Nombre: {informacion['nombre']}, Tamaño: {informacion['tamaño']} bytes, Fecha de modificación: {informacion['fecha_modificacion']}, Tipo: {informacion['tipo']}")
        tamaño_total = calcular_tamaño_total(archivos, directorio)
        print(f"Tamaño total de los archivos: {tamaño_total} bytes")
        tamaño_promedio = calcular_tamaño_promedio(archivos, directorio)
        print(f"Tamaño promedio de los archivos: {tamaño_promedio} bytes")
        print("Resumen ejecutivo:")
        print(f"Se han encontrado {len(archivos)} archivos y directorios en el directorio '{directorio}'.")
        print(f"El tamaño total de los archivos es de {tamaño_total} bytes.")
        print(f"El tamaño promedio de los archivos es de {tamaño_promedio} bytes.")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()