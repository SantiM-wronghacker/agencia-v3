# ARCHIVO: clasificador_prioridad_tareas.py
# AREA: REAL ESTATE
# DESCRIPCION: Agente que realiza clasificador prioridad tareas
# TECNOLOGIA: Python

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

def clasificar_prioridad(tarea, prioridades=None):
    if prioridades is None:
        prioridades = {
            'alta': 1,
            'media': 2,
            'baja': 3
        }
    try:
        return prioridades[tarea['prioridad']]
    except (KeyError, ValueError):
        return 3

def calcular_tiempo_estimado(tarea, horas_trabajadas_por_dia=8):
    try:
        return float(tarea['tiempo_estimado']) * horas_trabajadas_por_dia  # convertir a horas trabajadas
    except (ValueError, KeyError):
        return 0.0

def calcular_costo_estimado(tarea, tipo_cambio=20):
    try:
        return float(tarea['costo_estimado']) * tipo_cambio  # convertir a MXN
    except (ValueError, KeyError):
        return 0.0

def calcular_fecha_vencimiento(tarea):
    try:
        return datetime.datetime.strptime(tarea['fecha_vencimiento'], '%Y-%m-%d')
    except (ValueError, KeyError):
        return datetime.datetime.now()

def main():
    try:
        if len(sys.argv) > 1:
            archivo_tareas = sys.argv[1]
        else:
            archivo_tareas = 'tareas.json'

        if len(sys.argv) > 2:
            prioridades = sys.argv[2].split(',')
            prioridades = {p.split(':')[0]: int(p.split(':')[1]) for p in prioridades}
        else:
            prioridades = {
                'alta': 1,
                'media': 2,
                'baja': 3
            }

        if len(sys.argv) > 3:
            horas_trabajadas_por_dia = int(sys.argv[3])
        else:
            horas_trabajadas_por_dia = 8

        if len(sys.argv) > 4:
            tipo_cambio = float(sys.argv[4])
        else:
            tipo_cambio = 20

        if not os.path.exists(archivo_tareas):
            print("Archivo de tareas no encontrado")
            return

        with open(archivo_tareas, 'r') as f:
            tareas = json.load(f)

        tareas_clasificadas = []
        for tarea in tareas:
            prioridad = clasificar_prioridad(tarea, prioridades)
            tarea['prioridad_numerica'] = prioridad
            tarea['tiempo_estimado_horas'] = calcular_tiempo_estimado(tarea, horas_trabajadas_por_dia)
            tarea['costo_estimado_mxn'] = calcular_costo_estimado(tarea, tipo_cambio)
            tarea['fecha_vencimiento_date'] = calcular_fecha_vencimiento(tarea)
            tareas_clasificadas.append(tarea)

        tareas_clasificadas.sort(key=lambda x: x['prioridad_numerica'])

        for tarea in tareas_clasificadas:
            print(f"Tarea: {tarea['nombre']}")
            print(f"Prioridad: {tarea['prioridad']}")
            print(f"Prioridad numerica: {tarea['prioridad_numerica']}")
            print(f"Tiempo estimado (horas): {tarea['tiempo_estimado_horas']}")
            print(f"Costo estimado (MXN): {tarea['costo_estimado_mxn']}")
            print(f"Fecha vencimiento: {tarea['fecha_vencimiento_date']}")
            print("--------------------")

        print("Resumen ejecutivo:")
        print(f"Total de tareas: {len(tareas_clasificadas)}")
        print(f"Total de horas estimadas: {sum(t['tiempo_estimado_horas'] for t in tareas_clasificadas)}")
        print(f"Total de costo estimado: {sum(t['costo_estimado_mxn'] for t in tareas_clasificadas)}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()