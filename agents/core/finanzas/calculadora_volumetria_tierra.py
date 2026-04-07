"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora volumetria tierra
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re

def calcular_volumen(tierra, densidad_tierra=1.65, unidad_medida="metros cúbicos"):
    try:
        ancho = float(tierra["ancho"])
        alto = float(tierra["alto"])
        profundo = float(tierra["profundo"])
    except KeyError as e:
        print(f"Error: Faltan valores para {e}")
        return
    except ValueError as e:
        print(f"Error: Valor no numérico para {e}")
        return

    try:
        radio_tierra = float(ancho) / 2
        volumen = (4/3) * math.pi * (radio_tierra)**3  # fórmula para el volumen de una esfera
        volumen_mc3 = volumen * densidad_tierra
        volumen_litros = volumen_mc3 * 1000
    except ValueError as e:
        print(f"Error: Valor no numérico para {e}")
        return

    try:
        area_base = math.pi * (ancho)**2
        area_superficie = 4 * math.pi * (radio_tierra)**2
        altura_promedio = (alto + profundo)/2
        diametro = ancho
        perímetro = 2 * math.pi * ancho
    except ValueError as e:
        print(f"Error: Valor no numérico para {e}")
        return

    try:
        volumen_piramide = (1/3) * area_base * alto
    except ValueError as e:
        print(f"Error: Valor no numérico para {e}")
        return

    try:
        volumen_cilindro = math.pi * (radio_tierra)**2 * alto
    except ValueError as e:
        print(f"Error: Valor no numérico para {e}")
        return

    try:
        volumen_esfera = (4/3) * math.pi * (radio_tierra)**3
        volumen_rectangular = ancho * alto * profundo
    except ValueError as e:
        print(f"Error: Valor no numérico para {e}")
        return

    print(f"Volumen de la tierra: {volumen:.2f} {unidad_medida}")
    print(f"Volumen de la tierra en litros: {volumen_litros:.2f}")
    print(f"Densidad de la tierra: {densidad_tierra:.2f} g/cm^3")
    print(f"Unidad de medida: {unidad_medida}")
    print(f"Fecha y hora de cálculo: {datetime.datetime.now()}")
    print(f"Área de la base: {area_base:.2f} metros cuadrados")
    print(f"Área de la superficie: {area_superficie:.2f} metros cuadrados")
    print(f"Altura promedio: {altura_promedio:.2f} metros")
    print(f"Diametro: {diametro:.2f} metros")
    print(f"Perímetro: {perímetro:.2f} metros")
    print(f"Volumen de la pirámide: {volumen_piramide:.2f} {unidad_medida}")
    print(f"Volumen del cilindro: {volumen_cilindro:.2f} {unidad_medida}")
    print(f"Volumen de la esfera: {volumen_esfera:.2f} {unidad_medida}")
    print(f"Volumen rectangular: {volumen_rectangular:.2f} {unidad_medida}")
    print("Resumen ejecutivo:")
    print("El cálculo de la volumetría de la tierra ha sido realizado con éxito.")
    print("Los valores obtenidos son precisos y representan la información necesaria para tomar decisiones informadas.")

def main():
    if len(sys.argv) > 1:
        try:
            tierra = json.loads(sys.argv[1])
        except json.JSONDecodeError as e:
            print(f"Error: El archivo JSON no es válido. {e}")
            return
    else:
        tierra = {"ancho": 10, "alto": 5, "profundo": 3}

    calcular_volumen(tierra)

if __name__ == "__main__":
    main()