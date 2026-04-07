"""
ÁREA: EDUCACION
DESCRIPCIÓN: Agente que realiza analizador rendimiento grupo
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
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def analizador_rendimiento_grupo(estudiantes=None, promedio=None, notas=None):
    try:
        if estudiantes is None:
            estudiantes = int(input("Ingrese el número de estudiantes: "))
        if promedio is None:
            promedio = float(input("Ingrese el promedio: "))
        if notas is None:
            notas = [float(input(f"Ingrese nota {i+1}: ")) for i in range(estudiantes)]

        # Verificar si hay estudiantes con notas menores a 0 o mayores a 100
        if any(notas[i] < 0 or notas[i] > 100 for i in range(len(notas))):
            raise ValueError("Nota inválida")

        # Calcular rendimiento del grupo
        notas_min = min(notas)
        notas_max = max(notas)
        notas_std = math.sqrt(sum((x - sum(notas) / len(notas)) ** 2 for x in notas) / len(notas))
        notas_media = sum(notas) / len(notas)
        notas_menor_5 = len([x for x in notas if x < 5])
        notas_mayor_90 = len([x for x in notas if x > 90])
        notas_aprobadas = len([x for x in notas if x >= 60])
        notas_reprobadas = len([x for x in notas if x < 60])
        rendimiento = (promedio / 100) * 100

        print(f"Estudiantes: {estudiantes}")
        print(f"Promedio: {promedio}%")
        print(f"Notas: {notas}")
        print(f"Notas minima: {notas_min}%")
        print(f"Notas maxima: {notas_max}%")
        print(f"Notas media: {notas_media}%")
        print(f"Notas estandar: {notas_std}%")
        print(f"Notas menores a 5: {notas_menor_5} ({notas_menor_5 / len(notas) * 100}%)")
        print(f"Notas mayores a 90: {notas_mayor_90} ({notas_mayor_90 / len(notas) * 100}%)")
        print(f"Notas aprobadas: {notas_aprobadas} ({notas_aprobadas / len(notas) * 100}%)")
        print(f"Notas reprobadas: {notas_reprobadas} ({notas_reprobadas / len(notas) * 100}%)")
        print(f"Rendimiento del grupo: {rendimiento}%")

        # Generar informe en formato JSON
        informe = {
            "estudiantes": estudiantes,
            "promedio": promedio,
            "notas": notas,
            "notas_min": notas_min,
            "notas_max": notas_max,
            "notas_media": notas_media,
            "notas_std": notas_std,
            "notas_menor_5": notas_menor_5,
            "notas_mayor_90": notas_mayor_90,
            "notas_aprobadas": notas_aprobadas,
            "notas_reprobadas": notas_reprobadas,
            "rendimiento": rendimiento
        }

        # Resumen ejecutivo
        if notas_aprobadas / len(notas) * 100 > 70:
            print("El grupo ha obtenido un buen rendimiento y la mayoría de los estudiantes han aprobado.")
        elif notas_aprobadas / len(notas) * 100 > 40:
            print("El grupo ha obtenido un rendimiento regular y un número moderado de estudiantes han aprobado.")
        else:
            print("El grupo ha obtenido un rendimiento bajo y un número pequeño de estudiantes han aprobado.")

        return json.dumps(informe, indent=4)

    except ValueError as e:
        print(f"Error: {e}")
        return None

def main():
    if len(sys.argv) > 1:
        estudiantes = int(sys.argv[1])
        promedio = float(sys.argv[2])
        notas = [float(sys.argv[i]) for i in range(3, len(sys.argv))]
    else:
        estudiantes = None
        promedio = None
        notas = None