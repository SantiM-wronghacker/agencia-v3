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
        if sueldo_anual < 0:
            raise ValueError("Sueldo anual no puede ser negativo")
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
    except ValueError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Error en cálculo de ISR: {e}")

def calcular_imss(sueldo_anual, año=2023):
    """Cálculo de IMSS anual con tope """
    try:
        if sueldo_anual < 0:
            raise ValueError("Sueldo anual no puede ser negativo")
        tope = 25000
        if sueldo_anual <= tope:
            return sueldo_anual * 0.065
        else:
            return tope * 0.065
    except ValueError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Error en cálculo de IMSS: {e}")

def calcular_subsidio(sueldo_anual, año=2023):
    """Cálculo de subsidio anual"""
    try:
        if sueldo_anual < 0:
            raise ValueError("Sueldo anual no puede ser negativo")
        if sueldo_anual <= 5000:
            return sueldo_anual * 0.1
        else:
            return 500
    except ValueError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Error en cálculo de subsidio: {e}")

def main():
    sueldo_anual = float(sys.argv[1]) if len(sys.argv) > 1 else 50000
    año = int(sys.argv[2]) if len(sys.argv) > 2 else 2023
    isr = calcular