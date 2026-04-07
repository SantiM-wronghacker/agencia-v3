"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza generador ficha producto
TECNOLOGÍA: Python estándar
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
        precio_unitario = float(sys.argv[1]) if len(sys.argv) > 1 else 199.99
        precio_total = float(sys.argv[2]) if len(sys.argv) > 2 else 399.98
        descuento = float(sys.argv[3]) if len(sys.argv) > 3 else 0.15
        return {
            "precio_unitario": precio_unitario,
            "precio_total": precio_total,
            "descuento": descuento
        }
    except (IndexError, ValueError):
        return {
            "precio_unitario": 199.99,
            "precio_total": 399.98,
            "descuento": 0.15
        }

def calcular_impuestos(subtotal):
    try:
        return subtotal * 0.16
    except TypeError:
        return 0

def calcular_iva(subtotal):
    try:
        return subtotal * 0.16
    except TypeError:
        return 0

def calcular_iva_mexico(subtotal):
    try:
        # IVA en México es 16% para la mayoría de los bienes y servicios
        return subtotal * 0.16
    except TypeError:
        return 0

def calcular_iva_mexico_especial(subtotal):
    try:
        # IVA en México es 0% para algunos bienes y servicios
        return 0
    except TypeError:
        return 0

def generar_ficha_producto():
    try:
        # Obtener datos del producto
        nombre = sys.argv[4] if len(sys.argv) > 4 else "Producto 1"
        descripcion = sys.argv[5] if len(sys.argv) > 5 else "Este es un producto de prueba"
        precio_unitario = extraer_precios()["precio_unitario"]
        precio_total = extraer_precios()["precio_total"]
        descuento = extraer_precios()["descuento"]

        # Calcular datos adicionales
        cantidad = random.randint(1, 10)
        subtotal = precio_unitario * cantidad
        impuestos = calcular_iva(subtotal)
        iva_mexico = calcular_iva_mexico(subtotal)
        total = subtotal + impuestos
        total_descuento = total - (total * descuento)
        porcentaje_impuestos = (impuestos / total) * 100
        porcentaje_descuento = (total - total_descuento) / total * 100

        # Imprimir datos del producto
        print(f"Nombre: {nombre}")
        print(f"Descripción: {descripcion}")
        print(f"Precio unitario: ${precio_unitario:.2f}")
        print(f"Precio total: ${precio_total:.2f}")
        print(f"Cantidad: {cantidad}")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Impuestos: ${impuestos:.2f} (16%)")
        print(f"IVA México: ${iva_mexico:.2f} (16%)")
        print(f"Total: ${total:.2f}")
        print(f"Total con descuento: ${total_descuento:.2f} (-{porcentaje_descuento:.2f}%)")
        print(f"Porcentaje impuestos: {porcentaje_impuestos:.2f}%")
        print(f"Porcentaje descuento: {porcentaje_descuento:.2f}%")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El producto {nombre} tiene un precio unitario de ${precio_unitario:.2f} y un precio total de ${precio_total:.2f}.")
        print(f"El subtotal es de ${subtotal:.2f} y los impuestos son de ${impuestos:.2f} (16%).")
        print(f"El total con descuento es de ${total_descuento:.2f} (-{porcentaje_descuento:.2f}%) y el porcentaje de impuestos es de {porcentaje_impuestos:.2f}%.")
    except (IndexError, ValueError):
        print("Error: No se proporcionaron suficientes argumentos.")

if __name__ == "__main__":
    generar_ficha_producto()