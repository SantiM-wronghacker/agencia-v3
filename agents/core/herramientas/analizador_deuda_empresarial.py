"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza analizador deuda empresarial
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_deuda(total_activos, total_pasivos, deuda_larga_plazo, deuda_corta_plazo):
    return deuda_larga_plazo + deuda_corta_plazo

def calcular_ratio_deuda(total_activos, deuda):
    if total_activos == 0:
        return 0
    return deuda / total_activos

def calcular_costo_deuda(tasa_interes, deuda):
    return deuda * tasa_interes

def calcular_tasa_interes_mensual(tasa_interes_anual):
    return tasa_interes_anual / 12

def calcular_pago_mensual(costo_deuda, plazo_meses):
    return costo_deuda / plazo_meses

def calcular_plazo_pago(deuda, tasa_interes_mensual, pago_mensual):
    return math.ceil(deuda / pago_mensual)

def calcular_tasa_efectiva(tasa_interes_anual, plazo_anos):
    return (1 + tasa_interes_anual) ** plazo_anos - 1

def main():
    if len(sys.argv) < 7:
        print("Error: Faltan argumentos")
        sys.exit(1)

    try:
        total_activos = float(sys.argv[1])
        total_pasivos = float(sys.argv[2])
        deuda_larga_plazo = float(sys.argv[3])
        deuda_corta_plazo = float(sys.argv[4])
        tasa_interes = float(sys.argv[5])
        plazo_meses = int(sys.argv[6])

        deuda = calcular_deuda(total_activos, total_pasivos, deuda_larga_plazo, deuda_corta_plazo)
        ratio_deuda = calcular_ratio_deuda(total_activos, deuda)
        costo_deuda = calcular_costo_deuda(tasa_interes, deuda)
        tasa_interes_mensual = calcular_tasa_interes_mensual(tasa_interes)
        pago_mensual = calcular_pago_mensual(costo_deuda, plazo_meses)
        plazo_pago = calcular_plazo_pago(deuda, tasa_interes_mensual, pago_mensual)
        tasa_efectiva = calcular_tasa_efectiva(tasa_interes, plazo_meses / 12)

        print("ÁREA: FINANZAS")
        print("DESCRIPCIÓN: Análisis de deuda empresarial")
        print(f"Total Activos: ${total_activos:,.2f}")
        print(f"Total Pasivos: ${total_pasivos:,.2f}")
        print(f"Deuda Larga Plazo: ${deuda_larga_plazo:,.2f}")
        print(f"Deuda Corta Plazo: ${deuda_corta_plazo:,.2f}")
        print(f"Deuda Total: ${deuda:,.2f}")
        print(f"Ratio Deuda: {ratio_deuda:.2%}")
        print(f"Costo Deuda: ${costo_deuda:,.2f}")
        print(f"Tasa Interés Mensual: {tasa_interes_mensual:.2%}")
        print(f"Pago Mensual: ${pago_mensual:,.2f}")
        print(f"Plazo Pago: {plazo_pago} meses")
        print(f"Tasa Efectiva: {tasa_efectiva:.2%}")
        print("Resumen Ejecutivo:")
        print(f"La empresa tiene una deuda total de ${deuda:,.2f}, con un ratio de deuda de {ratio_deuda:.2%}.")
        print(f"El costo de la deuda es de ${costo_deuda:,.2f} y el pago mensual es de ${pago_mensual:,.2f}.")
        print(f"El plazo de pago es de {plazo_pago} meses y la tasa efectiva es de {tasa_efectiva:.2%}.")
    except ValueError:
        print("Error: Argumentos inválidos")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()