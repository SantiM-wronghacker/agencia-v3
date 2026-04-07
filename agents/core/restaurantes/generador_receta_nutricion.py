#!/usr/bin/env python3
"""
ÁREA: SALUD
DESCRIPCIÓN: Agente que realiza generador receta nutricion
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def extraer_receta(nombre, ingredientes):
    """
    Receta de ejemplo
    """
    receta = {
        "nombre": nombre,
        "ingredientes": [
            {"nombre": ingrediente[0], "cantidad": ingrediente[1], "unidad": ingrediente[2]}
            for ingrediente in ingredientes
        ],
        "instrucciones": [
            "Lavar los ingredientes",
            "Cortar el pollo en trozos pequeños",
            "Mezclar todos los ingredientes en un tazón",
            "Servir frío"
        ]
    }
    return receta

def calcular_calorias(receta):
    """
    Calcula las calorias de la receta
    """
    calorias = 0
    for ingrediente in receta["ingredientes"]:
        if ingrediente["nombre"] == "pollo":
            calorias += 120
        elif ingrediente["nombre"] == "lechuga":
            calorias += 20
        elif ingrediente["nombre"] == "tomate":
            calorias += 25
        elif ingrediente["nombre"] == "aceitunas":
            calorias += 50
        elif ingrediente["nombre"] == "aceite de oliva":
            calorias += 90
        elif ingrediente["nombre"] == "vinagre":
            calorias += 5
        elif ingrediente["nombre"] == "sal":
            calorias += 0
    return calorias

def calcular_macronutrientes(receta):
    """
    Calcula los macronutrientes de la receta
    """
    macronutrientes = {"carbohidratos": 0, "proteínas": 0, "grasas": 0}
    for ingrediente in receta["ingredientes"]:
        if ingrediente["nombre"] == "lechuga":
            macronutrientes["carbohidratos"] += 5
        elif ingrediente["nombre"] == "tomate":
            macronutrientes["carbohidratos"] += 5
        elif ingrediente["nombre"] == "aceitunas":
            macronutrientes["grasas"] += 10
        elif ingrediente["nombre"] == "aceite de oliva":
            macronutrientes["grasas"] += 10
        elif ingrediente["nombre"] == "pollo":
            macronutrientes["proteínas"] += 30
    return macronutrientes

def main():
    if len(sys.argv) != 3:
        print("Uso: python generador_receta_nutricion.py <nombre> <ingredientes>")
        sys.exit(1)
    nombre = sys.argv[1]
    ingredientes = sys.argv[2].split(",")
    receta = extraer_receta(nombre, [(ingrediente.split(":")[0], int(ingrediente.split(":")[1]), ingrediente.split(":")[2]) for ingrediente in ingredientes])
    calorias = calcular_calorias(receta)
    macronutrientes = calcular_macronutrientes(receta)
    print("Receta:", receta["nombre"])
    print("Ingredientes:")
    for ingrediente in receta["ingredientes"]:
        print(f"{ingrediente['nombre']}: {ingrediente['cantidad']} {ingrediente['unidad']}")
    print("Instrucciones:")
    for instruccion in receta["instrucciones"]:
        print(instruccion)
    print("Calorias:", calorias)
    print("Macronutrientes:")
    print(f"  Carbohidratos: {macronutrientes['carbohidratos']}g")
    print(f"  Proteínas: {macronutrientes['proteínas']}g")
    print(f"  Grasas: {macronutrientes['grasas']}g")
    print("Resumen ejecutivo:")
    print("La receta de", receta["nombre"], "es una opción saludable para aquellos que buscan una dieta equilibrada.")

if __name__ == "__main__":
    main()