"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza evaluador desempeno
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios(tipo_cambio_dolar, tipo_cambio_euro):
    return {
        "dólar": tipo_cambio_dolar,
        "euro": tipo_cambio_euro,
        "peso": 1.00
    }

def calcular_desempeno(empleados, ventas, producción):
    try:
        desempeno = (ventas + producción) / empleados
        return desempeno
    except ZeroDivisionError:
        return 0

def calcular_porcentaje_de_cambio(desempeno_anterior, desempeno_actual):
    try:
        return ((desempeno_actual - desempeno_anterior) / desempeno_anterior) * 100
    except ZeroDivisionError:
        return 0

def calcular_tasa_de_crecimiento(ventas_anteriores, ventas_actuales):
    try:
        return ((ventas_actuales - ventas_anteriores) / ventas_anteriores) * 100
    except ZeroDivisionError:
        return 0

def calcular_indicadores_de_desempeno(empleados, ventas, producción):
    desempeno = calcular_desempeno(empleados, ventas, producción)
    ventas_por_empleado = ventas / empleados
    producción_por_empleado = producción / empleados
    utilidad_bruta = ventas - producción
    margen_utilidad = (utilidad_bruta / ventas) * 100
    return {
        "desempeno": desempeno,
        "ventas_por_empleado": ventas_por_empleado,
        "producción_por_empleado": producción_por_empleado,
        "utilidad_bruta": utilidad_bruta,
        "margen_utilidad": margen_utilidad
    }

def main():
    try:
        if len(sys.argv) > 1:
            tipo_cambio_dolar = float(sys.argv[1])
            tipo_cambio_euro = float(sys.argv[2])
            empleados = int(sys.argv[3])
            ventas = float(sys.argv[4])
            producción = float(sys.argv[5])
        else:
            tipo_cambio_dolar = 20.50
            tipo_cambio_euro = 23.20
            empleados = 100
            ventas = 5000000
            producción = 200000

        precios = extraer_precios(tipo_cambio_dolar, tipo_cambio_euro)
        indicadores = calcular_indicadores_de_desempeno(empleados, ventas, producción)

        print(f"Fecha de evaluación: {datetime.date.today()}")
        print(f"Tipo de cambio dólar: {precios['dólar']}")
        print(f"Tipo de cambio euro: {precios['euro']}")
        print(f"Empleados: {empleados}")
        print(f"Ventas: {ventas}")
        print(f"Producción: {producción}")
        print(f"Desempeño: {indicadores['desempeno']}")
        print(f"Ventas por empleado: {indicadores['ventas_por_empleado']}")
        print(f"Producción por empleado: {indicadores['producción_por_empleado']}")
        print(f"Utilidad bruta: {indicadores['utilidad_bruta']}")
        print(f"Margen de utilidad: {indicadores['margen_utilidad']}%")
        print(f"Resumen ejecutivo: El desempeño de la empresa ha mejorado un {calcular_porcentaje_de_cambio(0, indicadores['desempeno'])}% en comparación con el período anterior.")
        print(f"Tasa de crecimiento de ventas: {calcular_tasa_de_crecimiento(0, ventas)}%")

    except ValueError:
        print("Error: Los valores ingresados no son numéricos.")

if __name__ == "__main__":
    main()