"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza generador encuesta csat
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random
from datetime import date

def extraer_precios(fecha='actual', tipo='mxn'):
    try:
        if fecha == 'actual':
            fecha = date.today().strftime("%Y-%m-%d")
        precios = {
            'dólar': 20.50,
            'euro': 22.80,
            'peso': 1.00
        }
        if tipo == 'usd':
            return {'dólar': 1.00}
        elif tipo == 'mxn':
            return {'peso': 1.00}
        elif tipo == 'eur':
            return {'euro': 1.00}
        else:
            return precios
    except Exception as e:
        return {"error": str(e)}

def generar_encuesta():
    hoy = date.today()
    fecha = hoy.strftime("%d/%m/%Y")
    hora = datetime.datetime.now().strftime("%H:%M:%S")
    encuesta = {
        'fecha': fecha,
        'hora': hora,
        'pregunta1': '¿Cómo fue tu experiencia con el servicio?',
        'pregunta2': '¿Qué podemos mejorar?',
        'pregunta3': '¿Qué te gustaría que cambiáramos?',
        'respuesta1': 'Muy satisfecho',
        'respuesta2': 'Satisfecho',
        'respuesta3': 'Insatisfecho',
        'respuesta4': 'Muy insatisfecho'
    }
    return encuesta

def obtener_noticias():
    try:
        import requests
        url = 'https://newsapi.org/v2/top-headlines?country=mx&apiKey=YOUR_API_KEY'
        response = requests.get(url)
        noticias = response.json()['articles']
        return noticias
    except Exception as e:
        return {"error": str(e)}

def obtener_resumen_ejecutivo(encuesta, noticias):
    resumen = f"Fecha: {encuesta['fecha']}\nHora: {encuesta['hora']}\nEncuesta: {encuesta['pregunta1']} {encuesta['respuesta1']}\nNoticias del día: {noticias[0]['title']}"
    return resumen

def main():
    try:
        if len(sys.argv) > 1:
            fecha = sys.argv[1]
            tipo = sys.argv[2]
        else:
            fecha = 'actual'
            tipo = 'mxn'
        precios = extraer_precios(fecha, tipo)
        encuesta = generar_encuesta()
        noticias = obtener_noticias()
        resumen = obtener_resumen_ejecutivo(encuesta, noticias)
        print("ÁREA: HERRAMIENTAS")
        print("DESCRIPCIÓN: Agente que realiza generador encuesta csat")
        print("TECNOLOGÍA: Python estándar")
        print("Conexión a Internet: SI")
        print("Fecha actual: ", date.today())
        print("Hora actual: ", datetime.datetime.now().strftime("%H:%M:%S"))
        print("Precio dólar: ", precios['dólar'])
        print("Precio euro: ", precios['euro'])
        print("Precio peso: ", precios['peso'])
        print("Noticias del día: ", noticias[0]['title'])
        print("Encuesta:")
        print(f"Fecha: {encuesta['fecha']}")
        print(f"Hora: {encuesta['hora']}")
        print(f"Pregunta 1: {encuesta['pregunta1']} {encuesta['respuesta1']}")
        print(f"Pregunta 2: {encuesta['pregunta2']}")
        print(f"Pregunta 3: {encuesta['pregunta3']}")
        print("Resumen ejecutivo:")
        print(resumen)
    except Exception as e:
        print("Error: ", str(e))

if __name__ == "__main__":
    main()