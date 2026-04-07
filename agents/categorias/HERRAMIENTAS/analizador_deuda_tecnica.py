"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza analizador deuda tecnica
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_deuda_tecnica(inversion, tasa_interes, plazo):
    return inversion * (1 + tasa_interes) ** plazo

def calcular_costo_mantenimiento(deuda_tecnica, tasa_mantenimiento):
    return deuda_tecnica * tasa_mantenimiento

def calcular_impuestos(deuda_tecnica, tasa_impuesto):
    return deuda_tecnica * tasa_impuesto

def calcular_seguros(deuda_tecnica, tasa_seguro):
    return deuda_tecnica * tasa_seguro

def calcular_total_deuda_tecnica(inversion, tasa_interes, plazo, tasa_mantenimiento, tasa_impuesto, tasa_seguro):
    deuda_tecnica = calcular_deuda_tecnica(inversion, tasa_interes, plazo)
    costo_mantenimiento = calcular_costo_mantenimiento(deuda_tecnica, tasa_mantenimiento)
    impuestos = calcular_impuestos(deuda_tecnica, tasa_impuesto)
    seguros = calcular_seguros(deuda_tecnica, tasa_seguro)
    return deuda_tecnica + costo_mantenimiento + impuestos + seguros

def main():
    try:
        inversion = float(sys.argv[1]) if len(sys.argv) > 1 else 1000000.0
        tasa_interes = float(sys.argv[2]) if len(sys.argv) > 2 else 0.05
        plazo = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        tasa_mantenimiento = float(sys.argv[4]) if len(sys.argv) > 4 else 0.01
        tasa_impuesto = float(sys.argv[5]) if len(sys.argv) > 5 else 0.02
        tasa_seguro = float(sys.argv[6]) if len(sys.argv) > 6 else 0.005

        deuda_tecnica = calcular_deuda_tecnica(inversion, tasa_interes, plazo)
        costo_mantenimiento = calcular_costo_mantenimiento(deuda_tecnica, tasa_mantenimiento)
        impuestos = calcular_impuestos(deuda_tecnica, tasa_impuesto)
        seguros = calcular_seguros(deuda_tecnica, tasa_seguro)
        total_deuda_tecnica = calcular_total_deuda_tecnica(inversion, tasa_interes, plazo, tasa_mantenimiento, tasa_impuesto, tasa_seguro)

        print("Resumen Ejecutivo:")
        print("--------------------")
        print(f"Inversión inicial: ${inversion:.2f} MXN")
        print(f"Tasa de interés anual: {tasa_interes*100:.2f}%")
        print(f"Plazo de inversión: {plazo} años")
        print("--------------------")
        print(f"Deuda técnica: ${deuda_tecnica:.2f} MXN")
        print(f"Costo de mantenimiento: ${costo_mantenimiento:.2f} MXN")
        print(f"Impuestos: ${impuestos:.2f} MXN")
        print(f"Seguros: ${seguros:.2f} MXN")
        print(f"Total deuda técnica con mantenimiento: ${deuda_tecnica + costo_mantenimiento:.2f} MXN")
        print(f"Total deuda técnica con mantenimiento e impuestos: ${deuda_tecnica + costo_mantenimiento + impuestos:.2f} MXN")
        print(f"Total deuda técnica con mantenimiento, impuestos y seguros: ${total_deuda_tecnica:.2f} MXN")
    except IndexError:
        print("Error: No se proporcionaron suficientes argumentos.")
    except ValueError:
        print("Error: Los argumentos deben ser números.")

if __name__ == "__main__":
    main()