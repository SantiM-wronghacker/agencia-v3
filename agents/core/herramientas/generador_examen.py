"""
ÁREA: EDUCACION
DESCRIPCIÓN: Agente que realiza generador examen
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_examenes(num_examenes):
    try:
        if num_examenes < 1:
            raise ValueError("El número de examenes debe ser mayor o igual a 1")
        if not isinstance(num_examenes, int):
            raise TypeError("El número de examenes debe ser un número entero")
        examenes = []
        for i in range(num_examenes):
            examen = {
                "nombre": f"Examen {i+1}",
                "descripcion": f"Descripción del examen {i+1}",
                "preguntas": random.randint(5, 15),
                "tipo": random.choice(["multiple choice", "true or false", "abierto"]),
                "fecha": datetime.date.today().strftime("%Y-%m-%d")
            }
            examenes.append(examen)
        return examenes
    except ValueError as e:
        print(f"Error: {e}")
        return []
    except TypeError as e:
        print(f"Error: {e}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def generar_preguntas(examen):
    try:
        if examen["preguntas"] < 1:
            raise ValueError("El número de preguntas debe ser mayor o igual a 1")
        preguntas = []
        for i in range(examen["preguntas"]):
            pregunta = {
                "pregunta": f"Pregunta {i+1} del examen {examen['nombre']}",
                "opciones": random.sample(["Opción A", "Opción B", "Opción C", "Opción D"], 4),
                "respuesta": random.choice(["Opción A", "Opción B", "Opción C", "Opción D"])
            }
            preguntas.append(pregunta)
        return preguntas
    except KeyError as e:
        print(f"Error: {e}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def generar_resumen(examenes):
    resumen = {
        "total_examenes": len(examenes),
        "total_preguntas": sum(examen["preguntas"] for examen in examenes),
        "tipos_examenes": set(examen["tipo"] for examen in examenes)
    }
    return resumen

def main():
    if len(sys.argv) > 1:
        try:
            num_examenes = int(sys.argv[1])
            examenes = generar_examenes(num_examenes)
        except ValueError:
            print("Error: El argumento debe ser un número entero")
            return
    else:
        examenes = generar_examenes(5)

    for examen in examenes:
        print(f"\nExamen: {examen['nombre']}")
        print(f"Descripción: {examen['descripcion']}")
        print(f"Preguntas: {examen['preguntas']}")
        print(f"Tipo: {examen['tipo']}")
        print(f"Fecha: {examen['fecha']}")
        print(f"\nPreguntas:")
        for pregunta in generar_preguntas(examen):
            print(f"{pregunta['pregunta']}: {pregunta['opciones']}")
            print(f"Respuesta: {pregunta['respuesta']}")
            print()

    resumen = generar_resumen(examenes)
    print("\nResumen:")
    print(f"Total de examenes: {resumen['total_examenes']}")
    print(f"Total de preguntas: {resumen['total_preguntas']}")
    print(f"Tipos de examenes: {', '.join(resumen['tipos_examenes'])}")

if __name__ == "__main__":
    main()