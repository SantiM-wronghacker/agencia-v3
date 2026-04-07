"""
ÁREA: ECOMMERCE
DESCRIPCIÓN: Agente que realiza generador descripción categoría
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_descripcion_categoria(categoria, subcategoria, precio_min, precio_max):
    try:
        if categoria and subcategoria and precio_min and precio_max:
            precio = round(random.uniform(precio_min, precio_max), 2)
            descripcion = f"La categoría {categoria} cuenta con una variedad de productos, incluyendo {subcategoria}, que se pueden encontrar a partir de ${precio:.2f} MXN."
            return descripcion
        else:
            return "Error: Faltan parámetros"
    except Exception as e:
        return f"Error: {str(e)}"

def calcular_precio_medio(precio_min, precio_max, cantidad_productos):
    try:
        if precio_min and precio_max and cantidad_productos:
            return round((precio_min + precio_max) / 2, 2)
        else:
            return 0
    except Exception as e:
        return f"Error: {str(e)}"

def calcular_probabilidad_compra(precio, cantidad_productos):
    try:
        if precio and cantidad_productos:
            probabilidad = (precio / (20000 - 10000)) * 0.8 + 0.1
            return round(probabilidad, 2)
        else:
            return 0
    except Exception as e:
        return f"Error: {str(e)}"

def calcular_utilidad(precio, cantidad_productos):
    try:
        if precio and cantidad_productos:
            return round(precio * 0.8 * cantidad_productos, 2)
        else:
            return 0
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    try:
        categoria = "Electrónica" if len(sys.argv) < 2 else sys.argv[1]
        subcategoria = "Celulares" if len(sys.argv) < 3 else sys.argv[2]
        precio_min = float(sys.argv[3]) if len(sys.argv) > 3 else 10000.0
        precio_max = float(sys.argv[4]) if len(sys.argv) > 4 else 20000.0
        cantidad_productos = int(sys.argv[5]) if len(sys.argv) > 5 else 10
        descripcion = generar_descripcion_categoria(categoria, subcategoria, precio_min, precio_max)
        precio_medio = calcular_precio_medio(precio_min, precio_max, cantidad_productos)
        probabilidad_compra = calcular_probabilidad_compra(precio_medio, cantidad_productos)
        utilidad = calcular_utilidad(precio_medio, cantidad_productos)
        resumen_ejecutivo = f"Resumen Ejecutivo: La categoría {categoria} cuenta con una variedad de productos, incluyendo {subcategoria}, que se pueden encontrar a partir de ${precio_medio:.2f} MXN, con una probabilidad de compra del {probabilidad_compra*100}% y una utilidad de ${utilidad} MXN."
        print(f"ÁREA: ECOMMERCE")
        print(f"DESCRIPCIÓN: Agente que realiza generador descripción categoría")
        print(f"TECNOLOGÍA: Python estándar")
        print(f"Categoría: {categoria}")
        print(f"Subcategoría: {subcategoria}")
        print(f"Precio mínimo: ${precio_min:.2f} MXN")
        print(f"Precio máximo: ${precio_max:.2f} MXN")
        print(f"Cantidad de productos: {cantidad_productos}")
        print(f"Descripción: {descripcion}")
        print(f"Precio medio: ${precio_medio:.2f} MXN")
        print(f"Probabilidad de compra: {probabilidad_compra*100}%")
        print(f"Utilidad: ${utilidad} MXN")
        print(resumen_ejecutivo)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()