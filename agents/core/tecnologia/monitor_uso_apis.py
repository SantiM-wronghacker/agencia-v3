"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza monitor uso apis
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

def calcular_uso_diario(fecha_inicio, fecha_fin):
    dias = (fecha_fin - fecha_inicio).days + 1
    return random.randint(100, 5000) * dias

def calcular_uso_por_hora(uso_diario):
    return uso_diario / 24

def calcular_uso_por_minuto(uso_por_hora):
    return uso_por_hora / 60

def main():
    try:
        # Parámetros por defecto
        fecha_inicio = datetime.datetime.now() - datetime.timedelta(days=30)
        fecha_fin = datetime.datetime.now()
        umbral_alerta = 1000
        nombre_api = "API_GENERICA"

        # Lectura de parámetros desde sys.argv
        if len(sys.argv) > 1:
            fecha_inicio = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d')
        if len(sys.argv) > 2:
            fecha_fin = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d')
        if len(sys.argv) > 3:
            umbral_alerta = int(sys.argv[3])
        if len(sys.argv) > 4:
            nombre_api = sys.argv[4]

        # Validación de fechas
        if fecha_fin < fecha_inicio:
            raise ValueError("Fecha de fin no puede ser anterior a fecha de inicio")

        # Simulación de uso de APIs con datos más realistas
        uso_diario = calcular_uso_diario(fecha_inicio, fecha_fin)
        uso_por_hora = calcular_uso_por_hora(uso_diario)
        uso_por_minuto = calcular_uso_por_minuto(uso_por_hora)

        # Cálculo de estadísticas
        total_uso = uso_diario
        promedio_uso = total_uso / ((fecha_fin - fecha_inicio).days + 1)

        # Imprimir resultados
        print(f"Fecha de inicio: {fecha_inicio.strftime('%Y-%m-%d')}")
        print(f"Fecha de fin: {fecha_fin.strftime('%Y-%m-%d')}")
        print(f"API monitoreada: {nombre_api}")
        print(f"Uso total de API: {total_uso:,} llamadas")
        print(f"Uso promedio diario: {promedio_uso:.2f} llamadas/día")
        print(f"Uso por hora: {uso_por_hora:.2f} llamadas/hora")
        print(f"Uso por minuto: {uso_por_minuto:.2f} llamadas/minuto")
        print(f"Umbral de alerta: {umbral_alerta:,} llamadas")

        # Verificar si se supera el umbral de alerta
        if total_uso > umbral_alerta:
            print(f"ALERTA: Uso total de API supera el umbral de {umbral_alerta:,} llamadas")
        else:
            print(f"Uso total de API dentro del umbral de {umbral_alerta:,} llamadas")

        # Resumen ejecutivo
        print("\n=== RESUMEN EJECUTIVO ===")
        print(f"Periodo analizado: {fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}")
        print(f"API: {nombre_api}")
        print(f"Total llamadas: {total_uso:,}")
        print(f"Promedio diario: {promedio_uso:.2f} llamadas")
        print(f"Estado: {'ALERTA' if total_uso > umbral_alerta else 'NORMAL'}")

    except ValueError as ve:
        print(f"Error de validación: {str(ve)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()