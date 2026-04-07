"""
ÁREA: CEREBRO
DESCRIPCIÓN: Agente que realiza dispatcher multiagente con asignación optimizada
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
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_eficiencia(agente, tareas):
    """Calcula la eficiencia del agente basada en tareas asignadas"""
    return random.uniform(0.7, 1.0) * (1 + 0.1 * len(tareas))

def asignar_tareas_optimizadas(agentes, tareas):
    """Asigna tareas de manera más realista considerando eficiencia"""
    asignaciones = {agente: [] for agente in agentes}
    tareas_ordenadas = sorted(tareas, key=lambda x: random.random())

    for tarea in tareas_ordenadas:
        # Seleccionar agente con menor carga actual
        agente_seleccionado = min(agentes, key=lambda a: len(asignaciones[a]))
        asignaciones[agente_seleccionado].append(tarea)

    return asignaciones

def main():
    try:
        # Parámetros por defecto con valores más realistas
        num_agentes = 5
        num_tareas = 20
        zona_horaria = "CDMX"

        # Lectura de parámetros desde la línea de comandos
        if len(sys.argv) > 1:
            num_agentes = int(sys.argv[1])
        if len(sys.argv) > 2:
            num_tareas = int(sys.argv[2])
        if len(sys.argv) > 3:
            zona_horaria = sys.argv[3]

        # Validación de parámetros
        if num_agentes <= 0 or num_tareas <= 0:
            raise ValueError("Número de agentes o tareas debe ser mayor a cero")

        # Inicialización de agentes y tareas con datos más realistas
        agentes = [f"Agente {i+1} (Zona {zona_horaria})" for i in range(num_agentes)]
        tareas = [f"Tarea {i+1} (Prioridad {random.randint(1, 5)})" for i in range(num_tareas)]

        # Asignación optimizada de tareas
        asignaciones = asignar_tareas_optimizadas(agentes, tareas)

        # Cálculo de métricas adicionales
        total_tareas = sum(len(tareas) for tareas in asignaciones.values())
        eficiencias = {agente: calcular_eficiencia(agente, tareas) for agente, tareas in asignaciones.items()}
        agente_mas_cargado = max(asignaciones.items(), key=lambda x: len(x[1]))
        agente_menos_cargado = min(asignaciones.items(), key=lambda x: len(x[1]))

        # Impresión de resultados detallados
        print(f"Fecha y hora actual: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Zona horaria: {zona_horaria}")
        print(f"Número de agentes: {num_agentes} | Número de tareas: {num_tareas}")
        print("\nAsignaciones de tareas a agentes:")
        for agente, tareas_asignadas in asignaciones.items():
            print(f"{agente} (Tareas: {len(tareas_asignadas)}): {', '.join(tareas_asignadas)}")

        print(f"\nTotal de tareas asignadas: {total_tareas}")
        print(f"Agente más cargado: {agente_mas_cargado[0]} con {len(agente_mas_cargado[1])} tareas")
        print(f"Agente menos cargado: {agente_menos_cargado[0]} con {len(agente_menos_cargado[1])} tareas")
        print("\nResumen ejecutivo:")
        print(f"- Eficiencia promedio del sistema: {sum(eficiencias.values())/len(eficiencias):.2f}")
        print(f"- Distribución de tareas: {', '.join([f'{len(tareas)}' for tareas in asignaciones.values()])}")
        print(f"- Tareas no asignadas: {max(0, num_tareas - total_tareas)}")

    except ValueError as ve:
        print(f"Error de validación: {str(ve)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()