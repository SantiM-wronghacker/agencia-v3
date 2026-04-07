"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza generador calendario editorial
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import random
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def generar_calendario_editorial(anio=datetime.datetime.now().year):
    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    eventos = [
        {"nombre": "Día de la Independencia", "fecha": "16 de septiembre", "descripcion": "Día de la independencia de México"},
        {"nombre": "Día de Muertos", "fecha": "2 de noviembre", "descripcion": "Día de muertos, celebración mexicana"},
        {"nombre": "Navidad", "fecha": "25 de diciembre", "descripcion": "Día de Navidad, celebración cristiana"},
        {"nombre": "Día del Niño", "fecha": "30 de abril", "descripcion": "Día del niño, celebración mexicana"},
        {"nombre": "Día de la Madre", "fecha": "10 de mayo", "descripcion": "Día de la madre, celebración mexicana"}
    ]

    calendario = []
    for mes in meses:
        eventos_mes = [e for e in eventos if e["fecha"].split()[2] == mes]
        presupuesto = random.randint(5000, 20000)
        publicaciones = random.randint(3, 8)
        alcance = random.randint(1000, 5000)
        engagement = round(random.uniform(0.1, 0.5), 2)
        calendario.append({
            "mes": mes,
            "eventos": eventos_mes,
            "presupuesto": presupuesto,
            "publicaciones": publicaciones,
            "alcance": alcance,
            "engagement": engagement
        })

    return calendario

def main():
    try:
        if len(sys.argv) > 1:
            anio = int(sys.argv[1])
        else:
            anio = datetime.datetime.now().year

        calendario = generar_calendario_editorial(anio)

        total_presupuesto = 0
        total_publicaciones = 0
        total_alcance = 0
        total_engagement = 0

        for mes in calendario:
            print(f"Mes: {mes['mes']}")
            print(f"Eventos: {', '.join([e['nombre'] for e in mes['eventos']])}")
            print(f"Descripciones: {', '.join([e['descripcion'] for e in mes['eventos']])}")
            print(f"Presupuesto asignado: ${mes['presupuesto']:.2f} MXN")
            print(f"Publicaciones planificadas: {mes['publicaciones']}")
            print(f"Alcance estimado: {mes['alcance']} personas")
            print(f"Engagement estimado: {mes['engagement']*100:.2f}%")
            print("-" * 40)

            total_presupuesto += mes['presupuesto']
            total_publicaciones += mes['publicaciones']
            total_alcance += mes['alcance']
            total_engagement += mes['engagement']

        print("Resumen ejecutivo:")
        print(f"Total presupuesto: ${total_presupuesto:.2f} MXN")
        print(f"Total publicaciones: {total_publicaciones}")
        print(f"Total alcance: {total_alcance} personas")
        print(f"Total engagement: {total_engagement/len(calendario)*100:.2f}%")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

    except IndexError as e:
        print(f"Error de índice: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()