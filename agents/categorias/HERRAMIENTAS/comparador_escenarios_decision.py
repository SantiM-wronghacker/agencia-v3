# CEREBRO/Comparador de Escenarios de Decision/Python
# AREA: CEREBRO
# DESCRIPCION: Agente que realiza comparador escenarios decision
# TECNOLOGIA: Python

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

def main():
    try:
        # Obtener parametros por sys.argv
        if len(sys.argv) > 1:
            num_escenarios = int(sys.argv[1])
            escenarios = []
            for i in range(num_escenarios):
                nombre = f"Escenario {i+1}"
                costo = random.randint(100000, 200000)
                beneficio = random.randint(200000, 400000)
                escenarios.append({"nombre": nombre, "costo": costo, "beneficio": beneficio})
        else:
            # Definir escenarios de decision
            escenarios = [
                {"nombre": "Escenario 1", "costo": 100000, "beneficio": 200000},
                {"nombre": "Escenario 2", "costo": 150000, "beneficio": 300000},
                {"nombre": "Escenario 3", "costo": 200000, "beneficio": 400000}
            ]

        # Definir criterios de decision
        criterios = ["costo", "beneficio"]

        # Comparar escenarios de decision
        for escenario in escenarios:
            print(f"Escenario: {escenario['nombre']}")
            for criterio in criterios:
                print(f"{criterio.capitalize()}: ${escenario[criterio]:,}")
            print(f"Rentabilidad: ${escenario['beneficio'] - escenario['costo']:,}")
            print(f"Margen de beneficio: {(escenario['beneficio'] - escenario['costo']) / escenario['beneficio'] * 100:.2f}%")
            print(f"Tasa de retorno de la inversión (TIR): {(escenario['beneficio'] / escenario['costo'] - 1) * 100:.2f}%")
            print(f"Período de recuperación de la inversión (PRI): {escenario['costo'] / (escenario['beneficio'] - escenario['costo']):.2f} años")
            print("")

        # Seleccionar el mejor escenario
        mejor_escenario = max(escenarios, key=lambda x: x['beneficio'] - x['costo'])
        print(f"Mejor escenario: {mejor_escenario['nombre']}")
        print(f"Costo: ${mejor_escenario['costo']:,}")
        print(f"Beneficio: ${mejor_escenario['beneficio']:,}")
        print(f"Rentabilidad: ${mejor_escenario['beneficio'] - mejor_escenario['costo']:,}")
        print(f"Margen de beneficio: {(mejor_escenario['beneficio'] - mejor_escenario['costo']) / mejor_escenario['beneficio'] * 100:.2f}%")
        print(f"Tasa de retorno de la inversión (TIR): {(mejor_escenario['beneficio'] / mejor_escenario['costo'] - 1) * 100:.2f}%")
        print(f"Período de recuperación de la inversión (PRI): {mejor_escenario['costo'] / (mejor_escenario['beneficio'] - mejor_escenario['costo']):.2f} años")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"Fecha de análisis: {datetime.date.today()}")
        print(f"Numero de escenarios analizados: {len(escenarios)}")
        print(f"Mejor escenario: {mejor_escenario['nombre']}")
        print(f"Rentabilidad del mejor escenario: ${mejor_escenario['beneficio'] - mejor_escenario['costo']:,}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()