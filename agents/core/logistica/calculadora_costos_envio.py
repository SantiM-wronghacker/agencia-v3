"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora costos envio
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
from datetime import datetime
import math
import re
import random
import urllib.request

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion
except ImportError:
    WEB = False

def calcular_costos_envio(distancia, peso, tipo_envio):
    """
    Calcula el costo de envío basado en la distancia, peso y tipo de envío.

    Args:
    distancia (float): Distancia en kilómetros.
    peso (float): Peso en gramos.
    tipo_envio (str): Tipo de envío (e.g. "urgente", "estándar").

    Returns:
    float: Costo de envío en pesos mexicanos.
    """
    # Costos por kilómetro y gramo
    costo_km = 0.0125  # 12.5 centavos por kilómetro
    costo_g = 0.015  # 1.5 centavos por gramo

    # Costos adicionales por tipo de envío
    costos_adicionales = {
        "urgente": 10.0,
        "estándar": 5.0,
        "express": 20.0
    }

    # Calcula el costo de envío
    costo_envio = (distancia * costo_km) + (peso * costo_g) + costos_adicionales.get(tipo_envio, 0)

    return costo_envio

def obtener_precios_actualizados():
    """
    Obtiene los precios actualizados de envío desde una API en línea.

    Returns:
    dict: Precios actualizados en formato JSON.
    """
    if WEB:
        url = "https://api.preciosenvio.com/precios"
        try:
            response = urllib.request.urlopen(url)
            response.raise_for_status()
            precios = json.loads(response.read())
            return precios
        except Exception as e:
            print(f"Error al obtener precios actualizados: {e}")
            return {}
    else:
        # Fallback a precios de ejemplo hardcodeados
        precios = {
            "urgente": 150.0,
            "estándar": 80.0,
            "express": 120.0
        }
        return precios

def main():
    if len(sys.argv) != 4:
        print("Uso: python calculadora_costos_envio.py distancia peso tipo_envio")
        sys.exit(1)

    try:
        distancia = float(sys.argv[1])
        peso = float(sys.argv[2])
        tipo_envio = sys.argv[3]

        # Calcula el costo de envío
        costo_envio = calcular_costos_envio(distancia, peso, tipo_envio)

        # Obtiene los precios actualizados
        precios = obtener_precios_actualizados()

        # Muestra el costo de envío
        print(f"Costo de envío: {costo_envio:.2f} pesos")
        print(f"Distancia: {distancia} km")
        print(f"Peso: {peso} gramos")
        print(f"Tipo de envío: {tipo_envio}")
        print(f"Precios actuales:")
        for tipo, precio in precios.items():
            print(f"  - {tipo}: {precio:.2f} pesos")

        # Resumen ejecutivo
        print("\nResumen:")
        print(f"El costo de envío para una distancia de {distancia} km y un peso de {peso} gramos es de {costo_envio:.2f} pesos.")
        print(f"Los precios actuales para el tipo de envío {tipo_envio} son de {precios[tipo_envio]:.2f} pesos.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()