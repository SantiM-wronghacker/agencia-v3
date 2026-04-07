"""
ÁREA: EDUCACIÓN
DESCRIPCIÓN: Agente que realiza planificador de curso
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
from datetime import datetime, timedelta
import math
import re
import random

def calcular_horas_descanso(horas):
    # Se asume que el 20% de las horas son de descanso
    return horas * 0.2

def calcular_horas_estudio(horas):
    # Se asume que el 40% de las horas son de estudio
    return horas * 0.4

def calcular_horas_clase(creditos):
    # Se asume que cada crédito equivale a 12 horas de clase
    return creditos * 12

def calcular_horas_trabajo(creditos):
    # Se asume que cada crédito equivale a 8 horas de trabajo
    return creditos * 8

def planificador_curso(cursos=None, creditos_minimo=4, creditos_maximo=8, horas_minimo=60, horas_maximo=240):
    if cursos is None:
        cursos = [
            {"nombre": "Matemáticas", "creditos": 5, "horas": 180},
            {"nombre": "Física", "creditos": 6, "horas": 240},
            {"nombre": "Química", "creditos": 7, "horas": 300},
            {"nombre": "Biología", "creditos": 8, "horas": 360},
            {"nombre": "Inglés", "creditos": 5, "horas": 180},
        ]

    try:
        curso_planificado = random.choice(cursos)
        print(f"Curso planificado: {curso_planificado['nombre']}")
        print(f"Creditos: {curso_planificado['creditos']}")
        print(f"Horas: {curso_planificado['horas']} horas")
        print(f"Fecha de inicio: {datetime.now() + timedelta(days=7)}")
        print(f"Fecha de fin: {datetime.now() + timedelta(days=14)}")
        print(f"Total de horas semanales: {curso_planificado['horas'] / 14:.2f} horas")
        print(f"Total de horas diarias: {curso_planificado['horas'] / 14 / 7:.2f} horas")
        print(f"Total de semanas: {math.ceil(curso_planificado['horas'] / 14)}")
        print(f"Total de horas de descanso: {calcular_horas_descanso(curso_planificado['horas']):.2f} horas")
        print(f"Total de horas de estudio: {calcular_horas_estudio(curso_planificado['horas']):.2f} horas")
        print(f"Total de horas de clase: {calcular_horas_clase(curso_planificado['creditos']):.2f} horas")
        print(f"Total de horas de trabajo: {calcular_horas_trabajo(curso_planificado['creditos']):.2f} horas")
        print(f"Total de horas de trabajo diarias: {calcular_horas_trabajo(curso_planificado['creditos']) / 7:.2f} horas")
        print(f"Total de horas de clase diarias: {calcular_horas_clase(curso_planificado['creditos']) / 7:.2f} horas")
        print(f"Resumen ejecutivo: El curso planificado es {curso_planificado['nombre']} con {curso_planificado['creditos']} creditos y {curso_planificado['horas']} horas de duración.")
        print(f"Resumen ejecutivo: El curso planificado requiere un total de {math.ceil(curso_planificado['horas'] / 14)} semanas.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) > 1:
        cursos = []
        for i in range(1, len(sys.argv)):
            curso = {
                "nombre": sys.argv[i],
                "creditos": int(sys.argv[i+1]),
                "horas": int(sys.argv[i+2])
            }
            cursos.append(curso)
            i += 2
        planificador_curso(cursos)
    else:
        planificador_curso()

if __name__ == "__main__":
    main()