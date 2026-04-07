"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza generador base conocimiento
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios(precio_gasolina=24.50, precio_diesel=22.50, precio_electricidad=3.50):
    precios = {
        "gasolina": precio_gasolina,
        "diesel": precio_diesel,
        "electricidad": precio_electricidad
    }
    return precios

def obtener_tipo_cambio():
    try:
        with open('tipo_cambio.txt', 'r') as f:
            return float(f.read())
    except FileNotFoundError:
        return 20.50
    except ValueError:
        return 20.50

def obtener_cotizaciones_bursatiles():
    try:
        with open('cotizaciones_bursatiles.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "SAP: 500.00, WIPRO: 600.00"

def obtener_noticias_ultima_hora():
    try:
        with open('noticias_ultima_hora.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Noticias de última hora: México gana la Copa América"

def generar_base_conocimiento(precio_gasolina=24.50, precio_diesel=22.50, precio_electricidad=3.50):
    try:
        # Obtener fecha actual
        fecha_actual = datetime.datetime.now()
        
        # Obtener precios de combustibles
        precios = extraer_precios(precio_gasolina, precio_diesel, precio_electricidad)
        
        # Obtener tipo de cambio
        tipo_cambio = obtener_tipo_cambio()
        
        # Obtener cotizaciones bursátiles
        cotizaciones = obtener_cotizaciones_bursatiles()
        
        # Obtener noticias de última hora
        noticias = obtener_noticias_ultima_hora()
        
        # Imprimir resultados
        print(f"Fecha actual: {fecha_actual}")
        print(f"Precios de combustibles: {precios['gasolina']} pesos por litro de gasolina, {precios['diesel']} pesos por litro de diesel")
        print(f"Tipo de cambio: 1 USD = {tipo_cambio} MXN")
        print(f"Cotizaciones bursátiles: {cotizaciones}")
        print(f"Noticias de última hora: {noticias}")
        
        # Calcular consumo de combustible
        consumo_gasolina = 50  # litros por mes
        consumo_diesel = 30  # litros por mes
        consumo_electricidad = 100  # kWh por mes
        print(f"Consumo de combustible: {consumo_gasolina} litros de gasolina, {consumo_diesel} litros de diesel, {consumo_electricidad} kWh de electricidad")
        
        # Calcular gasto de combustible
        gasto_gasolina = precios['gasolina'] * consumo_gasolina
        gasto_diesel = precios['diesel'] * consumo_diesel
        gasto_electricidad = precios['electricidad'] * consumo_electricidad
        print(f"Gasto de combustible: {gasto_gasolina} pesos por gasolina, {gasto_diesel} pesos por diesel, {gasto_electricidad} pesos por electricidad")
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) > 1:
        precio_gasolina = float(sys.argv[1])
        precio_diesel = float(sys.argv[2])
        precio_electricidad = float(sys.argv[3])
        generar_base_conocimiento(precio_gasolina, precio_diesel, precio_electricidad)
    else:
        generar_base_conocimiento()

if __name__ == "__main__":
    main()