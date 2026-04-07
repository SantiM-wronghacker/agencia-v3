import os
import sys
import json
import datetime
import math
import re
import random

def extraer_sentimiento(texto, palabras_positivas, palabras_negativas):
    try:
        sentimiento = 0
        for palabra in texto.lower().split():
            if palabra in palabras_positivas:
                sentimiento += 1
            elif palabra in palabras_negativas:
                sentimiento -= 1
        return sentimiento
    except Exception as e:
        print(f"Error: {str(e)}")
        return 0

def calcular_tipo_de_cambio(tipo_de_cambio=None):
    try:
        if tipo_de_cambio is None:
            tipo_de_cambio = sys.argv[3] if len(sys.argv) > 3 else "1.0"
        tipo_de_cambio = float(tipo_de_cambio)
        return tipo_de_cambio
    except (ValueError, IndexError):
        print("Error: El tipo de cambio debe ser un número.")
        return 1.0

def calcular_precios(texto_precios, tipo_de_cambio):
    try:
        precio = float(texto_precios.replace("MXN", "").replace(",", "").strip())
        precio_usd = precio / tipo_de_cambio
        return precio, precio_usd
    except ValueError:
        print("Error: El precio debe ser un número.")
        return 0.0, 0.0

def analizar_sentimiento_marca(texto, texto_precios, tipo_de_cambio, palabras_positivas, palabras_negativas):
    sentimiento = extraer_sentimiento(texto, palabras_positivas, palabras_negativas)
    precio, precio_usd = calcular_precios(texto_precios, tipo_de_cambio)

    print("ÁREA: MARKETING")
    print("DESCRIPCIÓN: Agente que realiza análisis de sentimiento de marca")
    print("TECNOLOGÍA: Python estándar")
    print(f"Sentimiento de marca: {sentimiento}")
    print(f"Texto de análisis: {texto}")
    print(f"Precios de marca: {texto_precios} MXN / {precio_usd:.2f} USD")
    print(f"Tipo de cambio: {tipo_de_cambio}")
    print(f"Fecha y hora de análisis: {datetime.datetime.now()}")

    if sentimiento > 0:
        print("Resumen ejecutivo: La marca tiene un sentimiento positivo.")
    elif sentimiento < 0:
        print("Resumen ejecutivo: La marca tiene un sentimiento negativo.")
    else:
        print("Resumen ejecutivo: La marca tiene un sentimiento neutro.")

    if precio > 0:
        print(f"Comparación de precios: El precio actual es {precio:.2f} MXN, lo que representa un aumento del {math.ceil((precio - 1000) / 1000 * 100)}% con respecto a los 1000 MXN.")
    else:
        print("Comparación de precios: No se pudo calcular la comparación de precios.")

    if precio_usd > 0:
        print(f"Comparación de precios en USD: El precio actual en USD es {precio_usd:.2f}, lo que representa un aumento del {math.ceil((precio_usd - 0.5) / 0.5 * 100)}% con respecto a los 0.5 USD.")
    else:
        print("Comparación de precios en USD: No se pudo calcular la comparación de precios.")

def main():
    if len(sys.argv) < 4:
        print("Error: Faltan argumentos.")
        return

    texto = sys.argv[1]
    texto_precios = sys.argv[2]
    tipo_de_cambio = sys.argv[3]
    palabras_positivas = sys.argv[4].split(",")
    palabras_negativas = sys.argv[5].split(",")

    analizar_sentimiento_marca(texto, texto_precios, tipo_de_cambio, palabras_positivas, palabras_negativas)

if __name__ == "__main__":
    main()