"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza generador presentacion ventas
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
from datetime import datetime
import math
import re
import random

def extraer_precios(precios=None, productos=None):
    try:
        if precios is None:
            if productos is None:
                productos = ["producto1", "producto2", "producto3", "producto4", "producto5"]
            return {
                producto: round(random.uniform(1, 100), 2) for producto in productos
            }
        else:
            return precios
    except Exception as e:
        print(f"Error al extraer precios: {e}")
        return None

def calcular_ventas(precios):
    try:
        return sum(precios.values())
    except Exception as e:
        print(f"Error al calcular ventas: {e}")
        return 0

def calcular_impuestos(ventas):
    try:
        # Impuesto del 16% para Mexico
        return ventas * 0.16
    except Exception as e:
        print(f"Error al calcular impuestos: {e}")
        return 0

def calcular_utilidad(ventas, impuestos):
    try:
        # Utilidad del 20% para Mexico
        return ventas * 0.20 - impuestos
    except Exception as e:
        print(f"Error al calcular utilidad: {e}")
        return 0

def generar_presentacion_ventas(precios=None, productos=None):
    try:
        if precios is None:
            precios = extraer_precios(productos=productos)
        if precios is None:
            return None
        ventas = calcular_ventas(precios)
        impuestos = calcular_impuestos(ventas)
        utilidad = calcular_utilidad(ventas, impuestos)
        return {
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "ventas": ventas,
            "impuestos": impuestos,
            "utilidad": utilidad,
            "productos": precios
        }
    except Exception as e:
        print(f"Error al generar presentación de ventas: {e}")
        return None

def main():
    try:
        if len(sys.argv) > 1:
            try:
                precios = json.loads(sys.argv[1])
            except json.JSONDecodeError:
                print("Error al parsear JSON. Utilice formato JSON válido.")
                sys.exit(1)
        else:
            precios = None
        productos = sys.argv[2:] if len(sys.argv) > 2 else None
        presentacion = generar_presentacion_ventas(precios, productos)
        if presentacion is not None:
            print(f"ÁREA: VENTAS")
            print(f"DESCRIPCIÓN: Generador de presentación de ventas")
            print(f"TECNOLOGÍA: Python estándar")
            print(f"Fecha: {presentacion['fecha']}")
            print(f"Ventas totales: {presentacion['ventas']:.2f} MXN")
            print(f"Impuestos: {presentacion['impuestos']:.2f} MXN")
            print(f"Utilidad: {presentacion['utilidad']:.2f} MXN")
            print(f"Productos vendidos: {len(presentacion['productos'])}")
            print("Productos:")
            for producto, precio in presentacion['productos'].items():
                print(f"- {producto}: {precio:.2f} MXN")
            print("Resumen ejecutivo:")
            print(f"La fecha de la presentación es {presentacion['fecha']}.")
            print(f"Las ventas totales son de {presentacion['ventas']:.2f} MXN.")
            print(f"Los impuestos son de {presentacion['impuestos']:.2f} MXN.")
            print(f"La utilidad es de {presentacion['utilidad']:.2f} MXN.")
    except Exception as e:
        print(f"Error en el programa: {e}")

if __name__ == "__main__":
    main()