"""
ÁREA: LEGAL
DESCRIPCIÓN: Agente que realiza generador finiquito laboral
TECNOLOGÍA: Python estándar
"""

import sys
import json
from datetime import datetime, timedelta
import random

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_finiquito(salario_diario, antiguedad_dias, dias_trabajados_mes, dias_aguinaldo, dias_vacaciones):
    try:
        # Cálculos básicos
        prima_vacacional = salario_diario * dias_vacaciones * 0.25
        aguinaldo = salario_diario * dias_aguinaldo
        salario_mes = salario_diario * dias_trabajados_mes
        indemnizacion = salario_diario * antiguedad_dias * 0.3333

        # Total a pagar
        total = salario_mes + prima_vacacional + aguinaldo + indemnizacion

        return {
            "salario_diario": salario_diario,
            "antiguedad_dias": antiguedad_dias,
            "dias_trabajados_mes": dias_trabajados_mes,
            "dias_aguinaldo": dias_aguinaldo,
            "dias_vacaciones": dias_vacaciones,
            "prima_vacacional": prima_vacacional,
            "aguinaldo": aguinaldo,
            "indemnizacion": indemnizacion,
            "total": total
        }
    except Exception as e:
        print(f"Error en cálculo: {str(e)}")
        return None

def main():
    try:
        # Parámetros por defecto realistas para México
        salario_diario = float(sys.argv[1]) if len(sys.argv) > 1 else 350.0
        antiguedad_dias = int(sys.argv[2]) if len(sys.argv) > 2 else 180
        dias_trabajados_mes = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        dias_aguinaldo = int(sys.argv[4]) if len(sys.argv) > 4 else 15
        dias_vacaciones = int(sys.argv[5]) if len(sys.argv) > 5 else 6

        finiquito = calcular_finiquito(
            salario_diario,
            antiguedad_dias,
            dias_trabajados_mes,
            dias_aguinaldo,
            dias_vacaciones
        )

        if finiquito is not None:
            print("Finiquito Laboral Generado:")
            print(f"Salario diario: ${finiquito['salario_diario']:.2f}")
            print(f"Antigüedad: {finiquito['antiguedad_dias']} días")
            print(f"Días trabajados en el mes: {finiquito['dias_trabajados_mes']}")
            print(f"Días de aguinaldo: {finiquito['dias_aguinaldo']}")
            print(f"Días de vacaciones: {finiquito['dias_vacaciones']}")
            print(f"Prima vacacional: ${finiquito['prima_vacacional']:.2f}")
            print(f"Aguinaldo: ${finiquito['aguinaldo']:.2f}")
            print(f"Indemnización: ${finiquito['indemnizacion']:.2f}")
            print(f"Total a pagar: ${finiquito['total']:.2f}")
            print(f"Salario mensual: ${salario_diario * dias_trabajados_mes:.2f}")
            print(f"Total de prima vacacional y aguinaldo: ${finiquito['prima_vacacional'] + finiquito['aguinaldo']:.2f}")
            print("Resumen Ejecutivo:")
            print(f"El finiquito laboral para un trabajador con {antiguedad_dias} días de antigüedad, un salario diario de ${salario_diario:.2f} y {dias_trabajados_mes} días trabajados en el mes, es de ${finiquito['total']:.2f}.")
    except Exception as e:
        print(f"Error en main: {str(e)}")

if __name__ == "__main__":
    main()