"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora break even producto
TECNOLOGÍA: Python estándar
"""

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

def calculadora_break_even_producto(precio_venta, precio_costo, cantidad_unidades, margen_utilidad):
    """
    Calcula el punto de equilibrio de un producto.

    Args:
    - precio_venta (float): Precio de venta del producto.
    - precio_costo (float): Precio de costo del producto.
    - cantidad_unidades (int): Cantidad de unidades vendidas.
    - margen_utilidad (float): Margen de utilidad del producto.

    Returns:
    - float: Punto de equilibrio del producto.
    """
    try:
        # Calcular punto de equilibrio
        punto_equilibrio = (precio_costo + (precio_venta - precio_costo) * margen_utilidad) / (1 - margen_utilidad)
        return punto_equilibrio
    except ZeroDivisionError:
        return "No se puede calcular el punto de equilibrio"

def main():
    try:
        # Obtener parámetros desde sys.argv
        if len(sys.argv) == 5:
            precio_venta = float(sys.argv[1])
            precio_costo = float(sys.argv[2])
            cantidad_unidades = int(sys.argv[3])
            margen_utilidad = float(sys.argv[4])
        else:
            precio_venta = 100
            precio_costo = 50
            cantidad_unidades = 100
            margen_utilidad = 0.2

        # Calcular punto de equilibrio
        punto_equilibrio = calculadora_break_even_producto(precio_venta, precio_costo, cantidad_unidades, margen_utilidad)

        # Calculos adicionales
        utilidad_bruta = precio_venta * cantidad_unidades - precio_costo * cantidad_unidades
        utilidad_neta = utilidad_bruta - (precio_venta - precio_costo) * cantidad_unidades * margen_utilidad
        tiempo_de_pago = (precio_costo * cantidad_unidades) / utilidad_bruta if utilidad_bruta!= 0 else "No se puede calcular"
        tasa_de_retorno = (utilidad_neta / (precio_costo * cantidad_unidades)) * 100 if (precio_costo * cantidad_unidades)!= 0 else "No se puede calcular"
        punto_de_equilibrio_unidades = punto_equilibrio / precio_venta if punto_equilibrio!= "No se puede calcular" else "No se puede calcular"

        # Imprimir resultados
        print("Precio de venta: $", precio_venta)
        print("Precio de costo: $", precio_costo)
        print("Cantidad de unidades: ", cantidad_unidades)
        print("Margen de utilidad: ", margen_utilidad * 100, "%")
        print("Punto de equilibrio: $", punto_equilibrio)
        print("Utilidad bruta: $", utilidad_bruta)
        print("Utilidad neta: $", utilidad_neta)
        print("Tiempo de pago: ", tiempo_de_pago)
        print("Tasa de retorno: ", tasa_de_retorno, "%")
        print("Punto de equilibrio en unidades: ", punto_de_equilibrio_unidades)

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print("El punto de equilibrio del producto es de $", punto_equilibrio)
        print("La utilidad neta es de $", utilidad_neta)
        print("El tiempo de pago es de", tiempo_de_pago)
        print("La tasa de retorno es de", tasa_de_retorno, "%")

    except Exception as e:
        print("Error: ", str(e))

if __name__ == "__main__":
    main()