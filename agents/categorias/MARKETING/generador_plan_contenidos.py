"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza generador plan contenidos
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
        num_contenidos = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        fecha_inicial = datetime.date.today()
        fecha_final = fecha_inicial + datetime.timedelta(days=30)

        # Generar plan de contenidos
        plan_contenidos = []
        for i in range(num_contenidos):
            fecha_publicacion = fecha_inicial + datetime.timedelta(days=i)
            titulo = f"Contenido {i+1} - {fecha_publicacion.strftime('%d/%m/%Y')}"
            descripcion = f"Descripción del contenido {i+1}"
            keywords = [f"keyword {i+1}", f"keyword {i+2}"]
            plan_contenidos.append({
                "titulo": titulo,
                "descripcion": descripcion,
                "fecha_publicacion": fecha_publicacion.strftime('%d/%m/%Y'),
                "keywords": keywords
            })

        # Imprimir plan de contenidos
        print("Plan de Contenidos:")
        print("--------------------")
        for i, contenido in enumerate(plan_contenidos):
            print(f"Contenido {i+1}:")
            print(f"Fecha Publicación: {contenido['fecha_publicacion']}")
            print(f"Título: {contenido['titulo']}")
            print(f"Descripción: {contenido['descripcion']}")
            print(f"Keywords: {', '.join(contenido['keywords'])}")
            print(f"Tipo de contenido: {random.choice(['Artículo', 'Video', 'Imagen'])}")
            print(f"Plataforma de publicación: {random.choice(['Facebook', 'Instagram', 'Twitter'])}")
            print("--------------------")

        # Estadísticas del plan de contenidos
        print("Estadísticas del Plan de Contenidos:")
        print("-----------------------------------")
        print(f"Total de Contenidos: {len(plan_contenidos)}")
        print(f"Fecha Inicial: {fecha_inicial.strftime('%d/%m/%Y')}")
        print(f"Fecha Final: {fecha_final.strftime('%d/%m/%Y')}")
        print(f"Duración del Plan: {(fecha_final - fecha_inicial).days} días")
        print(f"Promedio de contenidos por día: {len(plan_contenidos) / (fecha_final - fecha_inicial).days}")
        print(f"Contenido más largo: {max(len(contenido['descripcion']) for contenido in plan_contenidos)} caracteres")

        # Resumen ejecutivo
        print("Resumen Ejecutivo:")
        print("--------------------")
        print(f"El plan de contenidos consta de {len(plan_contenidos)} contenidos, que se publicarán entre el {fecha_inicial.strftime('%d/%m/%Y')} y el {fecha_final.strftime('%d/%m/%Y')}.")
        print(f"El contenido más común será el {random.choice(['Artículo', 'Video', 'Imagen'])} y se publicará en {random.choice(['Facebook', 'Instagram', 'Twitter'])}.")
        print(f"El promedio de contenidos por día es de {len(plan_contenidos) / (fecha_final - fecha_inicial).days}.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()