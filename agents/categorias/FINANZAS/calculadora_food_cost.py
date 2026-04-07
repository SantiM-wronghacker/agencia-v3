# ARCHIVO: calculadora_food_cost.py
# AREA: FINANZAS
# DESCRIPCION: Calculadora Food Cost
# TECNOLOGIA: Python 3

import os
import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def calcular_food_cost(precio_unitario, cantidad, porcentaje_margen):
    try:
        if precio_unitario <= 0 or cantidad <= 0 or porcentaje_margen < 0:
            raise ValueError("Valores inválidos")
        margen = precio_unitario * (porcentaje_margen / 100)
        precio_venta = precio_unitario + margen
        food_cost = precio_venta - (precio_venta * 0.3)
        return food_cost
    except ValueError as e:
        print(f"Error: {e}")
        return None

def calcular_beneficio(food_cost):
    beneficio = food_cost * 0.3
    return beneficio

def calcular_impuesto(food_cost):
    impuesto = food_cost * 0.16
    return impuesto

def calcular_utilidad(food_cost, beneficio, impuesto):
    utilidad = food_cost + beneficio - impuesto
    return utilidad

def calcular_ganancia_neta(utilidad, impuesto):
    ganancia_neta = utilidad - impuesto
    return ganancia_neta

def calcular_retorno_inversion(precio_unitario, cantidad, porcentaje_margen, utilidad):
    try:
        inversion = precio_unitario * cantidad
        retorno = (utilidad / inversion) * 100
        return retorno
    except ZeroDivisionError:
        return 0

def main():
    if len(sys.argv) > 3:
        precio_unitario = float(sys.argv[1])
        cantidad = int(sys.argv[2])
        porcentaje_margen = float(sys.argv[3])
    elif WEB:
        # Buscar datos reales con web_bridge
        datos = web.buscar('precios_alimentos_mexico')
        precio_unitario = float(datos['precio_unitario'])
        cantidad = int(datos['cantidad'])
        porcentaje_margen = float(datos['porcentaje_margen'])
    else:
        # Datos de ejemplo
        precio_unitario = 50.0  # pesos mexicanos
        cantidad = 10
        porcentaje_margen = 20.0

    food_cost = calcular_food_cost(precio_unitario, cantidad, porcentaje_margen)
    if food_cost is not None:
        beneficio = calcular_beneficio(food_cost)
        impuesto = calcular_impuesto(food_cost)
        utilidad = calcular_utilidad(food_cost, beneficio, impuesto)
        ganancia_neta = calcular_ganancia_neta(utilidad, impuesto)
        retorno_inversion = calcular_retorno_inversion(precio_unitario, cantidad, porcentaje_margen, utilidad)

        print(f'**Calculadora Food Cost**')
        print(f'Precio unitario: ${precio_unitario:.2f} MXN')
        print(f'Cantidad: {cantidad} unidades')
        print(f'Porcentaje de margen: {porcentaje_margen}%')
        print(f'Food Cost: ${food_cost:.2f} MXN')
        print(f'Beneficio: ${beneficio:.2f} MXN')
        print(f'Impuesto: ${impuesto:.2f} MXN')
        print(f'Utilidad: ${utilidad:.2f} MXN')
        print(f'Ganancia neta: ${ganancia_neta:.2f} MXN')
        print(f'Retorno de la inversión: {retorno_inversion:.2f}%')
        print('**Resumen Ejecutivo**')
        print(f'La inversión de ${precio_unitario * cantidad:.2f} MXN en {cantidad} unidades con un margen de {porcentaje_margen}% puede generar una utilidad de ${utilidad:.2f} MXN y un retorno de la inversión de {retorno_inversion:.2f}%.')

if __name__ == "__main__":
    main()