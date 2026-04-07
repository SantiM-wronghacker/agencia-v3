"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza cotizador poliza vida
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def cotizador_poliza_vida(edad_min=25, edad_max=65, seguro_min=10000, seguro_max=50000):
    try:
        # Parámetros por sys.argv
        if len(sys.argv) > 1:
            edad_min = int(sys.argv[1])
            edad_max = int(sys.argv[2])
            seguro_min = float(sys.argv[3])
            seguro_max = float(sys.argv[4])

        # Casos edge
        if edad_min < 18:
            print("La edad mínima debe ser mayor o igual a 18 años")
            return
        if edad_max < edad_min:
            print("La edad máxima debe ser mayor o igual a la edad mínima")
            return
        if seguro_min < 0:
            print("El seguro mínimo no puede ser negativo")
            return
        if seguro_max < seguro_min:
            print("El seguro máximo debe ser mayor o igual al seguro mínimo")
            return
        if seguro_min < 10000 or seguro_max > 100000:
            print("El rango de seguro debe estar entre $10,000 y $100,000")
            return

        # Datos de ejemplo
        intereses = 0.05  # Tasa de interés anual
        inflacion = 0.03  # Tasa de inflación anual
        seguro_promedio = sum([20000, 30000, 40000, 50000]) / len([20000, 30000, 40000, 50000])  # Seguro promedio en MXN
        poblacion_mx = 130000000  # Población de México en millones

        # Calcular seguro para diferentes edades
        seguro_edad_min = seguro_min
        seguro_edad_max = seguro_max

        # Calcular seguro ajustado por edad
        seguro_promedio_ajustado = seguro_promedio * (edad_min + edad_max) / 2

        # Calcular seguro ajustado por intereses y inflación
        seguro_ajustado = seguro_min * (1 + intereses) ** (edad_max - edad_min) * (1 + inflacion) ** (edad_max - edad_min)

        # Calcular seguro promedio por edad
        seguro_promedio_por_edad = seguro_promedio / (edad_max - edad_min)

        # Calcular población por edad
        poblacion_por_edad = poblacion_mx / (edad_max - edad_min)

        # Mostrar resultados
        print(f"Edad mínima: {edad_min} años")
        print(f"Edad máxima: {edad_max} años")
        print(f"Seguro mínimo: ${seguro_min:.2f} MXN")
        print(f"Seguro máximo: ${seguro_max:.2f} MXN")
        print(f"Seguro promedio: ${seguro_promedio:.2f} MXN")
        print(f"Seguro promedio ajustado por edad: ${seguro_promedio_ajustado:.2f} MXN")
        print(f"Seguro ajustado por intereses y inflación: ${seguro_ajustado:.2f} MXN")
        print(f"Seguro promedio por edad: ${seguro_promedio_por_edad:.2f} MXN")
        print(f"Población por edad: {poblacion_por_edad} millones")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El seguro mínimo para la edad mínima de {edad_min} años es de ${seguro_min:.2f} MXN")
        print(f"El seguro máximo para la edad máxima de {edad_max} años es de ${seguro_max:.2f} MXN")
        print(f"El seguro promedio ajustado por edad es de ${seguro_promedio_ajustado:.2f} MXN")

    except ValueError:
        print("Error: los parámetros deben ser números")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    cotizador_poliza_vida(25, 65, 10000, 50000)