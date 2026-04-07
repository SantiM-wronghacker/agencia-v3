"""
AREA: REAL ESTATE
DESCRIPCION: Busca el crecimiento porcentual promedio de precios de vivienda en las colonias principales de CDMX.
TECNOLOGIA: Python, requests, BeautifulSoup
"""

import requests
from bs4 import BeautifulSoup
import time
import sys
import json
import math
import re
import random
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def buscar_crecimiento_plusvalia(colonias):
    resultados = {}
    url = "https://duckduckgo.com/"
    
    for colonia in colonias:
        try:
            params = {
                "q": f"crecimiento porcentual promedio de precios de vivienda en {colonia}, CDMX",
                "t": "h_",
                "ia": "web"
            }
            
            respuesta = requests.get(url, params=params)
            respuesta.raise_for_status()
            soup = BeautifulSoup(respuesta.text, "html.parser")
            
            for resultado in soup.find_all("a", class_="result__a"):
                texto_resultado = resultado.text
                if "por ciento" in texto_resultado or "%" in texto_resultado:
                    inicio = texto_resultado.find(" ") + 1
                    fin = texto_resultado.find("%")
                    if inicio < fin:
                        crecimiento = float(texto_resultado[inicio:fin])
                        resultados[colonia] = crecimiento
                    break
            else:
                resultados[colonia] = None
            
            time.sleep(2)
        except requests.exceptions.RequestException as e:
            print(f"Error al buscar {colonia}: {e}")
            resultados[colonia] = None
    
    return resultados

def calcular_promedio(resultados):
    total = 0
    count = 0
    for colonia, crecimiento in resultados.items():
        if crecimiento is not None:
            total += crecimiento
            count += 1
    if count > 0:
        return total / count
    else:
        return None

def calcular_desviacion_estandar(resultados):
    promedio = calcular_promedio(resultados)
    if promedio is not None:
        total = 0
        count = 0
        for colonia, crecimiento in resultados.items():
            if crecimiento is not None:
                total += (crecimiento - promedio) ** 2
                count += 1
        if count > 1:
            return math.sqrt(total / (count - 1))
        else:
            return 0
    else:
        return None

def main():
    if len(sys.argv) > 1:
        colonias = sys.argv[1:]
    else:
        colonias = ["Condesa", "Roma", "Juárez", "Cuauhtémoc", "Chapultepec", "Polanco", "Lomas de Chapultepec", "Santa Fe", "Reforma", "Del Valle"]
        print("Usando valores por defecto:")
        print("Colonias:", colonias)
    
    resultados = buscar_crecimiento_plusvalia(colonias)
    
    for colonia, crecimiento in resultados.items():
        if crecimiento is not None:
            print(f"Crecimiento porcentual promedio en {colonia}: {crecimiento}%")
        else:
            print(f"No se encontraron datos para {colonia}")
    
    promedio = calcular_promedio(resultados)
    if promedio is not None:
        print(f"Promedio de crecimiento porcentual: {promedio}%")
    else:
        print("No se pueden calcular promedios")
    
    desviacion_estandar = calcular_desviacion_estandar(resultados)
    if desviacion_estandar is not None:
        print(f"Desviación estándar del crecimiento porcentual: {desviacion_estandar}%")
    else:
        print("No se pueden calcular desviaciones estándar")
    
    print("Resumen ejecutivo:")
    print(f"Fecha de consulta: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total de colonias consultadas: {len(colonias)}")
    print(f"Total de colonias con datos: {sum(1 for colonia, crecimiento in resultados.items() if crecimiento is not None)}")

if __name__ == "__main__":
    main()