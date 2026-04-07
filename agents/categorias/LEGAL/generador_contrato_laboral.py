"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza generador contrato laboral
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def calcular_salario(base, horas_trabajadas):
    return base * horas_trabajadas

def calcular_impuestos(salario):
    # Impuestos en México: 16% de ISR y 2% de IMSS
    return salario * 0.18

def calcular_bonos(salario):
    # Bonos en México: 10% del salario
    return salario * 0.10

def calcular_aguinaldo(salario):
    # Aguinaldo en México: 15 días de salario
    return salario * 0.15

def calcular_vacaciones(salario):
    # Vacaciones en México: 15 días de salario
    return salario * 0.15

def calcular_deduciones(salario):
    # Deduciones en México: 10% del salario
    return salario * 0.10

def calcular_retencion(salario):
    # Retención en México: 15% del salario
    return salario * 0.15

def calcular_salario_dolares(salario_base, tipo_cambio):
    return salario_base / tipo_cambio

def main():
    try:
        nombre = sys.argv[1] if len(sys.argv) > 1 else "Juan Pérez"
        salario_base = float(sys.argv[2]) if len(sys.argv) > 2 else 150.0
        horas_trabajadas = float(sys.argv[3]) if len(sys.argv) > 3 else 40.0
        tipo_cambio = float(sys.argv[4]) if len(sys.argv) > 4 else 20.0
        fecha_contrato = datetime.date.today()

        salario_total = calcular_salario(salario_base, horas_trabajadas)
        impuestos = calcular_impuestos(salario_total)
        bonos = calcular_bonos(salario_total)
        aguinaldo = calcular_aguinaldo(salario_total)
        vacaciones = calcular_vacaciones(salario_total)
        deduciones = calcular_deduciones(salario_total)
        retencion = calcular_retencion(salario_total)
        salario_dolares = calcular_salario_dolares(salario_base, tipo_cambio)

        print(f"ÁREA: FINANZAS")
        print(f"DESCRIPCIÓN: Agente que realiza generador contrato laboral")
        print(f"TECNOLOGÍA: Python estándar")
        print(f"Nombre: {nombre}")
        print(f"Salario base: ${salario_base:.2f} MXN")
        print(f"Horas trabajadas: {horas_trabajadas:.2f} horas")
        print(f"Salario total: ${salario_total:.2f} MXN")
        print(f"Impuestos: ${impuestos:.2f} MXN")
        print(f"Bonos: ${bonos:.2f} MXN")
        print(f"Aguinaldo: ${aguinaldo:.2f} MXN")
        print(f"Vacaciones: ${vacaciones:.2f} MXN")
        print(f"Deduciones: ${deduciones:.2f} MXN")
        print(f"Retención: ${retencion:.2f} MXN")
        print(f"Salario en dólares: ${salario_dolares:.2f} USD")
        print(f"Tipo de cambio: 1 USD = {tipo_cambio:.2f} MXN")
        print(f"Fecha de contrato: {fecha_contrato}")
        print(f"Resumen ejecutivo: El empleado {nombre} tiene un salario total de ${salario_total:.2f} MXN.")
        print(f"El empleado tiene derecho a {aguinaldo:.2f} MXN de aguinaldo y {vacaciones:.2f} MXN de vacaciones.")
        print(f"El empleado tiene una retención de {retencion:.2f} MXN y deducciones de {deduciones:.2f} MXN.")

    except IndexError:
        print("Faltan argumentos de línea de comandos.")
    except ValueError:
        print("Los argumentos de línea de comandos deben ser números.")

if __name__ == "__main__":
    main()