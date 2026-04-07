"""
ÁREA: LOGISTICA
DESCRIPCIÓN: Agente que realiza tracker pedidos
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios(*args):
    if len(args) > 0:
        url = args[0]
    else:
        url = "https://www.example.com/precios"  # texto fijo para pruebas
    if url == "":
        return None
    try:
        with open('precios.json', 'r') as f:
            precios = json.load(f)
    except FileNotFoundError:
        precios = {
            'precio_unitario': 10.99,
            'precio_total': 100.99,
            'descuento': 5,
            'tipo_pago': {
                'efectivo': 0.16,
                'tarjeta': 0.12
            }
        }
    return precios

def calcular_costo(precio_unitario, cantidad, descuento):
    if precio_unitario <= 0 or cantidad <= 0 or descuento < 0:
        raise ValueError("Valores inválidos")
    costo = precio_unitario * cantidad
    costo_con_descuento = costo * (1 - descuento / 100)
    return costo_con_descuento

def calcular_impuestos(costo, tipo_pago):
    if tipo_pago not in ['efectivo', 'tarjeta']:
        raise ValueError("Tipo de pago desconocido")
    return costo * extraer_precios()[0]['tipo_pago'][tipo_pago]

def calcular_iva(costo):
    return costo * 0.16

def calcular_total(costo, impuestos):
    return costo + impuestos

def calcular_resumen(cantidad_pedidos, costo_total):
    return {
        'cantidad_pedidos': cantidad_pedidos,
        'costo_total': costo_total,
        'costo_promedio': costo_total / cantidad_pedidos,
        'iva_total': calcular_iva(costo_total),
        'descuento_total': costo_total * 0.05
    }

def main():
    if len(sys.argv) < 5:
        print("Faltan argumentos. Uso: python tracker_pedidos.py <cantidad_pedidos> <tipo_pago> <precio_unitario> <url>")
        return
    cantidad_pedidos = int(sys.argv[1])
    tipo_pago = sys.argv[2]
    precio_unitario = float(sys.argv[3])
    url = sys.argv[4]

    try:
        precios = extraer_precios(url)
        if precios is None:
            print("No se encontraron precios")
            return
        costo_con_descuento = calcular_costo(precio_unitario, cantidad_pedidos, precios['descuento'])
        impuestos = calcular_impuestos(costo_con_descuento, tipo_pago)
        costo_total = calcular_total(costo_con_descuento, impuestos)
        resumen = calcular_resumen(cantidad_pedidos, costo_total)
        print(f"ÁREA: LOGISTICA")
        print(f"DESCRIPCIÓN: Agente que realiza tracker pedidos")
        print(f"TECNOLOGÍA: Python estándar")
        print(f"Cantidad de pedidos: {cantidad_pedidos}")
        print(f"Tipo de pago: {tipo_pago}")
        print(f"Precio unitario: {precio_unitario}")
        print(f"Costo con descuento: {costo_con_descuento}")
        print(f"Impuestos: {impuestos}")
        print(f"Costo total: {costo_total}")
        print(f"Resumen:")
        print(f"  Cantidad de pedidos: {resumen['cantidad_pedidos']}")
        print(f"  Costo total: {resumen['costo_total']}")
        print(f"  Costo promedio: {resumen['costo_promedio']}")
        print(f"  IVA total: {resumen['iva_total']}")
        print(f"  Descuento total: {resumen['descuento_total']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()