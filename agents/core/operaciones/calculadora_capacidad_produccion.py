"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora capacidad produccion
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
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def calcular_capacidad_produccion(cantidad_productos, tiempo_produccion, costo_mano_obra, costo_maquinaria, precio_venta):
    try:
        capacidad_produccion = cantidad_productos / tiempo_produccion
        costo_total = (costo_mano_obra + costo_maquinaria) * tiempo_produccion
        beneficio = precio_venta * cantidad_productos - costo_total
        return capacidad_produccion, costo_total, beneficio
    except ZeroDivisionError:
        print("Error: Tiempo de producción no puede ser cero.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def calcular_costo_por_unidad(cantidad_productos, costo_total):
    try:
        return costo_total / cantidad_productos
    except ZeroDivisionError:
        print("Error: Cantidad de productos no puede ser cero.")
        return None

def calcular_margen_ganancia(precio_venta, costo_por_unidad):
    try:
        return (precio_venta - costo_por_unidad) / precio_venta * 100
    except ZeroDivisionError:
        print("Error: Precio de venta no puede ser cero.")
        return None

def main():
    try:
        if len(sys.argv) != 6:
            print("Error: Faltan argumentos. Uso: python calculadora_capacidad_produccion.py <cantidad_productos> <tiempo_produccion> <costo_mano_obra> <costo_maquinaria> <precio_venta>")
            return

        cantidad_productos = int(sys.argv[1])
        tiempo_produccion = float(sys.argv[2])
        costo_mano_obra = float(sys.argv[3])
        costo_maquinaria = float(sys.argv[4])
        precio_venta = float(sys.argv[5])

        capacidad_produccion, costo_total, beneficio = calcular_capacidad_produccion(cantidad_productos, tiempo_produccion, costo_mano_obra, costo_maquinaria, precio_venta)

        if capacidad_produccion is not None:
            costo_por_unidad = calcular_costo_por_unidad(cantidad_productos, costo_total)
            margen_ganancia = calcular_margen_ganancia(precio_venta, costo_por_unidad)

            # Mostrar resultados
            print(f"Capacidad de producción: {capacidad_produccion:.2f} productos/hora")
            print(f"Costo total: {costo_total:.2f} pesos mexicanos")
            print(f"Beneficio: {beneficio:.2f} pesos mexicanos")
            print(f"Costo por unidad: {costo_por_unidad:.2f} pesos mexicanos")
            print(f"Margen de ganancia: {margen_ganancia:.2f}%")

            # Guardar resultados en archivo
            ahora = datetime.datetime.now()
            with open(f"reporte_{ahora.strftime('%Y%m%d_%H%M%S')}.txt", "w") as archivo:
                archivo.write(f"Capacidad de producción: {capacidad_produccion:.2f} productos/hora\n")
                archivo.write(f"Costo total: {costo_total:.2f} pesos mexicanos\n")
                archivo.write(f"Beneficio: {beneficio:.2f} pesos mexicanos\n")
                archivo.write(f"Costo por unidad: {costo_por_unidad:.2f} pesos mexicanos\n")
                archivo.write(f"Margen de ganancia: {margen_ganancia:.2f}%\n")

        else:
            print("Error: No se pudo calcular la capacidad de producción.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()