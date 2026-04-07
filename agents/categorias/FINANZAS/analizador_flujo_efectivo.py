"""
AREA: FINANZAS
DESCRIPCION: Agente que realiza analizador flujo efectivo
TECNOLOGIA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def analizar_flujo_efectivo(ingresos, gastos, ingresos_no_monetarios, gastos_no_monetarios, tasa_inflacion, tasa_interes):
    try:
        # Calcular flujo efectivo
        flujo_efectivo_calculado = ingresos - gastos + ingresos_no_monetarios - gastos_no_monetarios

        # Calcular valor monetario equivalente
        valor_dinero = math.pow((1 + tasa_inflacion), 12) * (1 + tasa_interes/12)
        valor_monetario_equivalente = flujo_efectivo_calculado / valor_dinero

        # Calcular flujo efectivo mensual
        flujo_efectivo_mensual = flujo_efectivo_calculado / 12

        # Calcular flujo efectivo diario
        flujo_efectivo_diario = flujo_efectivo_calculado / 365

        # Calcular ahorro mensual
        ahorro_mensual = (ingresos - gastos) / 12

        # Calcular ahorro anual
        ahorro_anual = ingresos - gastos

        # Calcular ratio de ahorro
        ratio_ahorro = (ahorro_anual / ingresos) * 100

        # Mostrar resultados
        print(f"Flujo efectivo: {flujo_efectivo_calculado:.2f} MXN")
        print(f"Valor monetario equivalente: {valor_monetario_equivalente:.2f} MXN")
        print(f"Ingresos: {ingresos:.2f} MXN")
        print(f"Gastos: {gastos:.2f} MXN")
        print(f"Ingresos no monetarios: {ingresos_no_monetarios:.2f} MXN")
        print(f"Gastos no monetarios: {gastos_no_monetarios:.2f} MXN")
        print(f"Flujo efectivo mensual: {flujo_efectivo_mensual:.2f} MXN")
        print(f"Flujo efectivo diario: {flujo_efectivo_diario:.2f} MXN")
        print(f"Ahorro mensual: {ahorro_mensual:.2f} MXN")
        print(f"Ahorro anual: {ahorro_anual:.2f} MXN")
        print(f"Ratio de ahorro: {ratio_ahorro:.2f}%")
        print(f"Tasa de inflación: {tasa_inflacion:.2%}")
        print(f"Tasa de interés: {tasa_interes:.2%}")
        print(f"Fecha de análisis: {datetime.date.today()}")
        print(f"Hora de análisis: {datetime.datetime.now().strftime('%H:%M:%S')}")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El flujo efectivo calculado es de {flujo_efectivo_calculado:.2f} MXN.")
        print(f"El ahorro anual es de {ahorro_anual:.2f} MXN.")
        print(f"El ratio de ahorro es de {ratio_ahorro:.2f}%.")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    try:
        if len(sys.argv)!= 7:
            print("Uso: python analizador_flujo_efectivo.py <ingresos> <gastos> <ingresos_no_monetarios> <gastos_no_monetarios> <tasa_inflacion> <tasa_interes>")
            sys.exit(1)

        ingresos = float(sys.argv[1])
        gastos = float(sys.argv[2])
        ingresos_no_monetarios = float(sys.argv[3])
        gastos_no_monetarios = float(sys.argv[4])
        tasa_inflacion = float(sys.argv[5]) / 100
        tasa_interes = float(sys.argv[6]) / 100

        analizar_flujo_efectivo(ingresos, gastos, ingresos_no_monetarios, gastos_no_monetarios, tasa_inflacion, tasa_interes)
    except Exception as e:
        print