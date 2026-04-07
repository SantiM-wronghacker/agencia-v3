import os
import sys
import json
import datetime
import math
import re
import random

def calcular_costo_receta(ingredientes, cantidad_personas):
    try:
        # Verificar tipos de datos
        if not isinstance(ingredientes, dict):
            raise ValueError("Ingredientes deben ser un diccionario")
        if not isinstance(cantidad_personas, int) or cantidad_personas <= 0:
            raise ValueError("Cantidad de personas debe ser un número entero positivo")

        # Precios de ingredientes (parametrizados por sys.argv)
        precios = {
            'carne': float(sys.argv[2]) if len(sys.argv) > 2 else 50.0,
            'verduras': float(sys.argv[3]) if len(sys.argv) > 3 else 20.0,
            'arroz': float(sys.argv[4]) if len(sys.argv) > 4 else 15.0,
            'frijoles': float(sys.argv[5]) if len(sys.argv) > 5 else 10.0
        }

        # Buscar precios de ingredientes en línea (opcional)
        if len(sys.argv) > 1 and sys.argv[1] == "web":
            # Buscar precios de ingredientes en línea
            precios = {
                'carne': 60.0,
                'verduras': 25.0,
                'arroz': 18.0,
                'frijoles': 12.0
            }

        # Calcular costo total de la receta
        costo_total = sum([ingredientes.get(i, 0) * p for i, p in precios.items()]) * cantidad_personas

        # Calcular impuestos (IVA 16% y ISR 10%)
        impuestos = costo_total * 0.16 + costo_total * 0.10
        costo_total_con_impuestos = costo_total + impuestos

        return costo_total, costo_total_con_impuestos

    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None

def main():
    try:
        # Argumentos de entrada (opcional)
        cantidad_personas = int(sys.argv[1]) if len(sys.argv) > 1 else 4

        # Ingredientes (parametrizados por sys.argv)
        ingredientes = {
            'carne': float(sys.argv[2]) if len(sys.argv) > 2 else 2,
            'verduras': float(sys.argv[3]) if len(sys.argv) > 3 else 1,
            'arroz': float(sys.argv[4]) if len(sys.argv) > 4 else 1,
            'frijoles': float(sys.argv[5]) if len(sys.argv) > 5 else 1
        }

        # Calcular costo receta para la cantidad de personas
        costo_receta, costo_receta_con_impuestos = calcular_costo_receta(ingredientes, cantidad_personas)

        # Mostrar resultados
        print("ÁREA: RESTAURANTES")
        print("DESCRIPCIÓN: Agente que calcula costo receta")
        print("TECNOLOGÍA: Python estándar")
        print(f"Cantidad de personas: {cantidad_personas}")
        print(f"Ingredientes: {ingredientes}")
        print(f"Costo receta: ${costo_receta:.2f}")
        print(f"Costo receta con impuestos: ${costo_receta_con_impuestos:.2f}")
        print(f"IVA: {costo_receta_con_impuestos - costo_receta:.2f}")
        print(f"ISR: {costo_receta_con_impuestos - costo_receta - (costo_receta_con_impuestos - costo_receta):.2f}")
        print("RESUMEN EJECUTIVO:")
        print(f"El costo total de la receta para {cantidad_personas} personas es de ${costo_receta_con_impuestos:.2f}, lo que incluye un IVA de {costo_receta_con_impuestos - costo_receta:.2f} y un ISR de {costo_receta_con_impuestos - costo_receta - (costo_receta_con_impuestos - costo_receta):.2f}.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()