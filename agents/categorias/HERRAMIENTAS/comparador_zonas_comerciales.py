#!/usr/bin/env python3

# AREA: HERRAMIENTAS
# DESCRIPCION: Comparador Zonas Comerciales
# TECNOLOGIA: Python

import sys
import os
import json
import math
import re
import random
import datetime

# Parametros por defecto
zonas_precios = {
    "Zona Rosa": 120000,
    "Polanco": 180000,
    "Condesa": 150000,
    "Santa Fe": 200000,
    "Reforma": 160000,
    "Coyoacán": 100000
}

zonas_alquileres = {
    "Zona Rosa": 80000,
    "Polanco": 120000,
    "Condesa": 90000,
    "Santa Fe": 150000,
    "Reforma": 100000,
    "Coyoacán": 60000
}

def calcular_precio_promedio(zona, metros_cuadrados):
    try:
        precio_por_metro = zonas_precios.get(zona.lower(), 100000)
        return precio_por_metro * metros_cuadrados
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def calcular_alquiler_promedio(zona, metros_cuadrados):
    try:
        alquiler_por_metro = zonas_alquileres.get(zona.lower(), 70000)
        return alquiler_por_metro * (metros_cuadrados / 100)
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def calcular_rotacion(zona):
    try:
        return random.uniform(0.8, 1.2)
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def calcular_tendencia(zona):
    try:
        return random.choice(["Alta", "Media", "Baja"])
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def calcular_rentabilidad(zona, precio_promedio, alquiler_promedio):
    try:
        return (precio_promedio - alquiler_promedio) / precio_promedio
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def obtener_datos_zona(zona, metros_cuadrados):
    try:
        datos = {
            "zona": zona,
            "precio_promedio": calcular_precio_promedio(zona, metros_cuadrados),
            "alquiler_promedio": calcular_alquiler_promedio(zona, metros_cuadrados),
            "rotacion": calcular_rotacion(zona),
            "tendencia": calcular_tendencia(zona),
            "rentabilidad": calcular_rentabilidad(zona, calcular_precio_promedio(zona, metros_cuadrados), calcular_alquiler_promedio(zona, metros_cuadrados))
        }
        return datos
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def main():
    if len(sys.argv) != 3:
        print("Uso: python comparador_zonas_comerciales.py <zona> <metros_cuadrados>")
        print("Ejemplo: python comparador_zonas_comerciales.py Zona Rosa 100")
        sys.exit(1)

    zona = sys.argv[1]
    metros_cuadrados = int(sys.argv[2])

    datos = obtener_datos_zona(zona, metros_cuadrados)

    if datos:
        print(f"Zona: {datos['zona']}")
        print(f"Precio promedio: ${datos['precio_promedio']:,}")
        print(f"Alquiler promedio: ${datos['alquiler_promedio']:,}")
        print(f"Rotacion: {datos['rotacion']:.2f}")
        print(f"Tendencia: {datos['tendencia']}")
        print(f"Rentabilidad: {datos['rentabilidad']:.2f}")
        print(f"Fecha: {datetime.date.today()}")
        print("Resumen ejecutivo:")
        print(f"La zona de {datos['zona']} ofrece un precio promedio de ${datos['precio_promedio']:,} por metro cuadrado, con un alquiler promedio de ${datos['alquiler_promedio']:,}. La rotacion es de {datos['rotacion']:.2f} y la tendencia es {datos['tendencia']}. La rentabilidad es de {datos['rentabilidad']:.2f}.")

if __name__ == "__main__":
    main()