"""
ÁREA: SALUD
DESCRIPCIÓN: Agente que realiza planificador dieta
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def calcular_calorias(peso, altura, edad, sexo):
    try:
        if sexo == 'masculino':
            calorias = 66 + (13.7 * peso) + (5 * altura) - (6.8 * edad)
        elif sexo == 'femenino':
            calorias = 655 + (9.6 * peso) + (1.8 * altura) - (4.7 * edad)
        return calorias
    except TypeError:
        print('Los valores de peso, altura, edad y sexo deben ser números')
        return None
    except ValueError:
        print('Los valores de peso, altura, edad y sexo deben ser números válidos')
        return None

def calcular_macronutrientes(calorias, objetivo):
    try:
        if objetivo == 'baja':
            macronutrientes = {
                'carbohidratos': 2 * calorias / 10,
                'proteínas': calorias / 10,
                'grasas': calorias / 20
            }
        elif objetivo == 'media':
            macronutrientes = {
                'carbohidratos': 3 * calorias / 10,
                'proteínas': calorias / 10,
                'grasas': calorias / 25
            }
        elif objetivo == 'alta':
            macronutrientes = {
                'carbohidratos': 4 * calorias / 10,
                'proteínas': calorias / 10,
                'grasas': calorias / 30
            }
        return macronutrientes
    except TypeError:
        print('El valor de calorias y objetivo deben ser números')
        return None
    except ValueError:
        print('El valor de calorias y objetivo deben ser números válidos')
        return None

def planificar_dieta(peso, altura, edad, sexo, objetivo):
    calorias = calcular_calorias(peso, altura, edad, sexo)
    if calorias is not None:
        macronutrientes = calcular_macronutrientes(calorias, objetivo)
        if macronutrientes is not None:
            print(f'Calorias diarias recomendadas: {calorias} kcal')
            print(f'Macronutrientes recomendados:')
            print(f'  - Carbohidratos: {macronutrientes["carbohidratos"]} g (50-60% de la ingesta diaria)')
            print(f'  - Proteínas: {macronutrientes["proteínas"]} g (15-20% de la ingesta diaria)')
            print(f'  - Grasas: {macronutrientes["grasas"]} g (20-25% de la ingesta diaria)')
            print(f'  - Ejemplo de dieta diaria:')
            print(f'    - Desayuno: 3 huevos, 2 tostadas, 1 taza de leche')
            print(f'    - Almuerzo: 100g de carne, 1 taza de arroz, 1 taza de verduras')
            print(f'    - Cena: 100g de pescado, 1 taza de quinoa, 1 taza de verduras')
            print('  - Recuerda beber al menos 2 litros de agua al día')
            print('  - Ajusta la dieta según tus necesidades y preferencias personales')
    else:
        print('No se pudo calcular la dieta')

def main():
    if len(sys.argv) != 6:
        print('Uso: python planificador_dieta.py <peso> <altura> <edad> <sexo> <objetivo>')
        return
    peso = float(sys.argv[1])
    altura = float(sys.argv[2])
    edad = int(sys.argv[3])
    sexo = sys.argv[4]
    objetivo = sys.argv[5]
    planificar_dieta(peso, altura, edad, sexo, objetivo)

if __name__ == "__main__":
    main()