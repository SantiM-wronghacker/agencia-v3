"""
ÁREA: RRHH
DESCRIPCIÓN: Agente que realiza filtrador cv
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def filtrador_cv(nombres=None, experiencia=None, educacion=None):
    try:
        # Verificar si se proporcionaron los parámetros
        if nombres is None:
            nombres = sys.argv[1].split(",")
        if experiencia is None:
            experiencia = sys.argv[2].split(",")
        if educacion is None:
            educacion = sys.argv[3].split(",")

        # Buscar datos reales con web_bridge
        nombres = [nombre.strip() for nombre in nombres]
        experiencia = [int(exp) for exp in experiencia]
        educacion = [edu.strip() for edu in educacion]

        # Verificar si los parámetros son válidos
        if not all(isinstance(exp, int) for exp in experiencia):
            raise ValueError("La experiencia debe ser un número entero")
        if not all(isinstance(edu, str) for edu in educacion):
            raise ValueError("La educación debe ser una cadena de texto")

        # Filtrar datos
        nombres_filtrados = [nombre for nombre in nombres if len(nombre) > 5]
        experiencia_filtrada = [exp for exp in experiencia if exp > 5]
        educacion_filtrada = [edu for edu in educacion if edu.startswith("Licenciado")]

        # Imprimir resultados
        print("Nombres filtrados:")
        for nombre in nombres_filtrados:
            print(f"- {nombre}")

        print("\nExperiencia filtrada:")
        for exp in experiencia_filtrada:
            print(f"- {exp} años")

        print("\nEducación filtrada:")
        for edu in educacion_filtrada:
            print(f"- {edu}")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"Se encontraron {len(nombres_filtrados)} nombres que cumplen con el criterio de filtrado.")
        print(f"La experiencia laboral promedio de los candidatos es {sum(experiencia_filtrada) / len(experiencia_filtrada)} años.")
        print(f"La educación más común de los candidatos es {max(set(educacion_filtrada), key=educacion_filtrada.count)}.")

        # Calcular el promedio de la experiencia en años
        experiencia_promedio = sum(experiencia_filtrada) / len(experiencia_filtrada)
        experiencia_promedio_anos = experiencia_promedio * 12  # Año promedio en meses
        experiencia_promedio_anos = experiencia_promedio_anos * 12  # Año promedio en años

        # Calcular el total de años de experiencia
        total_experiencia = sum(experiencia_filtrada)

        # Imprimir resultados adicionales
        print("\nResultados adicionales:")
        print(f"El promedio de años de experiencia de los candidatos es {experiencia_promedio_anos} años.")
        print(f"El total de años de experiencia de los candidatos es {total_experiencia} años.")

    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) > 1:
        nombres = sys.argv[1].split(",")
        experiencia = sys.argv[2].split(",")
        educacion = sys.argv[3].split(",")
        filtrador_cv(nombres, experiencia, educacion)
    else:
        print("No se proporcionaron los parámetros necesarios")

if __name__ == "__main__":
    main()