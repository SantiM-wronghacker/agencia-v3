"""
ÁREA: EDUCACIÓN
DESCRIPCIÓN: Agente que realiza generador temario curso
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def generar_temario_curso(duracion_semanas_min=8, duracion_semanas_max=16, costo_mxn_min=2000, costo_mxn_max=5000, participantes_min=15, participantes_max=30):
    temas_base = [
        "Introducción a la educación en México",
        "Metodologías de enseñanza",
        "Evaluación educativa",
        "Tecnologías en el aula",
        "Inclusión y diversidad"
    ]

    sub_temas = {
        "Introducción a la educación en México": [
            "Sistema educativo mexicano",
            "Marco curricular nacional",
            "Políticas educativas actuales"
        ],
        "Metodologías de enseñanza": [
            "Aprendizaje basado en proyectos",
            "Clase invertida",
            "Gamificación educativa"
        ],
        "Evaluación educativa": [
            "Rúbricas de evaluación",
            "Evaluación formativa",
            "Evaluación sumativa"
        ],
        "Tecnologías en el aula": [
            "Herramientas digitales",
            "Plataformas educativas",
            "Seguridad digital en el aula"
        ],
        "Inclusión y diversidad": [
            "Educación inclusiva",
            "Atención a la diversidad",
            "Educación intercultural"
        ]
    }

    try:
        duracion_semanas = random.randint(duracion_semanas_min, duracion_semanas_max)
        costo_mxn = round(random.uniform(costo_mxn_min, costo_mxn_max), 2)
        participantes = random.randint(participantes_min, participantes_max)

        temario = {
            "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temas": temas_base,
            "sub_temas": sub_temas,
            "duracion_semanas": duracion_semanas,
            "costo_mxn": costo_mxn,
            "participantes": participantes
        }

        return temario
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def main():
    if len(sys.argv) > 1:
        try:
            duracion_semanas_min = int(sys.argv[1])
            duracion_semanas_max = int(sys.argv[2])
            costo_mxn_min = float(sys.argv[3])
            costo_mxn_max = float(sys.argv[4])
            participantes_min = int(sys.argv[5])
            participantes_max = int(sys.argv[6])
        except ValueError:
            print("Parámetros incorrectos")
            return
    else:
        duracion_semanas_min = 8
        duracion_semanas_max = 16
        costo_mxn_min = 2000
        costo_mxn_max = 5000
        participantes_min = 15
        participantes_max = 30

    temario = generar_temario_curso(duracion_semanas_min, duracion_semanas_max, costo_mxn_min, costo_mxn_max, participantes_min, participantes_max)

    if temario is not None:
        print("=== TEMARIO DE CURSO GENERADO ===")
        print(f"Fecha de generación: {temario['fecha_generacion']}")
        print(f"Duración: {temario['duracion_semanas']} semanas")
        print(f"Costo: ${temario['costo_mxn']} MXN")
        print(f"Participantes: {temario['participantes']}")
        print("Temas:")
        for tema in temario['temas']:
            print(f"- {tema}")
        print("Subtemas:")
        for tema, subtemas in temario['sub_temas'].items():
            print(f"- {tema}:")
            for subtema in subtemas:
                print(f"  - {subtema}")
        print("=== RESUMEN EJECUTIVO ===")
        print(f"Se ha generado un temario de curso con {temario['duracion_semanas']} semanas de duración, un costo de ${temario['costo_mxn']} MXN y {temario['participantes']} participantes.")

if __name__ == "__main__":
    main()