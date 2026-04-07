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
        valor_dinero = math.pow((1 + tasa_inflacion/100), 12) * (1 + (tasa_interes/100)/12)
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
        print(f"Tasa de inflación: {tasa_inflacion:.2f}%")
        print(f"Tasa de interés: {tasa_interes:.2f}%")
        print(f"Fecha de cálculo: {datetime.date.today()}")
        print(f"Resumen ejecutivo: El flujo efectivo es de {flujo_efectivo_calculado:.2f} MXN, lo que significa que la persona tiene un excedente de {flujo_efectivo_calculado - (ingresos - gastos):.2f} MXN al mes.")
        print(f"Resumen ejecutivo: El ratio de ahorro es de {ratio_ahorro:.2f}%, lo que significa que la persona ahorra {ratio_ahorro:.2f}% de sus ingresos.")

    except ZeroDivisionError:
        print("Error: No se puede dividir por cero.")
    except ValueError:
        print("Error: Valor no válido.")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Error: Faltan argumentos.")
        sys.exit(1)

    try:
        ingresos = float(sys.argv[1])
        gastos = float(sys.argv[2])
        ingresos_no_monetarios = float(sys.argv[3])
        gastos_no_monetarios = float(sys.argv[4])
        tasa_inflacion = float(sys.argv[5])
        tasa_interes = float(sys.argv[6])
    except ValueError:
        print("Error: Valor no válido.")
        sys.exit(1)

    analizar_flujo_efectivo(ingresos, gastos, ingresos_no_monetarios, gastos_no_monetarios, tasa_inflacion, tasa_interes)