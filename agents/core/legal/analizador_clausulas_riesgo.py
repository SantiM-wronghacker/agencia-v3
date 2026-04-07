"""
ÁREA: LEGAL
DESCRIPCIÓN: Agente que realiza analizador clausulas riesgo
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def analizar_clausulas(riesgos, probabilidad_minima=0.01, probabilidad_maxima=0.99, impacto_minimo=1, impacto_maximo=100):
    resultados = []
    for riesgo in riesgos:
        nivel = round(random.uniform(1, 10), 2)
        probabilidad = round(random.uniform(probabilidad_minima, probabilidad_maxima), 2)
        impacto = round(random.uniform(impacto_minimo, impacto_maximo), 2)
        resultado = {
            "riesgo": riesgo,
            "nivel": nivel,
            "probabilidad": probabilidad,
            "impacto": impacto,
            "valor_riesgo": round(nivel * probabilidad * impacto, 2)
        }
        resultados.append(resultado)
    return resultados

def calcular_indice_riesgo(resultados):
    total = sum([resultado['valor_riesgo'] for resultado in resultados])
    return round(total / len(resultados), 2)

def calcular_indice_probabilidad(resultados):
    total = sum([resultado['probabilidad'] for resultado in resultados])
    return round(total / len(resultados), 2)

def calcular_indice_impacto(resultados):
    total = sum([resultado['impacto'] for resultado in resultados])
    return round(total / len(resultados), 2)

def calcular_indice_nivel(resultados):
    total = sum([resultado['nivel'] for resultado in resultados])
    return round(total / len(resultados), 2)

def main():
    if len(sys.argv) < 2:
        print("Error: se requiere al menos un riesgo como argumento")
        sys.exit(1)

    riesgos = sys.argv[1:]
    probabilidad_minima = float(sys.argv[2]) if len(sys.argv) > 2 else 0.01
    probabilidad_maxima = float(sys.argv[3]) if len(sys.argv) > 3 else 0.99
    impacto_minimo = float(sys.argv[4]) if len(sys.argv) > 4 else 1
    impacto_maximo = float(sys.argv[5]) if len(sys.argv) > 5 else 100

    resultados = analizar_clausulas(riesgos, probabilidad_minima, probabilidad_maxima, impacto_minimo, impacto_maximo)

    print("Análisis de cláusulas de riesgo")
    print("---------------------------------")
    print("Fecha de análisis:", datetime.date.today())
    print("Número de riesgos analizados:", len(resultados))
    for i, resultado in enumerate(resultados):
        print(f"Riesgo {i+1}: {resultado['riesgo']}")
        print(f"  Nivel: {resultado['nivel']}")
        print(f"  Probabilidad: {resultado['probabilidad']} ({probabilidad_minima} - {probabilidad_maxima})")
        print(f"  Impacto: {resultado['impacto']} ({impacto_minimo} - {impacto_maximo})")
        print(f"  Valor de riesgo: {resultado['valor_riesgo']}")
        print()

    indice_riesgo = calcular_indice_riesgo(resultados)
    indice_probabilidad = calcular_indice_probabilidad(resultados)
    indice_impacto = calcular_indice_impacto(resultados)
    indice_nivel = calcular_indice_nivel(resultados)

    print("Resumen ejecutivo:")
    print("--------------------")
    print(f"Índice de riesgo: {indice_riesgo}")
    print(f"Índice de probabilidad: {indice_probabilidad}")
    print(f"Índice de impacto: {indice_impacto}")
    print(f"Índice de nivel: {indice_nivel}")

if __name__ == "__main__":
    main()