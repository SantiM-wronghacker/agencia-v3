"""
ÁREA: CEREBRO
DESCRIPCIÓN: Agente que realiza orquestador agentes industria
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_tiempo_realista(tiempo_estimado):
    # Ajuste para condiciones reales en México (tráfico, clima, etc.)
    factor_ajuste = random.uniform(0.8, 1.5)
    return round(tiempo_estimado * factor_ajuste, 2)

def main():
    try:
        # Obteniendo argumentos de la línea de comandos
        if len(sys.argv) > 1:
            num_agentes = int(sys.argv[1])
            num_tareas = int(sys.argv[2])
            if num_agentes <= 0 or num_tareas <= 0:
                raise ValueError("Número de agentes o tareas debe ser positivo")
        else:
            num_agentes = 5
            num_tareas = 10

        # Simulación de agentes y tareas
        agentes = []
        for i in range(num_agentes):
            agente = {
                "id": i,
                "tareas": [],
                "disponibilidad": random.choice(["Alta", "Media", "Baja"]),
                "ubicacion": random.choice(["CDMX", "Monterrey", "Guadalajara", "Puebla"])
            }
            agentes.append(agente)

        for i in range(num_tareas):
            tarea = {
                "id": i,
                "descripcion": f"Tarea {i}",
                "tiempo_estimado": random.uniform(1, 10),
                "prioridad": random.choice(["Alta", "Media", "Baja"]),
                "complejidad": random.randint(1, 5)
            }
            agente_asignado = random.choice(agentes)
            agente_asignado["tareas"].append(tarea)

        # Imprimiendo resultados
        print(f"Fecha y hora actual: {datetime.datetime.now()}")
        print(f"Número de agentes: {num_agentes}")
        print(f"Número de tareas: {num_tareas}")
        print(f"Agentes y tareas asignadas:")
        for agente in agentes:
            print(f"Agente {agente['id']} ({agente['ubicacion']}, {agente['disponibilidad']}): {len(agente['tareas'])} tareas")
            for tarea in agente["tareas"]:
                tiempo_real = calcular_tiempo_realista(tarea["tiempo_estimado"])
                print(f"  - Tarea {tarea['id']}: {tarea['descripcion']} (Prioridad: {tarea['prioridad']}, Complejidad: {tarea['complejidad']}, Tiempo estimado: {tiempo_real} horas)")

        # Estadísticas
        total_tareas = sum(len(agente["tareas"]) for agente in agentes)
        total_tiempo_estimado = sum(sum(calcular_tiempo_realista(tarea["tiempo_estimado"]) for tarea in agente["tareas"]) for agente in agentes)
        agentes_ocupados = sum(1 for agente in agentes if len(agente["tareas"]) > 0)
        tareas_alta_prioridad = sum(sum(1 for tarea in agente["tareas"] if tarea["prioridad"] == "Alta") for agente in agentes)

        print(f"\nEstadísticas detalladas:")
        print(f"Total de tareas: {total_tareas}")
        print(f"Tiempo total estimado (ajustado): {total_tiempo_estimado} horas")
        print(f"Agentes con tareas asignadas: {agentes_ocupados}/{num_agentes}")
        print(f"Tareas de alta prioridad: {tareas_alta_prioridad}")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"Se han asignado {total_tareas} tareas a {agentes_ocupados} agentes.")
        print(f"El tiempo total estimado para completar todas las tareas es de {total_tiempo_estimado} horas.")
        print(f"Se recomienda priorizar las {tareas_alta_prioridad} tareas críticas.")
        print(f"La distribución geográfica de los agentes muestra mayor concentración en {max(set(agente['ubicacion'] for agente in agentes), key=lambda x: list(agente['ubicacion'] for agente in agentes).count(x))}.")

    except ValueError as ve:
        print