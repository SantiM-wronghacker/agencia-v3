#!/usr/bin/env python3
"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora ROI campanas
TECNOLOGÍA: Python estándar
"""

import sys
import os
import json
import datetime
import math
import re

def calcular_roi(inversion, ganancia):
    if inversion == 0:
        raise ValueError("La inversión no puede ser cero")
    if ganancia < 0:
        raise ValueError("La ganancia no puede ser negativa")
    roi = (ganancia / inversion) * 100
    return roi

def calcular_roi_real(roi, inflacion):
    if inflacion < 0:
        raise ValueError("La inflación no puede ser negativa")
    if roi < 0:
        raise ValueError("El ROI no puede ser negativo")
    roi_real = roi - (inflacion / 100)
    return roi_real

def calcular_inversion_efectiva(inversion, roi):
    if roi < 0:
        raise ValueError("El ROI no puede ser negativo")
    if inversion <= 0:
        raise ValueError("La inversión no puede ser negativa o cero")
    inversion_efectiva = inversion / (1 + (roi / 100))
    return inversion_efectiva

def calcular_ganancia_por_inversión(inversion, roi):
    if roi < 0:
        raise ValueError("El ROI no puede ser negativo")
    if inversion <= 0:
        raise ValueError("La inversión no puede ser negativa o cero")
    ganancia_por_inversión = inversion * (roi / 100)
    return ganancia_por_inversión

def calcular_inflacion_anual(tipo_cambio):
    # Calculo aproximado de la inflación anual en México
    # Fuente: Instituto Nacional de Estadística y Geografía (INEGI)
    return 3.5

def calcular_inversion_efectiva_con_inflacion(inversion, roi, inflacion):
    if roi < 0:
        raise ValueError("El ROI no puede ser negativo")
    if inflacion < 0:
        raise ValueError("La inflación no puede ser negativa")
    if inversion <= 0:
        raise ValueError("La inversión no puede ser negativa o cero")
    inversion_efectiva = inversion / (1 + (roi / 100) * (1 + (inflacion / 100)))
    return inversion_efectiva

def calcular_inversion_efectiva_mexico(inversion, roi):
    # Calculo aproximado de la inflación anual en México
    # Fuente: Instituto Nacional de Estadística y Geografía (INEGI)
    inflacion = 3.5
    inversion_efectiva = inversion / (1 + (roi / 100) * (1 + (inflacion / 100)))
    return inversion_efectiva

def main():
    try:
        # Obtener parámetros por línea de comandos
        if len(sys.argv) < 5:
            print("Faltan parámetros")
            sys.exit(1)

        inversion = float(sys.argv[1])
        ganancia = float(sys.argv[2])
        tipo_cambio = float(sys.argv[3])
        inflacion = float(sys.argv[4])

        # Calculos
        roi = calcular_roi(inversion, ganancia)
        roi_real = calcular_roi_real(roi, inflacion)
        inversion_efectiva = calcular_inversion_efectiva_mexico(inversion, roi)
        ganancia_por_inversión = calcular_ganancia_por_inversión(inversion, roi)
        inflacion_anual = calcular_inflacion_anual(tipo_cambio)

        # Resumen ejecutivo
        print("Resumen Ejecutivo:")
        print("---------------------")
        print(f"Inversión: {inversion}")
        print(f"Ganancia: {ganancia}")
        print(f"ROI: {roi}%")
        print(f"ROI Real: {roi_real}%")
        print(f"Inversión Efectiva: {inversion_efectiva}")
        print(f"Ganancia por Inversión: {ganancia_por_inversión}")
        print(f"Inflación Anual: {inflacion_anual}%")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()