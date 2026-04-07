#!/usr/bin/env python3

"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora estadisticas
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def calcular_estadisticas(ventas=10000, gastos=5000, ingresos=20000, costo=3000):
    try:
        if ventas < 0 or gastos < 0 or ingresos < 0 or costo < 0:
            raise ValueError("Valores negativos no permitidos")
        if ventas == 0 or gastos == 0 or ingresos == 0 or costo == 0:
            raise ZeroDivisionError("No se puede calcular el beneficio con ceros")
        beneficio = ingresos - gastos - costo
        if beneficio < 0:
            beneficio = 0
        utilidad = (beneficio / ingresos) * 100 if ingresos > 0 else 0
        rendimiento = (beneficio / costo) * 100 if costo > 0 else 0
        eficiencia = ((ingresos - costo) / ingresos) * 100 if ingresos > 0 else 0
        return {
            "ventas": round(ventas, 2),
            "gastos": round(gastos, 2),
            "ingresos": round(ingresos, 2),
            "costo": round(costo, 2),
            "beneficio": round(beneficio, 2),
            "utilidad": round(utilidad, 2),
            "rendimiento": round(rendimiento, 2),
            "eficiencia": round(eficiencia, 2),
            "margen_de_beneficio": round((beneficio / ventas) * 100, 2) if ventas > 0 else 0,
            "tasa_de_retorno": round((beneficio / costo) * 100, 2) if costo > 0 else 0,
            "indice_de_rentabilidad": round((ingresos - costo) / ingresos * 100, 2) if ingresos > 0 else 0
        }
    except Exception as e:
        raise

def main():
    try:
        if len(sys.argv) > 1:
            ventas = float(sys.argv[1])
            gastos = float(sys.argv[2])
            ingresos = float(sys.argv[3])
            costo = float(sys.argv[4])
        else:
            ventas = 10000
            gastos = 5000
            ingresos = 20000
            costo = 3000
        datos = calcular_estadisticas(ventas, gastos, ingresos, costo)
        print("Ventas: $", datos["ventas"])
        print("Gastos: $", datos["gastos"])
        print("Ingresos: $", datos["ingresos"])
        print("Costo: $", datos["costo"])
        print("Beneficio: $", datos["beneficio"])
        print("Utilidad: {:.2f}%".format(datos["utilidad"]))
        print("Rendimiento: {:.2f}%".format(datos["rendimiento"]))
        print("Eficiencia: {:.2f}%".format(datos["eficiencia"]))
        print("Margen de beneficio: {:.2f}%".format(datos["margen_de_beneficio"]))
        print("Tasa de retorno: {:.2f}%".format(datos["tasa_de_retorno"]))
        print("Indice de rentabilidad: {:.2f}%".format(datos["indice_de_rentabilidad"]))
        print("\nResumen Ejecutivo:")
        print("El beneficio total es de ${:.2f}, con una utilidad del {:.2f}% y un rendimiento del {:.2f}%.".format(datos["beneficio"], datos["utilidad"], datos["rendimiento"]))
        print("La eficiencia es del {:.2f}%, con un margen de beneficio del {:.2f}% y una tasa de retorno del {:.2f}%.".format(datos["eficiencia"], datos["margen_de_beneficio"], datos["tasa_de_retorno"]))
    except Exception as e:
        print("Error: ", str(e))

if __name__ == "__main__":
    main()