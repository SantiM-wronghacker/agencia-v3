"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora takt time
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
from datetime import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def calcular_takt_time(duracion_proceso, frecuencia_produccion):
    """
    Calcula el tiempo takt (tasa de producción) en minutos.

    Args:
        duracion_proceso (float): Duración del proceso en minutos.
        frecuencia_produccion (float): Frecuencia de producción en unidades por hora.

    Returns:
        float: Tiempo takt en minutos.
    """
    return duracion_proceso / (frecuencia_produccion * 60)

def calcular_takt_time_mexico(duracion_proceso, frecuencia_produccion):
    """
    Calcula el tiempo takt (tasa de producción) en minutos para México.

    Args:
        duracion_proceso (float): Duración del proceso en minutos.
        frecuencia_produccion (float): Frecuencia de producción en unidades por hora.

    Returns:
        float: Tiempo takt en minutos.
    """
    # Considera la productividad media de México
    productividad_media = 0.8
    return duracion_proceso / (frecuencia_produccion * 60 * productividad_media)

def main():
    try:
        if WEB:
            # Buscar datos reales con web_bridge
            datos = web.buscar("datos de ejemplo")
            duracion_proceso = float(web.extraer_precios(datos, "duracion_proceso"))
            frecuencia_produccion = float(web.extraer_precios(datos, "frecuencia_produccion"))
        else:
            # Permite parametros por sys.argv
            if len(sys.argv) == 3:
                duracion_proceso = float(sys.argv[1])
                frecuencia_produccion = float(sys.argv[2])
            else:
                print("Error: Faltan argumentos. Utilice: python calculadora_takt_time.py <duracion_proceso> <frecuencia_produccion>")
                return

        # Agrega casos edge
        try:
            if duracion_proceso <= 0:
                raise ValueError("Duración del proceso no puede ser cero o negativo.")
            if frecuencia_produccion <= 0:
                raise ValueError("Frecuencia de producción no puede ser cero o negativo.")
            if duracion_proceso == 0:
                raise ValueError("Duración del proceso no puede ser cero.")
            if frecuencia_produccion == 0:
                raise ValueError("Frecuencia de producción no puede ser cero.")
            if frecuencia_produccion > 1000:
                raise ValueError("Frecuencia de producción no puede ser mayor a 1000 unidades por hora.")
            if duracion_proceso > 1000:
                raise ValueError("Duración del proceso no puede ser mayor a 1000 minutos.")
        except ValueError as e:
            print(f"Error: {e}")
            return

        takt_time = calcular_takt_time(duracion_proceso, frecuencia_produccion)
        takt_time_mexico = calcular_takt_time_mexico(duracion_proceso, frecuencia_produccion)

        print(f"Tiempo takt (tasa de producción) en minutos: {takt_time:.2f}")
        print(f"Tiempo takt (tasa de producción) en minutos para México: {takt_time_mexico:.2f}")
        print(f"Frecuencia de producción en unidades por hora: {frecuencia_produccion:.2f}")
        print(f"Duración del proceso en minutos: {duracion_proceso:.2f}")
        print(f"Resumen ejecutivo: El tiempo takt es un indicador importante para la producción. En este caso, el tiempo takt es de {takt_time:.2f} minutos y para México es de {takt_time_mexico:.2f} minutos.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()