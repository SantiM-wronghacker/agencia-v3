"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza generador onboarding
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios(tipo_cambio_dolar=20.50, tipo_cambio_euro=22.80):
    return {
        'dolar': tipo_cambio_dolar,
        'euro': tipo_cambio_euro,
        'peso': 1.00
    }

def buscar_datos(nombre='Juan', edad=30, cargo='Gerente'):
    return {
        'nombre': nombre,
        'edad': edad,
        'cargo': cargo
    }

def fetch_texto():
    return 'Texto de ejemplo'

def calcular_salario_promedio_mexico(salario_base=50000, incremento=0.15):
    return math.floor(salario_base * (1 + incremento))

def calcular_impuesto(salario, tasa_impuesto=0.10):
    return math.floor(salario * tasa_impuesto)

def calcular_total(salario, impuesto):
    return salario - impuesto

def calcular_diferencia_impuestos(tasa_impuesto1, tasa_impuesto2, salario):
    return math.floor(salario * (tasa_impuesto1 - tasa_impuesto2))

def calcular_descuento_por_edad(edad, salario):
    return math.floor(salario * 0.01 * edad)

def main():
    try:
        tipo_cambio_dolar = float(sys.argv[1]) if len(sys.argv) > 1 else 20.50
        tipo_cambio_euro = float(sys.argv[2]) if len(sys.argv) > 2 else 22.80
        nombre = sys.argv[3] if len(sys.argv) > 3 else 'Juan'
        edad = int(sys.argv[4]) if len(sys.argv) > 4 else 30
        cargo = sys.argv[5] if len(sys.argv) > 5 else 'Gerente'
        salario_base = float(sys.argv[6]) if len(sys.argv) > 6 else 50000
        incremento = float(sys.argv[7]) if len(sys.argv) > 7 else 0.15
        tasa_impuesto = float(sys.argv[8]) if len(sys.argv) > 8 else 0.10
        tasa_impuesto2 = float(sys.argv[9]) if len(sys.argv) > 9 else 0.10
        salario = calcular_salario_promedio_mexico(salario_base, incremento)

        print(f"Fecha actual: {datetime.date.today()}")
        print(f"Precios actuales: {extraer_precios(tipo_cambio_dolar, tipo_cambio_euro)}")
        print(f"Datos de ejemplo: {buscar_datos(nombre, edad, cargo)}")
        print(f"Texto de ejemplo: {fetch_texto()}")
        print(f"Número aleatorio: {random.randint(1, 100)}")
        print(f"Salario promedio en México: ${salario}")
        impuesto = calcular_impuesto(salario, tasa_impuesto)
        print(f"Total impuestos: ${impuesto}")
        diferencia_impuestos = calcular_diferencia_impuestos(tasa_impuesto, tasa_impuesto2, salario)
        print(f"Diferencia impuestos: ${diferencia_impuestos}")
        descuento_edad = calcular_descuento_por_edad(edad, salario)
        print(f"Descuento por edad: ${descuento_edad}")
        total = calcular_total(salario, impuesto)
        print(f"Salario neto: ${total}")

        print("\nResumen ejecutivo:")
        print(f"Nombre: {nombre}")
        print(f"Edad: {edad} años")
        print(f"Cargo: {cargo}")
        print(f"Salario promedio en México: ${salario}")
        print(f"Total impuestos: ${impuesto}")
        print(f"Salario neto: ${total}")

    except IndexError:
        print("Faltan argumentos de línea de comandos.")
    except ValueError:
        print("Argumentos de línea de comandos deben ser números.")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()