"""
ÁREA: LOGISTICA
DESCRIPCIÓN: Agente que realiza optimizador rutas entrega
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def calcular_distancia(lat1, lon1, lat2, lon2):
    radio_tierra = 6371  # en kilómetros
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distancia = radio_tierra * c
    return distancia

def optimizar_ruta(puntos_de_entrega):
    ruta_optima = []
    punto_actual = puntos_de_entrega[0]
    ruta_optima.append(punto_actual)
    puntos_de_entrega.remove(punto_actual)
    
    while puntos_de_entrega:
        punto_mas_cercano = None
        distancia_minima = float('inf')
        for punto in puntos_de_entrega:
            distancia = calcular_distancia(punto_actual[0], punto_actual[1], punto[0], punto[1])
            if distancia < distancia_minima:
                distancia_minima = distancia
                punto_mas_cercano = punto
        ruta_optima.append(punto_mas_cercano)
        punto_actual = punto_mas_cercano
        puntos_de_entrega.remove(punto_mas_cercano)
    
    return ruta_optima

def extraer_puntos_de_entrega():
    try:
        if len(sys.argv) > 1:
            puntos_de_entrega = []
            for i in range(1, len(sys.argv)):
                punto = tuple(map(float, sys.argv[i].split(',')))
                puntos_de_entrega.append(punto)
            return puntos_de_entrega
        else:
            return [
                (19.4326, -99.1332),  # Ciudad de México
                (20.6667, -103.3333),  # Guadalajara
                (25.6667, -100.3333),  # Monterrey
                (19.1667, -96.1333),  # Veracruz
                (22.2333, -97.8667),  # Tampico
                (16.7333, -99.1333),  # Puebla
                (21.0667, -102.3333),  # León
                (17.1667, -92.6333),  # Tabasco
                (24.6667, -103.3333),  # San Luis Potosí
                (18.6667, -98.3333)  # Querétaro
            ]
    except ValueError:
        print("Error: formato de punto de entrega inválido")
        return []

def imprimir_ruta(ruta_optima):
    print("Ruta óptima:")
    for i, punto in enumerate(ruta_optima):
        print(f"Punto {i+1}: ({punto[0]}, {punto[1]})")

def calcular_distancia_total(ruta_optima):
    distancia_total = 0
    for i in range(len(ruta_optima) - 1):
        punto_actual = ruta_optima[i]
        punto_siguiente = ruta_optima[i + 1]
        distancia = calcular_distancia(punto_actual[0], punto_actual[1], punto_siguiente[0], punto_siguiente[1])
        distancia_total += distancia
    return distancia_total

def imprimir_resumen_ejecutivo(ruta_optima, distancia_total):
    print(f"\nResumen ejecutivo:")
    print(f"Distancia total: {distancia_total:.2f} km")
    print(f"Número de puntos de entrega: {len(ruta_optima)}")

def main():
    puntos_de_entrega = extraer_puntos_de_entrega()
    if puntos_de_entrega:
        ruta_optima = optimizar_ruta(puntos_de_entrega)
        imprimir_ruta(ruta_optima)
        distancia_total = calcular_distancia_total(ruta_optima)
        imprimir_resumen_ejecutivo(ruta_optima, distancia_total)
    else:
        print("No se pudieron obtener puntos de entrega")

if __name__ == "__main__":
    main()