"""
ÁREA: ECOMMERCE
DESCRIPCION: Agente que realiza optimizador precios
TECNOLOGIA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def optimizador_precios(productos=None, archivo=None, rango=0.2):
    try:
        if productos is None:
            productos = [
                {"nombre": "Producto 1", "precio": 100.50},
                {"nombre": "Producto 2", "precio": 200.75},
                {"nombre": "Producto 3", "precio": 300.25}
            ]

        if archivo is not None:
            try:
                with open(archivo, 'r') as f:
                    productos = json.load(f)
            except Exception as e:
                print(f"Error al leer archivo: {str(e)}")

        # Extraer precios de los productos
        precios = [producto["precio"] for producto in productos]

        # Calcular promedio de precios
        promedio = sum(precios) / len(precios)

        # Calcular variación de precios
        variacion = [(precio - promedio) / promedio * 100 for precio in precios]

        # Imprimir resultados
        print("Productos:")
        for i, producto in enumerate(productos):
            print(f"- {producto['nombre']}: ${producto['precio']:.2f} ({variacion[i]:.2f}%)")

        print("\nPromedio de precios: ${:.2f}".format(promedio))
        print("Variación de precios:")
        for producto, var in zip(productos, variacion):
            print(f"- {producto['nombre']}: {var:.2f}%")

        # Determinar productos con precios fuera de rango
        rango_min = promedio * (1 - rango)
        rango_max = promedio * (1 + rango)
        fuera_de_rango = [producto for producto in productos if producto["precio"] < rango_min or producto["precio"] > rango_max]

        # Imprimir productos fuera de rango
        print("\nProductos fuera de rango:")
        for producto in fuera_de_rango:
            print(f"- {producto['nombre']}: ${producto['precio']:.2f}")

        # Calcular cuantos productos están fuera de rango
        fuera_de_rango_count = len(fuera_de_rango)
        print(f"\nHay {fuera_de_rango_count} productos fuera de rango.")

        # Calcular cantidad de productos que superan el precio máximo del 90%
        precio_max_90 = promedio * 0.9
        superan_precio_max_90 = len([producto for producto in productos if producto["precio"] > precio_max_90])
        print(f"\n{superan_precio_max_90} productos superan el precio máximo del 90%.")

        # Calcular cantidad de productos que están por debajo del precio mínimo del 80%
        precio_min_80 = promedio * 0.8
        por_debaajo_precio_min_80 = len([producto for producto in productos if producto["precio"] < precio_min_80])
        print(f"\n{por_debaajo_precio_min_80} productos están por debajo del precio mínimo del 80%.")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El promedio de precios es de ${promedio:.2f}.")
        print(f"La variación de precios es de {sum(variacion) / len(variacion):.2f}%.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        archivo = sys.argv[1]
    else:
        archivo = None

    if len(sys.argv) > 2:
        rango = float(sys.argv[2])
    else:
        rango = 0.2

    optimizador_precios(archivo=archivo, rango=rango)