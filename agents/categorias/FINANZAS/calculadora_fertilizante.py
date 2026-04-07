"""
ÁREA: AGRICULTURA
DESCRIPCIÓN: Agente que realiza calculadora fertilizante
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def calcular_fertilizante(cantidad_plantas, tipo_suelo, tipo_fertilizante, precio_fertilizante):
    """
    Calcula la cantidad de fertilizante necesaria para una cantidad de plantas en un tipo de suelo.

    Args:
    - cantidad_plantas (int): Cantidad de plantas a fertilizar.
    - tipo_suelo (str): Tipo de suelo en el que se encuentran las plantas.
    - tipo_fertilizante (str): Tipo de fertilizante a utilizar.
    - precio_fertilizante (float): Precio del fertilizante por unidad.

    Returns:
    - float: Cantidad de fertilizante necesaria en unidades.
    """
    # Constantes para cada tipo de suelo
    suelos = {
        "suelo_1": 0.5,  # suelo con baja fertilidad
        "suelo_2": 0.8,  # suelo con moderada fertilidad
        "suelo_3": 1.2  # suelo con alta fertilidad
    }

    # Constantes para cada tipo de fertilizante
    fertilizantes = {
        "fertilizante_1": 10,  # fertilizante básico
        "fertilizante_2": 20,  # fertilizante intermedio
        "fertilizante_3": 30  # fertilizante avanzado
    }

    # Cantidad de fertilizante necesaria
    if tipo_suelo not in suelos or tipo_fertilizante not in fertilizantes:
        raise ValueError("Tipo de suelo o tipo de fertilizante no válido")

    cantidad_fertilizante = (cantidad_plantas * suelos[tipo_suelo]) / fertilizantes[tipo_fertilizante]

    # Precio total del fertilizante
    precio_total = cantidad_fertilizante * precio_fertilizante

    return cantidad_fertilizante, precio_total

def main():
    try:
        # Argumentos de entrada
        cantidad_plantas = int(sys.argv[1])
        tipo_suelo = sys.argv[2]
        tipo_fertilizante = sys.argv[3]
        precio_fertilizante = float(sys.argv[4])

        # Calcula la cantidad de fertilizante necesaria
        cantidad_fertilizante, precio_total = calcular_fertilizante(cantidad_plantas, tipo_suelo, tipo_fertilizante, precio_fertilizante)

        # Muestra los resultados
        print("Área: AGRICULTURA")
        print("Descripción: Agente que realiza calculadora fertilizante")
        print("Tecnología: Python estándar")
        print(f"Cantidad de plantas: {cantidad_plantas}")
        print(f"Tipo de suelo: {tipo_suelo}")
        print(f"Tipo de fertilizante: {tipo_fertilizante}")
        print(f"Precio del fertilizante: ${precio_fertilizante:.2f} por unidad")
        print(f"Cantidad de fertilizante necesaria: {cantidad_fertilizante:.2f} unidades")
        print(f"Precio total del fertilizante: ${precio_total:.2f}")
        print("Resumen ejecutivo: El agente calcula la cantidad de fertilizante necesaria para una cantidad de plantas en un tipo de suelo.")

    except IndexError:
        print("Error: Faltan argumentos de entrada")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()