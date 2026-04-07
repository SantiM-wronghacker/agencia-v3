"""
ÁREA: AGRICULTURA
DESCRIPCIÓN: Agente que realiza planificador riego
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

def calcular_precipitacion():
    try:
        return round(random.uniform(0.1, 0.5), 2)
    except Exception as e:
        print(f"Error al calcular precipitación: {e}")
        return 0

def calcular_riego(precipitacion, umbral):
    try:
        if precipitacion < umbral:
            return round(10 * (umbral - precipitacion), 2)
        else:
            return 0
    except Exception as e:
        print(f"Error al calcular riego: {e}")
        return 0

def calcular_costo_riego(riego):
    try:
        return round(riego * 5, 2)
    except Exception as e:
        print(f"Error al calcular costo del riego: {e}")
        return 0

def calcular_eficiencia_riego(riego, area):
    try:
        if area > 0:
            return round(riego / area, 2)
        else:
            return 0
    except Exception as e:
        print(f"Error al calcular eficiencia del riego: {e}")
        return 0

def calcular_evapotranspiracion():
    try:
        return round(random.uniform(2.0, 5.0), 2)
    except Exception as e:
        print(f"Error al calcular evapotranspiración: {e}")
        return 0

def calcular_deficit_hidrico(riego, evapotranspiracion):
    try:
        return round(evapotranspiracion - riego, 2)
    except Exception as e:
        print(f"Error al calcular déficit hídrico: {e}")
        return 0

def main():
    try:
        if len(sys.argv) > 1:
            umbral = float(sys.argv[1])
        else:
            umbral = 0.2

        if len(sys.argv) > 2:
            area = float(sys.argv[2])
        else:
            area = 100

        if len(sys.argv) > 3:
            temperatura = float(sys.argv[3])
        else:
            temperatura = 25

        if len(sys.argv) > 4:
            humedad = float(sys.argv[4])
        else:
            humedad = 60

        precipitacion = calcular_precipitacion()
        riego = calcular_riego(precipitacion, umbral)
        costo_riego = calcular_costo_riego(riego)
        eficiencia_riego = calcular_eficiencia_riego(riego, area)
        evapotranspiracion = calcular_evapotranspiracion()
        deficit_hidrico = calcular_deficit_hidrico(riego, evapotranspiracion)

        print(f"Umbral de precipitación: {umbral} mm")
        print(f"Precipitación: {precipitacion} mm")
        print(f"Riego necesario: {riego} mm")
        print(f"Costo del riego: ${costo_riego}")
        print(f"Eficiencia del riego: {eficiencia_riego}")
        print(f"Evapotranspiración: {evapotranspiracion} mm")
        print(f"Déficit hídrico: {deficit_hidrico} mm")
        print(f"Temperatura: {temperatura} °C")
        print(f"Humedad: {humedad} %")
        print("Resumen ejecutivo:")
        print(f"El riego necesario es de {riego} mm, con un costo de ${costo_riego} y una eficiencia de {eficiencia_riego}.")
        print(f"La evapotranspiración es de {evapotranspiracion} mm y el déficit hídrico es de {deficit_hidrico} mm.")
        print(f"La temperatura es de {temperatura} °C y la humedad es de {humedad} %.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()