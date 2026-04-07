import os
import sys
import json
import datetime
import math
import re
import random
import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup

# Configuración de la aplicación
AREA = "MARKETING"
DESCRIPCION = "Agente que realiza análisis SEO de keywords"
TECNOLOGIA = "Python"

def analizar_seo_keywords(palabras_clave, url):
    try:
        # Buscar en Google
        url_google = f"https://www.google.com/search?q={quote(palabras_clave)}"
        respuesta_google = urllib.request.urlopen(url_google).read()
        soup_google = BeautifulSoup(respuesta_google, 'html.parser')
        resultados_google = soup_google.find_all('div', class_='BNeawe iBp4i AP7Wnd')
        if resultados_google:
            resultado_google = resultados_google[0].text
            print(f"Google says: {resultado_google}")
        else:
            print(f"No se encontraron resultados en Google")

        # Analizar la página
        respuesta = urllib.request.urlopen(url).read()
        respuesta = respuesta.decode('utf-8')
        palabras_frecuentes = re.findall(r'\b\w+\b', respuesta.lower())
        frecuencia = {}
        for palabra in palabras_frecuentes:
            if palabra in frecuencia:
                frecuencia[palabra] += 1
            else:
                frecuencia[palabra] = 1
        print("Frecuencia de palabras:")
        for palabra, cuenta in frecuencia.items():
            print(f"{palabra}: {cuenta}")

        # Calcular la frecuencia de palabras en la página
        frecuencia_total = sum(frecuencia.values())
        frecuencia_promedio = math.ceil(frecuencia_total / len(frecuencia))
        print(f"Frecuencia promedio de palabras: {frecuencia_promedio}")

        # Calcular la tasa de frecuencia de palabras en la página
        tasa_frecuencia = (frecuencia_promedio / len(palabras_frecuentes)) * 100
        print(f"Tasa de frecuencia de palabras: {tasa_frecuencia}%")

        # Calcular la tasa de frecuencia de palabras en el top 10 de Google
        top_10_google = soup_google.find_all('div', class_='BNeawe iBp4i AP7Wnd')[:10]
        palabras_top_10 = re.findall(r'\b\w+\b', str(top_10_google).lower())
        frecuencia_top_10 = {}
        for palabra in palabras_top_10:
            if palabra in frecuencia_top_10:
                frecuencia_top_10[palabra] += 1
            else:
                frecuencia_top_10[palabra] = 1
        tasa_frecuencia_top_10 = (sum(frecuencia_top_10.values()) / len(palabras_top_10)) * 100
        print(f"Tasa de frecuencia de palabras en el top 10 de Google: {tasa_frecuencia_top_10}%")

    except Exception as e:
        print(f"Error al buscar en Google o analizar la página: {e}")

def main():
    if len(sys.argv) < 3:
        print("Debes proporcionar una palabra clave y una URL como argumentos")
        sys.exit(1)
    palabras_clave = sys.argv[1]
    url = sys.argv[2]

    analizar_seo_keywords(palabras_clave, url)

    # Resumen ejecutivo
    print("\nResumen ejecutivo:")
    print(f"Palabras clave: {palabras_clave}")
    print(f"URL: {url}")
    print(f"Frecuencia de palabras promedio: {math.ceil(sum(f for f in frecuencia.values()) / len(frecuencia))}")
    print(f"Tasa de frecuencia de palabras: {tasa_frecuencia}%")
    print(f"Tasa de frecuencia de palabras en el top 10 de Google: {tasa_frecuencia_top_10}%")

if __name__ == "__main__":
    main()