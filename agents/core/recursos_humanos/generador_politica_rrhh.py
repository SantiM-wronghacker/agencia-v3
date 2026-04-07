"""
ÁREA: RRHH
DESCRIPCIÓN: Agente que realiza generador politica rrhh
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def calcular_salario_minimo(datos):
    try:
        return datos["salario_minimo"]
    except KeyError:
        return 2600

def calcular_tasa_inflacion(datos):
    try:
        return datos["tasa_inflacion"]
    except KeyError:
        return 3.5

def calcular_desempleo(datos):
    try:
        return datos["desempleo"]
    except KeyError:
        return 4.2

def calcular_tipo_cambio(datos):
    try:
        return datos["tipo_cambio"]
    except KeyError:
        return 20.5

def calcular_noticias(datos):
    try:
        return datos["noticias"]
    except KeyError:
        return "No hay noticias disponibles"

def calcular_indice_pobreza(datos):
    try:
        return datos["indice_pobreza"]
    except KeyError:
        return 45.5

def calcular_indice_desarrollo_humano(datos):
    try:
        return datos["indice_desarrollo_humano"]
    except KeyError:
        return 0.756

def calcular_tasa_participacion_femenina(datos):
    try:
        return datos["tasa_participacion_femenina"]
    except KeyError:
        return 45.2

def main():
    try:
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'r') as archivo:
                datos = json.load(archivo)
        else:
            datos = {
                "salario_minimo": 2600,
                "tasa_inflacion": 3.5,
                "desempleo": 4.2,
                "tipo_cambio": 20.5,
                "noticias": "No hay noticias disponibles",
                "indice_pobreza": 45.5,
                "indice_desarrollo_humano": 0.756,
                "tasa_participacion_femenina": 45.2
            }

        salario_minimo = calcular_salario_minimo(datos)
        tasa_inflacion = calcular_tasa_inflacion(datos)
        desempleo = calcular_desempleo(datos)
        tipo_cambio = calcular_tipo_cambio(datos)
        noticias = calcular_noticias(datos)
        indice_pobreza = calcular_indice_pobreza(datos)
        indice_desarrollo_humano = calcular_indice_desarrollo_humano(datos)
        tasa_participacion_femenina = calcular_tasa_participacion_femenina(datos)

        print("Política RRHH:")
        print(f"Salario mínimo: ${salario_minimo:.2f} MXN")
        print(f"Tasa de inflación: {tasa_inflacion}%")
        print(f"Desempleo: {desempleo}%")
        print(f"Tipo de cambio: 1 USD = {tipo_cambio} MXN")
        print(f"Noticias: {noticias}")
        print(f"Índice de pobreza: {indice_pobreza}%")
        print(f"Índice de desarrollo humano: {indice_desarrollo_humano}")
        print(f"Tasa de participación femenina: {tasa_participacion_femenina}%")

        print("\nResumen Ejecutivo:")
        print(f"La política RRHH se enfoca en mantener un salario mínimo de ${salario_minimo:.2f} MXN,")
        print(f"una tasa de inflación del {tasa_inflacion}%, y un desempleo del {desempleo}%. ")
        print(f"Además, se busca mejorar el índice de pobreza y el índice de desarrollo humano, ")
        print(f"y aumentar la tasa de participación femenina en el mercado laboral.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()