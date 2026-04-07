#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora de materiales
TECNOLOGÍA: Python estándar
"""

import os
import sys
import math

def calcular_materiales(largo, ancho, alto, tipo_construccion, tipo_materiales):
    # Constantes
    PESO_METRICO = 0.45359237  # Libras a kilos
    PRECIO_METRICO = 25.00  # Pesos mexicanos por metro cuadrado
    VOLUMEN_METRICO = 0.0283168466  # Libras a metros cúbicos
    IVA = 0.16  # Impuesto al valor agregado
    PESO_METRICO_POR_METRO_CUBICO = 1000  # Libras por metro cúbico
    COSTO_POR_KILOMETRO = 0.50  # Pesos mexicanos por kilómetro
    TIPO_CAMBIO = 20.00  # Tipo de cambio aproximado
    DENSIDAD_MADERA = 0.70  # Densidad de la madera en kg/m³
    DENSIDAD_METAL = 7.80  # Densidad del metal en kg/m³
    DENSIDAD_CONCRETO = 2.40  # Densidad del concreto en kg/m³
    COSTO_POR_METRO_CUBICO = PRECIO_METRICO * VOLUMEN_METRICO

    # Cálculos
    try:
        volumen = largo * ancho * alto
        peso_madera = volumen * DENSIDAD_MADERA
        peso_metal = volumen * DENSIDAD_METAL
        peso_concreto = volumen * DENSIDAD_CONCRETO
        costo_por_metro_cubico = volumen * PRECIO_METRICO
        costo_total = costo_por_metro_cubico * (1 + IVA)
        costo_total_kilometro = peso_madera * COSTO_POR_KILOMETRO
        costo_total_total = costo_total + costo_total_kilometro
        costo_total_dolares = costo_total_total / TIPO_CAMBIO  # Tipo de cambio aproximado
        tiempo_transporte = peso_madera / 1000  # Tiempo de transporte en horas
        tiempo_construccion = volumen / 10  # Tiempo de construcción en días
        tiempo_construccion_semanas = tiempo_construccion / 5  # Tiempo de construcción en semanas
    except ValueError:
        print("Error: Los argumentos de entrada deben ser números.")
        return

    # Resumen ejecutivo
    print("Resumen ejecutivo:")
    print(f"Tipo de construcción: {tipo_construccion}")
    print(f"Tipo de materiales: {', '.join(tipo_materiales)}")
    print(f"Costo total: ${costo_total_total:.2f} MXN")
    print(f"Costo total en dólares: ${costo_total_dolares:.2f} USD")
    print(f"Tiempo de transporte: {tiempo_transporte:.2f} horas")
    print(f"Tiempo de construcción: {tiempo_construccion:.2f} días")
    print(f"Tiempo de construcción en semanas: {tiempo_construccion_semanas:.2f} semanas")

def main():
    # Argumentos de entrada
    try:
        tipo_construccion = sys.argv[1] if len(sys.argv) > 1 else "Residencial"
        tipo_materiales = sys.argv[2].split(",") if len(sys.argv) > 2 else ["Madera", "Metal", "Concreto"]
        largo = float(sys.argv[3]) if len(sys.argv) > 3 else 10
        ancho = float(sys.argv[4]) if len(sys.argv) > 4 else 10
        alto = float(sys.argv[5]) if len(sys.argv) > 5 else 10
    except IndexError:
        print("Error: Faltan argumentos de entrada.")
        return
    except ValueError:
        print("Error: Los argumentos de entrada deben ser números o cadenas.")
        return

    # Llamada a la función
    calcular_materiales(largo, ancho, alto, tipo_construccion, tipo_materiales)

if __name__ == "__main__":
    main()