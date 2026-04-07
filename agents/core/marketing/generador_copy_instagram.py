"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza generador copy instagram
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def calcular_tipo_de_cambio(monto, tipo_de_cambio):
    try:
        tipo_de_cambio_real = monto * float(tipo_de_cambio.split(' ')[2]) / float(tipo_de_cambio.split(' ')[4])
        return tipo_de_cambio_real
    except (ValueError, IndexError):
        raise ValueError("Debes proporcionar un tipo de cambio válido")

def calcular_comision(monto, comision):
    try:
        comision_real = monto * comision / 100
        return comision_real
    except (ValueError, TypeError):
        raise ValueError("Debes proporcionar una comisión válida")

def generar_resumen_ejecutivo(precios, tipo_de_cambio_real, comision_real):
    return f"""
Resumen ejecutivo:
- Tipo de cambio: {tipo_de_cambio_real}
- Comisión: {comision_real}%
- Precios totales: {sum(precios.values())} pesos mexicanos
"""

def generar_copy_instagram(productos, tipo_de_cambio, noticias, cotizaciones, precios, comision):
    if len(productos) < 1:
        raise ValueError("Debes proporcionar al menos un producto")

    if len(tipo_de_cambio) < 1:
        raise ValueError("Debes proporcionar un tipo de cambio válido")

    if len(noticias) < 1:
        raise ValueError("Debes proporcionar noticias")

    if len(cotizaciones) < 1:
        raise ValueError("Debes proporcionar cotizaciones")

    if len(precios) < 1:
        raise ValueError("Debes proporcionar precios válidos")

    if comision < 0 or comision > 100:
        raise ValueError("Debes proporcionar una comisión válida")

    try:
        tipo_de_cambio_real = calcular_tipo_de_cambio(1000, tipo_de_cambio)
        comision_real = calcular_comision(1000, comision)
    except (ValueError, IndexError):
        raise ValueError("Debes proporcionar un tipo de cambio válido")

    # Generar copy instagram
    copy = f"""
¡Oferta del día! 🎉
{', '.join(f'* {producto}: {precios[producto]} pesos mexicanos' for producto in productos)}
¡Descubre las últimas noticias y cotizaciones bursátiles! 📰
{noticias}
{cotizaciones}
¿Qué esperas? ¡Comienza a comprar ahora! 🛍️
"""
    copy += generar_resumen_ejecutivo(precios, tipo_de_cambio_real, comision_real)
    return copy

def main():
    if len(sys.argv) < 7:
        print("Debes proporcionar los siguientes argumentos:")
        print("- productos")
        print("- tipo_de_cambio")
        print("- noticias")
        print("- cotizaciones")
        print("- precios")
        print("- comision")
        return

    productos = sys.argv[1].split(',')
    tipo_de_cambio = sys.argv[2]
    noticias = sys.argv[3]
    cotizaciones = sys.argv[4]
    precios_str = sys.argv[5]
    comision = float(sys.argv[6])

    precios = {}
    for precio in precios_str.split(','):
        producto, precio = precio.split(':')
        precios[producto] = float(precio)

    try:
        copy = generar_copy_instagram(productos, tipo_de_cambio, noticias, cotizaciones, precios, comision)
        print(copy)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()