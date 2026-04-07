"""
ÁREA: MANUFACTURA
DESCRIPCIÓN: Agente que realiza generador instructivo trabajo
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios(precio_dolar=None, precio_euro=None, precio_petroleo=None):
    if precio_dolar is None:
        precio_dolar = float(sys.argv[1]) if len(sys.argv) > 1 else 20.50
    if precio_euro is None:
        precio_euro = float(sys.argv[2]) if len(sys.argv) > 2 else 22.80
    if precio_petroleo is None:
        precio_petroleo = float(sys.argv[3]) if len(sys.argv) > 3 else 130.20
    return {
        "precio_dólar": precio_dolar,
        "precio_euro": precio_euro,
        "precio_petroleo": precio_petroleo
    }

def calcular_productividad(cantidad_productos, cantidad_empleados, cantidad_maquinas):
    return {
        "productividad_por_empleado": cantidad_productos / cantidad_empleados,
        "productividad_por_maquina": cantidad_productos / cantidad_maquinas
    }

def generar_instructivo_trabajo(precio_dolar=None, precio_euro=None, precio_petroleo=None):
    try:
        fecha_actual = datetime.date.today()
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        if precio_dolar is None:
            precio_dolar = extraer_precios()["precio_dólar"]
        if precio_euro is None:
            precio_euro = extraer_precios()["precio_euro"]
        if precio_petroleo is None:
            precio_petroleo = extraer_precios()["precio_petroleo"]
        
        cantidad_productos = random.randint(1000, 5000)
        cantidad_empleados = random.randint(50, 200)
        cantidad_maquinas = random.randint(100, 500)
        cantidad_productos_por_dia = cantidad_productos / 30
        cantidad_productos_por_empleado = cantidad_productos / cantidad_empleados
        cantidad_maquinas_por_empleado = cantidad_maquinas / cantidad_empleados
        
        print(f"Fecha actual: {fecha_actual}")
        print(f"Hora actual: {hora_actual}")
        print(f"Precio dólar: {precio_dolar} MXN")
        print(f"Precio euro: {precio_euro} MXN")
        print(f"Precio petróleo: {precio_petroleo} MXN")
        print(f"Cantidad de productos: {cantidad_productos}")
        print(f"Cantidad de empleados: {cantidad_empleados}")
        print(f"Cantidad de máquinas: {cantidad_maquinas}")
        print(f"Cantidad de productos por día: {cantidad_productos_por_dia:.2f}")
        print(f"Cantidad de productos por empleado: {cantidad_productos_por_empleado:.2f}")
        print(f"Cantidad de máquinas por empleado: {cantidad_maquinas_por_empleado:.2f}")
        print(f"Productividad por empleado: {calcular_productividad(cantidad_productos, cantidad_empleados, cantidad_maquinas)['productividad_por_empleado']:.2f}")
        print(f"Productividad por máquina: {calcular_productividad(cantidad_productos, cantidad_empleados, cantidad_maquinas)['productividad_por_maquina']:.2f}")
        
        print("\nResumen Ejecutivo:")
        print(f"El valor total de los productos producidos es: {cantidad_productos * precio_dolar} MXN")
        print(f"El valor total de los productos producidos es: {cantidad_productos * precio_euro} EUR")
        print(f"El valor total de los productos producidos es: {cantidad_productos * precio_petroleo} USD")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Error: Faltan argumentos. Utilice: python generador_instructivo_trabajo.py <precio_dolar> <precio_euro> <precio_petroleo>")
    else:
        generar_instructivo_trabajo()