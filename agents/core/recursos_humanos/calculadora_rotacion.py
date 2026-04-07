"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora rotacion
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def calculadora_rotacion(salario, dias_trabajados, tasa_rotacion, precio_peso_dolar):
    """
    Calcula la rotación de un empleado en un período determinado.

    Args:
        salario (float): Salario del empleado.
        dias_trabajados (int): Número de días trabajados en el período.
        tasa_rotacion (float): Tasa de rotación del empleado.
        precio_peso_dolar (float): Precio del peso mexicano al dolar.

    Returns:
        float: Rotación del empleado en el período.
    """
    if salario <= 0:
        raise ValueError("El salario debe ser mayor que 0")
    if dias_trabajados <= 0:
        raise ValueError("Los días trabajados deben ser mayores que 0")
    if tasa_rotacion <= 0:
        raise ValueError("La tasa de rotación debe ser mayor que 0")
    if precio_peso_dolar <= 0:
        raise ValueError("El precio del peso mexicano al dolar debe ser mayor que 0")

    rotacion = (salario / dias_trabajados) * tasa_rotacion
    return rotacion

def calcular_salario_diario(salario, dias_trabajados):
    """
    Calcula el salario diario del empleado.

    Args:
        salario (float): Salario del empleado.
        dias_trabajados (int): Número de días trabajados en el período.

    Returns:
        float: Salario diario del empleado.
    """
    return salario / dias_trabajados

def calcular_impuesto(salario_diario, tasa_impuesto):
    """
    Calcula el impuesto sobre el salario diario.

    Args:
        salario_diario (float): Salario diario del empleado.
        tasa_impuesto (float): Tasa de impuesto.

    Returns:
        float: Impuesto sobre el salario diario.
    """
    return salario_diario * tasa_impuesto

def main():
    try:
        if len(sys.argv) != 6:
            print("Error: Faltan argumentos")
            print("Uso: python calculadora_rotacion.py <salario> <dias_trabajados> <tasa_rotacion> <precio_peso_dolar> <tasa_impuesto>")
            sys.exit(1)

        salario = float(sys.argv[1])
        dias_trabajados = int(sys.argv[2])
        tasa_rotacion = float(sys.argv[3])
        precio_peso_dolar = float(sys.argv[4])
        tasa_impuesto = float(sys.argv[5])

        rotacion = calculadora_rotacion(salario, dias_trabajados, tasa_rotacion, precio_peso_dolar)
        salario_diario = calcular_salario_diario(salario, dias_trabajados)
        impuesto = calcular_impuesto(salario_diario, tasa_impuesto)

        print(f"ÁREA: FINANZAS")
        print(f"DESCRIPCIÓN: Agente que realiza calculadora rotacion")
        print(f"TECNOLOGÍA: Python estándar")
        print(f"Rotación del empleado: {rotacion:.2f} MXN")
        print(f"Precio del peso mexicano al dolar: {precio_peso_dolar:.2f} USD")
        print(f"Salario diario: {salario_diario:.2f} MXN")
        print(f"Impuesto sobre el salario diario: {impuesto:.2f} MXN")
        print(f"Resumen ejecutivo: La rotación del empleado es de {rotacion:.2f} MXN y el salario diario es de {salario_diario:.2f} MXN.")
        print(f"La tasa de impuesto es de {tasa_impuesto*100:.2f}% y el impuesto sobre el salario diario es de {impuesto:.2f} MXN.")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()