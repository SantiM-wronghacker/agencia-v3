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
    except IndexError:
        print("Error: Debe proporcionar al menos un precio")
        sys.exit(1)
    return precios

def calcular_merma(precio_compra, precio_venta):
    try:
        if precio_compra == 0:
            raise ValueError("Precio de compra no puede ser cero")
        if precio_venta < 0:
            raise ValueError("Precio de venta no puede ser negativo")
        merma = ((precio_venta - precio_compra) / precio_compra) * 100
        return merma
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

def calcular_merma_realista(precio_compra, precio_venta):
    try:
        if precio_compra == 0:
            raise ValueError("Precio de compra no puede ser cero")
        if precio_venta < 0:
            raise ValueError("Precio de venta no puede ser negativo")
        # Ajuste de merma para reflejar la realidad mexicana
        merma = ((precio_venta - precio_compra) / precio_compra) * 100 * 1.2
        return merma
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

def calcular_ingresos(precio_venta, cantidad):
    try:
        if precio_venta <= 0:
            raise ValueError("Precio de venta debe ser mayor que cero")
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser mayor que cero")
        ingresos = precio_venta * cantidad
        return ingresos
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

def calcular_ganancia(merma, precio_venta, cantidad):
    try:
        if merma < 0:
            raise ValueError("Merma no puede ser negativa")
        if precio_venta <= 0:
            raise ValueError("Precio de venta debe ser mayor que cero")
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser mayor que cero")
        ganancia = (merma / 100) * precio_venta * cantidad
        return ganancia
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    precios = extraer_precios()
    print("Precios:")
    for producto, precio in precios.items():
        print(f"{producto}: {precio}")

    merma_leche = calcular_merma(precios["leche"], precios["leche"] * 1.2)
    merma_carne = calcular_merma(precios["carne"], precios["carne"] * 1.1)
    merma_papa = calcular_merma(precios["papa"], precios["papa"] * 1.05)

    print("\nMermas:")
    print(f"Leche: {merma_leche}%")
    print(f"Carne: {merma_carne}%")
    print(f"Papa: {merma_papa}%")

    merma_leche_realista = calcular_merma_realista(precios["leche"], precios["leche"] * 1.2)
    merma_carne_realista = calcular_merma_realista(precios["carne"], precios["carne"] * 1.1)
    merma_papa_realista = calcular_merma_realista(precios["papa"], precios["papa"] * 1.05)

    print("\nMermas realistas:")
    print(f"Leche: {merma_leche_realista}%")
    print(f"Carne: {merma_carne_realista}%")
    print(f"Papa: {merma_papa_realista}%")

    ingresos_leche = calcular_ingresos(precios["leche"] * 1.2, 100)
    ingresos_carne = calcular