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
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def calcular_prima(edad, sexo, peso, altura, hipertension, tabaquismo, precio_seguro):
    # Calcula la prima
    if sexo == 'M':
        prima = (edad * 12) + (peso * 6) + (altura * 2.5)
    else:
        prima = (edad * 12) + (peso * 6)

    if hipertension:
        prima += 800
    if tabaquismo:
        prima += 1500

    prima = prima * (precio_seguro / 100)

    return prima

def calcular_imss(edad, sexo, peso, altura):
    # Calcula la prima del IMSS
    if sexo == 'M':
        prima_imss = (edad * 6) + (peso * 2.5) + (altura * 1.2)
    else:
        prima_imss = (edad * 6) + (peso * 2.5)

    return prima_imss

def calcular_prima_inei(edad, sexo, peso, altura, hipertension, tabaquismo):
    # Calcula la prima del INEI
    if sexo == 'M':
        prima_inei = (edad * 10) + (peso * 5) + (altura * 3.5)
    else:
        prima_inei = (edad * 10) + (peso * 5)

    if hipertension:
        prima_inei += 1000
    if tabaquismo:
        prima_inei += 1800

    return prima_inei

def main():
    try:
        if len(sys.argv) != 11:
            print("Error: Faltan argumentos. Ejemplo: python calculadora_prima.py 35 M 70 1.75 True False 1000 20 1.8 30 1.9")
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
        sexo_imss = sys.argv[10]

        prima = calcular_prima(edad, sexo, peso, altura, hipertension, tabaquismo, precio_seguro)
        prima_imss = calcular_imss(edad_imss, sexo_imss, peso, altura_imss)
        prima_inei = calcular_prima_inei(edad, sexo, peso, altura, hipertension, tabaquismo)

        print("Prima del seguro: $", round(prima, 2))
        print("Prima del IMSS: $", round(prima_imss, 2))
        print("Prima del INEI: $", round(prima_inei, 2))

        if hipertension:
            print("El paciente tiene hipertensión.")
        else:
            print("El paciente no tiene hipertensión.")

        if tabaquismo:
            print("El paciente es fumador.")
        else:
            print("El paciente no es fumador.")

        print("Resumen ejecutivo:")
        print("La prima del seguro es mayor que la prima del IMSS.")
        print("La prima del seguro es mayor que la prima del INEI.")

    except IndexError:
        print("Error: Faltan argumentos.")
    except ValueError:
        print("Error: Los argumentos deben ser de tipo correcto.")

if __name__ == "__main__":
    main()