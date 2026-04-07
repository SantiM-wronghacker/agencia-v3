#!/usr/bin/env python3
"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza generador newsletter
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios(fecha_actual=None):
    try:
        if fecha_actual is None:
            fecha_actual = datetime.datetime.now()
        precio_dolar = float(os.getenv('PRECIO_DOLAR', 20.50)) + (random.uniform(-0.1, 0.1) * 20.50)
        precio_euro = float(os.getenv('PRECIO_EURO', 23.20)) + (random.uniform(-0.1, 0.1) * 23.20)
        precio_peso = float(os.getenv('PRECIO_PESO', 1.00)) + (random.uniform(-0.01, 0.01) * 1.00)
        ipc = float(os.getenv('IPC', 4.5)) + (random.uniform(-0.5, 0.5) * 4.5)
        tasa_interes = float(os.getenv('TASA_INTERES', 5.5)) + (random.uniform(-0.5, 0.5) * 5.5)
        return {
            "dólar": precio_dolar,
            "euro": precio_euro,
            "peso": precio_peso,
            "IPC": ipc,
            "tasa_interes": tasa_interes
        }
    except Exception as e:
        print(f"Error al extraer precios: {e}")
        return None

def obtener_noticias():
    return [
        "Noticia 1: La empresa X anuncia un aumento de 10% en sus ventas.",
        "Noticia 2: El gobierno de México aprueba un nuevo plan para estimular la economía.",
        "Noticia 3: La empresa Y anuncia un nuevo producto que revoluciona el mercado.",
        "Noticia 4: El índice de precios al consumo (IPC) sube un 2% en un mes.",
        "Noticia 5: La tasa de interés de la Reserva Federal sube a 5.5%.",
        "Noticia 6: El dólar se vuelve más caro en México.",
        "Noticia 7: La inflación en México sigue en aumento.",
        "Noticia 8: El gobierno de México anuncia un plan para reducir la pobreza.",
        "Noticia 9: La empresa Z anuncia un nuevo producto que revoluciona el mercado.",
        "Noticia 10: El índice de confianza en la economía mexicana sube.",
        "Noticia 11: La empresa A anuncia un aumento de 15% en sus ventas.",
        "Noticia 12: El gobierno de México aprueba un nuevo plan para estimular la economía.",
        "Noticia 13: La empresa B anuncia un nuevo producto que revoluciona el mercado.",
        "Noticia 14: El gobierno de México anuncia un plan para estimular la economía.",
        "Noticia 15: La empresa X anuncia un aumento de 10% en sus ventas.",
        "Noticia 16: El índice de precios al consumo (IPC) sube un 2% en un mes.",
        "Noticia 17: La tasa de interés de la Reserva Federal sube a 5.5%.",
        "Noticia 18: El dólar se vuelve más caro en México.",
        "Noticia 19: La inflación en México sigue en aumento.",
        "Noticia 20: El gobierno de México anuncia un plan para reducir la pobreza."
    ]

def generar_resumen_ejecutivo(precios, noticias):
    resumen = f"Resumen Ejecutivo:\n"
    resumen += f"El dólar está valorizado a ${precios['dólar']:.2f}.\n"
    resumen += f"La tasa de interés de la Reserva Federal es de {precios['tasa_interes']:.2f}%.\n"
    resumen += f"El IPC subió un 2% en un mes.\n"
    resumen += f"Las noticias más destacadas son:\n"
    for i, noticia in enumerate(noticias[:5]):
        resumen += f"{i+1}. {noticia}\n"
    return resumen

def main():
    fecha_actual = datetime.datetime.now()
    precios = extraer_prec