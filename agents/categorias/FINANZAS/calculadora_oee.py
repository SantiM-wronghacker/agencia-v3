"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora OEE
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
from datetime import datetime
import math
import re
import random

def calcular_oee(produccion_teorica, produccion_real, tiempo_real, tiempo_disponible):
    """
    Calcula la eficiencia OEE (Overall Equipment Effectiveness)

    Args:
        produccion_teorica (float): Producción teórica esperada
        produccion_real (float): Producción real obtenida
        tiempo_real (float): Tiempo real empleado en la producción
        tiempo_disponible (float): Tiempo disponible para la producción

    Returns:
        float: Eficiencia OEE (0-1)
    """
    try:
        if produccion_teorica <= 0 or produccion_real <= 0 or tiempo_real <= 0 or tiempo_disponible <= 0:
            raise ValueError("Todos los valores deben ser positivos")
        disponibilidad = (tiempo_real / tiempo_disponible) * 100
        calidad = (produccion_real / produccion_teorica) * 100
        rendimiento = (produccion_real / (tiempo_real * (produccion_teorica / tiempo_disponible))) * 100
        oee = (disponibilidad / 100) * (calidad / 100) * (rendimiento / 100)
        return oee, disponibilidad, calidad, rendimiento
    except ZeroDivisionError:
        print("Error: No se puede dividir por cero")
        return None, None, None, None
    except ValueError as e:
        print(f"Error: {e}")
        return None, None, None, None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None, None, None, None

def main():
    try:
        if len(sys.argv) > 4:
            produccion_teorica = float(sys.argv[1])
            produccion_real = float(sys.argv[2])
            tiempo_real = float(sys.argv[3])
            tiempo_disponible = float(sys.argv[4])
        else:
            # Datos de ejemplo
            produccion_teorica = 1000  # Unidades por hora
            produccion_real = 800  # Unidades por hora
            tiempo_real = 8  # Horas
            tiempo_disponible = 10  # Horas

        oee, disponibilidad, calidad, rendimiento = calcular_oee(produccion_teorica, produccion_real, tiempo_real, tiempo_disponible)
        print(f"Producción teórica: {produccion_teorica} unidades/hora")
        print(f"Producción real: {produccion_real} unidades/hora")
        print(f"Tiempo real: {tiempo_real} horas")
        print(f"Tiempo disponible: {tiempo_disponible} horas")
        print(f"Disponibilidad: {disponibilidad:.2f}%")
        print(f"Calidad: {calidad:.2f}%")
        print(f"Rendimiento: {rendimiento:.2f}%")
        print(f"OEE: {oee:.2f}%")
        print("Resumen ejecutivo:")
        print(f"La eficiencia OEE es de {oee:.2f}%, lo que indica que hay un margen de mejora en la producción.")
        if oee < 0.5:
            print("Se recomienda revisar los procesos de producción y mantenimiento para mejorar la eficiencia.")
        elif oee < 0.8:
            print("Se recomienda realizar ajustes en los procesos de producción y mantenimiento para mejorar la eficiencia.")
        else:
            print("La eficiencia OEE es alta, lo que indica que los procesos de producción y mantenimiento están funcionando correctamente.")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()