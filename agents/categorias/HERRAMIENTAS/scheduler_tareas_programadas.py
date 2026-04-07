"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza scheduler tareas programadas
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import os
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def main():
    try:
        # Configuración de tareas programadas
        if len(sys.argv) > 1:
            tareas = json.loads(sys.argv[1])
        else:
            tareas = [
                {"nombre": "Tarea 1", "hora": 8, "minuto": 0, "duracion": 30},
                {"nombre": "Tarea 2", "hora": 12, "minuto": 30, "duracion": 60},
                {"nombre": "Tarea 3", "hora": 16, "minuto": 0, "duracion": 45},
            ]

        # Fecha y hora actual
        ahora = datetime.datetime.now()
        print(f"Fecha y hora actual: {ahora.strftime('%Y-%m-%d %H:%M:%S')}")

        # Listado de tareas programadas
        print("Tareas programadas:")
        for i, tarea in enumerate(tareas, 1):
            print(f"{i}. {tarea['nombre']} a las {tarea['hora']}:{tarea['minuto']:02d} durante {tarea['duracion']} minutos")

        # Simulación de ejecución de tareas
        print("\nEjecución de tareas:")
        for i, tarea in enumerate(tareas, 1):
            if ahora.hour == tarea["hora"] and ahora.minute == tarea["minuto"]:
                print(f"{i}. Ejecutando {tarea['nombre']}")
            elif ahora.hour > tarea["hora"] or (ahora.hour == tarea["hora"] and ahora.minute > tarea["minuto"]):
                print(f"{i}. {tarea['nombre']} ya ejecutada")
            else:
                print(f"{i}. {tarea['nombre']} pendiente de ejecución")

        # Estadísticas de tareas
        print("\nEstadísticas de tareas:")
        total_tareas = len(tareas)
        tareas_ejecutadas = 0
        tareas_pendientes = 0
        for tarea in tareas:
            if ahora.hour > tarea["hora"] or (ahora.hour == tarea["hora"] and ahora.minute > tarea["minuto"]):
                tareas_ejecutadas += 1
            elif ahora.hour < tarea["hora"] or (ahora.hour == tarea["hora"] and ahora.minute < tarea["minuto"]):
                tareas_pendientes += 1

        print(f"Total de tareas: {total_tareas}")
        print(f"Tareas ejecutadas: {tareas_ejecutadas}")
        print(f"Tareas pendientes: {tareas_pendientes}")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        if tareas_ejecutadas > 0:
            print(f"Se han ejecutado {tareas_ejecutadas} de {total_tareas} tareas.")
        else:
            print(f"No se han ejecutado tareas.")

        if tareas_pendientes > 0:
            print(f"Quedan {tareas_pendientes} tareas pendientes de ejecución.")
        else:
            print(f"No quedan tareas pendientes de ejecución.")

        if random.random() < 0.5:
            print(f"Se ha producido un error inesperado: {random.choice(['Error 1', 'Error 2', 'Error 3'])}")

    except json.JSONDecodeError as e:
        print(f"Error al cargar tareas: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()