"""
ÁREA: TURISMO
DESCRIPCIÓN: Agente que realiza generador guia destino
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generador_guia_destino(monto_inicial, tipo_cambio, destino):
    """
    Genera un guía de destino con información sobre un viaje a México.

    Args:
        monto_inicial (float): El monto inicial para el viaje.
        tipo_cambio (float): El tipo de cambio actual.
        destino (str): El destino del viaje.

    Returns:
        dict: Un diccionario con información sobre el viaje.
    """
    try:
        # Busca información sobre el destino en la web (simulación)
        info_destino = {
            "nombre": "México",
            "descripcion": "Un país con una rica historia y cultura",
            "atracciones": ["Chichén Itzá", "Teotihuacán", "Cancún"],
            "ciudades": ["Ciudad de México", "Guadalajara", "Monterrey"],
            "comida": ["Tacos al pastor", "Chiles rellenos", "Sopes"],
            "festivales": ["Día de Muertos", "Navidad", "Festival de Jazz"]
        }
        precios = {
            "alojamiento": 500.0,
            "comida": 300.0,
            "transporte": 200.0,
            "actividades": 400.0
        }
        tipo_cambio_actual = tipo_cambio  # uso el tipo de cambio proporcionado

        # Calcula el monto total para el viaje
        monto_total = monto_inicial * tipo_cambio_actual * 1.1  # incluye un 10% de impuestos
        impuestos = monto_total * 0.1
        gastos_adicionales = 100.0  # gastos adicionales para el viaje
        monto_total += gastos_adicionales

        # Genera un guía de destino con información sobre el viaje
        guia_destino = {
            "monto_inicial": monto_inicial,
            "tipo_cambio": tipo_cambio,
            "destino": destino,
            "info_destino": info_destino,
            "precios": precios,
            "tipo_cambio_actual": tipo_cambio_actual,
            "monto_total": monto_total,
            "impuestos": impuestos,
            "gastos_adicionales": gastos_adicionales,
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d")
        }

        return guia_destino

    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    if len(sys.argv) != 4:
        print("Uso: python generador_guia_destino.py <monto_inicial> <tipo_cambio> <destino>")
        sys.exit(1)

    monto_inicial = float(sys.argv[1])
    tipo_cambio = float(sys.argv[2])
    destino = sys.argv[3]

    guia_destino = generador_guia_destino(monto_inicial, tipo_cambio, destino)

    if guia_destino:
        print("Resumen Ejecutivo:")
        print(f"Monto Inicial: ${guia_destino['monto_inicial']:.2f}")
        print(f"Tipo de Cambio: ${guia_destino['tipo_cambio']:.2f}")
        print(f"Destino: {guia_destino['destino']}")
        print(f"Monto Total: ${guia_destino['monto_total']:.2f}")
        print(f"Fecha: {guia_destino['fecha']}")
        print("Información del Destino:")
        print(f"Nombre: {guia_destino['info_destino']['nombre']}")
        print(f"Descripción: {guia_destino['info_destino']['descripcion']}")
        print("Precios:")
        for precio, valor in guia_destino['precios'].items():
            print(f"{precio}: ${valor:.2f}")
        print(f"Tipo de Cambio Actual: ${guia_destino['tipo_cambio_actual']:.2f}")
        print(f"Impuestos: ${guia_destino['impuestos']:.2f}")
        print(f"Gastos Adicionales: ${guia_destino['gastos_adicionales']:.2f}")

if __name__ == "__main__":
    main()