"""
ÁREA: AGRICULTURA
DESCRIPCIÓN: Agente que realiza analizador precio cosecha
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random
import argparse
from statistics import mean, median

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def extraer_precios() -> Dict[str, List[float]]:
    if WEB:
        texto = web.fetch_texto('https://www.example.com/precios-cosecha')
        try:
            precios = web.extraer_precios(texto)
        except ValueError as e:
            print(f"Error al extraer precios: {e}")
            precios = {}
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('--maiz', type=float, default=15.50)
        parser.add_argument('--trigo', type=float, default=20.25)
        parser.add_argument('--soya', type=float, default=18.75)
        args = parser.parse_args(sys.argv[1:])
        precios = {
            'maíz': [args.maiz],
            'trigo': [args.trigo],
            'soya': [args.soya]
        }
    return precios

def calcular_indicadores(precios: Dict[str, List[float]]) -> Dict[str, float]:
    indicadores = {}
    for producto, precio_list in precios.items():
        if precio_list:
            indicadores[producto + '_precio_promedio'] = mean(precio_list)
            indicadores[producto + '_precio_max'] = max(precio_list)
            indicadores[producto + '_precio_min'] = min(precio_list)
            indicadores[producto + '_precio_mediana'] = median(precio_list)
            indicadores[producto + '_varianza'] = math.sqrt(sum((x - indicadores[producto + '_precio_promedio'])**2 for x in precio_list) / len(precio_list))
            indicadores[producto + '_desviacion_estandar'] = math.sqrt(sum((x - indicadores[producto + '_precio_promedio'])**2 for x in precio_list) / (len(precio_list) - 1))
        else:
            indicadores[producto + '_precio_promedio'] = 0
            indicadores[producto + '_precio_max'] = 0
            indicadores[producto + '_precio_min'] = 0
            indicadores[producto + '_precio_mediana'] = 0
            indicadores[producto + '_varianza'] = 0
            indicadores[producto + '_desviacion_estandar'] = 0
    return indicadores

def calcular_indicadores_mexico(precios: Dict[str, List[float]]) -> Dict[str, float]:
    indicadores = {}
    for producto, precio_list in precios.items():
        if precio_list:
            indicadores[producto + '_precio_promedio'] = mean(precio_list)
            indicadores[producto + '_precio_max'] = max(precio_list)
            indicadores[producto + '_precio_min'] = min(precio_list)
            indicadores[producto + '_precio_mediana'] = median(precio_list)
            indicadores[producto + '_varianza'] = math.sqrt(sum((x - indicadores[producto + '_precio_promedio'])**2 for x in precio_list) / len(precio_list))
            indicadores[producto + '_desviacion_estandar'] = math.sqrt(sum((x - indicadores[producto + '_precio_promedio'])**2 for x in precio_list) / (len(precio_list) - 1))
            indicadores[producto + '_precio_promedio_mexico'] = indicadores[producto + '_precio_promedio'] * 1.2  # ajuste para México
            indicadores[producto + '_precio_max_mexico'] = indicadores[producto + '_precio_max'] * 1.2  # ajuste para México
            indicadores[producto + '_precio_min_mexico'] = indicadores[producto + '_precio_min'] * 1.2  # ajuste para México
            indicadores[producto + '_precio_mediana_mexico'] = indicadores[producto + '_precio_mediana'] * 1.2  # ajuste para México
            indicadores[producto + '_varianza_mexico'] = indicadores[producto + '_varianza'] * 1.2  # ajuste para México
            indicadores[producto + '_desviacion_estandar_mexico'] = indicadores[producto + '_desviacion_estandar'] * 1.2