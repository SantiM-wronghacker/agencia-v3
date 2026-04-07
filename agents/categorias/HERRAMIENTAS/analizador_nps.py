"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza analizador nps
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
from datetime import datetime
import math
import re
import random

def extraer_nps(data):
    try:
        satisfaccion = data['satisfaccion']
        probabilidad_recomendacion = data['probabilidad_recomendacion']
        nps = (satisfaccion - (100 - probabilidad_recomendacion)) 
        return nps
    except KeyError as e:
        print(f'Ocurrió un error: {e}')
        return None

def calcular_precios(data):
    try:
        tipo_de_cambio = data['tipo_de_cambio']
        precio = data['precio']
        precio_usd = precio / tipo_de_cambio
        return precio, precio_usd
    except KeyError as e:
        print(f'Ocurrió un error: {e}')
        return None, None

def calcular_impuestos(precio_usd):
    try:
        impuesto_iwa = precio_usd * 0.16
        impuesto_iva = precio_usd * 0.08
        return impuesto_iwa, impuesto_iva
    except Exception as e:
        print(f'Ocurrió un error: {e}')
        return None, None

def calcular_costos(data):
    try:
        precio_mxn = data['precio']
        costo_produccion = precio_mxn * 0.7
        costo_logistica = precio_mxn * 0.1
        costo_marketing = precio_mxn * 0.2
        return costo_produccion, costo_logistica, costo_marketing
    except KeyError as e:
        print(f'Ocurrió un error: {e}')
        return None, None, None

def calcular_utilidad(data):
    try:
        precio_mxn = data['precio']
        costo_produccion, costo_logistica, costo_marketing = calcular_costos(data)
        impuesto_iwa, impuesto_iva = calcular_impuestos(calcular_precios(data)[1])
        utilidad = precio_mxn - (costo_produccion + costo_logistica + costo_marketing + impuesto_iwa + impuesto_iva)
        return utilidad
    except Exception as e:
        print(f'Ocurrió un error: {e}')
        return None

def main():
    try:
        if len(sys.argv) > 1:
            datos = json.loads(sys.argv[1])
        else:
            datos = {
                'satisfaccion': 80,
                'probabilidad_recomendacion': 70,
                'tipo_de_cambio': 20,
                'precio': 100
            }

        nps = extraer_nps(datos)
        precio_mxn, precio_usd = calcular_precios(datos)
        impuesto_iwa, impuesto_iva = calcular_impuestos(precio_usd)
        costo_produccion, costo_logistica, costo_marketing = calcular_costos(datos)
        utilidad = calcular_utilidad(datos)

        print("Resumen Ejecutivo:")
        print("--------------------")
        print(f"NPS: {nps}")
        print(f"Precio MXN: {precio_mxn}")
        print(f"Precio USD: {precio_usd}")
        print(f"Impuesto IWA: {impuesto_iwa}")
        print(f"Impuesto IVA: {impuesto_iva}")
        print(f"Costo Producción: {costo_produccion}")
        print(f"Costo Logística: {costo_logistica}")
        print(f"Costo Marketing: {costo_marketing}")
        print(f"Utilidad: {utilidad}")
        print("--------------------")
    except Exception as e:
        print(f'Ocurrió un error: {e}')

if __name__ == "__main__":
    main()