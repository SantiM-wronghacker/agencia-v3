"""
AREA: FINANZAS
DESCRIPCION: Agente que realiza conversor formatos datos
TECNOLOGIA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def main():
    try:
        # Conversión de temperatura
        temperatura_celsius = float(sys.argv[1]) if len(sys.argv) > 1 else 25
        temperatura_fahrenheit = temperatura_celsius * 9/5 + 32
        temperatura_kelvin = temperatura_celsius + 273.15
        temperatura_riesgo = temperatura_celsius * 1.5  # Temperatura de riesgo para salud
        temperatura_critica = temperatura_celsius * 2  # Temperatura crítica para salud
        print(f"Temperatura en Celsius: {temperatura_celsius}°C")
        print(f"Temperatura en Fahrenheit: {temperatura_fahrenheit}°F")
        print(f"Temperatura en Kelvin: {temperatura_kelvin} K")
        print(f"Diferencia entre Celsius y Fahrenheit: {(temperatura_fahrenheit - temperatura_celsius) * 5/9}°C")
        print(f"Diferencia entre Kelvin y Celsius: {temperatura_kelvin - temperatura_celsius} K")
        print(f"Temperatura de riesgo: {temperatura_riesgo}°C")
        print(f"Temperatura crítica: {temperatura_critica}°C")

        # Conversión de moneda
        cantidad_pesos = float(sys.argv[2]) if len(sys.argv) > 2 else 1000
        tipo_cambio_dolar = float(sys.argv[3]) if len(sys.argv) > 3 else 20.5
        tipo_cambio_euro = float(sys.argv[4]) if len(sys.argv) > 4 else 24.5
        cantidad_dolares = cantidad_pesos / tipo_cambio_dolar
        cantidad_euros = cantidad_pesos / tipo_cambio_euro
        cantidad_dolares_riesgo = cantidad_pesos / (tipo_cambio_dolar * 1.1)  # Tipo de cambio de riesgo
        cantidad_euros_riesgo = cantidad_pesos / (tipo_cambio_euro * 1.1)  # Tipo de cambio de riesgo
        print(f"Cantidad en Pesos Mexicanos: ${cantidad_pesos} MXN")
        print(f"Cantidad en Dólares Americanos: ${cantidad_dolares:.2f} USD")
        print(f"Cantidad en Euros: ${cantidad_euros:.2f} EUR")
        print(f"Diferencia entre Dólares y Euros: {(cantidad_euros - cantidad_dolares) * 100:.2f}%")
        print(f"Cantidad en Dólares de riesgo: ${cantidad_dolares_riesgo:.2f} USD")
        print(f"Cantidad en Euros de riesgo: ${cantidad_euros_riesgo:.2f} EUR")

        # Conversión de fecha
        fecha_actual = datetime.datetime.now()
        fecha_formateada = fecha_actual.strftime("%d/%m/%Y %H:%M:%S")
        fecha_formateada_corta = fecha_actual.strftime("%d/%m/%Y")
        fecha_formateada_ano = fecha_actual.strftime("%Y")
        print(f"Fecha Actual: {fecha_formateada}")
        print(f"Fecha Actual (corta): {fecha_formateada_corta}")
        print(f"Año actual: {fecha_formateada_ano}")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"Temperatura actual: {temperatura_celsius}°C")
        print(f"Cantidad actual en Pesos Mexicanos: ${cantidad_pesos} MXN")
        print(f"Cantidad actual en Dólares Americanos: ${cantidad_dolares:.2f} USD")
        print(f"Cantidad actual en Euros: ${cantidad_euros:.2f} EUR")
        print(f"Fecha actual: {fecha_formateada}")

    except IndexError:
        print("Error: Faltan argumentos de entrada.")
    except ValueError:
        print("Error: Los argumentos de entrada deben ser números.")

if __name__ == "__main__":
    main()