"""
AREA: HERRAMIENTAS
DESCRIPCION: Agente que realiza limpieza de archivos temporales
TECNOLOGIA: Python estándar
"""

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

def main():
    try:
        directorio_temp = sys.argv[1] if len(sys.argv) > 1 else '/tmp'
        extension_ignorar = sys.argv[2] if len(sys.argv) > 2 else None
        dias_minimos = int(sys.argv[3]) if len(sys.argv) > 3 else 0

        archivos_eliminados = 0
        archivos_ignorados = 0
        espacio_liberado = 0
        espacio_total = 0
        archivos_antiguos = 0
        archivos_recentes = 0

        if not os.path.exists(directorio_temp):
            print(f"Error: El directorio {directorio_temp} no existe")
            return

        for archivo in os.listdir(directorio_temp):
            ruta_completa = os.path.join(directorio_temp, archivo)
            if os.path.isfile(ruta_completa):
                tamaño_archivo = os.path.getsize(ruta_completa)
                espacio_total += tamaño_archivo
                fecha_modificacion = os.path.getmtime(ruta_completa)
                dias_archivo = (datetime.datetime.now() - datetime.datetime.fromtimestamp(fecha_modificacion)).days

                if extension_ignorar and archivo.endswith(extension_ignorar):
                    archivos_ignorados += 1
                    continue

                if dias_minimos > 0 and dias_archivo < dias_minimos:
                    archivos_recentes += 1
                    continue

                try:
                    os.remove(ruta_completa)
                    archivos_eliminados += 1
                    espacio_liberado += tamaño_archivo
                    if dias_archivo >= dias_minimos:
                        archivos_antiguos += 1
                except PermissionError:
                    print(f"Error: No se tiene permiso para eliminar el archivo {archivo}")
                except OSError as e:
                    print(f"Error: {str(e)}")

        print(f"Directorio de archivos temporales: {directorio_temp}")
        print(f"Archivos eliminados: {archivos_eliminados}")
        print(f"Archivos ignorados por extensión: {archivos_ignorados}")
        print(f"Archivos recientes ignorados: {archivos_recentes}")
        print(f"Archivos antiguos eliminados: {archivos_antiguos}")
        print(f"Espacio liberado: {espacio_liberado / (1024 * 1024):.2f} MB")
        print(f"Espacio total en el directorio: {espacio_total / (1024 * 1024):.2f} MB")
        print(f"Porcentaje de espacio liberado: {(espacio_liberado / espacio_total) * 100 if espacio_total > 0 else 0:.2f}%")
        print(f"Fecha de ejecución: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Versión de Python: {sys.version}")
        print(f"Sistema operativo: {sys.platform}")
        print(f"Nombre del host: {os.uname().nodename if hasattr(os, 'uname') else 'Unknown'}")
        print(f"Resumen ejecutivo: Se eliminaron {archivos_eliminados} archivos ({archivos_antiguos} antiguos), se ignoraron {archivos_ignorados + archivos_recentes} archivos y se liberaron {espacio_liberado / (1024 * 1024):.2f} MB de espacio en el directorio {directorio_temp}")
        print(f"Detalles adicionales: {archivos_ignorados} archivos ignorados por extensión y {archivos_recentes} archivos ignorados por ser recientes")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()