#!/usr/bin/env python3

"""
ÁREA: SEGUROS
DESCRIPCION: Agente que realiza comparador seguros auto
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import os
import random

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_precio_seguro(marca, modelo, año, kilometraje, seguro):
    precio_base = 5000
    ajuste_marca = {
        "Toyota": 1.1,
        "Honda": 1.05,
        "Volkswagen": 1.0,
        "Nissan": 0.95,
        "Ford": 0.9
    }
    ajuste_modelo = {
        "Sedan": 1.0,
        "Hatchback": 0.9,
        "SUV": 1.1,
        "Camioneta": 1.2
    }
    ajuste_año = 1 - (datetime.datetime.now().year - año) * 0.05
    ajuste_kilometraje = 1 - (kilometraje / 100000) * 0.1
    ajuste_seguro = {
        "Seguro Azteca": 1.05,
        "Seguro Banamex": 1.10,
        "Seguro Inbursa": 1.15,
        "Seguro Mapfre": 1.20,
        "Seguro GNP": 1.25
    }
    if seguro not in ajuste_seguro:
        print(f"Error: Seguro '{seguro}' no encontrado")
        return None
    precio_seguro = precio_base * ajuste_marca.get(marca, 1.0) * ajuste_modelo.get(modelo, 1.0) * ajuste_año * ajuste_kilometraje * ajuste_seguro.get(seguro, 1.0)
    return precio_seguro

def calcular_iva(precio):
    return precio * 0.16

def comparar_seguros(marca, modelo, año, kilometraje):
    try:
        seguros = [
            {"nombre": "Seguro Azteca", "precio": calcular_precio_seguro(marca, modelo, año, kilometraje, "Seguro Azteca")},
            {"nombre": "Seguro Banamex", "precio": calcular_precio_seguro(marca, modelo, año, kilometraje, "Seguro Banamex")},
            {"nombre": "Seguro Inbursa", "precio": calcular_precio_seguro(marca, modelo, año, kilometraje, "Seguro Inbursa")},
            {"nombre": "Seguro Mapfre", "precio": calcular_precio_seguro(marca, modelo, año, kilometraje, "Seguro Mapfre")},
            {"nombre": "Seguro GNP", "precio": calcular_precio_seguro(marca, modelo, año, kilometraje, "Seguro GNP")},
            {"nombre": "Seguro Nacional", "precio": calcular_precio_seguro(marca, modelo, año, kilometraje, "Seguro Nacional")},
            {"nombre": "Seguro Mundial", "precio": calcular_precio_seguro(marca, modelo, año, kilometraje, "Seguro Mundial")},
        ]
        for seguro in seguros:
            seguro["iva"] = calcular_iva(seguro["precio"])
            seguro["total"] = seguro["precio"] + seguro["iva"]
        return seguros
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def main():
    if len(sys.argv) != 5:
        print("Uso: python comparador_seguros_auto.py <marca> <modelo> <año> <kilometraje>")
        return
    marca = sys.argv[1]
    modelo = sys.argv[2]
    año = int(sys.argv[3])
    kilometraje = int(sys.argv[4])
    seguros = comparar_seguros(marca, modelo, año, kilometraje)
    if seguros:
        print("Comparación de seguros:")
        for i, seguro in enumerate(seguros):
            print(f"{i+1}. {seguro['nombre']}: ${seguro['precio']:.2f} (IVA: ${seguro['iva']:.2f}, Total: ${seguro['total']:.2f})")
        print