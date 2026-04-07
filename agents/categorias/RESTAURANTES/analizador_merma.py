"""
AREA: HERRAMIENTAS
DESCRIPCION: Agente que realiza analizador de merma
TECNOLOGIA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios():
    try:
        precios = {
            "leche": float(sys.argv[1]) if len(sys.argv) > 1 else 25.50,
            "carne": float(sys.argv[2]) if len(sys.argv) > 2 else 80.00,
            "papa": float(sys.argv[3]) if len(sys.argv) > 3 else 10.00
        }
    except ValueError:
        print("Error: Los precios deben ser números")
        sys.exit(1)
    return precios

def calcular_merma(precio_compra, precio_venta):
    try:
        if precio_compra == 0:
            raise ValueError("Precio de compra no puede ser cero")
        merma = ((precio_venta - precio_compra) / precio_compra) * 100
        return merma
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

def calcular_merma_realista(precio_compra, precio_venta):
    try:
        if precio_compra == 0:
            raise ValueError("Precio de compra no puede ser cero")
        # Ajuste de merma para reflejar la realidad mexicana
        merma = ((precio_venta - precio_compra) / precio_compra) * 100 * 1.2
        return merma
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

def calcular_ingresos(precio_venta, cantidad):
    try:
        if precio_venta <= 0 or cantidad <= 0:
            raise ValueError("Precio de venta y cantidad deben ser mayores que cero")
        ingresos = precio_venta * cantidad
        return ingresos
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

def calcular_ganancia(merma, precio_venta, cantidad):
    try:
        if merma < 0 or precio_venta <= 0 or cantidad <= 0:
            raise ValueError("Merma, precio de venta y cantidad deben ser mayores que cero")
        ganancia = (merma / 100) * precio_venta * cantidad
        return ganancia
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    try:
        precios = extraer_precios()
        fecha = datetime.date.today().strftime("%Y-%m-%d")
        print(f"Fecha: {fecha}")
        print(f"Precio de la leche: {precios['leche']} MXN")
        print(f"Precio de la carne: {precios['carne']} MXN")
        print(f"Precio de la papa: {precios['papa']} MXN")
        precio_compra = 20.00
        precio_venta = 30.00
        cantidad = 100
        merma = calcular_merma_realista(precio_compra, precio_venta)
        print(f"Merma: {merma:.2f}%")
        ingresos = calcular_ingresos(precio_venta, cantidad)
        print(f"Ingresos: {ingresos:.2f} MXN")
        ganancia = calcular_ganancia(merma, precio_venta, cantidad)
        print(f"Ganancia: {ganancia:.2f} MXN")
        print(f"Costo total: {precio_compra * cantidad:.2f} MXN")
        print(f"Margen de ganancia: {(ganancia / ingresos) * 100:.2f}%")
        print(f"Resumen ejecutivo: La merma en la venta de productos es significativa, lo que afecta negativamente la rentabilidad del negocio.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()