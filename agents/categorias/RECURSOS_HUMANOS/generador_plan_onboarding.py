"""
ÁREA: RECURSOS HUMANOS
DESCRIPCIÓN: Agente que realiza generador plan onboarding
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
        nombre = sys.argv[1] if len(sys.argv) > 1 else "Juan Pérez"
        puesto = sys.argv[2] if len(sys.argv) > 2 else "Desarrollador"
        fecha_inicio = sys.argv[3] if len(sys.argv) > 3 else datetime.date.today().strftime("%Y-%m-%d")
        fecha_fin = sys.argv[4] if len(sys.argv) > 4 else (datetime.date.today() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")

        plan_onboarding = {
            "nombre": nombre,
            "puesto": puesto,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "actividades": [
                {"dia": 1, "actividad": "Presentación con el equipo"},
                {"dia": 3, "actividad": "Revisión de políticas y procedimientos"},
                {"dia": 7, "actividad": "Entrega de equipo y herramientas"},
                {"dia": 14, "actividad": "Revisión de progreso y objetivos"},
                {"dia": 30, "actividad": "Evaluación final y retroalimentación"}
            ]
        }

        print("Plan de Onboarding para", nombre)
        print("Puesto:", puesto)
        print("Fecha de inicio:", fecha_inicio)
        print("Fecha de fin:", fecha_fin)
        print("Número de días de onboarding:", (datetime.datetime.strptime(fecha_fin, "%Y-%m-%d") - datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")).days)

        for actividad in plan_onboarding["actividades"]:
            print("Día", actividad["dia"], ":", actividad["actividad"])

        print("Detalles del plan de onboarding:")
        print("Duración del plan:", (datetime.datetime.strptime(fecha_fin, "%Y-%m-%d") - datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")).days, "días")
        print("Fecha de inicio de la evaluación final:", (datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d") + datetime.timedelta(days=29)).strftime("%Y-%m-%d"))
        print("Fecha de fin de la evaluación final:", (datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d") + datetime.timedelta(days=30)).strftime("%Y-%m-%d"))
        print("Resumen del plan de onboarding:")
        print("El plan de onboarding para", nombre, "tiene una duración de", (datetime.datetime.strptime(fecha_fin, "%Y-%m-%d") - datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")).days, "días")
        print("El plan incluye", len(plan_onboarding["actividades"]), "actividades")
        print("La evaluación final se realizará el día", (datetime.datetime.strptime(fecha_fin, "%Y-%m-%d") - datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")).days)

        print("\nResumen Ejecutivo:")
        print("Nombre:", nombre)
        print("Puesto:", puesto)
        print("Duración del plan de onboarding:", (datetime.datetime.strptime(fecha_fin, "%Y-%m-%d") - datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")).days, "días")
        print("Número de actividades:", len(plan_onboarding["actividades"]))

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()