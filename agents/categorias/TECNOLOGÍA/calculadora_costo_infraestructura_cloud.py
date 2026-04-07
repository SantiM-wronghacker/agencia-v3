#!/usr/bin/env python3
"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora costo infraestructura cloud
TECNOLOGÍA: Python estándar
"""

import sys
import json
import math
from datetime import datetime

def main():
    try:
        # Parámetros por defecto
        region = sys.argv[1] if len(sys.argv) > 1 else "mexico"
        tipo_instancia = sys.argv[2] if len(sys.argv) > 2 else "t2.micro"
        horas_mes = int(sys.argv[3]) if len(sys.argv) > 3 else 730
        tipo_pago = sys.argv[4] if len(sys.argv) > 4 else "on-demand"
        impuesto_anual = float(sys.argv[5]) if len(sys.argv) > 5 else 0.16
        tasa_cambio = float(sys.argv[6]) if len(sys.argv) > 6 else 20.0  # MXN/USD

        # Precios en USD (ejemplo con AWS)
        precios = {
            "mexico": {
                "t2.micro": {"on-demand": 0.023, "reserved": 0.015},
                "t2.small": {"on-demand": 0.046, "reserved": 0.030},
                "t2.medium": {"on-demand": 0.092, "reserved": 0.060}
            },
            "us-east": {
                "t2.micro": {"on-demand": 0.020, "reserved": 0.013},
                "t2.small": {"on-demand": 0.040, "reserved": 0.026},
                "t2.medium": {"on-demand": 0.080, "reserved": 0.052}
            }
        }

        # Cálculo
        if region not in precios:
            raise ValueError(f"Región '{region}' no encontrada")
        if tipo_instancia not in precios[region]:
            raise ValueError(f"Tipo de instancia '{tipo_instancia}' no encontrado en la región '{region}'")
        if tipo_pago not in precios[region][tipo_instancia]:
            raise ValueError(f"Tipo de pago '{tipo_pago}' no encontrado para la instancia '{tipo_instancia}' en la región '{region}'")

        costo_hora_usd = precios[region][tipo_instancia][tipo_pago]
        costo_hora_mxn = costo_hora_usd * tasa_cambio
        costo_mes = costo_hora_mxn * horas_mes
        costo_anual = costo_mes * 12
        impuesto = costo_anual * impuesto_anual
        costo_total = costo_anual + impuesto

        print("Calculadora de Costo de Infraestructura Cloud")
        print("-----------------------------------------------")
        print(f"Región: {region}")
        print(f"Tipo de Instancia: {tipo_instancia}")
        print(f"Tipo de Pago: {tipo_pago}")
        print(f"Horas por Mes: {horas_mes}")
        print(f"Tasa de Cambio: {tasa_cambio} MXN/USD")
        print(f"Costo por Hora en USD: {costo_hora_usd}")
        print(f"Costo por Hora en MXN: {costo_hora_mxn}")
        print(f"Costo por Mes en MXN: {costo_mes}")
        print(f"Costo por Año en MXN: {costo_anual}")
        print(f"Impuesto Anual: {impuesto_anual * 100}%")
        print(f"Costo Total: {costo_total} MXN")
        print("-----------------------------------------------")
        print("Resumen Ejecutivo:")
        print("La calculadora de costo de infraestructura cloud ha calculado el costo total de una instancia de tipo {} en la región {} con un tipo de pago de {} y una tasa de cambio de {} MXN/USD. El costo total es de {} MXN, lo que incluye un impuesto anual del {}%.".format(tipo_instancia, region, tipo_pago, tasa_cambio, costo_total, impuesto_anual * 100))

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()