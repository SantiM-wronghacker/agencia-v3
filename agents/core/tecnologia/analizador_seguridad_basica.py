"""
ÁREA: TECNOLOGÍA
DESCRIPCIÓN: Agente que realiza análisis de seguridad básica con métricas mejoradas
TECNOLOGÍA: Python estándar
"""

import sys
import os
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

def calcular_porcentaje(eventos, eventos_recentes):
    if eventos:
        return (len(eventos_recentes) / len(eventos)) * 100
    return 0

def obtener_fecha_actual():
    return datetime.datetime.now().strftime('%Y-%m-%d')

def main():
    try:
        # Configuración predeterminada con parámetros mejorados
        archivo = sys.argv[1] if len(sys.argv) > 1 else "seguridad.json"
        dias = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        umbral_critico = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        umbral_alta = int(sys.argv[4]) if len(sys.argv) > 4 else 10

        # Verificar existencia del archivo
        if not os.path.exists(archivo):
            print(f"Error: Archivo {archivo} no encontrado")
            return

        # Leer datos de seguridad
        with open(archivo, 'r') as f:
            datos = json.load(f)

        # Análisis básico con manejo de casos edge
        eventos = datos.get('eventos', [])
        eventos_recentes = []
        fecha_actual = datetime.datetime.now()

        for e in eventos:
            try:
                fecha_evento = datetime.datetime.strptime(e['fecha'], '%Y-%m-%d')
                if (fecha_actual - fecha_evento).days <= dias:
                    eventos_recentes.append(e)
            except (KeyError, ValueError):
                continue

        # Estadísticas mejoradas
        total_eventos = len(eventos)
        eventos_recentes_count = len(eventos_recentes)
        eventos_criticos = sum(1 for e in eventos_recentes if e.get('nivel', '').upper() == 'CRÍTICO')
        eventos_alta = sum(1 for e in eventos_recentes if e.get('nivel', '').upper() == 'ALTA')
        eventos_baja = sum(1 for e in eventos_recentes if e.get('nivel', '').upper() == 'BAJA')
        eventos_desconocidos = eventos_recentes_count - (eventos_criticos + eventos_alta + eventos_baja)
        porcentaje_recentes = calcular_porcentaje(eventos, eventos_recentes)

        # Métricas adicionales para México
        eventos_por_dia = eventos_recentes_count / dias if dias > 0 else 0
        eventos_criticos_por_dia = eventos_criticos / dias if dias > 0 else 0

        # Resumen ejecutivo
        resumen = "ALTO RIESGO" if eventos_criticos >= umbral_critico else (
            "RIESGO MODERADO" if eventos_alta >= umbral_alta else "RIESGO BAJO")

        # Salida de resultados mejorada
        print("=== ANÁLISIS DE SEGURIDAD BÁSICO ===")
        print(f"Fecha de análisis: {obtener_fecha_actual()}")
        print(f"Total eventos registrados: {total_eventos}")
        print(f"Eventos en últimos {dias} días: {eventos_recentes_count} ({porcentaje_recentes:.1f}%)")
        print(f"Eventos críticos recientes: {eventos_criticos} ({eventos_criticos_por_dia:.2f} por día)")
        print(f"Eventos de alta prioridad recientes: {eventos_alta}")
        print(f"Eventos de baja prioridad recientes: {eventos_baja}")
        print(f"Eventos sin prioridad definida: {eventos_desconocidos}")
        print(f"Eventos por día en el periodo: {eventos_por_dia:.2f}")
        print("\n=== RESUMEN EJECUTIVO ===")
        print(f"Nivel de riesgo actual: {resumen}")
        print(f"Se recomienda atención especial si el nivel de riesgo es {resumen}")

    except Exception as e:
        print(f"Error en el análisis: {str(e)}")

if __name__ == "__main__":
    main()