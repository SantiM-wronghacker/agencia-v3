"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora margen producto
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

def calculadora_margen_producto(precio_costo, precio_venta, costo_unitario):
    if precio_costo <= 0 or precio_venta <= 0 or costo_unitario < 0:
        return 0
    if precio_costo > precio_venta:
        raise ValueError("Precio de costo no puede ser mayor que el precio de venta")
    if costo_unitario > precio_venta:
        raise ValueError("Costo unitario no puede ser mayor que el precio de venta")
    margen = (precio_venta - costo_unitario) / precio_venta * 100
    return margen

def calcular_ingresos_totales(precio_venta, cantidad):
    return precio_venta * cantidad

def calcular_ganancia_por_unidad(precio_venta, costo_unitario, cantidad):
    return (precio_venta - costo_unitario) * cantidad

def calcular_ganancia_total(precio_venta, costo_unitario, cantidad):
    return (precio_venta - costo_unitario) * cantidad

def main():
    try:
        if WEB:
            # Buscar precios en tiempo real
            precios = web.buscar("precios de productos")
            if 'precio_costo' in precios and 'precio_venta' in precios:
                precio_costo = float(precios['precio_costo'])
                precio_venta = float(precios['precio_venta'])
            else:
                print("No se encontraron precios en tiempo real.")
                sys.exit(1)
        else:
            # Leer precios desde sys.argv
            if len(sys.argv) not in [4, 5]:
                print("Uso: python calculadora_margen_producto.py <precio_costo> <precio_venta> <costo_unitario> [<cantidad>]")
                sys.exit(1)
            precio_costo = float(sys.argv[1])
            precio_venta = float(sys.argv[2])
            costo_unitario = float(sys.argv[3])
            cantidad = float(sys.argv[4]) if len(sys.argv) == 5 else 100
        
        margen = calculadora_margen_producto(precio_costo, precio_venta, costo_unitario)
        
        print(f"Precio de costo: {precio_costo} MXN")
        print(f"Precio de venta: {precio_venta} MXN")
        print(f"Costo unitario: {costo_unitario} MXN")
        print(f"Cantidad: {cantidad} unidades")
        print(f"Márgen de ganancia: {margen:.2f}%")
        print(f"Ingresos totales: {calcular_ingresos_totales(precio_venta, cantidad):.2f} MXN")
        print(f"Ganancia por unidad: {calcular_ganancia_por_unidad(precio_venta, costo_unitario, cantidad):.2f} MXN")
        print(f"Ganancia total: {calcular_ganancia_total(precio_venta, costo_unitario, cantidad):.2f} MXN")
        
        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El producto tiene un márgen de ganancia de {margen:.2f}%")
        print(f"Los ingresos totales son de {calcular_ingresos_totales(precio_venta, cantidad):.2f} MXN")
        print(f"La ganancia por unidad es de {calcular_ganancia_por_unidad(precio_venta, costo_unitario, cantidad):.2f} MXN")
        print(f"La ganancia total es de {calcular_ganancia_total(precio_venta, costo_unitario, cantidad):.2f} MXN")
        
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()