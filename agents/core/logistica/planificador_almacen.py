"""
ÁREA: LOGISTICA
DESCRIPCIÓN: Agente que realiza planificador almacen
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def planificador_almacen(productos=None):
    try:
        if productos is None:
            productos = [
                {"nombre": "Producto 1", "precio": 100.00, "stock": 50},
                {"nombre": "Producto 2", "precio": 200.00, "stock": 20},
                {"nombre": "Producto 3", "precio": 300.00, "stock": 30},
                {"nombre": "Producto 4", "precio": 400.00, "stock": 40},
                {"nombre": "Producto 5", "precio": 500.00, "stock": 50},
                {"nombre": "Producto 6", "precio": 600.00, "stock": 60},
                {"nombre": "Producto 7", "precio": 700.00, "stock": 70},
                {"nombre": "Producto 8", "precio": 800.00, "stock": 80},
                {"nombre": "Producto 9", "precio": 900.00, "stock": 90},
                {"nombre": "Producto 10", "precio": 1000.00, "stock": 100}
            ]

        # Calcular el planificador del almacen
        planificador = {}
        for producto in productos:
            planificador[producto["nombre"]] = {
                "precio": producto["precio"],
                "stock": producto["stock"],
                "utilidad": producto["precio"] * 0.20,  # 20% de utilidad
                "costo_unitario": producto["precio"] / (1 + 0.20)  # Costo unitario con 20% de utilidad
            }

        # Imprimir el planificador del almacen
        print("Planificador del Almacen:")
        print("---------------------------")
        for producto, detalles in planificador.items():
            print(f"{producto}: Precio ${detalles['precio']:.2f}, Stock {detalles['stock']}, Utilidad ${detalles['utilidad']:.2f}, Costo unitario ${detalles['costo_unitario']:.2f}")
        print("---------------------------")
        print(f"Total productos: {len(planificador)}")
        print(f"Total precio: ${sum(detalle['precio'] for detalle in planificador.values()):.2f}")
        print(f"Total stock: {sum(detalle['stock'] for detalle in planificador.values())}")
        print(f"Total utilidad: ${sum(detalle['utilidad'] for detalle in planificador.values()):.2f}")
        print(f"Total costo unitario: ${sum(detalle['costo_unitario'] for detalle in planificador.values()):.2f}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        productos = []
        for i in range(1, len(sys.argv)):
            producto = {
                "nombre": sys.argv[i],
                "precio": float(sys.argv[i + 1]),
                "stock": int(sys.argv[i + 2])
            }
            productos.append(producto)
            i += 2
        planificador_almacen(productos)
    else:
        planificador_almacen()

    print("Resumen Ejecutivo:")
    print("-------------------")
    print(f"El planificador del almacen ha sido calculado con éxito.")
    print(f"Se han encontrado {len(planificador_almacen.__defaults__[0])} productos en el almacen.")
    print(f"El total de precio de los productos es ${sum(detalle['precio'] for detalle in planificador_almacen.__defaults__[0]):.2f}.")
    print(f"El total de stock de los productos es {sum(detalle['stock'] for detalle in planificador_almacen.__defaults__[0])}.")