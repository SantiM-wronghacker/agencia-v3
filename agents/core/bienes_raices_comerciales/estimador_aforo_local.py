"""
ARCHIVO: estimador_aforo_local.py
AREA: HERRAMIENTAS
DESCRIPCION: Agente que realiza estimador aforo local
TECNOLOGIA: Python estándar
"""

import sys
import json
import random
import math
import datetime
import os

def estimar_aforo(dia_semana, hora, zona, ajuste_estacional=1.0, ajuste_temporada=None):
    zonas = {
        "polanco": {"lunes_a_viernes": 0.75, "sabado": 0.9, "domingo": 0.4, "temporada": 1.1},
        "condesa": {"lunes_a_viernes": 0.8, "sabado": 0.95, "domingo": 0.5, "temporada": 1.2},
        "centro": {"lunes_a_viernes": 0.6, "sabado": 0.85, "domingo": 0.3, "temporada": 1.0},
        "santa_fe": {"lunes_a_viernes": 0.7, "sabado": 0.8, "domingo": 0.45, "temporada": 1.1}
    }

    ajustes_hora = {
        "mañana": 0.9,
        "tarde": 1.0,
        "noche": 0.7
    }

    try:
        if dia_semana.lower() in ["sabado", "domingo"]:
            base = zonas.get(zona.lower(), zonas["polanco"]).get(dia_semana.lower(), 0.5)
        else:
            base = zonas.get(zona.lower(), zonas["polanco"]).get("lunes_a_viernes", 0.5)
    except AttributeError:
        print("Error: zona no válida")
        return None

    try:
        if ajuste_temporada:
            base *= zonas.get(zona.lower(), zonas["polanco"]).get("temporada", 1.0)
    except TypeError:
        print("Error: ajuste temporal no válido")
        return None

    try:
        if 6 <= hora < 12:
            ajuste = ajustes_hora["mañana"]
        elif 12 <= hora < 20:
            ajuste = ajustes_hora["tarde"]
        else:
            ajuste = ajustes_hora["noche"]
    except TypeError:
        print("Error: hora no válida")
        return None

    try:
        if zona.lower() == "polanco":
            aforo = base * ajuste * ajuste_estacional * (1 + random.uniform(-0.05, 0.05)) * 1000
        elif zona.lower() == "condesa":
            aforo = base * ajuste * ajuste_estacional * (1 + random.uniform(-0.05, 0.05)) * 1200
        elif zona.lower() == "centro":
            aforo = base * ajuste * ajuste_estacional * (1 + random.uniform(-0.05, 0.05)) * 800
        elif zona.lower() == "santa_fe":
            aforo = base * ajuste * ajuste_estacional * (1 + random.uniform(-0.05, 0.05)) * 900
        return aforo
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    if len(sys.argv) > 1:
        zona = sys.argv[1]
        dia_semana = sys.argv[2]
        hora = int(sys.argv[3])
        ajuste_estacional = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        ajuste_temporada = sys.argv[5] if len(sys.argv) > 5 else None
    else:
        zona = "polanco"
        dia_semana = "lunes"
        hora = 10
        ajuste_estacional = 1.0
        ajuste_temporada = None

    aforo = estimar_aforo(dia_semana, hora, zona, ajuste_estacional, ajuste_temporada)
    if aforo:
        print(f"Aforo estimado en {zona} el {dia_semana} a las {hora}: {aforo} personas")
        print(f"Zona: {zona}")
        print(f"Día de la semana: {dia_semana}")