"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza generador estado resultados
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
from datetime import datetime
import math
import re
import random

def generar_estado_resultados(inflacion, tasa_interes, cotizacion_dolar, precio_oro, precio_petroleo, noticias):
    try:
        # Calcula algunos indicadores financieros
        inflacion_anual = (math.pow(1 + inflacion / 100, 12) - 1) * 100
        tasa_de_interes_efectiva = (1 + tasa_interes / 100) ** 12 - 1

        # Imprime el estado de resultados
        print(f"Inflación anual: {inflacion_anual}%")
        print(f"Tasa de interés efectiva: {tasa_de_interes_efectiva * 100}%")
        print(f"Cotización del dólar: {cotizacion_dolar} pesos")
        print(f"Precio del oro: {precio_oro} pesos")
        print(f"Precio del petróleo: {precio_petroleo} pesos")
        print(f"Noticias financieras: {noticias}")

        # Calcula otros indicadores financieros
        ipc_anual = (math.pow(1 + inflacion_anual / 100, 12) - 1) * 100
        reajuste_salarios = ipc_anual * 0.5
        print(f"IPC anual: {ipc_anual}%")
        print(f"Reajuste de salarios: {reajuste_salarios}%")

        # Indicadores de liquidez
        liquidez_corriente = 1000000 * (1 + tasa_de_interes_efectiva)
        liquidez_corriente_anual = 1000000 * (1 + tasa_de_interes_efectiva) ** 12
        print(f"Liquidez corriente: {liquidez_corriente}")
        print(f"Liquidez corriente anual: {liquidez_corriente_anual}")

        # Indicadores de solvencia
        solvencia = 1000000 * (1 + tasa_de_interes_efectiva)
        solvencia_anual = 1000000 * (1 + tasa_de_interes_efectiva) ** 12
        print(f"Solvencia: {solvencia}")
        print(f"Solvencia anual: {solvencia_anual}")

        # Indicadores de rentabilidad
        rentabilidad = 0.1 * (1 + tasa_de_interes_efectiva)
        rentabilidad_anual = rentabilidad * 12
        print(f"Rentabilidad: {rentabilidad * 100}%")
        print(f"Rentabilidad anual: {rentabilidad_anual * 100}%")

        # Resumen ejecutivo
        resumen_ejecutivo = f"Inflación anual: {inflacion_anual}%\nTasa de interés efectiva: {tasa_de_interes_efectiva * 100}%\nIPC anual: {ipc_anual}%\nReajuste de salarios: {reajuste_salarios}%\nLiquidez corriente: {liquidez_corriente}\nSolvencia: {solvencia}\nRentabilidad: {rentabilidad * 100}%\n"
        print(f"Resumen ejecutivo:\n{resumen_ejecutivo}")

    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) != 7:
        print("Uso: python generador_estado_resultados.py <inflacion> <tasa_interes> <cotizacion_dolar> <precio_oro> <precio_petroleo> <noticias>")
        sys.exit(1)

    try:
        inflacion = float(sys.argv[1])
        tasa_interes = float(sys.argv[2])
        cotizacion_dolar = float(sys.argv[3])
        precio_oro = float(sys.argv[4])
        precio_petroleo = float(sys.argv[5])
        noticias = sys.argv[6]
    except ValueError:
        print("Error: los valores deben ser números")
        sys.exit(1)

    generar_estado_resultados(inflacion, tasa_interes, cotizacion_dolar, precio_oro, precio_petroleo, noticias)

if __name__ == "__main__":
    main()