"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculo capital trabajo
TECNOLOGÍA: Python estándar
"""

import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_capital_trabajo(activo_circulante, pasivo_circulante):
    try:
        capital_trabajo = activo_circulante - pasivo_circulante
        return capital_trabajo
    except Exception as e:
        print(f"Error en cálculo: {e}")
        return None

def calcular_margen_seguridad(capital_trabajo, activo_circulante):
    try:
        margen_seguridad = (capital_trabajo / activo_circulante) * 100
        return margen_seguridad
    except Exception as e:
        print(f"Error en cálculo: {e}")
        return None

def calcular_liquidez_inmediata(activo_circulante, pasivo_circulante):
    try:
        liquidez_inmediata = activo_circulante / pasivo_circulante
        return liquidez_inmediata
    except Exception as e:
        print(f"Error en cálculo: {e}")
        return None

def calcular_prueba_acidez(activo_circulante, pasivo_circulante):
    try:
        prueba_acidez = (activo_circulante - pasivo_circulante) / activo_circulante
        return prueba_acidez
    except Exception as e:
        print(f"Error en cálculo: {e}")
        return None

def main():
    try:
        # Valores por defecto en MXN
        activo_circulante = float(sys.argv[1]) if len(sys.argv) > 1 else 500000.0
        pasivo_circulante = float(sys.argv[2]) if len(sys.argv) > 2 else 300000.0

        capital_trabajo = calcular_capital_trabajo(activo_circulante, pasivo_circulante)
        margen_seguridad = calcular_margen_seguridad(capital_trabajo, activo_circulante) if capital_trabajo is not None else None
        liquidez_inmediata = calcular_liquidez_inmediata(activo_circulante, pasivo_circulante)
        prueba_acidez = calcular_prueba_acidez(activo_circulante, pasivo_circulante)

        if capital_trabajo is not None:
            print("Cálculo de Capital de Trabajo:")
            print(f"Activo Circulante: ${activo_circulante:,.2f} MXN")
            print(f"Pasivo Circulante: ${pasivo_circulante:,.2f} MXN")
            print(f"Capital de Trabajo: ${capital_trabajo:,.2f} MXN")
            print(f"Margen de Seguridad: {margen_seguridad:.2f}%")
            print(f"Liquidez Inmediata: {liquidez_inmediata:.2f}")
            print(f"Prueba de Acidez: {prueba_acidez:.2f}")
            print(f"Relación Activo/Pasivo: {activo_circulante/pasivo_circulante:.2f}")
            print(f"Relación Pasivo/Activo: {pasivo_circulante/activo_circulante:.2f}")
            print("Resumen Ejecutivo:")
            if capital_trabajo > 0:
                print("La empresa tiene un capital de trabajo positivo, lo que indica una buena salud financiera.")
            elif capital_trabajo < 0:
                print("La empresa tiene un capital de trabajo negativo, lo que indica una mala salud financiera.")
            else:
                print("La empresa tiene un capital de trabajo igual a cero, lo que indica una situación financiera neutral.")
    except Exception as e:
        print(f"Error en ejecución: {e}")

if __name__ == "__main__":
    main()