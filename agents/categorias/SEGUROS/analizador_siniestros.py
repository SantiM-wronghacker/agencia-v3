import os
import sys
import json
import datetime
import math
import re
import random

"""
ÁREA: SEGUROS
DESCRIPCIÓN: Agente que realiza analizador siniestros
TECNOLOGÍA: Python estándar
"""

def extraer_precios(precios):
    try:
        return {
            "dólar": float(precios.get("dólar", 20.50)),
            "euro": float(precios.get("euro", 22.75)),
            "peso argentino": float(precios.get("peso argentino", 4.50)),
            "peso mexicano": float(precios.get("peso mexicano", 20.00))
        }
    except ValueError:
        print("Error: Precios inválidos")
        return {}

def buscar_siniestros(siniestros):
    try:
        return [
            {"id": 1, "tipo": "incendio", "valor": float(siniestros.get("siniestros", {}).get("1", 10000))},
            {"id": 2, "tipo": "robo", "valor": float(siniestros.get("siniestros", {}).get("2", 5000))},
            {"id": 3, "tipo": "accidente", "valor": float(siniestros.get("siniestros", {}).get("3", 20000))},
            {"id": 4, "tipo": "hundimiento", "valor": float(siniestros.get("siniestros", {}).get("4", 30000))},
            {"id": 5, "tipo": "desastre natural", "valor": float(siniestros.get("siniestros", {}).get("5", 40000))}
        ]
    except ValueError:
        print("Error: Siniestros inválidos")
        return []

def analizar_siniestros(siniestros):
    try:
        total = sum(siniestro["valor"] for siniestro in siniestros)
        incendios = sum(1 for siniestro in siniestros if siniestro["tipo"] == "incendio")
        robos = sum(1 for siniestro in siniestros if siniestro["tipo"] == "robo")
        porcentaje_incendios = (incendios / len(siniestros)) * 100
        porcentaje_robo = (robos / len(siniestros)) * 100
        return total, porcentaje_incendios, porcentaje_robo
    except ZeroDivisionError:
        print("Error: No hay siniestros")
        return 0, 0, 0

def calcular_inflacion(total):
    try:
        return total * 0.05
    except TypeError:
        print("Error: Total inválido")
        return 0

def calcular_inflacion_mexicana(total):
    try:
        # Inflación promedio en México en el 2022
        return total * 0.08
    except TypeError:
        print("Error: Total inválido")
        return 0

def main():
    if len(sys.argv) > 1:
        try:
            siniestros = json.loads(sys.argv[1])
            precios = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            print("Error: Parámetros inválidos")
            return
    else:
        print("Error: Faltan parámetros")
        return

    precios = extraer_precios(precios)
    siniestros = buscar_siniestros(siniestros)
    total, porcentaje_incendios, porcentaje_robo = analizar_siniestros(siniestros)
    inflacion = calcular_inflacion(total)
    inflacion_mexicana = calcular_inflacion_mexicana(total)

    print("ÁREA: SEGUROS")
    print("DESCRIPCIÓN: Agente que realiza analizador siniestros")
    print("TECNOLOGÍA: Python estándar")

    print("\nPrecios actuales:")
    for moneda, valor in precios.items():
        print(f"{moneda}: {valor}")

    print("\nSiniestros detectados:")
    for siniestro in siniestros:
        print(f"ID: {siniestro['id']}, Tipo: {siniestro['tipo']}, Valor: {siniestro['valor']}")

    print("\nAnálisis de siniestros:")
    print(f"Total: {total}")