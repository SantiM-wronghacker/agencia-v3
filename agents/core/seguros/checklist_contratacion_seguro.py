"""
ÁREA: SEGUROS
DESCRIPCIÓN: Agente que realiza checklist contratación seguro
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_prima(edad, sexo, estado_civil):
    try:
        prima_base = 0
        if edad < 20:
            prima_base += 800
        elif edad < 25:
            prima_base += 600
        elif edad < 35:
            prima_base += 750
        elif edad < 45:
            prima_base += 1000
        elif edad < 55:
            prima_base += 1200
        else:
            prima_base += 1500

        if sexo == "M":
            prima_base += 250
        elif sexo == "F":
            prima_base += 200

        if estado_civil == "Casado":
            prima_base -= 100
        elif estado_civil == "Soltero":
            prima_base += 50
        elif estado_civil == "Divorciado":
            prima_base += 100
        elif estado_civil == "Viudo":
            prima_base += 150

        prima = prima_base * (1 + 0.10)  # 10% de prima adicional por riesgo
        return prima
    except ValueError:
        return "Error: Edad no válida"

def calcular_deducible(monto_asegurado):
    try:
        deducible = monto_asegurado * 0.10
        return deducible
    except ValueError:
        return "Error: Monto asegurado no válido"

def calcular_comision(prima):
    try:
        comision = prima * 0.05
        return comision
    except ValueError:
        return "Error: Prima no válida"

def calcular_iva(prima):
    try:
        iva = prima * 0.16
        return iva
    except ValueError:
        return "Error: Prima no válida"

def calcular_total(prima, comision, iva, deducible):
    try:
        total = prima + comision + iva + deducible
        return total
    except ValueError:
        return "Error: Cálculo no válido"

def calcular_premium(prima, deducible):
    try:
        premium = prima - deducible
        return premium
    except ValueError:
        return "Error: Cálculo no válido"

def main():
    if len(sys.argv) < 6:
        print("Error: Faltan argumentos")
        return

    edad = int(sys.argv[1])
    sexo = sys.argv[2]
    estado_civil = sys.argv[3]
    monto_asegurado = int(sys.argv[4])
    prima = calcular_prima(edad, sexo, estado_civil)
    deducible = calcular_deducible(monto_asegurado)
    comision = calcular_comision(prima)
    iva = calcular_iva(prima)
    total = calcular_total(prima, comision, iva, deducible)
    premium = calcular_premium(prima, deducible)

    print("Resumen de la contratación de seguro:")
    print(f"Edad: {edad} años")
    print(f"Sexo: {sexo}")
    print(f"Estado civil: {estado_civil}")
    print(f"Monto asegurado: ${monto_asegurado:,}")
    print(f"Prima: ${prima:,.2f}")
    print(f"Deducible: ${deducible:,.2f}")
    print(f"Comisión: ${comision:,.2f}")
    print(f"IVA: ${iva:,.2f}")
    print(f"Total: ${total:,.2f}")
    print(f"Premio: ${premium:,.2f}")
    print(f"Resumen ejecutivo: La prima total es de ${prima:,.2f}, con un deducible de ${deducible:,.2f} y una comisión de ${comision:,.2f}. El IVA es de ${iva:,.2f} y el total es de ${total:,.2f}. El premio es de ${premium:,.2f}.")

if __name__ == "__main__":
    main()