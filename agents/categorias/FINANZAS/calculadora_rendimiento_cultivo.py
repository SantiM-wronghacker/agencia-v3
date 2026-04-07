"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora rendimiento cultivo
TECNOLOGÍA: Python estándar
"""

import sys
import os
import json
import datetime
import math
import re
import random

def calcular_rendimiento_cultivo(precio_harina, precio_maiz, rendimiento_maiz, hectareas):
    try:
        # Verifica que el rendimiento sea positivo
        if rendimiento_maiz <= 0:
            raise ValueError("Rendimiento de maíz debe ser positivo")

        # Verifica que el precio de la harina sea positivo
        if precio_harina <= 0:
            raise ValueError("Precio de la harina debe ser positivo")

        # Verifica que el precio del maíz sea positivo
        if precio_maiz <= 0:
            raise ValueError("Precio del maíz debe ser positivo")

        # Verifica que el número de hectáreas sea positivo
        if hectareas <= 0:
            raise ValueError("Número de hectáreas debe ser positivo")

        # Calcula el rendimiento total de maíz
        rendimiento_total_maiz = rendimiento_maiz * hectareas

        # Calcula el costo total de producción
        costo_total_produccion = (rendimiento_total_maiz * precio_maiz) + (rendimiento_total_maiz * 0.1)  # 10% de impuestos

        # Calcula el beneficio neto
        beneficio_neto = (rendimiento_total_maiz * precio_harina) - costo_total_produccion

        # Calcula el margen de beneficio
        margen_beneficio = (beneficio_neto / costo_total_produccion) * 100 if costo_total_produccion > 0 else 0

        # Calcula el ingreso total por hectárea
        ingreso_total_por_hectarea = (rendimiento_total_maiz * precio_harina) / hectareas

        # Muestra los resultados
        print("Rendimiento total de maíz:", rendimiento_total_maiz, "toneladas")
        print("Costo total de producción:", costo_total_produccion, "pesos mexicanos")
        print("Beneficio neto:", beneficio_neto, "pesos mexicanos")
        print("Margen de beneficio:", margen_beneficio, "%")
        print("Fecha de cálculo:", datetime.datetime.now())
        print("Ingresos totales por hectárea:", ingreso_total_por_hectarea, "pesos mexicanos")
        print("Costo de producción por hectárea:", (rendimiento_total_maiz * precio_maiz) / hectareas, "pesos mexicanos")
        print("Beneficio por hectárea:", (rendimiento_total_maiz * precio_harina) / hectareas - (rendimiento_total_maiz * precio_maiz) / hectareas, "pesos mexicanos")
        print("Resumen ejecutivo: El cultivo de maíz en la superficie de {} hectáreas genera un beneficio neto de {} pesos mexicanos, con un margen de beneficio del {}%.".format(hectareas, beneficio_neto, margen_beneficio))

    except ValueError as e:
        print("Error:", e)

def main():
    if len(sys.argv) != 5:
        print("Uso: python calculadora_rendimiento_cultivo.py <precio_harina> <precio_maiz> <rendimiento_maiz> <hectareas>")
    else:
        try:
            precio_harina = float(sys.argv[1])
            precio_maiz = float(sys.argv[2])
            rendimiento_maiz = float(sys.argv[3])
            hectareas = float(sys.argv[4])
            calcular_rendimiento_cultivo(precio_harina, precio_maiz, rendimiento_maiz, hectareas)
        except ValueError:
            print("Error: Los valores deben ser números.")

if __name__ == "__main__":
    main()