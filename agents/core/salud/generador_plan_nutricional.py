"""
ÁREA: SALUD
DESCRIPCIÓN: Agente que realiza generador plan nutricional
TECNOLOGÍA: Python estándar
"""

import sys
import random
import datetime
import json
import math
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_imc(peso, altura):
    return peso / (altura ** 2)

def calcular_tmb(peso, altura, edad, actividad):
    if actividad == "sedentario":
        tmb = 1.2
    elif actividad == "ligero":
        tmb = 1.375
    elif actividad == "moderado":
        tmb = 1.55
    elif actividad == "intenso":
        tmb = 1.725
    else:
        raise ValueError("Actividad no válida")
    return (10 * peso) + (6.25 * altura * 100) - (5 * edad) + 5 * tmb

def calcular_calorias_diarias(tmb, factor):
    return tmb * factor

def calcular_macronutrientes(calorias_diarias):
    # Proporciones recomendadas para un adulto saludable en México
    proteínas = calorias_diarias * 0.15
    carbohidratos = calorias_diarias * 0.55
    grasas = calorias_diarias * 0.30
    return proteínas, carbohidratos, grasas

def generar_plan_nutricional(edad, peso, altura, actividad):
    try:
        imc = calcular_imc(peso, altura)
        print(f"IMC: {imc:.2f}")
        tmb = calcular_tmb(peso, altura, edad, actividad)
        print(f"TMB: {tmb:.2f}")
        calorias_diarias = calcular_calorias_diarias(tmb, 1.2)
        print(f"Calorias diarias: {calorias_diarias:.2f}")
        
        proteínas, carbohidratos, grasas = calcular_macronutrientes(calorias_diarias)
        print(f"Proteínas: {proteínas:.2f}g")
        print(f"Carbohidratos: {carbohidratos:.2f}g")
        print(f"Grasas: {grasas:.2f}g")
        
        plan = {
            "desayuno": [
                {"alimento": "Huevos revueltos", "cantidad": "2 unidades", "calorias": 140},
                {"alimento": "Tortilla de maíz", "cantidad": "2 piezas", "calorias": 100},
                {"alimento": "Fresas", "cantidad": "100g", "calorias": 33}
            ],
            "comida": [
                {"alimento": "Pollo a la plancha", "cantidad": "150g", "calorias": 230},
                {"alimento": "Arroz integral", "cantidad": "100g", "calorias": 110},
                {"alimento": "Brócoli al vapor", "cantidad": "100g", "calorias": 35}
            ],
            "cena": [
                {"alimento": "Salmón al horno", "cantidad": "120g", "calorias": 180},
                {"alimento": "Zanahorias al vapor", "cantidad": "100g", "calorias": 25},
                {"alimento": "Aguacate", "cantidad": "100g", "calorias": 160}
            ]
        }
        print("Plan nutricional recomendado:")
        print(json.dumps(plan, indent=4))
        
        resumen_ejecutivo = f"Se recomienda un plan nutricional con {proteínas:.2f}g de proteínas, {carbohidratos:.2f}g de carbohidratos y {grasas:.2f}g de grasas. El plan nutricional recomendado es el siguiente: {json.dumps(plan, indent=4)}"
        print("\nResumen ejecutivo:")
        print(resumen_ejecutivo)
        
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    if len(sys.argv) != 5:
        print("Uso: python generador_plan_nutricional.py <edad> <peso> <altura> <actividad>")
        sys.exit(1)
    
    edad = int