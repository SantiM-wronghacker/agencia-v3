"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora finiquito
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def calcular_finiquito(dias_trabajados, salario_diario, antiguedad):
    finiquito = dias_trabajados * salario_diario
    if antiguedad >= 5 * 365:
        finiquito *= 1.1
    return finiquito

def calcular_antiguedad(fecha_ingreso, fecha_salida):
    try:
        fecha_ingreso = datetime.datetime.strptime(fecha_ingreso, "%Y-%m-%d")
        fecha_salida = datetime.datetime.strptime(fecha_salida, "%Y-%m-%d")
        antiguedad = (fecha_salida - fecha_ingreso).days
        return antiguedad
    except ValueError:
        print("Error: Fecha ingresada no es válida.")
        return None

def calcular_salario_anual(salario_diario):
    return salario_diario * 365

def calcular_impuestos(finiquito):
    if finiquito <= 100000:
        return finiquito * 0.1
    elif finiquito <= 200000:
        return 10000 + (finiquito - 100000) * 0.15
    else:
        return 25000 + (finiquito - 200000) * 0.2

def calcular_tasa_inss(finiquito):
    if finiquito <= 100000:
        return finiquito * 0.065
    elif finiquito <= 200000:
        return 6500 + (finiquito - 100000) * 0.075
    else:
        return 10500 + (finiquito - 200000) * 0.08

def main():
    try:
        if len(sys.argv) == 5:
            dias_trabajados = int(sys.argv[1])
            salario_diario = float(sys.argv[2])
            fecha_ingreso = sys.argv[3]
            fecha_salida = sys.argv[4]
        else:
            dias_trabajados = 365
            salario_diario = 500
            fecha_ingreso = "2020-01-01"
            fecha_salida = "2022-12-31"

        antiguedad = calcular_antiguedad(fecha_ingreso, fecha_salida)
        if antiguedad is None:
            return

        finiquito = calcular_finiquito(dias_trabajados, salario_diario, antiguedad)
        salario_anual = calcular_salario_anual(salario_diario)
        impuestos = calcular_impuestos(finiquito)
        tasa_inss = calcular_tasa_inss(finiquito)
        neto = finiquito - impuestos - tasa_inss

        print("Días trabajados:", dias_trabajados)
        print("Salario diario: $", salario_diario)
        print("Salario anual: $", salario_anual)
        print("Fecha de ingreso:", fecha_ingreso)
        print("Fecha de salida:", fecha_salida)
        print("Antiguedad:", antiguedad, "días")
        print("Años de antiguedad:", antiguedad / 365)
        print("Finiquito: $", finiquito)
        print("Impuestos:", impuestos)
        print("Tasa INSS:", tasa_inss)
        print("Neto:", neto)

        print("\nResumen ejecutivo:")
        print("El empleado ha trabajado durante", antiguedad, "días, lo que equivale a", antiguedad / 365, "años.")
        print("El finiquito calculado es de $", finiquito, "y después de aplicar los impuestos y la tasa INSS, el empleado queda con un monto neto de $", neto)
    except ValueError:
        print("Error: Parámetros ingresados no son válidos.")
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()