import requests
from bs4 import BeautifulSoup
import re
import sys
import os
import json
import datetime
import math
import random
import time

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def buscar_inmobiliarias(zona, max_results=5):
    try:
        url = f"https://duckduckgo.com/html?q=inmobiliarias+{zona}+mexico"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        inmobiliarias = []
        for result in soup.find_all("a", class_="result__a"):
            link = result.get("href")
            if link:
                title = result.text.strip()
                description = result.find_next("a", class_="result__snippet")
                if description:
                    diferenciador = re.sub(r"<.*?>", "", str(description)).strip()
                    if diferenciador and len(diferenciador) > 10:
                        inmobiliarias.append((title, diferenciador, link))
                        if len(inmobiliarias) >= max_results:
                            break

        return inmobiliarias
    except requests.exceptions.RequestException as e:
        print(f"Error al buscar inmobiliarias: {str(e)}")
        return []
    except Exception as e:
        print(f"Error desconocido: {str(e)}")
        return []

def obtener_diferenciadores(inmobiliarias):
    diferenciadores = []
    for inmobiliaria in inmobiliarias:
        nombre, diferenciador, link = inmobiliaria
        diferenciadores.append((nombre, diferenciador, link))

    return diferenciadores

def generar_resumen(diferenciadores):
    if not diferenciadores:
        return "No se encontraron inmobiliarias en la zona seleccionada."
    resumen = "Inmobiliarias más activas en la zona de {}:\n".format(os.environ.get('ZONA', ''))
    for i, inmobiliaria in enumerate(diferenciadores):
        nombre, diferenciador, link = inmobiliaria
        resumen += f"{i+1}. {nombre} - {diferenciador}\n"
    return resumen

def generar_resumen_ejecutivo(diferenciadores):
    if not diferenciadores:
        return "No se encontraron inmobiliarias en la zona seleccionada."
    num_inmobiliarias = len(diferenciadores)
    num_diferenciadores = sum(len(diferenciador) > 10 for _, diferenciador, _ in diferenciadores)
    resumen = "Resumen ejecutivo:\n"
    resumen += f"Número de inmobiliarias encontradas: {num_inmobiliarias}\n"
    resumen += f"Número de diferenciadores de servicio encontrados: {num_diferenciadores}\n"
    resumen += f"Porcentaje de inmobiliarias con diferenciadores de servicio: {num_diferenciadores / num_inmobiliarias * 100:.2f}%\n"
    return resumen

def main():
    zona = os.environ.get('ZONA', 'Mexico')
    max_results = int(os.environ.get('MAX_RESULTS', 5))
    inmobiliarias = buscar_inmobiliarias(zona, max_results)
    diferenciadores = obtener_diferenciadores(inmobiliarias)
    resumen = generar_resumen(diferenciadores)
    resumen_ejecutivo = generar_resumen_ejecutivo(diferenciadores)
    print(resumen)
    print(resumen_ejecutivo)

if __name__ == "__main__":
    main()