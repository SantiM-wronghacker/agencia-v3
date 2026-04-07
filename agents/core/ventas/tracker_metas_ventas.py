#!/usr/bin/env python3
"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza tracker metas ventas
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random
import requests

def obtener_datos_ejemplo():
    # Datos de ejemplo
    metas_venta = 10000000.0  # Se ajusta a la realidad mexicana
    ventas_reales = 5000000.0  # Se ajusta a la realidad mexicana
    meta_cumplimiento = (ventas_reales / metas_venta) * 100
    ventas_por_canal = {'canal1': 1000000.0, 'canal2': 2000000.0}
    return metas_venta, ventas_reales, meta_cumplimiento, ventas_por_canal

def obtener_datos_reales(url):
    try:
        texto = requests.get(url).text
        precios = json.loads(texto)
        metas_venta = float(precios['meta_ventas'])
        ventas_reales = float(precios['ventas_reales'])
        meta_cumplimiento = (ventas_reales / metas_venta) * 100
        ventas_por_canal = precios['ventas_por_canal']
        return metas_venta, ventas_reales, meta_cumplimiento, ventas_por_canal
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos reales: {e}")
        return obtener_datos_ejemplo()
    except KeyError as e:
        print(f"Error al obtener datos reales: Faltan claves en la respuesta del servidor. {e}")
        return obtener_datos_ejemplo()
    except Exception as e:
        print(f"Error al obtener datos reales: {e}")
        return obtener_datos_ejemplo()

def calcular_margen_ganancia(metas_venta, ventas_reales):
    if metas_venta == 0:
        return 0
    return ((ventas_reales / metas_venta) * 100 - 100)

def calcular_porcentaje_ventas_canal(ventas_por_canal):
    total_ventas = sum(ventas_por_canal.values())
    if total_ventas == 0:
        return {}
    return {canal: (ventas / total_ventas) * 100 for canal, ventas in ventas_por_canal.items()}

def calcular_margen_utilidad(metas_venta, ventas_reales, precio_costo_unitario):
    if metas_venta == 0 or ventas_reales == 0:
        return 0
    return ((ventas_reales / metas_venta) * 100 - (precio_costo_unitario / metas_venta) * 100)

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else 'https://api.example.com/ventas'
    precio_costo_unitario = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    metas_venta, ventas_reales, meta_cumplimiento, ventas_por_canal = obtener_datos_reales(url)
    print(f"ÁREA: VENTAS")
    print(f"DESCRIPCIÓN: Agente que realiza tracker metas ventas")
    print(f"TECNOLOGÍA: Python estándar")
    print(f"URL: {url}")
    print(f"Precio costo unitario: ${precio_costo_unitario:.2f}")
    print(f"Meta de ventas: ${metas_venta:.2f}")
    print(f"Ventas reales: ${ventas_reales:.2f}")
    print(f"Meta cumplimiento: {meta_cumplimiento:.2f}%")
    print(f"Margen de ganancia: {calcular_margen_ganancia(metas_venta, ventas_reales):.2f}%")
    print(f"Margen de utilidad: {calcular_margen_utilidad(metas_venta, ventas_reales, precio_costo_unitario):.2f}%")
    print(f"Porcentaje de ventas por canal:")
    for canal, porcentaje in calcular_porcentaje_ventas_canal(ventas_por_canal).items():
        print(f"  {canal}: {porcentaje:.2f}%")
    print(f"Resumen ejecutivo: El meta de ventas ha sido cumplido al {meta_cumplimiento:.2f}%.")

if __name__ == "__main__":
    main()