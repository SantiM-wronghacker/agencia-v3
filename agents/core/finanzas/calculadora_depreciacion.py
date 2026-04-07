# ARCHIVO: calculadora_depreciacion.py
# AREA: FINANZAS
# DESCRIPCION: Calculadora Depreciacion
# TECNOLOGIA: Python

import os
import sys
import json
import datetime
import math
import re
import random

def calcular_depreciacion(actividad, precio_compra, vida_util, tasa_interes):
    try:
        if tasa_interes == 0:
            raise ZeroDivisionError
        depreciacion_acumulada = 0
        for i in range(1, vida_util + 1):
            depreciacion_anual = precio_compra * (tasa_interes / 100) * i
            depreciacion_acumulada += depreciacion_anual
        return depreciacion_acumulada
    except ZeroDivisionError:
        print("Error: Tasa de interés no puede ser 0")
        return 0

def calcular_depreciacion_lineal(actividad, precio_compra, vida_util, tasa_interes):
    try:
        if tasa_interes == 0:
            raise ZeroDivisionError
        depreciacion_anual = precio_compra * (tasa_interes / 100)
        depreciacion_acumulada = depreciacion_anual * vida_util
        return depreciacion_acumulada
    except ZeroDivisionError:
        print("Error: Tasa de interés no puede ser 0")
        return 0

def calcular_depreciacion_acelerada(actividad, precio_compra, vida_util, tasa_interes):
    try:
        if tasa_interes == 0:
            raise ZeroDivisionError
        depreciacion_acumulada = 0
        for i in range(1, vida_util + 1):
            depreciacion_anual = precio_compra * (tasa_interes / 100) * (1 - (1 + tasa_interes / 100) ** (-i))
            depreciacion_acumulada += depreciacion_anual
        return depreciacion_acumulada
    except ZeroDivisionError:
        print("Error: Tasa de interés no puede ser 0")
        return 0

def calcular_depreciacion_mexicana(actividad, precio_compra, vida_util, tasa_interes):
    try:
        if tasa_interes == 0:
            raise ZeroDivisionError
        depreciacion_acumulada = 0
        for i in range(1, vida_util + 1):
            depreciacion_anual = precio_compra * (tasa_interes / 100) * (i / 12)
            depreciacion_acumulada += depreciacion_anual
        return depreciacion_acumulada
    except ZeroDivisionError:
        print("Error: Tasa de interés no puede ser 0")
        return 0

def main():
    if len(sys.argv) != 8:
        print("Error: Faltan argumentos")
        print("Uso: python calculadora_depreciacion.py <actividad> <precio_compra> <vida_util> <tasa_interes> <tipo_depreciacion> <tasa_interes_mexicana> <tipo_depreciacion_mexicana>")
        return
    actividad = sys.argv[1]
    precio_compra = float(sys.argv[2])
    vida_util = int(sys.argv[3])
    tasa_interes = float(sys.argv[4])
    tipo_depreciacion = sys.argv[5]
    tasa_interes_mexicana = float(sys.argv[6])
    tipo_depreciacion_mexicana = sys.argv[7]
    if tipo_depreciacion not in ["lineal", "acelerada", "anual"]:
        print("Error: Tipo de depreciación no válido")
        return
    if tipo_depreciacion_mexicana not in ["lineal", "acelerada", "anual"]:
        print("Error: Tipo de depreciación mexicana no válido")
        return

    if tipo_depreciacion == "lineal":
        depreciacion_acumulada = calcular_depreciacion_lineal(actividad, precio_compra, vida_util, tasa_interes)
        depreciacion_acumulada_mexicana = calcular_depreciacion_lineal(actividad, precio_compra, vida_util, tasa_interes_mexicana)
    elif tipo_depreciacion == "acelerada":
        depreciacion_acumulada = calcular_depreciacion_acelerada(actividad, precio_compra, vida_util, tasa_interes)
        depreciacion_acumulada_mexicana = calcular_depreciacion_acelerada(actividad, precio_compra, vida_util, tasa_interes_mexicana)