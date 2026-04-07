"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza comparador hipotecas bancos mexico
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

def calcular_cuota(monto, plazo, tasa):
    try:
        if monto <= 0 or plazo <= 0 or tasa <= 0:
            raise ValueError("Valores deben ser positivos")

        tasa_mensual = tasa / 100 / 12
        plazo_meses = plazo * 12

        cuota = monto * tasa_mensual * (1 + tasa_mensual) ** plazo_meses / ((1 + tasa_mensual) ** plazo_meses - 1)
        return cuota
    except Exception as e:
        raise ValueError(f"Error en cálculo: {str(e)}")

def obtener_tasas():
    # Tasas promedio actualizadas (2023)
    return {
        'banamex': 8.5,
        'santander': 9.2,
        'banorte': 8.8,
        'hsbc': 9.0,
        'bbva': 9.1
    }

def calcular_intereses_totales(monto, plazo, tasa):
    cuota = calcular_cuota(monto, plazo, tasa)
    plazo_meses = plazo * 12
    intereses = (cuota * plazo_meses) - monto
    return intereses

def main():
    try:
        # Parámetros por defecto
        monto = 500000
        plazo = 20

        # Obtener parámetros desde sys.argv
        if len(sys.argv) > 1:
            monto = float(sys.argv[1])
        if len(sys.argv) > 2:
            plazo = int(sys.argv[2])

        # Validar parámetros
        if monto <= 0 or plazo <= 0:
            raise ValueError("Monto y plazo deben ser positivos")

        # Obtener tasas
        tasas = obtener_tasas()

        # Calcular cuotas e intereses
        resultados = {}
        for banco, tasa in tasas.items():
            try:
                cuota = calcular_cuota(monto, plazo, tasa)
                intereses = calcular_intereses_totales(monto, plazo, tasa)
                resultados[banco] = {
                    'tasa': tasa,
                    'cuota_mensual': cuota,
                    'intereses_totales': intereses
                }
            except Exception as e:
                resultados[banco] = {'error': str(e)}

        # Encontrar banco más barato
        banco_mas_barato = min(
            (banco for banco in resultados if 'error' not in resultados[banco]),
            key=lambda x: resultados[x]['cuota_mensual']
        )

        # Imprimir resultados
        print(f"Comparador de Hipotecas México - {datetime.date.today().strftime('%d/%m/%Y')}")
        print(f"Monto del préstamo: ${monto:,.2f} MXN")
        print(f"Plazo del préstamo: {plazo} años")
        print("\nResultados por banco:")
        for banco, datos in resultados.items():
            if 'error' in datos:
                print(f"{banco.upper()}: Error en cálculo - {datos['error']}")
            else:
                print(f"{banco.upper()}:")
                print(f"  Tasa anual: {datos['tasa']}%")
                print(f"  Cuota mensual: ${datos['cuota_mensual']:,.2f} MXN")
                print(f"  Intereses totales: ${datos['intereses_totales']:,.2f} MXN")

        print("\nResumen Ejecutivo:")
        print(f"Banco con menor cuota: {banco_mas_barato.upper()}")
        print(f"Cuota mensual más baja: ${resultados[banco_mas_barato]['cuota_mensual']:,.2f} MXN")
        print(f"Diferencia con el banco más caro: ${resultados[banco_mas_barato]['cuota_mensual'] - max(d['cuota_mensual'] for d in resultados.values() if 'cuota_mensual' in d):,.2f} MXN")

    except Exception as e:
        print(f"Error general: {str(e)}")

if __name__ == "__main__":
    main()