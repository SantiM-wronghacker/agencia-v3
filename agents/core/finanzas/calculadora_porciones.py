"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora porciones
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import math
import datetime
import re

def calculadora_porciones(precios=None, tipo_de_cambio=None, noticias=None, porciones=None, fecha=None):
    if precios is None:
        try:
            precios = json.loads(sys.argv[1])
        except (IndexError, json.JSONDecodeError):
            precios = {
                "menu": 100,
                "bebida": 50,
                "postre": 75
            }
    if tipo_de_cambio is None:
        try:
            tipo_de_cambio = float(sys.argv[2])
        except (IndexError, ValueError):
            tipo_de_cambio = 20  # MXN/USD
    if noticias is None:
        noticias = "Noticias de restaurantes en México"
    if porciones is None:
        porciones = {
            "menu": 4,
            "bebida": 8,
            "postre": 6
        }
    if fecha is None:
        fecha = datetime.date.today().strftime("%Y-%m-%d")

    # Validación de precios
    try:
        menu = float(precios["menu"])
        bebida = float(precios["bebida"])
        postre = float(precios["postre"])
    except (KeyError, ValueError):
        raise ValueError("Precios deben ser un diccionario con claves 'menu', 'bebida' y 'postre'")

    # Calcular porciones
    porcion_menu = menu / porciones["menu"]
    porcion_bebida = bebida / porciones["bebida"]
    porcion_postre = postre / porciones["postre"]

    # Calcular tipo de cambio
    precio_usd = menu / tipo_de_cambio

    # Calcular inflación anual
    if menu > 0:
        inflation = ((math.pow((menu / 100), 12) - 1) * 100)
    else:
        inflation = 0

    # Calcular índice de precios al consumidor
    ipc = math.pow((menu / 100), 12)

    # Calcular precio de la porción del menu en USD
    porcion_menu_usd = porcion_menu / tipo_de_cambio

    # Calcular precio de la porción de bebida en USD
    porcion_bebida_usd = porcion_bebida / tipo_de_cambio

    # Calcular precio de la porción de postre en USD
    porcion_postre_usd = porcion_postre / tipo_de_cambio

    # Imprimir resultados
    print(f"Menu: {menu} MXN")
    print(f"Bebida: {bebida} MXN")
    print(f"Postre: {postre} MXN")
    print(f"Precio de la porción del menu: {porcion_menu} MXN")
    print(f"Precio de la porción de bebida: {porcion_bebida} MXN")
    print(f"Precio de la porción de postre: {porcion_postre} MXN")
    print(f"Precio de la porción del menu en USD: {porcion_menu_usd} USD")
    print(f"Precio de la porción de bebida en USD: {porcion_bebida_usd} USD")
    print(f"Precio de la porción de postre en USD: {porcion_postre_usd} USD")
    print(f"Inflación anual: {inflation}%")
    print(f"Índice de precios al consumidor: {ipc}")
    print(f"Noticias: {noticias}")
    print(f"Fecha: {fecha}")

    # Resumen ejecutivo
    print("\nResumen ejecutivo:")
    print(f"El precio del menu es de {menu} MXN y el precio de la porción del menu es de {porcion_menu} MXN.")
    print(f"El precio de la bebida es de {bebida} MXN y el precio de la porción de bebida es de {porcion_bebida} MXN.")
    print(f"El precio del postre es de {postre} MXN y el precio de la porción de postre es de {porcion_postre} MXN.")
    print(f"El tipo de cambio es de {tipo_de_cambio} MXN/USD.")

def main():
    if len(sys.argv) > 1:
        calculadora_porciones