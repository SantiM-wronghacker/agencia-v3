"""
ÁREA: SALUD
DESCRIPCIÓN: Agente que realiza calculadora riesgo cardiovascular
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def calcular_riesgo_cardiovascular(edad, peso, talla, presion_sangre, colesterol, glucosa):
    """
    Calcula el riesgo cardiovascular según la fórmula de Framingham adaptada para México

    Args:
        edad (int): Edad del paciente en años
        peso (float): Peso del paciente en kg
        talla (float): Talla del paciente en m
        presion_sangre (float): Presión arterial del paciente en mmHg
        colesterol (float): Nivel de colesterol del paciente en mg/dL
        glucosa (float): Nivel de glucosa del paciente en mg/dL

    Returns:
        float: Riesgo cardiovascular en porcentaje
    """
    # Constantes para la fórmula de Framingham adaptada para México
    const1 = 0.07
    const2 = 0.02
    const3 = 0.02
    const4 = 0.02

    # Calcula el riesgo cardiovascular
    riesgo = (const1 * edad) + (const2 * peso) + (const3 * talla) + (const4 * presion_sangre) + (0.02 * colesterol) + (0.02 * glucosa)

    # Convierte el riesgo a porcentaje
    riesgo = riesgo * 100

    return riesgo

def main():
    try:
        # Argumentos de línea de comandos
        edad = int(sys.argv[1]) if len(sys.argv) > 1 else 40
        peso = float(sys.argv[2]) if len(sys.argv) > 2 else 70
        talla = float(sys.argv[3]) if len(sys.argv) > 3 else 1.70
        presion_sangre = float(sys.argv[4]) if len(sys.argv) > 4 else 120
        colesterol = float(sys.argv[5]) if len(sys.argv) > 5 else 200
        glucosa = float(sys.argv[6]) if len(sys.argv) > 6 else 100

        # Calcula el riesgo cardiovascular
        riesgo = calcular_riesgo_cardiovascular(edad, peso, talla, presion_sangre, colesterol, glucosa)

        # Muestra los resultados
        print("Resultados:")
        print(f"Edad: {edad} años")
        print(f"Peso: {peso} kg")
        print(f"Talla: {talla} m")
        print(f"Presión arterial: {presion_sangre} mmHg")
        print(f"Nivel de colesterol: {colesterol} mg/dL")
        print(f"Nivel de glucosa: {glucosa} mg/dL")
        print(f"Riesgo cardiovascular: {riesgo:.2f}%")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        if riesgo < 20:
            print("El paciente tiene un bajo riesgo de enfermedad cardiovascular.")
        elif riesgo < 40:
            print("El paciente tiene un riesgo moderado de enfermedad cardiovascular. Es importante realizar cambios en el estilo de vida y, si es necesario, tomar medicamentos para reducir el riesgo.")
        else:
            print("El paciente tiene un alto riesgo de enfermedad cardiovascular. Es importante realizar cambios en el estilo de vida y tomar medicamentos para reducir el riesgo.")

    except IndexError:
        print("Faltan argumentos de línea de comandos. Por favor, ingrese los siguientes argumentos: edad, peso, talla, presión arterial, nivel de colesterol y nivel de glucosa.")
    except ValueError:
        print("Error: los argumentos de línea de comandos deben ser números.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()