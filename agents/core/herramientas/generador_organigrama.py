"""
AREA: HERRAMIENTAS
DESCRIPCION: Agente que realiza generador organigrama
TECNOLOGIA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_organigrama(nombre, cargo, departamento, salario, beneficios):
    try:
        # Procesar datos y generar organigrama
        organigrama = {
            "nombre": nombre,
            "cargo": cargo,
            "departamento": departamento,
            "salario": salario,
            "beneficios": beneficios,
            "fecha_de_inicio": datetime.date.today().strftime("%Y-%m-%d"),
            "dias_de_vacaciones": 15,
            "horas_de_trabajo": 40,
            "impuestos": calcular_impuestos(salario),
            "total_anual": calcular_total_anual(salario, beneficios),
            "bonos": calcular_bonos(salario),
            "prestaciones": calcular_prestaciones(salario, beneficios)
        }
        return organigrama
    except Exception as e:
        print(f"Error: {e}")
        return None

def calcular_impuestos(salario):
    try:
        # Calculo de impuestos simplificado
        if salario < 20000:
            return salario * 0.10
        elif salario < 50000:
            return salario * 0.15
        elif salario < 100000:
            return salario * 0.18
        else:
            return salario * 0.20
    except Exception as e:
        print(f"Error: {e}")
        return 0

def calcular_total_anual(salario, beneficios):
    try:
        # Calculo de total anual
        return salario * 12 + beneficios
    except Exception as e:
        print(f"Error: {e}")
        return 0

def calcular_bonos(salario):
    try:
        # Calculo de bonos
        if salario < 20000:
            return salario * 0.05
        elif salario < 50000:
            return salario * 0.10
        elif salario < 100000:
            return salario * 0.15
        else:
            return salario * 0.20
    except Exception as e:
        print(f"Error: {e}")
        return 0

def calcular_prestaciones(salario, beneficios):
    try:
        # Calculo de prestaciones
        if salario < 20000:
            return beneficios * 0.10
        elif salario < 50000:
            return beneficios * 0.15
        elif salario < 100000:
            return beneficios * 0.20
        else:
            return beneficios * 0.25
    except Exception as e:
        print(f"Error: {e}")
        return 0

def main():
    try:
        if len(sys.argv) != 6:
            print("Uso: python generador_organigrama.py <nombre> <cargo> <departamento> <salario> <beneficios>")
            return

        nombre = sys.argv[1]
        cargo = sys.argv[2]
        departamento = sys.argv[3]
        salario = float(sys.argv[4])
        beneficios = float(sys.argv[5])

        organigrama = generar_organigrama(nombre, cargo, departamento, salario, beneficios)

        if organigrama:
            print("Resumen Ejecutivo:")
            print(f"Nombre: {organigrama['nombre']}")
            print(f"Cargo: {organigrama['cargo']}")
            print(f"Departamento: {organigrama['departamento']}")
            print(f"Salario: ${organigrama['salario']}")
            print(f"Beneficios: ${organigrama['beneficios']}")
            print(f"Fecha de Inicio: {organigrama['fecha_de_inicio']}")
            print(f"Días de Vacaciones: {organigrama['dias_de_vacaciones']}")
            print(f"Horas de Trabajo: {organigrama['horas_de_trabajo']}")
            print(f"Impuestos: ${organigrama['impuestos']}")
            print(f"Total Anual: ${organigrama['total_anual']}")
            print(f"Bonos: ${organigrama['bonos']}")
            print(f"Prestaciones: ${organigrama['prestaciones']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()