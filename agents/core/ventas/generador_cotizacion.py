"""
AREA: HERRAMIENTAS
DESCRIPCION: Agente que realiza generador de cotizacion
TECNOLOGIA: Python estandar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generador_cotizacion(producto, cantidad, precio_unitario, tipo_cambio, fecha_cotizacion):
    try:
        # Verificar si los valores son validos
        if not isinstance(producto, str) or not isinstance(cantidad, (int, float)) or not isinstance(precio_unitario, (int, float)) or not isinstance(tipo_cambio, (int, float)) or not isinstance(fecha_cotizacion, str):
            raise ValueError("Valores invalidos")

        # Calculos precisos y realistas para Mexico
        subtotal = precio_unitario * cantidad * tipo_cambio
        iva = subtotal * 0.16
        total = subtotal + iva
        costo_por_unidad = total / cantidad
        margen_utilidad = total * 0.20
        margen_utilidad_por_unidad = margen_utilidad / cantidad

        # Output con mas datos utiles
        print(f"{'-' * 40}")
        print(f"Area: Ventas")
        print(f"Descripcion: Generador de cotizacion")
        print(f"Fecha de generacion: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Fecha de cotizacion: {fecha_cotizacion}")
        print(f"{'-' * 40}")
        print(f"Producto: {producto}")
        print(f"Cantidad: {cantidad} unidades")
        print(f"Precio unitario: {precio_unitario:.2f} MXN")
        print(f"Tipo de cambio: {tipo_cambio:.2f} MXN/USD")
        print(f"Subtotal: {subtotal:.2f} MXN")
        print(f"IVA (16%): {iva:.2f} MXN")
        print(f"Total: {total:.2f} MXN")
        print(f"Costo por unidad: {costo_por_unidad:.2f} MXN")
        print(f"Margen de utilidad (20%): {margen_utilidad:.2f} MXN")
        print(f"Margen de utilidad por unidad: {margen_utilidad_por_unidad:.2f} MXN")
        print(f"{'-' * 40}")
        print(f"Resumen ejecutivo:")
        print(f"El costo total del producto {producto} para {cantidad} unidades es de {subtotal:.2f} MXN")
        print(f"El IVA correspondiente es de {iva:.2f} MXN")
        print(f"El margen de utilidad es de {margen_utilidad:.2f} MXN")
        print(f"{'-' * 40}")
        print(f"Resumen final:")
        print(f"Total de la cotizacion: {total:.2f} MXN")
        print(f"Fecha de pago: {datetime.datetime.now().strftime('%Y-%m-%d')}")
        print(f"{'-' * 40}")
        print(f"Observaciones:")
        print(f"Se ha realizado la cotizacion con los siguientes valores:")
        print(f"Producto: {producto}")
        print(f"Cantidad: {cantidad} unidades")
        print(f"Precio unitario: {precio_unitario:.2f} MXN")
        print(f"Tipo de cambio: {tipo_cambio:.2f} MXN/USD")
        print(f"{'-' * 40}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

def main():
    if len(sys.argv) != 6:
        print("Error: Faltan argumentos")
        return

    producto = sys.argv[1]
    cantidad = int(sys.argv[2])
    precio_unitario = float(sys.argv[3])
    tipo_cambio = float(sys.argv[4])
    fecha_cotizacion = sys.argv[5]

    generador_cotizacion(producto, cantidad, precio_unitario, tipo_cambio, fecha_cotizacion)

if __name__ == "__main__":
    main()