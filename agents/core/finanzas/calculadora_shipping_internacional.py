"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora shipping internacional
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
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def calcular_costo_peso(peso):
    """
    Calcula el costo de envío basado en el peso del paquete
    """
    costo_por_kg = 10.00  # Costo por kilogramo
    costo_envío = peso * costo_por_kg
    return costo_envío

def calcular_costo_dimensiones(largo, ancho, alto):
    """
    Calcula el costo de envío basado en las dimensiones del paquete
    """
    costo_por_dimension = 5.00  # Costo por dimensión
    costo_envío = (largo + ancho + alto) * costo_por_dimension
    return costo_envío

def calcular_costo_total(peso, largo, ancho, alto):
    """
    Calcula el costo total de envío
    """
    costo_peso = calcular_costo_peso(peso)
    costo_dimensiones = calcular_costo_dimensiones(largo, ancho, alto)
    costo_total = costo_peso + costo_dimensiones
    return costo_total

def obtener_datos_ejemplo():
    """
    Devuelve datos de ejemplo para el cálculo de costo de envío
    """
    peso = 1.5  # Peso del paquete en kilogramos
    largo = 30  # Largo del paquete en centímetros
    ancho = 20  # Ancho del paquete en centímetros
    alto = 10  # Alto del paquete en centímetros
    return peso, largo, ancho, alto

def obtener_tarifa_envio():
    """
    Devuelve la tarifa de envío actual
    """
    # Tarifa de envío actual para México
    tarifa_envio = 20.00  # Tarifa de envío por paquete
    return tarifa_envio

def calcular_costo_envio(peso, largo, ancho, alto):
    """
    Calcula el costo de envío
    """
    costo_peso = calcular_costo_peso(peso)
    costo_dimensiones = calcular_costo_dimensiones(largo, ancho, alto)
    costo_total = costo_peso + costo_dimensiones
    costo_envio = costo_total + obtener_tarifa_envio()
    return costo_envio

def main():
    if len(sys.argv) > 1:
        peso = float(sys.argv[1])
        largo = float(sys.argv[2])
        ancho = float(sys.argv[3])
        alto = float(sys.argv[4])
    else:
        peso, largo, ancho, alto = obtener_datos_ejemplo()

    try:
        if WEB:
            # Buscar datos en línea
            peso = web.buscar("peso paquete")
            largo = web.buscar("largo paquete")
            ancho = web.buscar("ancho paquete")
            alto = web.buscar("alto paquete")

        costo_envio = calcular_costo_envio(peso, largo, ancho, alto)
        print("Costo de envío:", costo_envio)
        print("Peso del paquete:", peso, "kg")
        print("Largo del paquete:", largo, "cm")
        print("Ancho del paquete:", ancho, "cm")
        print("Alto del paquete:", alto, "cm")
        print("Tarifa de envío:", obtener_tarifa_envio())
        print("Resumen ejecutivo: El costo de envío para el paquete de", peso, "kg, con dimensiones", largo, "cm x", ancho, "cm x", alto, "cm, es de", costo_envio)
    except ValueError as e:
        print("Error: ", str(e))
    except Exception as e:
        print("Error: ", str(e))

if __name__ == "__main__":
    main()