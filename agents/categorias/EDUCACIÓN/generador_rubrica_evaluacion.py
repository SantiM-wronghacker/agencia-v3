"""
ÁREA: EDUCACIÓN
DESCRIPCIÓN: Agente que realiza generador rubrica evaluacion
TECNOLOGÍA: Python estándar
"""

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
        # Configuración por defecto
        if len(sys.argv) > 1:
            nivel_educativo = sys.argv[1]
            materia = sys.argv[2]
            numero_preguntas = int(sys.argv[3])
            puntaje_total = int(sys.argv[4])
        else:
            nivel_educativo = "Secundaria"
            materia = "Matemáticas"
            numero_preguntas = 10
            puntaje_total = 100

        # Validar parámetros
        if numero_preguntas < 1:
            raise ValueError("Número de preguntas debe ser mayor que 0")
        if puntaje_total < 1:
            raise ValueError("Puntaje total debe ser mayor que 0")

        # Generar rubrica de evaluación
        rubrica = []
        for i in range(numero_preguntas):
            pregunta = f"Pregunta {i+1}"
            puntaje = random.randint(1, 10)
            rubrica.append({"pregunta": pregunta, "puntaje": puntaje})

        # Calcular puntaje total
        puntaje_total_calculado = sum([p["puntaje"] for p in rubrica])

        # Calcular porcentaje de cada pregunta
        porcentajes = []
        for pregunta in rubrica:
            porcentaje = (pregunta["puntaje"] / puntaje_total_calculado) * 100
            porcentajes.append({"pregunta": pregunta["pregunta"], "porcentaje": porcentaje})

        # Calcular estadísticas
        max_puntaje = max([p["puntaje"] for p in rubrica])
        min_puntaje = min([p["puntaje"] for p in rubrica])
        promedio_puntaje = puntaje_total_calculado / numero_preguntas

        # Imprimir resultados
        print(f"Nivel Educativo: {nivel_educativo}")
        print(f"Materia: {materia}")
        print(f"Numero de Preguntas: {numero_preguntas}")
        print(f"Puntaje Total: {puntaje_total_calculado}")
        print(f"Puntaje Total Configurado: {puntaje_total}")
        print("Rubrica de Evaluación:")
        for pregunta in rubrica:
            print(f"{pregunta['pregunta']}: {pregunta['puntaje']} puntos")
        print("Estadísticas:")
        print(f"Máximo Puntaje: {max_puntaje} puntos")
        print(f"Mínimo Puntaje: {min_puntaje} puntos")
        print(f"Promedio Puntaje: {promedio_puntaje:.2f} puntos")
        print("Porcentajes:")
        for porcentaje in porcentajes:
            print(f"{porcentaje['pregunta']}: {porcentaje['porcentaje']:.2f}%")
        print("Resumen Ejecutivo:")
        print(f"La evaluación consta de {numero_preguntas} preguntas con un puntaje total de {puntaje_total_calculado} puntos.")
        print(f"El puntaje máximo es de {max_puntaje} puntos y el mínimo es de {min_puntaje} puntos.")
        print(f"El promedio de puntaje es de {promedio_puntaje:.2f} puntos.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()