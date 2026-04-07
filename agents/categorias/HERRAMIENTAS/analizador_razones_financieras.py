"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza analizador razones financieras
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_razones_financieras(ventas, costos, gastos, activos, pasivos):
    try:
        # Calcular razón de liquidez
        liquidez = activos / pasivos

        # Calcular razón de endeudamiento
        endeudamiento = pasivos / activos

        # Calcular margen de utilidad neta
        utilidad_neta = (ventas - costos - gastos) / ventas

        # Calcular retorno sobre la inversión (ROI)
        roi = (utilidad_neta * ventas) / activos

        # Calcular razón de cobertura de intereses
        intereses = (pasivos * 0.12) / utilidad_neta  # 12% de interés anual

        # Calcular razón de cobertura de dividendos
        dividendos = (activos * 0.05) / utilidad_neta  # 5% de dividendos anuales

        return {
            "liquidez": liquidez,
            "endeudamiento": endeudamiento,
            "utilidad_neta": utilidad_neta,
            "roi": roi,
            "intereses": intereses,
            "dividendos": dividendos
        }
    except ZeroDivisionError:
        return {
            "error": "No se puede dividir por cero"
        }
    except Exception as e:
        return {
            "error": str(e)
        }

def main():
    if __name__ == "__main__":
        # Parámetros por defecto
        ventas = 1000000
        costos = 600000
        gastos = 150000
        activos = 500000
        pasivos = 200000

        # Obtener parámetros de la línea de comandos
        if len(sys.argv) > 1:
            ventas = int(sys.argv[1])
        if len(sys.argv) > 2:
            costos = int(sys.argv[2])
        if len(sys.argv) > 3:
            gastos = int(sys.argv[3])
        if len(sys.argv) > 4:
            activos = int(sys.argv[4])
        if len(sys.argv) > 5:
            pasivos = int(sys.argv[5])

        # Calcular razones financieras
        razones_financieras = calcular_razones_financieras(ventas, costos, gastos, activos, pasivos)

        # Imprimir resultados
        print("ÁREA: FINANZAS")
        print("DESCRIPCIÓN: Agente que realiza analizador razones financieras")
        print("TECNOLOGÍA: Python estándar")
        print("\nRazones Financieras:")
        print(f"Liquidez: {razones_financieras.get('liquidez', 0):.2f}")
        print(f"Endeudamiento: {razones_financieras.get('endeudamiento', 0):.2f}")
        print(f"Margen de Utilidad Neta: {razones_financieras.get('utilidad_neta', 0):.2%}")
        print(f"Retorno sobre la Inversión (ROI): {razones_financieras.get('roi', 0):.2f}")
        print(f"Cobertura de Intereses: {razones_financieras.get('intereses', 0):.2f}")
        print(f"Cobertura de Dividendos: {razones_financieras.get('dividendos', 0):.2f}")

        # Resumen ejecutivo
        if razones_financieras.get('liquidez', 0) > 1:
            print("\nResumen Ejecutivo:")
            print("La empresa cuenta con una liquidez adecuada para cubrir sus compromisos a corto plazo.")
        else:
            print("\nResumen Ejecutivo:")
            print("La empresa cuenta con una liquidez insuficiente para cubrir sus compromisos a corto plazo.")

        if razones_financieras.get('endeudamiento', 0) < 0.5:
            print("\nResumen Ejecutivo:")