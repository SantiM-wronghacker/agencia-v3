"""
AREA: CEREBRO
DESCRIPCION: Agente que procesa órdenes y muestra resultados
TECNOLOGIA: Python, importlib, sys
"""

import importlib.util
import sys
import traceback
import time
import os
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def cargar_maestro_ceo(archivo="maestro_ceo.py", path=None):
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    archivo = os.path.join(path, archivo)
    try:
        spec = importlib.util.spec_from_file_location("maestro_ceo", archivo)
        maestro_ceo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(maestro_ceo)
        return maestro_ceo
    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar el módulo maestro_ceo: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

def obtener_orden(argv):
    if len(argv) > 1:
        orden = argv[1]
        if orden.isdigit():
            orden = int(orden)
        return orden
    else:
        return 0

def enviar_orden(orden, maestro_ceo):
    try:
        if hasattr(maestro_ceo, "procesar_orden"):
            resultado = getattr(maestro_ceo, "procesar_orden")(orden)
            return resultado
        else:
            print("El módulo maestro_ceo no tiene la función procesar_orden")
            return None
    except ValueError as e:
        print(f"Error de valor: {str(e)}")
    except TypeError as e:
        print(f"Error de tipo: {str(e)}")
    except Exception as e:
        print(f"Error al procesar la orden: {str(e)}")
        traceback.print_exc()
        return None

def mostrar_progreso(resultado):
    if resultado is not None:
        print(f"Resultado: {resultado}")
        print(f"Valor de la orden: {obtener_orden(sys.argv)}")
        print(f"Fecha y hora actual: {datetime.datetime.now()}")
        print(f"Conexión a internet: {WEB}")
        print(f"Path actual: {os.path.dirname(os.path.abspath(__file__))}")
        print(f"Cantidad de argumentos: {len(sys.argv)}")
    else:
        print("No se obtuvo resultado")

def calcular_precio(orden):
    try:
        if orden > 0:
            precio = orden * 10.99
            return precio
        else:
            return None
    except Exception as e:
        print(f"Error al calcular el precio: {str(e)}")
        traceback.print_exc()
        return None

def calcular_descuento(orden):
    try:
        if orden > 0:
            descuento = orden * 0.10
            return descuento
        else:
            return None
    except Exception as e:
        print(f"Error al calcular el descuento: {str(e)}")
        traceback.print_exc()
        return None

def calcular_total(orden):
    try:
        precio = calcular_precio(orden)
        descuento = calcular_descuento(orden)
        if precio is not None and descuento is not None:
            total = precio - descuento
            return total
        else:
            return None
    except Exception as e:
        print(f"Error al calcular el total: {str(e)}")
        traceback.print_exc()
        return None

def resumen_ejecutivo(resultado):
    if resultado is not None:
        print(f"Resumen ejecutivo: El resultado de la orden {obtener_orden(sys.argv)} es {resultado}.")
    else:
        print("No se obtuvo resultado")

def main():
    archivo_maestro = "maestro_ceo.py"
    path_maestro = None
    orden = obtener_orden(sys.argv)
    maestro_ceo = cargar_maestro_ceo(archivo_maestro, path_maestro)
    resultado = enviar_orden(orden, maestro_ceo)
    mostrar_progreso(resultado)
    resultado = calcular_total(orden)
    mostrar_progreso(resultado)
    resumen_ejecutivo(resultado)

if __name__ == "__main__":
    main()