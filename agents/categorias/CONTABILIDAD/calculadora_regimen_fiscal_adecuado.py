"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora regimen fiscal adecuado para México
TECNOLOGÍA: Python estándar
"""

import sys
import math
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcula_regimen_fiscal(ingreso_anual, deducciones, regimen="general"):
    try:
        if regimen == "simplificado":
            tasa_isr = 0.08
        elif regimen == "intermedio":
            tasa_isr = 0.12
        else:  # general
            tasa_isr = 0.15
        base_gravable = max(0, ingreso_anual - deducciones)
        impuesto = base_gravable * tasa_isr
        return impuesto
    except Exception as e:
        print(f"Error en calcula_regimen_fiscal: {str(e)}")
        return None

def calcula_impuesto_marginal(ingreso_anual):
    try:
        if ingreso_anual <= 400000:
            return 0.01
        elif ingreso_anual <= 700000:
            return 0.02
        elif ingreso_anual <= 1000000:
            return 0.03
        elif ingreso_anual <= 2000000:
            return 0.04
        elif ingreso_anual <= 5000000:
            return 0.05
        else:
            return 0.06
    except Exception as e:
        print(f"Error en calcula_impuesto_marginal: {str(e)}")
        return None

def calcula_iva(ingreso_anual, tasa_iva=0.16):
    try:
        return ingreso_anual * tasa_iva
    except Exception as e:
        print(f"Error en calcula_iva: {str(e)}")
        return None

def calcula_impuestos(ingreso_anual, deducciones, regimen="general"):
    try:
        impuesto = calcula_regimen_fiscal(ingreso_anual, deducciones, regimen)
        impuesto_marginal = calcula_impuesto_marginal(ingreso_anual)
        iva = calcula_iva(ingreso_anual)
        return impuesto, impuesto_marginal, iva
    except Exception as e:
        print(f"Error en calcula_impuestos: {str(e)}")
        return None, None, None

def main():
    try:
        if len(sys.argv) < 2:
            print("Error: faltan argumentos")
            return

        ingreso_anual = float(sys.argv[1])
        deducciones = float(sys.argv[2])
        regimen = sys.argv[3] if len(sys.argv) > 3 else "general"

        impuesto, impuesto_marginal, iva = calcula_impuestos(ingreso_anual, deducciones, regimen)

        if impuesto is None or impuesto_marginal is None or iva is None:
            print("Error: no se pudo calcular algun impuesto")
            return

        print("=== ANÁLISIS FISCAL MEXICANO ===")
        print(f"Ingreso anual: ${ingreso_anual:,.2f}")
        print(f"Deducciones: ${deducciones:,.2f}")
        print(f"Base gravable: ${max(0, ingreso_anual - deducciones):,.2f}")
        print(f"Impuesto sobre la renta (ISR): ${impuesto:,.2f}")
        print(f"Impuesto marginal: {impuesto_marginal*100:.2f}%")
        print(f"IVA estimado: ${iva:,.2f}")
        print(f"Total de impuestos (ISR + IVA): ${impuesto + iva:,.2f}")
        print(f"Resumen ejecutivo: El ingreso anual de ${ingreso_anual:,.2f} se ve afectado por un impuesto sobre la renta de ${impuesto:,.2f} y un IVA de ${iva:,.2f}")
    except Exception as e:
        print(f"Error en main: {str(e)}")

if __name__ == "__main__":
    main()