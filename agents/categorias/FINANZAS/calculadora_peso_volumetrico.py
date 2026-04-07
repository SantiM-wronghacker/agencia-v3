# ÁREA: FINANZAS
# DESCRIPCIÓN: Agente que realiza calculadora peso volumétrico
# TECNOLOGÍA: Python estándar

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

def calcular_peso_volumetrico(largo, ancho, alto, densidad):
    """
    Calcula el peso volumétrico de un paquete.

    Args:
        largo (float): Largo del paquete en metros.
        ancho (float): Ancho del paquete en metros.
        alto (float): Alto del paquete en metros.
        densidad (float): Densidad del paquete en kg/m^3.

    Returns:
        float: Peso volumétrico del paquete en kilogramos.
    """
    volumen = largo * ancho * alto
    peso = volumen * densidad
    return peso

def calcular_densidad_realista(material):
    # Densidades aproximadas de materiales comunes en México
    densidades = {
        "madera": 0.5,
        "plástico": 0.9,
        "metal": 7.9,
        "vidrio": 2.5,
        "papel": 0.8,
        "cartón": 0.2,
        "textil": 0.05,
        "cerámica": 2.5
    }
    return densidades.get(material, 0)

def calcular_peso_maximo_paquete():
    # Peso máximo permitido por la ley mexicana es de 50 kg
    return 50

def calcular_costo_envío(peso, distancia):
    # Costo de envío aproximado en México (en pesos)
    costo_envío = peso * distancia * 0.1
    return costo_envío

def main():
    try:
        if WEB:
            # Buscar datos reales con web_bridge
            # (precios, tipo de cambio, noticias, cotizaciones)
            pass
        else:
            # Permitir parámetros por sys.argv
            largo = float(sys.argv[1]) if len(sys.argv) > 1 else 1.5  # metros
            ancho = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5  # metros
            alto = float(sys.argv[3]) if len(sys.argv) > 3 else 0.2  # metros
            densidad = float(sys.argv[4]) if len(sys.argv) > 4 else 50  # kg/m^3
            material = sys.argv[5] if len(sys.argv) > 5 else "madera"
            distancia = float(sys.argv[6]) if len(sys.argv) > 6 else 100  # km

        peso = calcular_peso_volumetrico(largo, ancho, alto, calcular_densidad_realista(material))
        peso_maximo = calcular_peso_maximo_paquete()
        if peso > peso_maximo:
            print(f"El peso del paquete ({peso:.2f} kg) excede el peso máximo permitido ({peso_maximo} kg)")
        costo_envío = calcular_costo_envío(peso, distancia)
        print(f"Peso volumétrico: {peso:.2f} kg")
        print(f"Densidad realista: {calcular_densidad_realista(material):.2f} kg/m^3")
        print(f"Largo: {largo:.2f} m")
        print(f"Ancho: {ancho:.2f} m")
        print(f"Alto: {alto:.2f} m")
        print(f"Distancia: {distancia:.2f} km")
        print(f"Costo de envío: {costo_envío:.2f} pesos")
        print(f"Resumen ejecutivo: El peso volumétrico del paquete es de {peso:.2f} kg, lo que representa un costo de envío de {costo_envío:.2f} pesos por una distancia de {distancia:.2f} km")

    except IndexError:
        print("Falta de parámetros")
    except ValueError:
        print("Error en la conversión de tipos de datos")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()