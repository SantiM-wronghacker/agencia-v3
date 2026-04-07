"""
ÁREA: RRHH
DESCRIPCIÓN: Agente que realiza generador vacante
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random
from datetime import date

def generar_vacante(nombre, descripcion, ubicacion, salario_min, salario_max, requerimientos):
    try:
        if salario_min > salario_max:
            raise ValueError("El salario mínimo no puede ser mayor que el salario máximo")

        # Calcula el salario con precisión para México
        salario = round(random.uniform(salario_min, salario_max) * 100, 2) / 100

        vacante = {
            "id": random.randint(1000, 9999),
            "nombre": nombre,
            "descripcion": descripcion,
            "requerimientos": requerimientos,
            "salario": salario,
            "ubicacion": ubicacion,
            "fecha_publicacion": date.today().strftime('%d/%m/%Y'),
            "horario": ["mañana", "tarde"],
            "beneficios": ["vacaciones", "bono navideño"],
            "experiencia": random.randint(1, 10),
            "horas_trabajo": random.randint(30, 40),
            "dias_trabajo": random.choice(["lunes a viernes", "martes a sábado"])
        }
        return vacante

    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    try:
        if len(sys.argv) != 7:
            print("Uso: python generador_vacante.py <nombre> <descripcion> <ubicacion> <salario_min> <salario_max> <requerimientos>")
            sys.exit(1)

        nombre = sys.argv[1]
        descripcion = sys.argv[2]
        ubicacion = sys.argv[3]
        salario_min = float(sys.argv[4])
        salario_max = float(sys.argv[5])
        requerimientos = sys.argv[6].split(',')

        vacante = generar_vacante(nombre, descripcion, ubicacion, salario_min, salario_max, requerimientos)

        if vacante is not None:
            print(f"ID: {vacante['id']}")
            print(f"Nombre: {vacante['nombre']}")
            print(f"Descripción: {vacante['descripcion']}")
            print(f"Requerimientos: {', '.join(vacante['requerimientos'])}")
            print(f"Salario: {vacante['salario']} MXN")
            print(f"Ubicación: {vacante['ubicacion']}")
            print(f"Horario: {vacante['horario'][0]} y {vacante['horario'][1]}")
            print(f"Beneficios: {', '.join(vacante['beneficios'])}")
            print(f"Experiencia requerida: {vacante['experiencia']} años")
            print(f"Horas de trabajo diarias: {vacante['horas_trabajo']} horas")
            print(f"Días de trabajo: {vacante['dias_trabajo']}")
            print(f"Fecha de publicación: {vacante['fecha_publicacion']}")

            # Resumen ejecutivo
            print("\nResumen ejecutivo:")
            print(f"La empresa busca un/a {vacante['nombre']} con experiencia en {', '.join(vacante['requerimientos'])} para trabajar en {vacante['ubicacion']}.")
            print(f"El salario es de {vacante['salario']} MXN y se requiere {vacante['experiencia']} años de experiencia.")
            print(f"El horario es de {vacante['horario'][0]} y {vacante['horario'][1]} y se trabajan {vacante['horas_trabajo']} horas diarias.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()