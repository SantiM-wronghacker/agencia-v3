"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza generador estrategia referidos
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

def calcular_comision_diaria_promedio(comision_total, dias):
    return comision_total / dias

def calcular_monto_referido(porcentaje_comision, monto_promedio):
    return monto_promedio * (porcentaje_comision / 100)

def main():
    try:
        # Parámetros por defecto
        num_referidos = int(sys.argv[1]) if len(sys.argv) > 1 else 100
        porcentaje_comision = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
        monto_promedio = float(sys.argv[3]) if len(sys.argv) > 3 else 500.0
        dias = int(sys.argv[4]) if len(sys.argv) > 4 else 30

        # Validar parámetros
        if num_referidos <= 0:
            raise ValueError("Número de referidos debe ser mayor que 0")
        if porcentaje_comision < 0 or porcentaje_comision > 100:
            raise ValueError("Porcentaje de comisión debe estar entre 0 y 100")
        if monto_promedio <= 0:
            raise ValueError("Monto promedio debe ser mayor que 0")
        if dias <= 0:
            raise ValueError("Número de días debe ser mayor que 0")

        # Generar estrategia de referidos
        estrategia = {
            "num_referidos": num_referidos,
            "porcentaje_comision": porcentaje_comision,
            "monto_promedio": monto_promedio,
            "comision_total": num_referidos * monto_promedio * (porcentaje_comision / 100),
            "fecha_inicio": datetime.datetime.now().strftime("%Y-%m-%d"),
            "fecha_fin": (datetime.datetime.now() + datetime.timedelta(days=dias)).strftime("%Y-%m-%d"),
            "comision_diaria_promedio": calcular_comision_diaria_promedio(num_referidos * monto_promedio * (porcentaje_comision / 100), dias),
            "monto_referido": calcular_monto_referido(porcentaje_comision, monto_promedio),
            "comision_dia": num_referidos * monto_promedio * (porcentaje_comision / 100) / dias
        }

        # Imprimir resultados
        print(f"ÁREA: MARKETING")
        print(f"DESCRIPCIÓN: Agente que realiza generador estrategia referidos")
        print(f"TECNOLOGÍA: Python estándar")
        print(f"")
        print(f"Parámetros:")
        print(f"  Número de referidos: {estrategia['num_referidos']}")
        print(f"  Porcentaje de comisión: {estrategia['porcentaje_comision']}%")
        print(f"  Monto promedio por referido: ${estrategia['monto_promedio']:.2f} MXN")
        print(f"  Número de días: {estrategia['dias']}")
        print(f"")
        print(f"Resultados:")
        print(f"  Comisión total: ${estrategia['comision_total']:.2f} MXN")
        print(f"  Fecha de inicio: {estrategia['fecha_inicio']}")
        print(f"  Fecha de fin: {estrategia['fecha_fin']}")
        print(f"  Comisión diaria promedio: ${estrategia['comision_diaria_promedio']:.2f} MXN")
        print(f"  Monto referido por referido: ${estrategia['monto_referido']:.2f} MXN")
        print(f"  Comisión diaria: ${estrategia['comision_dia']:.2f} MXN")
        print(f"")
        print(f"Resumen ejecutivo:")
        print(f"La estrategia de referidos prevista generará una comisión total de ${estrategia['comision_total']:.2f} MXN en un período de {estrategia['dias']} días, con una comisión diaria promedio de ${estrategia['comision_diaria_promedio']:.2f} MXN.")

    except ValueError as e:
        print(f"Error: {e}")