"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora calificaciones
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
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def calcular_calificaciones(notas):
    calificaciones = []
    for nota in notas:
        try:
            if nota >= 90:
                calificacion = 5
            elif nota >= 80:
                calificacion = 4
            elif nota >= 70:
                calificacion = 3
            elif nota >= 60:
                calificacion = 2
            else:
                calificacion = 1
            calificaciones.append(calificacion)
        except Exception as e:
            print(f"Error al calcular calificación para nota {nota}: {str(e)}")
    return calificaciones

def calcular_promedio(calificaciones):
    try:
        return sum(calificaciones) / len(calificaciones)
    except ZeroDivisionError:
        return 0

def calcular_estudiantes_por_calificacion(calificaciones, calificacion):
    try:
        return calificaciones.count(calificacion)
    except Exception as e:
        print(f"Error al contar estudiantes con calificación {calificacion}: {str(e)}")
        return 0

def main():
    try:
        if len(sys.argv) > 1:
            notas = [float(nota) for nota in sys.argv[1:]]
        else:
            notas = [85, 92, 78, 95, 88, 70, 60, 80, 90, 50, 40, 30]
        
        if WEB:
            # Buscar datos reales con web_bridge
            datos = web.buscar("calificaciones estudiantes")
            texto = web.fetch_texto(datos)
            precios = web.extraer_precios(texto)
            print("Precios:", precios)
        else:
            calificaciones = calcular_calificaciones(notas)
            print("Notas:", notas)
            print("Calificaciones:", calificaciones)
            promedio = calcular_promedio(calificaciones)
            print("Promedio:", promedio)
            print("Número de estudiantes con calificación 5:", calcular_estudiantes_por_calificacion(calificaciones, 5))
            print("Número de estudiantes con calificación 4:", calcular_estudiantes_por_calificacion(calificaciones, 4))
            print("Número de estudiantes con calificación 3:", calcular_estudiantes_por_calificacion(calificaciones, 3))
            print("Número de estudiantes con calificación 2:", calcular_estudiantes_por_calificacion(calificaciones, 2))
            print("Número de estudiantes con calificación 1:", calcular_estudiantes_por_calificacion(calificaciones, 1))
        
        print("\nResumen Ejecutivo:")
        print("El promedio de calificaciones es:", promedio)
        print("El número de estudiantes con calificación 5 es:", calcular_estudiantes_por_calificacion(calificaciones, 5))
        print("El número de estudiantes con calificación 4 es:", calcular_estudiantes_por_calificacion(calificaciones, 4))
        print("El número de estudiantes con calificación 3 es:", calcular_estudiantes_por_calificacion(calificaciones, 3))
        print("El número de estudiantes con calificación 2 es:", calcular_estudiantes_por_calificacion(calificaciones, 2))
        print("El número de estudiantes con calificación 1 es:", calcular_estudiantes_por_calificacion(calificaciones, 1))
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()