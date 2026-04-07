"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora punto reorden
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def calculadora_punto_reorden(peso, costo_unitario, distancia, costo_flete, tiempo_transito, costo_transito):
    try:
        if WEB:
            # Buscar datos en tiempo real
            pass
        else:
            # Validar datos de entrada
            peso = float(peso)
            costo_unitario = float(costo_unitario)
            distancia = float(distancia)
            costo_flete = float(costo_flete)
            tiempo_transito = float(tiempo_transito)
            costo_transito = float(costo_transito)

            # Calcular punto reorden
            punto_reorden = (costo_flete * distancia) + (costo_transito * tiempo_transito)
            costo_total = punto_reorden + (peso * costo_unitario)
            costo_unitario_total = costo_total / peso
            costo_flete_total = costo_flete * distancia
            costo_transito_total = costo_transito * tiempo_transito

            # Calcular otros costos
            costo_carretera = 0.05 * costo_flete_total
            costo_señalización = 0.01 * costo_flete_total
            costo_mantenimiento = 0.02 * costo_flete_total

            # Imprimir resultados
            print(f"Peso de la carga: {peso} kg")
            print(f"Costo unitario: {costo_unitario} MXN/kg")
            print(f"Distancia: {distancia} km")
            print(f"Costo flete: {costo_flete} MXN/km")
            print(f"Tiempo de transito: {tiempo_transito} días")
            print(f"Costo de transito: {costo_transito} MXN/día")
            print(f"Punto reorden: {punto_reorden} MXN")
            print(f"Costo total: {costo_total} MXN")
            print(f"Costo unitario total: {costo_unitario_total} MXN/kg")
            print(f"Costo flete total: {costo_flete_total} MXN")
            print(f"Costo transito total: {costo_transito_total} MXN")
            print(f"Costo carretera: {costo_carretera} MXN")
            print(f"Costo señalización: {costo_señalización} MXN")
            print(f"Costo mantenimiento: {costo_mantenimiento} MXN")

            # Imprimir resumen ejecutivo
            print("\nResumen Ejecutivo:")
            print(f"El punto reorden calculado es de {punto_reorden} MXN, lo que representa un costo total de {costo_total} MXN.")
            print(f"El costo unitario total es de {costo_unitario_total} MXN/kg.")
            print(f"El costo flete total es de {costo_flete_total} MXN.")
            print(f"El costo transito total es de {costo_transito_total} MXN.")
            print(f"El costo carretera es de {costo_carretera} MXN.")
            print(f"El costo señalización es de {costo_señalización} MXN.")
            print(f"El costo mantenimiento es de {costo_mantenimiento} MXN.")

    except ValueError:
        print("Error: Los valores de entrada deben ser números.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Error: Faltan argumentos.")
    else:
        calculadora_punto_reorden(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])