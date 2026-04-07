"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora prima
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def calcular_prima(edad, sexo, peso, altura, hipertension, tabaquismo, precio_seguro):
    # Calcula la prima
    if sexo == 'M':
        prima = (edad * 10) + (peso * 5) + (altura * 2)
    else:
        prima = (edad * 10) + (peso * 5)

    if hipertension:
        prima += 500
    if tabaquismo:
        prima += 1000

    prima = prima * (precio_seguro / 100)

    return prima

def calcular_imss(edad, sexo, peso, altura):
    # Calcula la prima del IMSS
    if sexo == 'M':
        prima_imss = (edad * 5) + (peso * 2) + (altura * 1)
    else:
        prima_imss = (edad * 5) + (peso * 2)

    return prima_imss

def calcular_prima_inei(edad, sexo, peso, altura, hipertension, tabaquismo):
    # Calcula la prima del INEI
    if sexo == 'M':
        prima_inei = (edad * 8) + (peso * 4) + (altura * 3)
    else:
        prima_inei = (edad * 8) + (peso * 4)

    if hipertension:
        prima_inei += 700
    if tabaquismo:
        prima_inei += 1200

    return prima_inei

def main():
    try:
        if len(sys.argv)!= 9:
            print("Error: Faltan argumentos. Ejemplo: python calculadora_prima.py 35 M 70 1.75 True False 1000 20 1.8")
            sys.exit(1)

        edad = int(sys.argv[1])
        sexo = sys.argv[2]
        peso = int(sys.argv[3])
        altura = float(sys.argv[4])
        hipertension = sys.argv[5] == "True"
        tabaquismo = sys.argv[6] == "True"
        precio_seguro = int(sys.argv[7])
        edad_imss = int(sys.argv[8])
        altura_imss = float(sys.argv[9])

        prima = calcular_prima(edad, sexo, peso, altura, hipertension, tabaquismo, precio_seguro)
        prima_imss = calcular_imss(edad_imss, sexo, peso, altura_imss)
        prima_inei = calcular_prima_inei(edad, sexo, peso, altura, hipertension, tabaquismo)

        print(f"Prima de seguro: {prima:.2f} pesos")
        print(f"Prima de IMSS: {prima_imss:.2f} pesos")
        print(f"Prima de INEI: {prima_inei:.2f} pesos")
        print(f"Edad: {edad} años")
        print(f"Sexo: {sexo}")
        print(f"Peso: {peso} kg")
        print(f"Altura: {altura:.2f} m")
        print(f"Hipertensión: {hipertension}")
        print(f"Tabaquismo: {tabaquismo}")
        print(f"Precio de seguro: {precio_seguro} pesos")
        print(f"Resumen ejecutivo: El costo total de la prima de seguro es de {prima:.2f} pesos, considerando una edad de {edad} años, sexo {sexo}, peso {peso} kg, altura {altura:.2f} m, hipertensión {hipertension} y tabaquismo {tabaquismo}. El costo de la prima de IMSS es de {prima_imss:.2f} pesos y el costo de la prima de INEI es de {prima_inei:.2f} pesos.")

    except ValueError:
        print("Error: Los argumentos deben ser números enteros o flotantes.")
        sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()