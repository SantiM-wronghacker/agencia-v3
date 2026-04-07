import sys
import os
import json
import datetime
import math
import re
import random

# ARCHIVO: generador_descripcion_puesto.py
# AREA: HERRAMIENTAS
# DESCRIPCION: Generador Descripcion Puesto
# TECNOLOGIA: Python

def calcular_isr(sueldo_anual, año=2023):
    """Cálculo del ISR anual según tabla 2023 México"""
    try:
        if sueldo_anual <= 758.75:
            return sueldo_anual * 0.0192
        elif sueldo_anual <= 1046.08:
            return 14.45 + (sueldo_anual - 758.75) * 0.064
        elif sueldo_anual <= 1379.88:
            return 47.73 + (sueldo_anual - 1046.08) * 0.08
        elif sueldo_anual <= 1654.54:
            return 81.73 + (sueldo_anual - 1379.88) * 0.103
        elif sueldo_anual <= 2137.21:
            return 136.98 + (sueldo_anual - 1654.54) * 0.12
        elif sueldo_anual <= 3205.82:
            return 246.98 + (sueldo_anual - 2137.21) * 0.142
        elif sueldo_anual <= 4537.14:
            return 444.21 + (sueldo_anual - 3205.82) * 0.164
        elif sueldo_anual <= 9726.81:
            return 719.68 + (sueldo_anual - 4537.14) * 0.179
        elif sueldo_anual <= 12968.47:
            return 1485.96 + (sueldo_anual - 9726.81) * 0.2136
        elif sueldo_anual <= 24185.57:
            return 2331.83 + (sueldo_anual - 12968.47) * 0.2352
        elif sueldo_anual <= 37658.32:
            return 4693.53 + (sueldo_anual - 24185.57) * 0.3
        elif sueldo_anual <= 72349.50:
            return 9381.13 + (sueldo_anual - 37658.32) * 0.32
        elif sueldo_anual <= 97268.10:
            return 19136.73 + (sueldo_anual - 72349.50) * 0.34
        else:
            return 27063.93 + (sueldo_anual - 97268.10) * 0.35
    except ValueError:
        print("Error: Sueldo anual debe ser un número.")
        return None
    except Exception as e:
        print(f"Error en cálculo de ISR: {e}")

def calcular_imss(sueldo_anual, año=2023):
    """Cálculo de IMSS anual con tope máximo"""
    umbral = 25 * 730.55  # 25 UMA 2023
    if sueldo_anual > umbral:
        sueldo_anual = umbral
    return sueldo_anual * 0.0625

def calcular_imss_adicional(sueldo_anual, año=2023):
    """Cálculo de IMSS adicional"""
    umbral = 25 * 730.55  # 25 UMA 2023
    if sueldo_anual > umbral:
        sueldo_anual = umbral
    return sueldo_anual * 0.01

def main():
    if len(sys.argv)!= 2:
        print("Uso: python generador_descripcion_puesto.py <sueldo_anual>")
        return

    try:
        sueldo_anual = float(sys.argv[1])
    except ValueError:
        print("Error: Sueldo anual debe ser un número.")
        return

    isr = calcular_isr(sueldo_anual)
    imss = calcular_imss(sueldo_anual)
    imss_adicional = calcular_imss_adicional(sueldo_anual)

    print(f"Sueldo anual: {sueldo_anual:.2f}")
    print(f"ISR: {isr:.2f}")
    print(f"IMSS: {imss:.2f}")
    print(f"IMSS adicional: {imss_adicional:.2f}")
    print