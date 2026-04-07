#!/usr/bin/env python3

"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza analizador tiempos respuesta
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
from datetime import datetime
import math
import re
import random

def extraer_precios(precio_dolar=20.50, precio_euro=23.25, precio_pesos=1.0):
    return {"dólar": precio_dolar, "euro": precio_euro, "pesos": precio_pesos}

def buscar_tiempos_respuesta():
    try:
        with open("tiempos_respuesta.txt", "r") as archivo:
            return [linea.strip() for linea in archivo.readlines()]
    except FileNotFoundError:
        return ["10 ms", "20 ms", "30 ms"]
    except Exception as e:
        print(f"Error al leer archivo: {e}")
        return []

def analizar_tiempos_respuesta(precio_dolar=20.50, precio_euro=23.25, precio_pesos=1.0):
    tiempos_respuesta = buscar_tiempos_respuesta()
    precios = extraer_precios(precio_dolar, precio_euro, precio_pesos)
    total = 0
    tiempos_menores_20 = 0
    tiempos_mayores_50 = 0
    tiempos_promedio = []
    tiempos_maximos = {}
    tiempos_minimos = {}
    for tiempo in tiempos_respuesta:
        try:
            tiempo_ms = float(re.search(r"(\d+)", tiempo).group())
            total += tiempo_ms
            tiempos_promedio.append(tiempo_ms)
            tiempos_maximos[tiempo_ms] = tiempos_maximos.get(tiempo_ms, 0) + 1
            tiempos_minimos[tiempo_ms] = tiempos_minimos.get(tiempo_ms, 0) + 1
            if tiempo_ms < 20:
                tiempos_menores_20 += 1
            elif tiempo_ms > 50:
                tiempos_mayores_50 += 1
        except AttributeError:
            print(f"Error al parsear tiempo de respuesta: {tiempo}")
        except ValueError:
            print(f"Error al convertir tiempo de respuesta a float: {tiempo}")
    if tiempos_respuesta:
        promedio = total / len(tiempos_respuesta)
        porcentaje_menores_20 = (tiempos_menores_20 / len(tiempos_respuesta)) * 100
        porcentaje_mayores_50 = (tiempos_mayores_50 / len(tiempos_respuesta)) * 100
        tiempos_maximos = sorted(tiempos_maximos.items(), key=lambda x: x[0], reverse=True)
        tiempos_minimos = sorted(tiempos_minimos.items(), key=lambda x: x[0])
        print(f"Promedio de tiempos de respuesta: {promedio:.2f} ms")
        print(f"Porcentaje de tiempos menores a 20 ms: {porcentaje_menores_20:.2f}%")
        print(f"Porcentaje de tiempos mayores a 50 ms: {porcentaje_mayores_50:.2f}%")
        print(f"Tiempos máximos: {tiempos_maximos}")
        print(f"Tiempos mínimos: {tiempos_minimos}")
        print(f"Resumen ejecutivo: El análisis de tiempos de respuesta muestra que el promedio es de {promedio:.2f} ms, con un porcentaje de tiempos menores a 20 ms de {porcentaje_menores_20:.2f}% y un porcentaje de tiempos mayores a 50 ms de {porcentaje_mayores_50:.2f}%.")

def main():
    if len(sys.argv) > 1:
        precio_dolar = float(sys.argv[1])
        precio_euro = float(sys.argv[2])
        precio_pesos = float(sys.argv[3])
    else:
        precio_dolar = 20.50
        precio_euro = 23.25
        precio_pesos = 1.0
    analizar_tiempos_respuesta(precio_dolar, precio_euro, precio_pesos)

if __name__ == "__main__":
    main()