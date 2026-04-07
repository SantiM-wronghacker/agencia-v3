"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza generador reporte automatico
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
    WEB = web.WEB  # True si hay conexion
except ImportError:
    WEB = False

def extraer_precios(fecha='2024-03-01'):
    if WEB:
        return web.extraer_precios()
    else:
        return {
            "dólar": 20.50 + (random.uniform(-0.1, 0.1) * 20.50),  # Simula fluctuación
            "euro": 22.75 + (random.uniform(-0.1, 0.1) * 22.75),  # Simula fluctuación
            "peso": 1 / (extraer_precios()["dólar"] / 20.50),  # Simula tipo de cambio
        }

def buscar_datos():
    if WEB:
        return web.buscar()
    else:
        return {
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d"),
            "temperatura": 25.5 + (random.uniform(-0.1, 0.1) * 25.5),  # Simula fluctuación
            "humedad": 60 + (random.uniform(-0.1, 0.1) * 60),  # Simula fluctuación
            "viento": 10 + (random.uniform(-0.1, 0.1) * 10),  # Simula fluctuación
            "presion_atmosferica": 1013 + (random.uniform(-0.1, 0.1) * 1013),  # Simula fluctuación
            "radiacion_uv": 5 + (random.uniform(-0.1, 0.1) * 5),  # Simula fluctuación
        }

def fetch_texto():
    if WEB:
        return web.fetch_texto()
    else:
        return "Texto de ejemplo"

def calcular_inflacion(precio_dolar, temperatura, humedad, presion_atmosferica):
    # Simula un cálculo de inflación más realista para México
    return (precio_dolar * 0.1) + (temperatura * 0.05) - (humedad * 0.01) + (presion_atmosferica * 0.001)

def main():
    try:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d")
        temperatura = buscar_datos()["temperatura"]
        precio_dolar = extraer_precios()["dólar"]
        texto = fetch_texto()
        humedad = buscar_datos()["humedad"]
        viento = buscar_datos()["viento"]
        presion_atmosferica = buscar_datos()["presion_atmosferica"]
        radiacion_uv = buscar_datos()["radiacion_uv"]
        inflacion = calcular_inflacion(precio_dolar, temperatura, humedad, presion_atmosferica)
        print(f"Fecha: {fecha}")
        print(f"Temperatura: {temperatura}°C")
        print(f"Humedad: {humedad}%")
        print(f"Viento: {viento} km/h")
        print(f"Precio del dólar: {precio_dolar} MXN")
        print(f"Presión atmosférica: {presion_atmosferica} mbar")
        print(f"Radiación UV: {radiacion_uv} índice")
        print(f"Inflación: {inflacion}%")
        print(f"Texto: {texto}")
        print("Resumen ejecutivo:")
        print(f"La temperatura y la humedad actuales son {temperatura}°C y {humedad}%, respectivamente.")
        print(f"El precio del dólar es {precio_dolar} MXN y la inflación es {inflacion}%.")
        print(f"Se recomienda tomar medidas para protegerse de la radiación UV con un índice de {radiacion_uv}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fecha = sys.argv[1]
    else:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    main()