"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza analizador buyer persona
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_edad(fecha_nacimiento):
    hoy = datetime.date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

def calcular_categoria_edad(edad):
    if edad < 25:
        return "Joven"
    elif edad < 45:
        return "Adulto"
    else:
        return "Adulto mayor"

def calcular_categoria_ingreso(ingreso):
    if ingreso < 15000:
        return "Bajo"
    elif ingreso < 30000:
        return "Medio"
    else:
        return "Alto"

def calcular_categoria_gastos(gastos):
    if gastos < 5000:
        return "Bajo"
    elif gastos < 10000:
        return "Medio"
    else:
        return "Alto"

def calcular_porcentaje_ahorro(ingreso, gastos):
    if ingreso > 0:
        return ((ingreso - gastos) / ingreso) * 100
    else:
        return 0

def analizar_buyer_persona(nombre, fecha_nacimiento, sexo, ingreso, gastos):
    edad = calcular_edad(fecha_nacimiento)
    categoria_edad = calcular_categoria_edad(edad)
    categoria_ingreso = calcular_categoria_ingreso(ingreso)
    categoria_gastos = calcular_categoria_gastos(gastos)
    porcentaje_ahorro = calcular_porcentaje_ahorro(ingreso, gastos)

    return {
        "nombre": nombre,
        "edad": edad,
        "categoria_edad": categoria_edad,
        "sexo": sexo,
        "ingreso": ingreso,
        "categoria_ingreso": categoria_ingreso,
        "gastos": gastos,
        "categoria_gastos": categoria_gastos,
        "porcentaje_ahorro": porcentaje_ahorro
    }

def main():
    try:
        nombre = sys.argv[1] if len(sys.argv) > 1 else "Juan Pérez"
        fecha_nacimiento = datetime.date(1995, 1, 1) if len(sys.argv) < 3 else datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
        sexo = sys.argv[3] if len(sys.argv) > 3 else "Masculino"
        ingreso = int(sys.argv[4]) if len(sys.argv) > 4 else 25000
        gastos = int(sys.argv[5]) if len(sys.argv) > 5 else 8000

        buyer_persona = analizar_buyer_persona(nombre, fecha_nacimiento, sexo, ingreso, gastos)

        print("Nombre:", buyer_persona["nombre"])
        print("Edad:", buyer_persona["edad"])
        print("Categoría de edad:", buyer_persona["categoria_edad"])
        print("Sexo:", buyer_persona["sexo"])
        print("Ingreso:", buyer_persona["ingreso"])
        print("Categoría de ingreso:", buyer_persona["categoria_ingreso"])
        print("Gastos:", buyer_persona["gastos"])
        print("Categoría de gastos:", buyer_persona["categoria_gastos"])
        print("Porcentaje de ahorro:", buyer_persona["porcentaje_ahorro"], "%")
        print("Resumen ejecutivo:")
        print("El comprador es un", buyer_persona["categoria_edad"], "de", buyer_persona["edad"], "años con un ingreso de", buyer_persona["ingreso"], "y gastos de", buyer_persona["gastos"])
        print("Su categoría de ingreso es", buyer_persona["categoria_ingreso"], "y su categoría de gastos es", buyer_persona["categoria_gastos"])
        print("Su porcentaje de ahorro es del", buyer_persona["porcentaje_ahorro"], "%")
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()