"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza generador plan rotacion cultivos
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_plan_rotacion_cultivos(cultivos=None, precios=None, tiempos_cultivo=None, tiempos_reposo=None):
    if cultivos is None:
        cultivos = ['Maíz', 'Trigo', 'Cebada', 'Soja', 'Sorgo']
    if precios is None:
        precios = [120.50, 150.25, 100.75, 180.00, 130.00]
    if tiempos_cultivo is None:
        tiempos_cultivo = [120, 90, 110, 150, 100]
    if tiempos_reposo is None:
        tiempos_reposo = [60, 90, 80, 120, 90]

    try:
        if len(sys.argv) > 1 and sys.argv[1] == 'online':
            # Buscar precios en tiempo real
            precios = [120.50, 150.25, 100.75, 180.00, 130.00]  # Reemplazar con llamada a API
            # Buscar tiempos de cultivo y reposo en tiempo real
            tiempos_cultivo = [120, 90, 110, 150, 100]  # Reemplazar con llamada a API
            tiempos_reposo = [60, 90, 80, 120, 90]  # Reemplazar con llamada a API
    except Exception as e:
        print(f"Error: {e}")

    plan = []
    for i in range(len(cultivos)):
        plan.append({
            'cultivo': cultivos[i],
            'precio': precios[i],
            'tiempo_cultivo': tiempos_cultivo[i],
            'tiempo_reposo': tiempos_reposo[i],
            'fecha_siembra': datetime.date.today() + datetime.timedelta(days=tiempos_cultivo[i]),
            'fecha_cosecha': datetime.date.today() + datetime.timedelta(days=tiempos_cultivo[i] + tiempos_reposo[i]),
            'rendimiento': random.uniform(100, 200)  # Rendimiento promedio en kg/ha
        })

    return plan

def main():
    try:
        if len(sys.argv) > 1:
            cultivos = sys.argv[1].split(',')
            precios = [float(x) for x in sys.argv[2].split(',')]
            tiempos_cultivo = [int(x) for x in sys.argv[3].split(',')]
            tiempos_reposo = [int(x) for x in sys.argv[4].split(',')]
        else:
            cultivos = None
            precios = None

        plan = generar_plan_rotacion_cultivos(cultivos, precios, tiempos_cultivo, tiempos_reposo)

        print("Plan de rotación de cultivos:")
        print("--------------------------------")
        print("Cultivo\tPrecio\tTiempo de cultivo\tTiempo de reposo\tFecha de siembra\tFecha de cosecha\tRendimiento")
        print("--------------------------------")
        for i in range(len(plan)):
            print(f"{plan[i]['cultivo']}\t{plan[i]['precio']}\t{plan[i]['tiempo_cultivo']}\t{plan[i]['tiempo_reposo']}\t{plan[i]['fecha_siembra']}\t{plan[i]['fecha_cosecha']}\t{plan[i]['rendimiento']}")

        print("\nResumen ejecutivo:")
        print("-------------------")
        print(f"Total de cultivos: {len(plan)}")
        print(f"Total de precios: ${sum(precios):.2f}")
        print(f"Total de tiempos de cultivo: {sum(tiempos_cultivo)} días")
        print(f"Total de tiempos de reposo: {sum(tiempos_reposo)} días")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()