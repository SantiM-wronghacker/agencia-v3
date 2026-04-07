"""
ÁREA: MANUFACTURA
DESCRIPCIÓN: Agente que realiza generador spc
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios(precios=None):
    if precios is None:
        precios = {
            "precio_aluminio": 220.50,
            "precio_acero": 150.00,
            "precio_pvc": 80.00
        }
    return precios

def calcular_margen_ganancia(costo_unidad, precio_venta):
    return (precio_venta - costo_unidad) / costo_unidad * 100

def calcular_costo_total(cantidad_produccion, costo_unidad):
    return cantidad_produccion * costo_unidad

def calcular_recaudacion(cantidad_produccion, precio_venta):
    return cantidad_produccion * precio_venta

def calcular_precio_unitario(costo_unidad, margen_ganancia):
    return costo_unidad + (costo_unidad * margen_ganancia / 100)

def calcular_utilidad_bruta(costo_total, recaudacion):
    return recaudacion - costo_total

def generar_spc(precios=None, cantidad_produccion=None, costo_unidad=None, precio_venta=None, margen_ganancia=None):
    try:
        if precios is None:
            precios = extraer_precios()

        if cantidad_produccion is None:
            cantidad_produccion = random.randint(100, 500)
        if costo_unidad is None:
            costo_unidad = random.uniform(10.00, 20.00)
        if precio_venta is None:
            precio_venta = random.uniform(25.00, 35.00)
        if margen_ganancia is None:
            margen_ganancia = random.uniform(15.00, 25.00)

        fecha_actual = datetime.date.today()
        margen_ganancia_calculado = calcular_margen_ganancia(costo_unidad, calcular_precio_unitario(costo_unidad, margen_ganancia))
        costo_total = calcular_costo_total(cantidad_produccion, costo_unidad)
        recaudacion = calcular_recaudacion(cantidad_produccion, calcular_precio_unitario(costo_unidad, margen_ganancia))
        precio_unitario = calcular_precio_unitario(costo_unidad, margen_ganancia)
        utilidad_bruta = calcular_utilidad_bruta(costo_total, recaudacion)

        print(f"Fecha: {fecha_actual}")
        print(f"Cantidad de producción: {cantidad_produccion} unidades")
        print(f"Costo de unidad: ${costo_unidad:.2f}")
        print(f"Precio de venta: ${precio_venta:.2f}")
        print(f"Márgen de ganancia: {margen_ganancia:.2f}%")
        print(f"Precio de aluminio: ${precios['precio_aluminio']:.2f}")
        print(f"Precio de acero: ${precios['precio_acero']:.2f}")
        print(f"Precio de PVC: ${precios['precio_pvc']:.2f}")
        print(f"Costo total: ${costo_total:.2f}")
        print(f"Recaudación: ${recaudacion:.2f}")
        print(f"Precio unitario: ${precio_unitario:.2f}")
        print(f"Utilidad bruta: ${utilidad_bruta:.2f}")
        print(f"Índice de rentabilidad: {(utilidad_bruta / costo_total) * 100:.2f}%")
        print(f"Tiempo de pago: {(costo_total / utilidad_bruta) if utilidad_bruta != 0 else 'No calculable'} días")
        print(f"Resumen ejecutivo: El proyecto tiene un margen de ganancia de {margen_ganancia_calculado:.2f}% y una utilidad bruta de ${utilidad_bruta:.2f}.")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            print("Uso: python generador_spc.py [opciones]")
            print("Opciones:")
            print("  --precios <precio_aluminio,precio_acero,precio_pvc>")
            print("  --cantidad_produccion <número>")
            print("  --costo_unidad <precio>")
            print("  --precio_venta <precio>")