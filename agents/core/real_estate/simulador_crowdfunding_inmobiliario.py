#!/usr/bin/env python3

"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza simulador crowdfunding inmobiliario
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_interes_inmobiliario(inversion, plazo, tasa):
    return inversion * (tasa / 100) * math.pow((1 + tasa/100), plazo/12) - inversion

def calcular_pago_mensual_inmobiliario(inversion, plazo, tasa):
    return (inversion * (tasa / 100) * math.pow((1 + tasa/100), plazo/12)) / plazo + (inversion / plazo)

def calcular_pago_total_inmobiliario(inversion, plazo, tasa):
    return inversion + calcular_interes_inmobiliario(inversion, plazo, tasa)

def calcular_tasa_efectiva_inmobiliario(tasa):
    return math.pow((1 + tasa/100), 12) - 1

def calcular_tasa_efectiva_anual_inmobiliario(tasa):
    return tasa * math.pow((1 + tasa/100), 12)

def calcular_pago_total_anual_inmobiliario(inversion, plazo, tasa):
    return calcular_pago_total_inmobiliario(inversion, plazo, tasa) * 12

def main():
    try:
        inversion = float(sys.argv[1]) if len(sys.argv) > 1 else 500000.0  # Inversión promedio en México
        plazo = int(sys.argv[2]) if len(sys.argv) > 2 else 24  # Plazo promedio en México
        tasa = float(sys.argv[3]) if len(sys.argv) > 3 else 12.0  # Tasa de interés promedio en México

        if plazo <= 0:
            raise ValueError("El plazo debe ser mayor que cero")
        if tasa < 0:
            raise ValueError("La tasa de interés no puede ser negativa")
        if inversion <= 0:
            raise ValueError("La inversión debe ser mayor que cero")

        interes_inmobiliario = calcular_interes_inmobiliario(inversion, plazo, tasa)
        pago_mensual_inmobiliario = calcular_pago_mensual_inmobiliario(inversion, plazo, tasa)
        pago_total_inmobiliario = calcular_pago_total_inmobiliario(inversion, plazo, tasa)
        tasa_efectiva_inmobiliario = calcular_tasa_efectiva_inmobiliario(tasa)
        tasa_efectiva_anual_inmobiliario = calcular_tasa_efectiva_anual_inmobiliario(tasa)
        pago_total_anual_inmobiliario = calcular_pago_total_anual_inmobiliario(inversion, plazo, tasa)

        print(f"{'-' * 50}")
        print(f"{'Simulador Crowdfunding Inmobiliario':^50}")
        print(f"{'-' * 50}")
        print(f"Inversión: {inversion:.2f}")
        print(f"Plazo: {plazo} meses")
        print(f"Tasa de interés: {tasa:.2f}%")
        print(f"Interés inmobiliario: {interes_inmobiliario:.2f}")
        print(f"Pago mensual: {pago_mensual_inmobiliario:.2f}")
        print(f"Pago total: {pago_total_inmobiliario:.2f}")
        print(f"Tasa efectiva anual: {tasa_efectiva_anual_inmobiliario:.2f}%")
        print(f"Pago total anual: {pago_total_anual_inmobiliario:.2f}")
        print(f"{'-' * 50}")
        print(f"Resumen ejecutivo:")
        print(f"El simulador crowdfunding inmobiliario calcula que con una inversión de {inversion:.2f}, un plazo de {plazo} meses y una tasa de interés de {tasa:.2f}%, el pago total anual será de {pago_total_anual_inmobiliario:.2f}.")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()