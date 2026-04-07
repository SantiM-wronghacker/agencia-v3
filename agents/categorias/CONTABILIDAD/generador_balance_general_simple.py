import sys
import json
from datetime import datetime
import math
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        fecha = datetime.now().strftime("%Y-%m-%d")
        activos = 1500000.00
        pasivos = 800000.00
        capital = 700000.00
        impuestos = 0.16
        depreciacion = 0.05
        utilidad_bruta = 500000.00
        gastos_operativos = 200000.00
        beneficio_operativo = utilidad_bruta - gastos_operativos

        # Procesar argumentos
        if len(sys.argv) > 1:
            try:
                fecha = sys.argv[1]
                activos = float(sys.argv[2]) if len(sys.argv) > 2 else activos
                pasivos = float(sys.argv[3]) if len(sys.argv) > 3 else pasivos
                capital = float(sys.argv[4]) if len(sys.argv) > 4 else capital
                impuestos = float(sys.argv[5]) if len(sys.argv) > 5 else impuestos
                depreciacion = float(sys.argv[6]) if len(sys.argv) > 6 else depreciacion
                utilidad_bruta = float(sys.argv[7]) if len(sys.argv) > 7 else utilidad_bruta
                gastos_operativos = float(sys.argv[8]) if len(sys.argv) > 8 else gastos_operativos
            except (ValueError, IndexError):
                pass

        # Validar ecuación contable
        if activos <= 0 or pasivos < 0 or capital < 0 or beneficio_operativo < 0:
            raise ValueError("Error: Los valores deben ser positivos")

        # Generar balance general
        balance = {
            "fecha": fecha,
            "activos": activos,
            "pasivos": pasivos,
            "capital": capital,
            "total": activos + pasivos + capital,
            "impuestos": activos * impuestos,
            "depreciacion": activos * depreciacion,
            "utilidad_bruta": utilidad_bruta,
            "gastos_operativos": gastos_operativos,
            "beneficio_operativo": beneficio_operativo,
            "utilidad_neta": beneficio_operativo - (activos * impuestos) - (activos * depreciacion)
        }

        # Validar ecuación contable
        if not math.isclose(balance["total"], balance["activos"] + balance["pasivos"] + balance["capital"], rel_tol=1e-9):
            raise ValueError("Error: La ecuación contable no se cumple")

        # Imprimir resultados
        print("ÁREA: FINANZAS")
        print("DESCRIPCIÓN: Agente que realiza generador balance general simple")
        print("TECNOLOGÍA: Python estándar")
        print(f"Fecha: {balance['fecha']}")
        print(f"Activos: ${balance['activos']:.2f}")
        print(f"Pasivos: ${balance['pasivos']:.2f}")
        print(f"Capital: ${balance['capital']:.2f}")
        print(f"Total: ${balance['total']:.2f}")
        print(f"Impuestos: ${balance['impuestos']:.2f}")
        print(f"Depreciación: ${balance['depreciacion']:.2f}")
        print(f"Utilidad bruta: ${balance['utilidad_bruta']:.2f}")
        print(f"Gastos operativos: ${balance['gastos_operativos']:.2f}")
        print(f"Beneficio operativo: ${balance['beneficio_operativo']:.2f}")
        print(f"Utilidad neta: ${balance['utilidad_neta']:.2f}")
        print("Resumen ejecutivo:")
        print(f"El balance general muestra un total de ${balance['total']:.2f} y una utilidad neta de ${balance['utilidad_neta']:.2f}.")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()