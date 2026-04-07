"""
ÁREA: EDUCACIÓN
DESCRIPCIÓN: Agente que realiza generador de certificado
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_certificado(nombre, institucion, fecha, calificacion_final, calificacion_promedio, materias, semestre, carrera, nota_minima_aprobacion, nota_maxima_aprobacion, nota_minima_reprobacion, nota_maxima_reprobacion):
    certificado = f"Certificado de {nombre}\n"
    certificado += f"Institución: {institucion}\n"
    certificado += f"Fecha: {fecha}\n"
    certificado += f"Semestre: {semestre}\n"
    certificado += f"Carrera: {carrera}\n"
    certificado += f"Calificación promedio: {calificacion_promedio:.2f}\n"
    certificado += f"Materias aprobadas: {', '.join(materias)}\n"
    certificado += f"Este certificado es oficial y fue generado por el sistema de educación.\n"
    certificado += f"Promedio de calificaciones: {calificacion_promedio:.2f}\n"
    certificado += f"Calificación final: {calificacion_final:.2f}\n"
    certificado += f"Calificación final calculada: {(calificacion_promedio * 0.6 + calificacion_final * 0.4):.2f}\n"
    certificado += f"Cantidad de materias aprobadas: {len(materias)}\n"
    certificado += f"Nota mínima para aprobar: {nota_minima_aprobacion:.2f}\n"
    certificado += f"Nota máxima para aprobar: {nota_maxima_aprobacion:.2f}\n"
    certificado += f"Nota mínima para reprobar: {nota_minima_reprobacion:.2f}\n"
    certificado += f"Nota máxima para reprobar: {nota_maxima_reprobacion:.2f}\n"
    certificado += f"Resumen ejecutivo: El estudiante ha demostrado un buen desempeño en el semestre actual.\n"
    certificado += f"Resumen ejecutivo: El estudiante ha aprobado {len(materias)} de {len(materias) + 1} materias.\n"
    return certificado

def calcular_promedio(calificaciones):
    try:
        return sum(calificaciones) / len(calificaciones)
    except ZeroDivisionError:
        return 0

def calcular_calificacion_final(calificacion_promedio, calificacion_final):
    try:
        return calificacion_promedio * 0.6 + calificacion_final * 0.4
    except TypeError:
        return 0

def main():
    try:
        if len(sys.argv) != 14:
            print("Error: Faltan argumentos. Ejemplo: python generador_certificado.py Juan Pérez Universidad Nacional Autónoma de México 90.5 8.5 'Matemáticas, Física, Química' 1 Ingeniería en Sistemas Computacionales 70 80 60 50")
            sys.exit(1)

        nombre = sys.argv[1]
        institucion = sys.argv[2]
        calificacion_final = float(sys.argv[3])
        calificacion_promedio = float(sys.argv[4])
        materias = sys.argv[5].split(', ')
        semestre = sys.argv[6]
        carrera = sys.argv[7]
        nota_minima_aprobacion = float(sys.argv[8])
        nota_maxima_aprobacion = float(sys.argv[9])
        nota_minima_reprobacion = float(sys.argv[10])
        nota_maxima_reprobacion = float(sys.argv[11])
        fecha = sys.argv[12]
        print(generar_certificado(nombre, institucion, fecha, calificacion_final, calificacion_promedio, materias, semestre, carrera, nota_minima_aprobacion, nota_maxima_aprobacion, nota_minima_reprobacion, nota_maxima_reprobacion))

    except Exception as e:
        print("Error: ", str(e))

if __name__ == "__main__":
    main()