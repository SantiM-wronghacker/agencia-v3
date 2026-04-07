"""
ÁREA: MANUFACTURA
DESCRIPCIÓN: Agente que realiza generador amef
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios(precio_materia_prima=100.50, precio_material=50.25, precio_maquinaria=200.75):
    return {
        'precio_materia_prima': precio_materia_prima,
        'precio_material': precio_material,
        'precio_maquinaria': precio_maquinaria
    }

def calcular_costo(precios):
    try:
        # Agregar un 10% de margen para calcular el costo
        costo = (precios['precio_materia_prima'] + precios['precio_material'] + precios['precio_maquinaria']) * 1.10
        # Agregar un 16% de impuesto
        costo += costo * 0.16
        return costo
    except KeyError as e:
        print(f"Error: {e}")
        return None

def generar_amef(fecha_actual=None, precios=None):
    if fecha_actual is None:
        fecha_actual = datetime.datetime.now()
    if precios is None:
        precios = extraer_precios()
    costo = calcular_costo(precios)
    if costo is None:
        return None
    amef = {
        'fecha': fecha_actual.strftime('%Y-%m-%d'),
        'costo': costo,
        'precio_materia_prima': precios['precio_materia_prima'],
        'precio_material': precios['precio_material'],
        'precio_maquinaria': precios['precio_maquinaria'],
        'margen': 10,
        'impuesto': 16,
        'total_materia_prima': precios['precio_materia_prima'] * 100,
        'total_material': precios['precio_material'] * 50,
        'total_maquinaria': precios['precio_maquinaria'] * 200,
        'total_costo': costo * 100
    }
    return amef

def main():
    try:
        if len(sys.argv) > 1:
            precio_materia_prima = float(sys.argv[1])
            precio_material = float(sys.argv[2])
            precio_maquinaria = float(sys.argv[3])
        else:
            precio_materia_prima = 100.50
            precio_material = 50.25
            precio_maquinaria = 200.75
        
        amef = generar_amef(precios=extraer_precios(precio_materia_prima, precio_material, precio_maquinaria))
        if amef is not None:
            print("ÁREA: MANUFACTURA")
            print("DESCRIPCIÓN: Agente que realiza generador amef")
            print("TECNOLOGÍA: Python estándar")
            print("Fecha:", amef['fecha'])
            print("Costo:", amef['costo'])
            print("Precio materia prima:", amef['precio_materia_prima'])
            print("Precio material:", amef['precio_material'])
            print("Precio maquinaria:", amef['precio_maquinaria'])
            print("Margen:", amef['margen'], "%")
            print("Impuesto:", amef['impuesto'], "%")
            print("Total materia prima:", amef['total_materia_prima'])
            print("Total material:", amef['total_material'])
            print("Total maquinaria:", amef['total_maquinaria'])
            print("Total costo:", amef['total_costo'])
            print("\nResumen ejecutivo:")
            print("El costo total del proyecto es de", amef['costo'], "con un margen de", amef['margen'], "% y un impuesto de", amef['impuesto'], "%.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()