"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza generador ficha tecnica receta
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios(precio_base):
    return {
        "harina": precio_base,
        "azúcar": precio_base * 0.6,
        "huevos": precio_base * 0.4,
        "leche": precio_base * 0.8,
        "mantequilla": precio_base * 0.7,
        "azúcar moreno": precio_base * 0.8,
        "chocolate": precio_base * 1.2,
        "cacao en polvo": precio_base * 1.0
    }

def obtener_precios(precios, ingredientes):
    precios_receta = {}
    for ingrediente in ingredientes:
        precios_receta[ingrediente['nombre']] = precios[ingrediente['nombre']]
    return precios_receta

def generar_ficha_tecnica_receta(nombre_receta, ingredientes, precios):
    try:
        # Generar ficha técnica
        ficha_tecnica = f"""
**Nombre de la receta:** {nombre_receta}
**Ingredientes:**
{os.linesep.join(f"{i['nombre']} ({i['unidad']}): {i['cantidad']} unidades" for i in ingredientes)}
**Precios:**
{os.linesep.join(f"{i}: ${precios[i]} MXN" for i in precios)}
**Total:** ${sum(precios.values())} MXN
**Impuestos (16%):** ${(sum(precios.values()) * 0.16)} MXN
**Total con impuestos:** ${(sum(precios.values()) + (sum(precios.values()) * 0.16))} MXN
**Tiempo de preparación:** 30 minutos
**Tiempo de cocción:** 20 minutos
**Cantidad de ingredientes:** {len(ingredientes)}
**Peso total de la receta:** {sum(float(i['cantidad']) * float(i['peso']) for i in ingredientes)} gramos
"""
        return ficha_tecnica
    except Exception as e:
        print(f"Error: {e}")
        return None

def calcular_total(precios):
    try:
        return sum(precios.values())
    except Exception as e:
        print(f"Error: {e}")
        return None

def generar_resumen_ejecutivo(nombre_receta, ingredientes, precios):
    try:
        total = calcular_total(precios)
        return f"""
**Resumen Ejecutivo:**
La receta de {nombre_receta} requiere un total de ${total} MXN en ingredientes.
**Peso total de la receta:** {sum(float(i['cantidad']) * float(i['peso']) for i in ingredientes)} gramos
"""
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    if len(sys.argv) != 4:
        print("Uso: python generador_ficha_tecnica_receta.py <nombre_receta> <cantidad_ingredientes> <precio_base>")
        sys.exit(1)

    nombre_receta = sys.argv[1]
    cantidad_ingredientes = int(sys.argv[2])
    precio_base = float(sys.argv[3])

    ingredientes = []
    for i in range(cantidad_ingredientes):
        ingrediente = {
            'nombre': f"Ingrediente {i+1}",
            'unidad': "unidades",
            'cantidad': random.randint(1, 10),
            'peso': random.uniform(1, 100)
        }
        ingredientes.append(ingrediente)

    precios = extraer_precios(precio_base)
    precios_receta = obtener_precios(precios, ingredientes)

    ficha_tecnica = generar_ficha_tecnica_receta(nombre_receta, ingredientes, precios_receta)
    resumen_ejecutivo = generar_resumen_ejecutivo(nombre_receta, ingredientes, precios_receta)

    print(ficha_tecnica)
    print(resumen_ejecutivo)

if __name__ == "__main__":
    main()