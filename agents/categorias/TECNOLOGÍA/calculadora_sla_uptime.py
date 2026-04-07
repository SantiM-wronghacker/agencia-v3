import sys
import math
from datetime import datetime, timedelta
import os

ARCHIVO = os.path.basename(__file__)
AREA = "FINANZAS"
DESCRIPCION = "Calculadora Sla Uptime"
TECNOLOGIA = "Python"

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_sla_uptime(dias_baja=0, horas_baja=0, minutos_baja=0, sla_objetivo=99.9):
    """
    Calcula el SLA y uptime basado en tiempo de baja.
    """
    # Convertir tiempo de baja a segundos
    tiempo_baja_total = dias_baja * 86400 + horas_baja * 3600 + minutos_baja * 60

    # Tiempo total en un año (365 días)
    tiempo_total_anio = 365 * 86400

    # Calcular uptime
    uptime = (tiempo_total_anio - tiempo_baja_total) / tiempo_total_anio * 100

    # Calcular SLA
    sla = min(uptime, sla_objetivo)

    # Calcular tiempo de baja en días y horas
    tiempo_baja_dias = round(tiempo_baja_total / 86400, 2)
    tiempo_baja_horas = round(tiempo_baja_total / 3600, 2)

    # Calcular tiempo de baja en porcentaje del año
    tiempo_baja_porcentaje = (tiempo_baja_total / tiempo_total_anio) * 100

    # Calcular tiempo de baja en semanas y minutos
    tiempo_baja_semanas = round(tiempo_baja_total / (7 * 86400), 2)
    tiempo_baja_minutos = round(tiempo_baja_total / 60, 2)

    # Calcular tiempo de baja en meses y años
    tiempo_baja_meses = round(tiempo_baja_total / (30 * 86400), 2)
    tiempo_baja_anios = round(tiempo_baja_total / (365 * 86400), 2)

    return {
        "tiempo_baja_total": tiempo_baja_total,
        "uptime": round(uptime, 2),
        "sla": round(sla, 2),
        "tiempo_baja_horas": tiempo_baja_horas,
        "tiempo_baja_dias": tiempo_baja_dias,
        "tiempo_baja_porcentaje": tiempo_baja_porcentaje,
        "tiempo_baja_semanas": tiempo_baja_semanas,
        "tiempo_baja_minutos": tiempo_baja_minutos,
        "tiempo_baja_meses": tiempo_baja_meses,
        "tiempo_baja_anios": tiempo_baja_anios
    }

def calcular_sla_uptime_mexico(dias_baja=0, horas_baja=0, minutos_baja=0, sla_objetivo=99.9):
    """
    Calcula el SLA y uptime basado en tiempo de baja, teniendo en cuenta el horario de México.
    """
    # Convertir tiempo de baja a segundos
    tiempo_baja_total = dias_baja * 86400 + horas_baja * 3600 + minutos_baja * 60

    # Tiempo total en un año (365 días)
    tiempo_total_anio = 365 * 86400

    # Calcular uptime
    uptime = (tiempo_total_anio - tiempo_baja_total) / tiempo_total_anio * 100

    # Calcular SLA
    sla = min(uptime, sla_objetivo)

    # Calcular tiempo de baja en días y horas
    tiempo_baja_dias = round(tiempo_baja_total / 86400, 2)
    tiempo_baja_horas = round(tiempo_baja_total / 3600, 2)

    # Calcular tiempo de baja en porcentaje del año
    tiempo_baja_porcentaje = (tiempo_baja_total / tiempo_total_anio) * 100

    # Calcular tiempo de baja en semanas y minutos
    tiempo_baja_semanas = round(tiempo_baja_total / (7 * 86400), 2)
    tiempo_baja_minutos = round(tiempo_baja_total / 60, 2)

    # Calcular tiempo de baja en meses y años
    tiempo_baja_meses = round(tiempo_baja_total / (30 * 86400), 2)
    tiempo_baja_anios = round(tiempo_baja_total / (365 * 86400), 2)

    # Aplicar