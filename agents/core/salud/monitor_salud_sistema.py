"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza monitor salud sistema con métricas ampliadas
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def obtener_memoria_total():
    try:
        return os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    except Exception as e:
        print(f"Error al obtener memoria total: {e}")
        return 0

def obtener_memoria_disponible():
    try:
        return os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_AVPHYS_PAGES')
    except Exception as e:
        print(f"Error al obtener memoria disponible: {e}")
        return 0

def obtener_memoria_porcentaje():
    try:
        total = obtener_memoria_total()
        disponible = obtener_memoria_disponible()
        if total > 0:
            return (disponible / total) * 100
        return 0
    except Exception as e:
        print(f"Error al calcular porcentaje de memoria: {e}")
        return 0

def obtener_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            uptime = float(f.readline().split()[0])
            dias = math.floor(uptime / 60 / 60 / 24)
            horas = math.floor((uptime % (60 * 60 * 24)) / 60 / 60)
            minutos = math.floor((uptime % (60 * 60)) / 60)
            return f"{dias} días, {horas} horas, {minutos} minutos"
    except Exception as e:
        print(f"Error al obtener uptime: {e}")
        return "No disponible"

def obtener_procesos_actuales():
    try:
        return len(os.listdir('/proc')) - 2
    except Exception as e:
        print(f"Error al obtener procesos: {e}")
        return 0

def obtener_carga_promedio():
    try:
        with open('/proc/loadavg', 'r') as f:
            carga = f.readline().split()
            return carga[0], carga[1], carga[2]
    except Exception as e:
        print(f"Error al obtener carga promedio: {e}")
        return 0, 0, 0

def obtener_uso_cpu():
    try:
        with open('/proc/stat', 'r') as f:
            line = f.readline()
            values = line.split()[1:5]
            idle = float(values[3])
            total = sum(float(x) for x in values)
            return (1 - idle / total) * 100
    except Exception as e:
        print(f"Error al obtener uso de CPU: {e}")
        return 0

def obtener_temperatura_cpu():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.readline()) / 1000
            return temp
    except Exception as e:
        print(f"Error al obtener temperatura CPU: {e}")
        return 0

def obtener_fecha_hora():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generar_resumen_ejecutivo(memoria_porcentaje, uso_cpu, carga_1min):
    try:
        resumen = []
        if memoria_porcentaje < 20:
            resumen.append("ALERTA: Memoria crítica (menos del 20% disponible)")
        elif memoria_porcentaje < 40:
            resumen.append("ADVERTENCIA: Memoria baja (menos del 40% disponible)")

        if uso_cpu > 90:
            resumen.append("ALERTA: Uso de CPU crítico (más del 90%)")
        elif uso_cpu > 70:
            resumen.append("ADVERTENCIA: Uso de CPU alto (más del 70%)")

        if float(carga_1min) > 2.0:
            resumen.append("ALERTA: Carga del sistema elevada (más de 2.0 en 1 minuto)")

        if not resumen:
            resumen.append("Sistema operativo en condiciones normales")

        return " - ".join(resumen)
    except Exception as e:
        print(f"Error al generar resumen ejecutivo: {e}")
        return "No disponible"