import os
import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def calcular_acero(largo, ancho, espesor):
    """
    Calcula el peso del acero en kg.
    """
    # Peso por metro cuadrado de acero en kg
    peso_metro_cuadrado = 7.85
    
    # Superficie del acero en metros cuadrados
    superficie = largo * ancho
    
    # Peso total del acero en kg
    peso_total = peso_metro_cuadrado * superficie * espesor
    
    # Peso por metro lineal de acero en kg
    peso_metro_lineal = 0.785 * peso_metro_cuadrado * espesor
    
    # Peso por metro cúbico de acero en kg
    peso_metro_cubico = 7850
    
    return peso_total, peso_metro_lineal, peso_metro_cubico

def calcular_costo_acero(peso_total):
    """
    Calcula el costo del acero en MXN.
    """
    # Costo del acero en MXN por kg
    costo_por_kg = 25.00
    
    # Costo total del acero en MXN
    costo_total = peso_total * costo_por_kg
    
    return costo_total

def calcular_impacto_medio(peso_total):
    """
    Calcula el impacto medio del acero en kg CO2e.
    """
    # Factor de emisión de CO2e por kg de acero
    factor_emision = 1.98
    
    # Impacto medio del acero en kg CO2e
    impacto_medio = peso_total * factor_emision
    
    return impacto_medio

def main():
    """
    Función principal que ejecuta el agente.
    """
    if len(sys.argv) < 4:
        print("Error: Faltan parámetros de entrada.")
        return
    
    try:
        # Parámetros de entrada
        largo = float(sys.argv[1])
        ancho = float(sys.argv[2])
        espesor = float(sys.argv[3])
        
        # Calcula el peso del acero
        peso_total, peso_metro_lineal, peso_metro_cubico = calcular_acero(largo, ancho, espesor)
        
        # Calcula el costo del acero
        costo_total = calcular_costo_acero(peso_total)
        
        # Calcula el impacto medio del acero
        impacto_medio = calcular_impacto_medio(peso_total)
        
        # Muestra los resultados
        print("ÁREA: CONSTRUCCION")
        print("DESCRIPCIÓN: Agente que calcula el peso, costo y impacto del acero")
        print("TECNOLOGÍA: Python estándar")
        print(f"Largo: {largo} m")
        print(f"Ancho: {ancho} m")
        print(f"Espesor: {espesor} m")
        print(f"Peso total: {peso_total:.2f} kg")
        print(f"Peso por metro lineal: {peso_metro_lineal:.2f} kg/m")
        print(f"Peso por metro cúbico: {peso_metro_cubico:.2f} kg/m³")
        print(f"Costo total: {costo_total:.2f} MXN")
        print(f"Impacto medio: {impacto_medio:.2f} kg CO2e")
        
        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El peso total del acero para un largo de {largo} m, ancho de {ancho} m y espesor de {espesor} m es de {peso_total:.2f} kg.")
        print(f"El costo total del acero es de {costo_total:.2f} MXN.")
        print(f"El impacto medio del acero es de {impacto_medio:.2f} kg CO2e.")
        
    except ValueError:
        print("Error: Los parámetros de entrada deben ser números.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()