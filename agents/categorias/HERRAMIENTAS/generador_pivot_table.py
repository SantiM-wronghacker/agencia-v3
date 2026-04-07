#!/usr/bin/env python3
"""
ÁREA: HERRAMIENTAS
DESCRIPCION: Agente que realiza generador pivot table
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_pivot_table(fecha_inicio, fecha_fin, meses, tipo_moneda, tasa_cambio):
    try:
        # Validar fechas
        datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")
        datetime.datetime.strptime(fecha_fin, "%Y-%m-%d")
    except ValueError:
        print("Error: Fechas no válidas")
        return

    # Datos de ejemplo
    datos = {}

    # Generar pivot table
    for anio in range(int(fecha_inicio[:4]), int(fecha_fin[:4]) + 1):
        for mes in range(1, 13):
            if str(mes) in meses:
                fecha = f"{anio}-{mes:02d}"
                datos[fecha] = {str(mes): round(random.uniform(100, 500) * tasa_cambio, 2)}

    # Mostrar datos
    print("Pivot Table:")
    for fecha, valores in datos.items():
        print(f"{fecha}:")
        for mes, valor in valores.items():
            print(f"  {mes}: {valor} {tipo_moneda}")
        print(f"Total de {mes}: {sum(datos[fecha][mes] for fecha in datos if mes in datos[fecha])} {tipo_moneda}")
        print(f"Promedio de {mes}: {sum(datos[fecha][mes] for fecha in datos if mes in datos[fecha]) / len([fecha for fecha in datos if mes in datos[fecha]])} {tipo_moneda}")
        print()
        print(f"Total de {fecha}: {sum(valores.values())} {tipo_moneda}")
        print(f"Promedio de {fecha}: {sum(valores.values()) / len(valores)} {tipo_moneda}")
        print()

    # Resumen de datos por mes
    for mes in meses:
        total = sum(datos[fecha][mes] for fecha in datos if mes in datos[fecha])
        promedio = total / len([fecha for fecha in datos if mes in datos[fecha]])
        print(f"Total de {mes}: {total} {tipo_moneda}")
        print(f"Promedio de {mes}: {promedio} {tipo_moneda}")
        print()

    # Resumen de datos por anio
    for anio in range(int(fecha_inicio[:4]), int(fecha_fin[:4]) + 1):
        total = sum(sum(valores.values()) for fecha, valores in datos.items() if int(fecha[:4]) == anio)
        promedio = total / len([fecha for fecha, valores in datos.items() if int(fecha[:4]) == anio])
        print(f"Total de {anio}: {total} {tipo_moneda}")
        print(f"Promedio de {anio}: {promedio} {tipo_moneda}")
        print()

    # Resumen de datos por tipo de moneda
    total = sum(sum(valores.values()) for fecha, valores in datos.items())
    promedio = total / len(datos)
    print(f"Total de {tipo_moneda}: {total} {tipo_moneda}")
    print(f"Promedio de {tipo_moneda}: {promedio} {tipo_moneda}")
    print()

    # Resumen ejecutivo
    print("Resumen ejecutivo:")
    print(f"La moneda {tipo_moneda} ha tenido un total de {total} {tipo_moneda} durante el período de {fecha_inicio} a {fecha_fin}. El promedio diario ha sido de {promedio} {tipo_moneda}.")
    print(f"El año con mayor total ha sido {max(datos, key=lambda x: sum(datos[x].values()))} con un total de {sum(datos[max(datos, key=lambda x: sum(datos[x].values()))].values())} {tipo_moneda}.")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Error: Faltan argumentos")
        sys.exit(1)

    fecha_inicio = sys.argv[1]
    fecha_fin = sys.argv[2]
    meses = sys.argv[3].split(",")
    tipo_moneda = sys.argv[4]
    tasa_cambio = float(sys.argv[5])

    generar_pivot_table(fecha_inicio, fecha_fin, meses, tipo_moneda, tasa_cambio)