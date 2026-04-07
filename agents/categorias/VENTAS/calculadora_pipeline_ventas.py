#!/usr/bin/env python3
# ÁREA: FINANZAS
# DESCRIPCIÓN: Agente que realiza calculadora pipeline ventas
# TECNOLOGÍA: Python estándar

import sys
import json
import math
from datetime import datetime
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        ventas_mes_actual = float(sys.argv[1]) if len(sys.argv) > 1 else 500000.0
        tasa_conversion = float(sys.argv[2]) if len(sys.argv) > 2 else 0.35
        dias_restantes = int(sys.argv[3]) if len(sys.argv) > 3 else 15
        meta_crecimiento = float(sys.argv[4]) if len(sys.argv) > 4 else 10.0
        impuesto_ventas = float(sys.argv[5]) if len(sys.argv) > 5 else 16.0  # IVA en México

        # Cálculos
        pipeline_actual = ventas_mes_actual / tasa_conversion
        pipeline_diario = pipeline_actual / dias_restantes
        meta_mes_siguiente = ventas_mes_actual * (1 + (meta_crecimiento / 100))
        pipeline_requerido = meta_mes_siguiente / tasa_conversion
        diferencia_pipeline = pipeline_requerido - pipeline_actual
        tasa_crecimiento = ((meta_mes_siguiente - ventas_mes_actual) / ventas_mes_actual) * 100
        ventas_neto = ventas_mes_actual * (1 - (impuesto_ventas / 100))
        ventas_bruta = ventas_mes_actual * (1 + (impuesto_ventas / 100))
        tasa_cambio_dolar = 20.0  # Tasa de cambio Dólar/MXN en México
        pipeline_diario_dolar = pipeline_diario * tasa_cambio_dolar

        # Salida
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"Ventas mes actual: ${ventas_mes_actual:,.2f} MXN")
        print(f"Ventas netas (después de IVA): ${ventas_neto:,.2f} MXN")
        print(f"Ventas brutas (antes de IVA): ${ventas_bruta:,.2f} MXN")
        print(f"Tasa de conversión: {tasa_conversion*100:.2f}%")
        print(f"Días restantes en el mes: {dias_restantes} días")
        print(f"Pipeline actual: ${pipeline_actual:,.2f} MXN")
        print(f"Pipeline diario requerido: ${pipeline_diario:,.2f} MXN")
        print(f"Pipeline diario requerido en dólares: ${pipeline_diario_dolar:,.2f} USD")
        print(f"Meta mes siguiente: ${meta_mes_siguiente:,.2f} MXN")
        print(f"Tasa de crecimiento: {meta_crecimiento:.2f}%")
        print(f"Tasa de crecimiento real: {tasa_crecimiento:.2f}%")
        print(f"Diferencia de pipeline: ${diferencia_pipeline:,.2f} MXN")
        print(f"Tasa de cambio Dólar/MXN: {tasa_cambio_dolar:.2f}")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"Se requiere un pipeline diario de ${pipeline_diario:,.2f} MXN para cumplir con la meta de ventas del mes siguiente.")
        print(f"La diferencia entre el pipeline actual y el requerido es de ${diferencia_pipeline:,.2f} MXN.")
        print(f"Se recomienda aumentar la tasa de conversión para alcanzar la meta de ventas.")

    except IndexError:
        print("Error: Faltan parámetros de entrada.")
    except ValueError:
        print("Error: Los parámetros de entrada deben ser números.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()