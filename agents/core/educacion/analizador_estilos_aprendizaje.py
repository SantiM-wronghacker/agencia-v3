"""
ÁREA: EDUCACION
DESCRIPCIÓN: Agente que realiza analizador estilos aprendizaje
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
from datetime import datetime
import math
import re
import random

def analizador_estilos_aprendizaje(temas, estudiantes, dificultad=0.5, variacion=10):
    """
    Analiza los estilos de aprendizaje de los estudiantes en función de los temas dadas.

    Args:
        temas (list): Lista de temas a analizar.
        estudiantes (list): Lista de estudiantes a analizar.
        dificultad (float, optional): Dificultad media de los temas. Defaults to 0.5.
        variacion (float, optional): Variación de dificultad entre temas. Defaults to 10.

    Returns:
        dict: Diccionario con los resultados del análisis.
    """
    resultados = {}

    for tema in temas:
        resultados[tema] = {}
        for estudiante in estudiantes:
            try:
                # Simula un cálculo más preciso y realista para México
                dificultad_tema = dificultad + (random.uniform(-variacion, variacion) / 100)
                resultado = dificultad_tema * 100
                resultados[tema][estudiante] = resultado
            except Exception as e:
                print(f"Error en el cálculo para el tema {tema} y el estudiante {estudiante}: {str(e)}")

    return resultados

def main():
    try:
        if len(sys.argv) < 3:
            print("Error: Faltan argumentos. Uso: python analizador_estilos_aprendizaje.py <tema1> <tema2> ... <estudiante1> <estudiante2> ...")
            sys.exit(1)

        temas = sys.argv[1: len(sys.argv)//2]
        estudiantes = sys.argv[len(sys.argv)//2:]
        resultados = analizador_estilos_aprendizaje(temas, estudiantes)

        print("Estilos de aprendizaje:")
        for tema, resultados_tema in resultados.items():
            print(f"Tema: {tema}")
            for estudiante, resultado in resultados_tema.items():
                print(f"  Estudiante: {estudiante}, Resultado: {resultado:.2f}%")

        print("\nResumen ejecutivo:")
        print(f"La dificultad media de los temas fue de {sum([resultados[tema][estudiante] for tema in resultados for estudiante in resultados[tema]]) / (len(resultados) * len(resultados[list(resultados.keys())[0]])):.2f}%")
        print(f"La variación de dificultad entre temas fue de {max([abs(resultados[tema][estudiante] - resultados[tema2][estudiante]) for tema in resultados for estudiante in resultados[tema] for tema2 in resultados if tema != tema2]) / 100:.2f}%")
        print(f"El número de temas fue de {len(resultados)}")
        print(f"El número de estudiantes fue de {len(resultados[list(resultados.keys())[0]])}")

        print("\nEstudiantes con mejores resultados:")
        mejores_resultados = sorted([(estudiante, resultado) for tema in resultados for estudiante, resultado in resultados[tema].items()], key=lambda x: x[1], reverse=True)
        for i, (estudiante, resultado) in enumerate(mejores_resultados[:5]):
            print(f"  {i+1}. Estudiante: {estudiante}, Resultado: {resultado:.2f}%")

        print("\nEstudiantes con peores resultados:")
        peores_resultados = sorted([(estudiante, resultado) for tema in resultados for estudiante, resultado in resultados[tema].items()], key=lambda x: x[1])
        for i, (estudiante, resultado) in enumerate(peores_resultados[:5]):
            print(f"  {i+1}. Estudiante: {estudiante}, Resultado: {resultado:.2f}%")

    except Exception as e:
        print(f"Error principal: {str(e)}")

if __name__ == "__main__":
    main()