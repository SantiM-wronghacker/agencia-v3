"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza reporte avaluo básico con cálculos mejorados para el mercado inmobiliario mexicano
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_valor_m2(metros, habitaciones, banos, zona):
    base = 12000 if zona.lower() == "cdmx" else 9000
    ajuste_metros = 1 - (0.001 * max(0, 100 - metros))
    ajuste_hab = 1 + (0.1 * min(habitaciones, 4))
    ajuste_banos = 1 + (0.05 * min(banos, 3))
    valor_m2 = base * ajuste_metros * ajuste_hab * ajuste_banos
    return max(8000, min(25000, valor_m2))

def main():
    try:
        # Parámetros por defecto
        direccion = sys.argv[1] if len(sys.argv) > 1 else "Av. Revolución 123, CDMX"
        metros = float(sys.argv[2]) if len(sys.argv) > 2 else 85.5
        habitaciones = int(sys.argv[3]) if len(sys.argv) > 3 else 2
        banos = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        zona = sys.argv[5] if len(sys.argv) > 5 else "CDMX"

        # Validaciones
        if metros <= 0 or metros > 500:
            raise ValueError("Área inválida (0-500 m²)")
        if habitaciones < 1 or habitaciones > 10:
            raise ValueError("Número de habitaciones inválido (1-10)")
        if banos < 1 or banos > 5:
            raise ValueError("Número de baños inválido (1-5)")

        # Cálculos mejorados
        valor_m2 = calcular_valor_m2(metros, habitaciones, banos, zona)
        valor_terreno = metros * valor_m2
        valor_por_hab = habitaciones * 50000
        valor_por_bano = banos * 30000
        valor_total = valor_terreno + valor_por_hab + valor_por_bano

        # Ajustes por ubicación
        if zona.lower() == "cdmx":
            valor_total *= 1.15
        elif zona.lower() == "zona metropolitana":
            valor_total *= 1.05

        # Fecha de generación
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Reporte detallado
        print("=== REPORTE DE AVALUO BÁSICO ===")
        print(f"Dirección: {direccion}")
        print(f"Metros cuadrados: {metros:.1f} m²")
        print(f"Habitaciones: {habitaciones}")
        print(f"Baños: {banos}")
        print(f"Zona: {zona}")
        print(f"Valor estimado por m²: ${valor_m2:,.2f} MXN")
        print(f"Valor por habitaciones: ${valor_por_hab:,.2f} MXN")
        print(f"Valor por baños: ${valor_por_bano:,.2f} MXN")
        print(f"Valor del terreno: ${valor_terreno:,.2f} MXN")
        print(f"Valor total estimado: ${valor_total:,.2f} MXN")
        print(f"Generado el: {fecha}")

        # Resumen ejecutivo
        print("\n=== RESUMEN EJECUTIVO ===")
        print(f"Propiedad en {zona} con {habitaciones} habitaciones y {banos} baños")
        print(f"Valor estimado por m²: ${valor_m2:,.2f} MXN")
        print(f"Valor total estimado: ${valor_total:,.2f} MXN")
        print(f"Recomendación: {random.choice(['Excelente oportunidad', 'Valor justo', 'Considerar negociación'])}")

    except ValueError as ve:
        print(f"Error de validación: {str(ve)}")
        print