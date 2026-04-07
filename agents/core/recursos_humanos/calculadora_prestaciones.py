#!/usr/bin/env python3
# AREA: FINANZAS
# DESCRIPCION: Agente que realiza calculadora prestaciones
# TECNOLOGIA: Python estándar

import sys
import json
import datetime
import math
import re
import random
import os

def calcular_prestaciones(salario_diario, dias_trabajados, antiguedad):
    if salario_diario <= 0 or dias_trabajados <= 0 or antiguedad <= 0:
        raise ValueError("Valores deben ser mayores a cero")

    prestaciones = {}
    prestaciones['aguinaldo'] = salario_diario * 15
    prestaciones['vacaciones'] = salario_diario * 15
    prestaciones['prima_vacacional'] = salario_diario * 5
    prestaciones['total'] = prestaciones['aguinaldo'] + prestaciones['vacaciones'] + prestaciones['prima_vacacional']

    # Calculo de prestaciones adicionales
    prestaciones['prestacion_1'] = salario_diario * 10
    prestaciones['prestacion_2'] = salario_diario * 20
    prestaciones['prestacion_3'] = salario_diario * (antiguedad / 10)

    return prestaciones

def calcular_imss(salario_diario):
    if salario_diario <= 0:
        raise ValueError("Salario diario debe ser mayor a cero")

    imss = {}
    imss['cuota_fija'] = salario_diario * 0.05
    imss['cuota_variable'] = salario_diario * 0.015
    imss['total'] = imss['cuota_fija'] + imss['cuota_variable']

    return imss

def calcular_infonavit(salario_diario):
    if salario_diario <= 0:
        raise ValueError("Salario diario debe ser mayor a cero")

    infonavit = {}
    infonavit['cuota_fija'] = salario_diario * 0.05
    infonavit['total'] = infonavit['cuota_fija']

    return infonavit

def main():
    try:
        if len(sys.argv) == 4:
            salario_diario = float(sys.argv[1])
            dias_trabajados = int(sys.argv[2])
            antiguedad = int(sys.argv[3])
        else:
            salario_diario = 500  # valor ejemplo
            dias_trabajados = 365  # valor ejemplo
            antiguedad = 5  # valor ejemplo

        prestaciones = calcular_prestaciones(salario_diario, dias_trabajados, antiguedad)
        imss = calcular_imss(salario_diario)
        infonavit = calcular_infonavit(salario_diario)

        print("Prestaciones:")
        print(f"Aguinaldo: ${prestaciones['aguinaldo']:.2f}")
        print(f"Vacaciones: ${prestaciones['vacaciones']:.2f}")
        print(f"Prima vacacional: ${prestaciones['prima_vacacional']:.2f}")
        print(f"Prestacion 1: ${prestaciones['prestacion_1']:.2f}")
        print(f"Prestacion 2: ${prestaciones['prestacion_2']:.2f}")
        print(f"Prestacion 3: ${prestaciones['prestacion_3']:.2f}")
        print(f"Total: ${prestaciones['total']:.2f}")

        print("\nIMSS:")
        print(f"Cuota fija: ${imss['cuota_fija']:.2f}")
        print(f"Cuota variable: ${imss['cuota_variable']:.2f}")
        print(f"Total: ${imss['total']:.2f}")

        print("\nInfonavit:")
        print(f"Cuota fija: ${infonavit['cuota_fija']:.2f}")
        print(f"Total: ${infonavit['total']:.2f}")

        print("\nResumen ejecutivo:")
        print(f"Salario diario: ${salario_diario:.2f}")
        print(f"Dias trabajados: {dias_trabajados}")
        print(f"Antiguedad: {antiguedad} años")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()