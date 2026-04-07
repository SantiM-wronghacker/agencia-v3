"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza simulador fondo emergencia
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_fondo_emergencia(ingreso_mensual, gastos_fijos, ahorro_mensual, meses):
    fondo_emergencia = 0
    for _ in range(meses):
        fondo_emergencia += ahorro_mensual
        gastos_fijos_mensuales = gastos_fijos / 12
        fondo_emergencia -= gastos_fijos_mensuales
        if fondo_emergencia < 0:
            fondo_emergencia = 0
    return fondo_emergencia

def calcular_interes(fondo_emergencia, tasa_interes, meses):
    interes = fondo_emergencia * tasa_interes / 100 * meses / 12
    return interes

def calcular_impuesto_renta(fondo_emergencia):
    if fondo_emergencia > 0:
        impuesto_renta = fondo_emergencia * 0.01  # 1% de impuesto sobre la renta
    else:
        impuesto_renta = 0
    return impuesto_renta

def calcular_inflacion(fondo_emergencia, tasa_inflacion, meses):
    inflacion = fondo_emergencia * tasa_inflacion / 100 * meses / 12
    return inflacion

def main():
    try:
        ingreso_mensual = float(sys.argv[1]) if len(sys.argv) > 1 else 25000.0
        gastos_fijos = float(sys.argv[2]) if len(sys.argv) > 2 else 120000.0
        ahorro_mensual = float(sys.argv[3]) if len(sys.argv) > 3 else 5000.0
        meses = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        tasa_interes = float(sys.argv[5]) if len(sys.argv) > 5 else 4.0
        tasa_inflacion = float(sys.argv[6]) if len(sys.argv) > 6 else 3.0
        
        fondo_emergencia = calcular_fondo_emergencia(ingreso_mensual, gastos_fijos, ahorro_mensual, meses)
        interes = calcular_interes(fondo_emergencia, tasa_interes, meses)
        impuesto_renta = calcular_impuesto_renta(fondo_emergencia)
        inflacion = calcular_inflacion(fondo_emergencia, tasa_inflacion, meses)
        
        print(f"Ingreso mensual: ${ingreso_mensual:.2f} MXN")
        print(f"Gastos fijos anuales: ${gastos_fijos:.2f} MXN")
        print(f"Ahorro mensual: ${ahorro_mensual:.2f} MXN")
        print(f"Meses de simulación: {meses} meses")
        print(f"Fondo de emergencia después de {meses} meses: ${fondo_emergencia:.2f} MXN")
        print(f"Interés ganado después de {meses} meses: ${interes:.2f} MXN")
        print(f"Impuesto sobre la renta: ${impuesto_renta:.2f} MXN")
        print(f"Inflación después de {meses} meses: ${inflacion:.2f} MXN")
        print(f"Valor real del fondo de emergencia después de {meses} meses: ${fondo_emergencia - impuesto_renta - inflacion:.2f} MXN")
        
        print("\nResumen Ejecutivo:")
        print(f"El fondo de emergencia después de {meses} meses es de ${fondo_emergencia:.2f} MXN.")
        print(f"El interés ganado después de {meses} meses es de ${interes:.2f} MXN.")
        print(f"El impuesto sobre la renta es de ${impuesto_renta:.2f} MXN.")
        print(f"La inflación después de {meses} meses es de ${inflacion:.2f} MXN.")
        print(f"El valor real del fondo de emergencia después de {meses} meses es de ${fondo_emergencia - impuesto_renta - inflacion:.2f} MXN.")
        
    except Exception as e:
        print(f"Error: {str(e)}")