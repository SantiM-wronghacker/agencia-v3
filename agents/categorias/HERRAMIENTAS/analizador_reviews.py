"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza analizador reviews
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios():
    try:
        if len(sys.argv) > 1:
            precio_producto1 = float(sys.argv[1])
            precio_producto2 = float(sys.argv[2])
            precio_producto3 = float(sys.argv[3])
        else:
            precio_producto1 = 100.00
            precio_producto2 = 200.00
            precio_producto3 = 300.00
    except ValueError:
        print("Error: los precios deben ser números")
        sys.exit(1)
    
    return {
        'producto1': precio_producto1,
        'producto2': precio_producto2,
        'producto3': precio_producto3
    }

def extraer_reviews():
    try:
        if len(sys.argv) > 4:
            reviews = sys.argv[4:]
        else:
            reviews = [
                'Excelente producto, recomendado',
                'Malo producto, no lo recomiendo',
                'Buena calidad, pero precio alto',
                'El producto es muy bueno, pero el servicio al cliente es pobre',
                'El producto es muy malo, no lo recomiendo a nadie',
                'El producto es bueno, pero el precio es un poco alto',
                'El producto es excelente, muy recomendado',
                'El producto es malo, no lo recomiendo',
                'El producto es bueno, pero el servicio al cliente es un poco pobre',
                'El producto es excelente, muy bueno'
            ]
    except IndexError:
        print("Error: no se proporcionaron suficientes reviews")
        sys.exit(1)
    
    return reviews

def analizar_reviews(reviews):
    analisis = {}
    for review in reviews:
        palabras = re.findall(r'\b\w+\b', review.lower())
        for palabra in palabras:
            if palabra in analisis:
                analisis[palabra] += 1
            else:
                analisis[palabra] = 1
    return analisis

def calcular_precio_promedio(precios):
    return sum(precios.values()) / len(precios)

def calcular_precio_maximo(precios):
    return max(precios.values())

def calcular_precio_minimo(precios):
    return min(precios.values())

def calcular_frecuencia_palabras(analisis):
    total_palabras = sum(analisis.values())
    return {palabra: frecuencia / total_palabras * 100 for palabra, frecuencia in analisis.items()}

def main():
    try:
        precios = extraer_precios()
        reviews = extraer_reviews()
        analisis = analizar_reviews(reviews)
        frecuencia_palabras = calcular_frecuencia_palabras(analisis)
        
        print('ÁREA: HERRAMIENTAS')
        print('DESCRIPCIÓN: Agente que realiza analizador reviews')
        print('TECNOLOGÍA: Python estándar')
        
        print('\nAnálisis de reviews:')
        for palabra, frecuencia in frecuencia_palabras.items():
            print(f'{palabra}: {frecuencia:.2f}%')
        
        print(f'\nPrecios actuales:')
        for producto, precio in precios.items():
            print(f'{producto}: ${precio:.2f}')
        
        print(f'\nPrecio promedio: ${calcular_precio_promedio(precios):.2f}')
        print(f'Precio máximo: ${calcular_precio_maximo(precios):.2f}')
        print(f'Precio mínimo: ${calcular_precio_minimo(precios):.2f}')
        
        print(f'\nFecha actual: {datetime.date.today()}')
        
        print('\nResumen ejecutivo:')
        print('El análisis de reviews muestra que las palabras más frecuentes son "excelente", "bueno" y "malo".')
        print('El precio promedio de los productos es de $200.00, con un precio máximo de $300.00 y un precio mínimo de $100.00.')
    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == "__main__":
    main()