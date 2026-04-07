"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora tipo cambio viaje
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def calcular_tipo_cambio():
    try:
        tipo_cambio = 1.0  # Fallback si no hay conexión a internet
    except NameError:
        tipo_cambio = 1.0

    try:
        if hasattr(web_bridge, 'WEB'):  
            # Buscar tipo de cambio actual en tiempo real
            texto = web_bridge.buscar("tipo de cambio actual")
            precios = web_bridge.extraer_precios(texto)
            tipo_cambio = float(precios["tipo de cambio"])
    except Exception as e:
        print(f"Error: {e}")

    return tipo_cambio

def calcular_costo_viaje(distancia, tipo_cambio, precio_gasolina):
    try:
        costo_gasolina = distancia * precio_gasolina * tipo_cambio
        return costo_gasolina
    except Exception as e:
        print(f"Error: {e}")
        return 0.0

def calcular_costo_alimentos(distancia, precio_alimentos):
    try:
        costo_alimentos = distancia * precio_alimentos
        return costo_alimentos
    except Exception as e:
        print(f"Error: {e}")
        return 0.0

def calcular_costo_hotel(distancia, precio_hotel):
    try:
        costo_hotel = distancia * precio_hotel
        return costo_hotel
    except Exception as e:
        print(f"Error: {e}")
        return 0.0

def calcular_costo_total(distancia, tipo_cambio, precio_gasolina, precio_alimentos, precio_hotel):
    try:
        costo_gasolina = calcular_costo_viaje(distancia, tipo_cambio, precio_gasolina)
        costo_alimentos = calcular_costo_alimentos(distancia, precio_alimentos)
        costo_hotel = calcular_costo_hotel(distancia, precio_hotel)
        costo_total = costo_gasolina + costo_alimentos + costo_hotel
        return costo_total
    except Exception as e:
        print(f"Error: {e}")
        return 0.0

def main():
    if len(sys.argv) != 6:
        print("Uso: python calculadora_tipo_cambio_viaje.py <distancia> <tipo_cambio> <precio_gasolina> <precio_alimentos> <precio_hotel>")
        sys.exit(1)

    distancia = float(sys.argv[1])
    tipo_cambio = float(sys.argv[2])
    precio_gasolina = float(sys.argv[3])
    precio_alimentos = float(sys.argv[4])
    precio_hotel = float(sys.argv[5])

    # Calcular costo del viaje
    costo_gasolina = calcular_costo_viaje(distancia, tipo_cambio, precio_gasolina)
    costo_alimentos = calcular_costo_alimentos(distancia, precio_alimentos)
    costo_hotel = calcular_costo_hotel(distancia, precio_hotel)
    costo_total = calcular_costo_total(distancia, tipo_cambio, precio_gasolina, precio_alimentos, precio_hotel)

    # Imprimir resultados
    print(f"Distancia: {distancia} km")
    print(f"Tipo de cambio: {tipo_cambio}")
    print(f"Precio gasolina: {precio_gasolina}")
    print(f"Precio alimentos: {precio_alimentos}")
    print(f"Precio hotel: {precio_hotel}")
    print(f"Costo gasolina: {costo_gasolina}")
    print(f"Costo alimentos: {costo_alimentos}")
    print(f"Costo hotel: {costo_hotel}")
    print(f"Costo total: {costo_total}")

    # Resumen ejecutivo
    print("\nResumen Ejecutivo:")
    print(f"El costo total del viaje es de {costo_total} con una distancia de {distancia} km.")
    print(f"El costo de gasolina es de {costo_gasolina}, el costo de alimentos es de {costo_alimentos} y el costo de hotel es de {costo_hotel}.")
    print(f"El tipo de cambio utilizado es de {tipo_cambio} y el precio de gasolina es de {precio_gasolina}.")

if __name__ == "__main__":
    main()