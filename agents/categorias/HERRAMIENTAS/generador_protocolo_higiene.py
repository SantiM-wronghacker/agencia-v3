"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza generador protocolo higiene
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random
from datetime import date

def generador_protocolo_higiene(nombre_restaurante, fecha_actual, temperatura, humedad, presión, contaminación):
    # Generar protocolo de higiene
    print("Nombre del restaurante:", nombre_restaurante)
    print("Fecha actual:", fecha_actual)
    print("Temperatura:", temperatura, "°C")
    print("Humedad:", humedad, "%")
    print("Presión:", presión, "hPa")
    print("Contaminación:", contaminación, "%")
    print("Protocolo de higiene:", nombre_restaurante, "el", fecha_actual)
    print("Recomendaciones:")
    print("  - Mantener la temperatura entre 18°C y 24°C")
    print("  - Mantener la humedad entre 40% y 60%")
    print("  - Verificar la presión atmosférica diariamente")
    print("  - Realizar limpieza y desinfección diaria")
    print("  - Verificar la calidad del agua y el aire")
    print("Resumen ejecutivo:")
    print("  - El protocolo de higiene se debe seguir diariamente para garantizar la salud y seguridad de los clientes y empleados")
    print("  - Se deben realizar inspecciones periódicas para verificar el cumplimiento del protocolo")
    print("Indicadores de calidad:")
    print("  - Temperatura: {:.2f} °C".format(temperatura))
    print("  - Humedad: {:.2f} %".format(humedad))
    print("  - Presión: {:.2f} hPa".format(presión))
    print("  - Contaminación: {:.2f} %".format(contaminación))
    print("Resumen ejecutivo final:")
    print("  - El restaurante debe mantener un ambiente seguro y saludable para sus clientes y empleados")
    print("  - Se deben tomar medidas para reducir la contaminación y mejorar la calidad del aire")
    print("  - Se deben realizar capacitaciones para los empleados sobre higiene y seguridad")
    print("  - Se deben realizar auditorías para verificar el cumplimiento del protocolo")

    # Calcular indicadores de calidad
    if temperatura < 18 or temperatura > 24:
        print("  - La temperatura está fuera del rango recomendado")
    if humedad < 40 or humedad > 60:
        print("  - La humedad está fuera del rango recomendado")
    if presión < 950 or presión > 1050:
        print("  - La presión está fuera del rango recomendado")
    if contaminación > 50:
        print("  - La contaminación es alta")

def main():
    try:
        nombre_restaurante = sys.argv[1]
        fecha_actual = date.today().strftime("%d-%m-%Y")
        temperatura = float(sys.argv[2])
        humedad = float(sys.argv[3])
        presión = float(sys.argv[4])
        contaminación = float(sys.argv[5])
    except IndexError:
        print("Error: Faltan argumentos")
        return
    except ValueError:
        print("Error: Los argumentos deben ser números")
        return

    if temperatura < 0 or temperatura > 50:
        print("Error: La temperatura debe estar entre 0°C y 50°C")
        return
    if humedad < 0 or humedad > 100:
        print("Error: La humedad debe estar entre 0% y 100%")
        return
    if presión < 900 or presión > 1100:
        print("Error: La presión debe estar entre 900 hPa y 1100 hPa")
        return
    if contaminación < 0 or contaminación > 100:
        print("Error: La contaminación debe estar entre 0% y 100%")
        return

    generador_protocolo_higiene(nombre_restaurante, fecha_actual, temperatura, humedad, presión, contaminación)

if __name__ == "__main__":
    main()