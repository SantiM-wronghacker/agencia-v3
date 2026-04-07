"""
ÁREA: EDUCACION
DESCRIPCIÓN: Agente que realiza planificador academico
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
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def obtener_datos_academicos(filename='datos_academicos.json'):
    try:
        # Obtiene datos académicos desde archivo JSON
        with open(filename, 'r') as archivo:
            datos_academicos = json.load(archivo)
        return datos_academicos
    except FileNotFoundError:
        print(f"Error: No se encuentra el archivo de datos académicos '{filename}'.")
        return None
    except json.JSONDecodeError:
        print(f"Error: El archivo de datos académicos '{filename}' no es válido.")
        return None

def calcular_promedio_notas(datos_academicos):
    try:
        return sum(datos_academicos["notas"]) / len(datos_academicos["notas"])
    except ZeroDivisionError:
        print("Error: No se pueden calcular promedios con cero notas.")
        return None
    except KeyError:
        print("Error: Faltan datos académicos.")
        return None

def calcular_plan_estudios(datos_academicos):
    try:
        plan_estudios = {}
        for i in range(len(datos_academicos["materias"])):
            plan_estudios[datos_academicos["materias"][i]] = {
                "creditos": datos_academicos["creditos"][i],
                "nota": datos_academicos["notas"][i]
            }
        return plan_estudios
    except KeyError:
        print("Error: Faltan datos académicos.")
        return None

def buscar_precios_libros():
    try:
        if WEB:
            # Busca datos de precios de libros de texto
            precios_libros = web.buscar("precios de libros de texto")
            # Extrae precios de libros de texto
            precios_libros = web.extraer_precios(precios_libros)
            return precios_libros
        else:
            print("Error: No hay conexión a internet.")
            return None
    except Exception as e:
        print("Error:", str(e))
        return None

def calcular_cuota_estudios(datos_academicos):
    try:
        promedio_notas = calcular_promedio_notas(datos_academicos)
        creditos_total = sum(datos_academicos["creditos"])
        cuota_estudios = promedio_notas * creditos_total
        return cuota_estudios
    except TypeError:
        print("Error: No se pueden calcular la cuota de estudios.")
        return None

def calcular_cantidad_libros(datos_academicos):
    try:
        cantidad_libros = sum(datos_academicos["creditos"]) * 0.5
        return cantidad_libros
    except TypeError:
        print("Error: No se pueden calcular la cantidad de libros.")
        return None

def imprimir_resumen(datos_academicos):
    print("Resumen ejecutivo:")
    print(f"Promedio de notas: {calcular_promedio_notas(datos_academicos)}")
    print(f"Plan de estudios: {calcular_plan_estudios(datos_academicos)}")
    print(f"Cuota de estudios: {calcular_cuota_estudios(datos_academicos)}")
    print(f"Cantidad de libros: {calcular_cantidad_libros(datos_academicos)}")

def main():
    filename = 'datos_academicos.json'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    datos_academicos = obtener_datos_academicos(filename)
    if datos_academicos:
        imprimir_resumen(datos_academicos)
        if WEB:
            precios_libros = buscar_precios_libros()
            if precios_libros:
                print(f"Precios de libros de texto: {precios_libros}")
        else:
            print("No hay conexión a internet.")

if __name__ == "__main__":
    main()