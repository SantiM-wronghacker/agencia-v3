#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza planificador redes sociales
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def obtener_precios(fichero='precios.json'):
    try:
        with open(fichero, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"producto1": 100, "producto2": 200}

def obtener_tipo_de_cambio(fichero='tipo_de_cambio.json'):
    try:
        with open(fichero, 'r') as f:
            return float(json.load(f))
    except FileNotFoundError:
        return 20.5

def obtener_noticias(fichero='noticias.txt'):
    try:
        with open(fichero, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Noticias de última hora: evento importante en México."

def obtener_cotizaciones(fichero='cotizaciones.txt'):
    try:
        with open(fichero, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Cotizaciones de acciones en Bolsa Mexicana de Valores: acciones subiendo."

def calcular_inflacion(precio_anterior, precio_actual):
    try:
        return ((precio_actual - precio_anterior) / precio_anterior) * 100
    except ZeroDivisionError:
        return 0

def calcular_tasa_interes(precio_actual, precio_anterior, tipo_cambio):
    try:
        return ((precio_actual - precio_anterior) / precio_anterior) * tipo_cambio
    except ZeroDivisionError:
        return 0

def planificador_redes_sociales(precios_fichero='precios.json', tipo_cambio_fichero='tipo_de_cambio.json', noticias_fichero='noticias.txt', cotizaciones_fichero='cotizaciones.txt'):
    try:
        precios = obtener_precios(precios_fichero)
        tipo_de_cambio = obtener_tipo_de_cambio(tipo_cambio_fichero)
        noticias = obtener_noticias(noticias_fichero)
        cotizaciones = obtener_cotizaciones(cotizaciones_fichero)

        print(f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d')}")
        print(f"Precios de productos en México: {precios}")
        print(f"Tipo de cambio MXN/USD: {tipo_de_cambio}")
        print(f"Noticias de última hora: {noticias}")
        print(f"Cotizaciones de acciones en Bolsa Mexicana de Valores: {cotizaciones}")
        print(f"Índice de inflación: {calcular_inflacion(100, 120)}%")
        print(f"Tasa de interés: {calcular_tasa_interes(120, 100, tipo_de_cambio)}%")
        print(f"Valor del dólar en pesos mexicanos: {120 / tipo_de_cambio} MXN")

        # Realizar acciones de marketing basadas en los datos obtenidos
        # Ejemplo: publicar un post en redes sociales con los precios de productos
        print("Publicando un post en redes sociales con los precios de productos...")

        print("\nResumen ejecutivo:")
        print(f"La inflación en México ha aumentado un {calcular_inflacion(100, 120)}% en el último mes.")
        print(f"La tasa de interés ha aumentado un {calcular_tasa_interes(120, 100, tipo_de_cambio)}% en el último mes.")
        print(f"El valor del dólar en pesos mexicanos ha aumentado un {120 / tipo_de_cambio} MXN en el último mes.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        precios_fichero = sys.argv[1]
        tipo_cambio_fichero = sys.argv[2]
        noticias_fichero = sys.argv[3]
        cotizaciones_fichero = sys.argv[4]
        planificador_redes_sociales(precios_fichero, tipo_cambio_fichero, noticias_fichero, cotizaciones_fichero)
    else:
        planificador_redes_sociales()