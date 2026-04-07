"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza analizador de anomalias
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def analizador_anomalias():
    try:
        # Cargar datos de ejemplo hardcodeados
        if len(sys.argv) != 3:
            print("Error: Debe proporcionar dos argumentos: ventas y gastos")
            return

        ventas = float(sys.argv[1])
        gastos = float(sys.argv[2])

        # Casos edge
        if gastos == 0:
            print("Error: No se pueden calcular indicadores con gastos iguales a cero")
            return
        elif ventas < 0:
            print("Error: No se pueden calcular indicadores con ventas negativas")
            return
        elif ventas == 0 and gastos > 0:
            print("Error: No se pueden calcular indicadores con ventas iguales a cero")
            return

        # Calcular indicadores
        indice = ventas / gastos
        margen = (ventas - gastos) / ventas * 100 if ventas > 0 else 0
        beneficio = ventas - gastos
        utilidad = beneficio - (beneficio * 0.25)  # Utilidad después de impuestos
        porcentaje_utilidad = (utilidad / ventas) * 100
        rentabilidad = beneficio / gastos * 100
        liquidez = ventas / gastos

        # Imprimir resultados
        print("Resultados:")
        print(f"Índice de ventas/gastos: {indice:.2f}")
        print(f"Márgen de beneficio: {margen:.2f}%")
        print(f"Ventas: {ventas:.2f} MXN")
        print(f"Gastos: {gastos:.2f} MXN")
        print(f"Beneficio: {beneficio:.2f} MXN")
        print(f"Utilidad: {utilidad:.2f} MXN")
        print(f"Porcentaje de utilidad: {porcentaje_utilidad:.2f}%")
        print(f"Margen de beneficio por cada MXN de ventas: {margen/100:.2f} MXN")
        print(f"Rentabilidad: {rentabilidad:.2f}%")
        print(f"Líquidez: {liquidez:.2f}")

        # Resumen ejecutivo
        if margen > 20:
            print("La empresa tiene un margen de beneficio alto, lo que sugiere una buena gestión financiera.")
        elif margen < 10:
            print("La empresa tiene un margen de beneficio bajo, lo que sugiere problemas de competitividad.")
        else:
            print("La empresa tiene un margen de beneficio moderado, lo que sugiere una gestión financiera estable.")

        # Resumen final
        print("\nResumen ejecutivo:")
        if rentabilidad > 15:
            print("La empresa tiene una rentabilidad alta, lo que sugiere una buena gestión financiera.")
        elif rentabilidad < 5:
            print("La empresa tiene una rentabilidad baja, lo que sugiere problemas de competitividad.")
        else:
            print("La empresa tiene una rentabilidad moderada, lo que sugiere una gestión financiera estable.")

        if liquidez > 2:
            print("La empresa tiene una liquidez alta, lo que sugiere una buena gestión financiera.")
        elif liquidez < 1:
            print("La empresa tiene una liquidez baja, lo que sugiere problemas de pago.")
        else:
            print("La empresa tiene una liquidez moderada, lo que sugiere una gestión financiera estable.")

    except ValueError:
        print("Error: Los valores deben ser números.")
    except ZeroDivisionError:
        print("Error: No se pueden calcular indicadores con ventas iguales a cero.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analizador_anomalias()