"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza parser archivos configuracion
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def main():
    try:
        archivo_configuracion = sys.argv[1] if len(sys.argv) > 1 else "configuracion.json"
        if not os.path.exists(archivo_configuracion):
            raise FileNotFoundError("El archivo de configuración no existe")
        
        with open(archivo_configuracion, "r") as archivo:
            configuracion = json.load(archivo)
        
        print(f"Fecha de ejecución: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Nombre del archivo de configuración: {archivo_configuracion}")
        print(f"Número de secciones en el archivo de configuración: {len(configuracion)}")
        print(f"Valor de la primera sección: {list(configuracion.values())[0]}")
        print(f"Resultado de una operación matemática aleatoria: {random.randint(1, 100) * math.pi}")
        print(f"Nombre del sistema operativo: {sys.platform}")
        print(f"Versión de Python: {sys.version}")
        print(f"Ruta del archivo de configuración: {os.path.abspath(archivo_configuracion)}")
        print(f"Tamaño del archivo de configuración: {os.path.getsize(archivo_configuracion)} bytes")
        print(f"Fecha de modificación del archivo de configuración: {datetime.datetime.fromtimestamp(os.path.getmtime(archivo_configuracion)).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Fecha de creación del archivo de configuración: {datetime.datetime.fromtimestamp(os.path.getctime(archivo_configuracion)).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Permisos del archivo de configuración: {oct(os.stat(archivo_configuracion).st_mode)}")
        print(f"UID del propietario del archivo de configuración: {os.stat(archivo_configuracion).st_uid}")
        print(f"GID del grupo del archivo de configuración: {os.stat(archivo_configuracion).st_gid}")
        
        # Calculos adicionales
        numero_aleatorio = random.randint(1, 100)
        print(f"Resultado de una operación matemática aleatoria con raíz cuadrada: {math.sqrt(numero_aleatorio)}")
        print(f"Resultado de una operación matemática aleatoria con logaritmo: {math.log(numero_aleatorio)}")
        print(f"Resultado de una operación matemática aleatoria con seno: {math.sin(numero_aleatorio)}")
        print(f"Resultado de una operación matemática aleatoria con coseno: {math.cos(numero_aleatorio)}")
        print(f"Resultado de una operación matemática aleatoria con tangente: {math.tan(numero_aleatorio)}")
        
        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El archivo de configuración {archivo_configuracion} tiene {len(configuracion)} secciones.")
        print(f"El tamaño del archivo es de {os.path.getsize(archivo_configuracion)} bytes.")
        print(f"El archivo fue modificado por última vez el {datetime.datetime.fromtimestamp(os.path.getmtime(archivo_configuracion)).strftime('%Y-%m-%d %H:%M:%S')}.")
        print(f"El archivo fue creado el {datetime.datetime.fromtimestamp(os.path.getctime(archivo_configuracion)).strftime('%Y-%m-%d %H:%M:%S')}.")
        print(f"El archivo tiene permisos {oct(os.stat(archivo_configuracion).st_mode)}.")
        print(f"El propietario del archivo es el UID {os.stat(archivo_configuracion).st_uid}.")
        print(f"El grupo del archivo es el GID {os.stat(archivo_configuracion).st_gid}.")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()