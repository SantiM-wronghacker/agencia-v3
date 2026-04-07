"""
ÁREA: MANUFACTURA
DESCRIPCIÓN: Agente que realiza generador orden produccion
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
from datetime import datetime
import math
import re
import random

def generar_orden_produccion(precio_materiales=None, tipo_cambio=None, cotizaciones=None):
    try:
        # Valores por defecto
        if precio_materiales is None:
            precio_materiales = 100.0
        if tipo_cambio is None:
            tipo_cambio = 20.0
        if cotizaciones is None:
            cotizaciones = 5000.0
        
        # Generar orden de producción
        orden_produccion = {
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "hora": datetime.now().strftime("%H:%M:%S"),
            "cantidad": random.randint(100, 1000),
            "precio_unitario": precio_materiales,
            "total": precio_materiales * random.randint(100, 1000),
            "tipo_cambio": tipo_cambio,
            "cotizaciones": cotizaciones,
            "total_cif": precio_materiales * tipo_cambio * random.randint(100, 1000),
            "utilidad": (precio_materiales * tipo_cambio * random.randint(100, 1000)) * 0.2,
            "costo_total": precio_materiales * tipo_cambio * random.randint(100, 1000) + (precio_materiales * tipo_cambio * random.randint(100, 1000)) * 0.2,
        }
        
        # Imprimir orden de producción
        print(f"Fecha: {orden_produccion['fecha']}")
        print(f"Hora: {orden_produccion['hora']}")
        print(f"Cantidad: {orden_produccion['cantidad']}")
        print(f"Precio unitario: {orden_produccion['precio_unitario']}")
        print(f"Total: {orden_produccion['total']}")
        print(f"Tipo de cambio: {orden_produccion['tipo_cambio']}")
        print(f"Cotizaciones: {orden_produccion['cotizaciones']}")
        print(f"Total CIF: {orden_produccion['total_cif']}")
        print(f"Utilidad: {orden_produccion['utilidad']}")
        print(f"Costo total: {orden_produccion['costo_total']}")
        
        # Guardar orden de producción en archivo JSON
        with open("orden_produccion.json", "w") as archivo:
            json.dump(orden_produccion, archivo, indent=4)
        
        return orden_produccion
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    if len(sys.argv) > 1:
        precio_materiales = float(sys.argv[1])
        tipo_cambio = float(sys.argv[2])
        cotizaciones = float(sys.argv[3])
    else:
        precio_materiales = 100.0
        tipo_cambio = 20.0
        cotizaciones = 5000.0
    
    orden_produccion = generar_orden_produccion(precio_materiales, tipo_cambio, cotizaciones)
    if orden_produccion:
        print("Orden de producción generada con éxito.")
        print("Resumen ejecutivo:")
        print(f"Fecha: {orden_produccion['fecha']}")
        print(f"Hora: {orden_produccion['hora']}")
        print(f"Cantidad: {orden_produccion['cantidad']}")
        print(f"Precio unitario: {orden_produccion['precio_unitario']}")
        print(f"Total: {orden_produccion['total']}")
        print(f"Tipo de cambio: {orden_produccion['tipo_cambio']}")
        print(f"Cotizaciones: {orden_produccion['cotizaciones']}")
        print(f"Total CIF: {orden_produccion['total_cif']}")
        print(f"Utilidad: {orden_produccion['utilidad']}")
        print(f"Costo total: {orden_produccion['costo_total']}")

if __name__ == "__main__":
    main()