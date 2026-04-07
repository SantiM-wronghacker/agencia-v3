# ÁREA: FINANZAS
# DESCRIPCIÓN: Agente que realiza calculadora ROI agro
# TECNOLOGÍA: Python estándar

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

def calcular_roi_agro(inversion, ingresos, años):
    try:
        # Calcula ROI
        roi = ((ingresos - inversion) / inversion) * 100 * años
        return roi, (ingresos - inversion), roi * inversion / 100
    except ZeroDivisionError:
        print("Error: La inversión no puede ser cero")
        sys.exit(1)
    except ValueError:
        print("Error: La inversión o los ingresos deben ser números")
        sys.exit(1)

def buscar_precios():
    # Busca datos reales en internet
    # (por ejemplo, precios de productos agrícolas)
    if WEB:
        precios = web.buscar("precios de productos agrícolas en México")
        return web.extraer_precios(precios)
    else:
        # Usa datos de ejemplo hardcodeados como fallback
        return {
            "maíz": 150000,  # Ingresos anuales en pesos mexicanos
            "trigo": 120000,
            "soya": 180000,
            "café": 200000,
            "chile": 100000,
            "frijol": 110000,
            "calabaza": 130000,
            "papaya": 160000,
            "tomate": 140000
        }

def calcular_ingresos_anuales(inversion, años, tasa_interes):
    try:
        # Calcula ingresos anuales con interés compuesto
        ingresos = inversion * (1 + tasa_interes / 100) ** años
        return ingresos
    except ValueError:
        print("Error: La tasa de interés debe ser un número")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def calcular_inversión_mínima(tipo_inversión, años, tasa_interes):
    try:
        # Calcula la inversión mínima necesaria para obtener un ROI determinado
        ingresos = inversion_calculada(tipo_inversión, años, tasa_interes)
        inversion_minima = ingresos / (1 + tasa_interes / 100) ** años
        return inversion_minima
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def inversion_calculada(tipo_inversión, años, tasa_interes):
    # Calcula la inversión necesaria para obtener un ROI determinado
    try:
        ingresos_anuales = calcular_ingresos_anuales(10000, años, tasa_interes)
        inversion = ingresos_anuales / (1 + tasa_interes / 100) ** años
        return inversion
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def main():
    if len(sys.argv) != 7:
        print("Error: Faltan argumentos. Uso: python calculadora_roi_agro.py <inversión> <tasa_interes> <años> <tipo_inversión> <tipo_interés> <modo_calculo>")
        sys.exit(1)

    inversion = float(sys.argv[1])
    tasa_interes = float(sys.argv[2])
    años = int(sys.argv[3])
    tipo_inversión = sys.argv[4]
    tipo_interés = sys.argv[5]
    modo_calculo = sys.argv[6]

    if inversion <= 0 or tasa_interes <= 0 or años <= 0:
        print("Error: Valores deben ser positivos")
        sys.exit(1)

    # Busca precios de productos agrícolas
    precios = buscar_precios()

    # Calcula ROI
    roi, diferencia, ingresos = calcular_roi_agro(inversion, precios[tipo_inversión], años)

    # Calcula ingresos anuales
    ingresos_anuales = calcular_ingresos_anuales(inversion, años, tasa_interes)

    # Calcula inversión mínima
    inversion_minima = calcular_inversión_mínima(tipo_inversión, años, tasa_interes)