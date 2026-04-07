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

def calcular_precios(data, tipo_de_cambio):
    try:
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

def calcular_utilidad(data, tipo_de_cambio):
    try:
        precio_mxn = data['precio']
        costo_produccion, costo_logistica, costo_marketing = calcular_costos(data)
        impuesto_iwa, impuesto_iva = calcular_impuestos(calcular_precios(data, tipo_de_cambio)[1])
        utilidad = precio_mxn - (costo_produccion + costo_logistica + costo_marketing + impuesto_iwa + impuesto_iva)
        return utilidad
    except Exception as e:
        print(f'Ocurrió un error: {e}')
        return None

def main():
    try:
        if len(sys.argv) > 1:
            datos = json.loads(sys.argv[1])
            tipo_de_cambio = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0
        else:
            datos = {
                'satisfaccion': 80,
                'probabilidad_recomendacion': 70,
                'precio': 100.0
            }
            tipo_de_cambio = 20.0

        nps = extraer_nps(datos)
        precio, precio_usd = calcular_precios(datos, tipo_de_cambio)
        impuesto_iwa, impuesto_iva = calcular_impuestos(precio_usd)
        costo_produccion, costo_logistica, costo_marketing = calcular_costos(datos)
        utilidad = calcular_utilidad(datos, tipo_de_cambio)

        print(f'NPS: {nps}')
        print(f'Precio (MXN): {precio}')
        print(f'Precio (USD): {precio_usd}')
        print(f'Impuesto IWA: {impuesto_iwa}')
        print(f'Impuesto IVA: {impuesto_iva}')
        print(f'Costo de producción: {costo_produccion}')
        print(f'Costo de logística: {costo_logistica}')
        print(f'Costo de marketing: {costo_marketing}')
        print(f'Utilidad: {utilidad}')
        print(f'Resumen ejecutivo: La utilidad es de {utilidad} con un NPS de {nps} y un precio de {precio} MXN')
    except Exception as e:
        print(f'Ocurrió un error: {e}')

if __name__ == "__main__":
    main()