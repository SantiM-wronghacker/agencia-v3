"""
ÁREA: TURISMO
DESCRIPCIÓN: Agente que realiza generador checklist viaje
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random
from urllib.request import urlopen
from bs4 import BeautifulSoup

def extraer_precios():
    url = "https://www.xe.com/es/currency-table/USD"
    try:
        response = urlopen(url)
        soup = BeautifulSoup(response, 'html.parser')
        precio_dolar = soup.find('span', {'class': 'w-xxl'}).text
        return precio_dolar
    except Exception as e:
        print(f"Error al obtener precio del dólar: {e}")
        return "1 USD = 20.50 MXN"

def calcular_costo_total(destino, duración, costo_diario):
    try:
        precio_dolar = extraer_precios()
        precio_dolar = precio_dolar.replace(" USD", "").replace("MXN", "")
        costo_total = (costo_diario * duración) / float(precio_dolar)
        return costo_total
    except ZeroDivisionError:
        return 0
    except ValueError:
        return 0

def calcular_costo_total_mexico(destino, duración, costo_diario):
    try:
        precio_dolar = extraer_precios()
        precio_dolar = precio_dolar.replace(" USD", "").replace("MXN", "")
        costo_total = (costo_diario * duración) / float(precio_dolar) * 20.50
        return costo_total
    except ZeroDivisionError:
        return 0
    except ValueError:
        return 0

def calcular_costo_vuelo(duracion, costo_diario):
    try:
        return costo_diario * duracion * 0.2
    except Exception as e:
        print(f"Error al calcular costo de vuelo: {e}")
        return 0

def calcular_costo_alojamiento(duracion, costo_diario):
    try:
        return costo_diario * duracion * 0.3
    except Exception as e:
        print(f"Error al calcular costo de alojamiento: {e}")
        return 0

def generar_checklist_viaje(destino, duración, costo_diario):
    fecha_actual = datetime.date.today()
    costo_total_usd = calcular_costo_total(destino, duración, costo_diario)
    costo_total_mxn = calcular_costo_total_mexico(destino, duración, costo_diario)
    costo_vuelo = calcular_costo_vuelo(duracion, costo_diario)
    costo_alojamiento = calcular_costo_alojamiento(duracion, costo_diario)

    print(f"Destino: {destino}")
    print(f"Fecha de viaje: {fecha_actual}")
    print(f"Duración: {duracion} días")
    print(f"Costo diario: {costo_diario} MXN")
    print(f"Costo total USD: {costo_total_usd} USD ({costo_total_mxn} MXN)")
    print(f"Precio del dólar: {extraer_precios()}")
    print(f"Costo de vuelo: {costo_vuelo} MXN")
    print(f"Costo de alojamiento: {costo_alojamiento} MXN")
    print(f"Costo de comida: {costo_diario * duracion * 0.5} MXN")
    print(f"Costo de transporte: {costo_diario * duracion * 0.1} MXN")
    print(f"Costo de entretenimiento: {costo_diario * duracion * 0.1} MXN")
    print(f"Resumen ejecutivo:")
    print(f"El costo total del viaje es de {costo_total_mxn} MXN")
    print(f"El costo del vuelo es de {costo_vuelo} MXN")
    print(f"El costo del alojamiento es de {costo_alojamiento} MXN")

def main():
    if len(sys.argv) != 4:
        print("Uso: python generador_checklist_viaje.py <destino> <duracion> <costo_diario>")
    else:
        destino = sys.argv[1]
        duracion = int(sys.argv[2])
        costo_diario = float(sys.argv[3])
        generar_checklist_viaje(destino, duracion, costo_diario)

if __name__ == "__main__":
    main()