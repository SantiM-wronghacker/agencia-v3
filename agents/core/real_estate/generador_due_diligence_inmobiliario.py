#!/usr/bin/env python3
# AREA: REAL ESTATE
# DESCRIPCION: Generador de Due Diligence Inmobiliario para Agencia Santi (Mexico)
# TECNOLOGIA: Python (stdlib)

import sys
import os
import json
import random
from datetime import datetime, timedelta
import math

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_gastos_comunes(precio):
    return round(precio * 0.05, 2)

def calcular_impuestos_anuales(precio):
    return round(precio * 0.02, 2)

def calcular_valor_terreno(precio):
    return round(precio * 0.3, 2)

def calcular_valor_edificio(precio):
    return round(precio * 0.7, 2)

def main():
    try:
        # Parámetros por defecto
        tipo_inmueble = sys.argv[1] if len(sys.argv) > 1 else "departamento"
        ubicacion = sys.argv[2] if len(sys.argv) > 2 else "CDMX"
        precio_min = float(sys.argv[3]) if len(sys.argv) > 3 else 2500000.0
        precio_max = float(sys.argv[4]) if len(sys.argv) > 4 else 5000000.0

        # Verificar que el precio mínimo sea menor que el precio máximo
        if precio_min >= precio_max:
            raise ValueError("Precio mínimo debe ser menor que el precio máximo")

        # Generar datos de due diligence
        fecha_actual = datetime.now()
        fecha_registro = (fecha_actual - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")

        precio = round(random.uniform(precio_min, precio_max), 2)
        metros_cuadrados = round(random.uniform(50, 200), 2)
        anos_antiguedad = random.randint(0, 50)

        # Calcular valores
        valor_terreno = calcular_valor_terreno(precio)
        valor_edificio = calcular_valor_edificio(precio)
        gastos_comunes = calcular_gastos_comunes(precio)
        impuestos_anuales = calcular_impuestos_anuales(precio)

        # Generar reporte
        reporte = {
            "tipo_inmueble": tipo_inmueble,
            "ubicacion": ubicacion,
            "fecha_registro": fecha_registro,
            "precio": f"${precio:,.2f} MXN",
            "metros_cuadrados": f"{metros_cuadrados} m²",
            "antiguedad": f"{anos_antiguedad} años",
            "valor_terreno": f"${valor_terreno:,.2f} MXN",
            "valor_edificio": f"${valor_edificio:,.2f} MXN",
            "gastos_comunes": f"${gastos_comunes:,.2f} MXN",
            "impuestos_anuales": f"${impuestos_anuales:,.2f} MXN"
        }

        # Imprimir reporte
        print("=== REPORTE DE DUE DILIGENCE INMOBILIARIO ===")
        print(f"Tipo: {reporte['tipo_inmueble']}")
        print(f"Ubicación: {reporte['ubicacion']}")
        print(f"Precio: {reporte['precio']}")
        print(f"Metros cuadrados: {reporte['metros_cuadrados']}")
        print(f"Antigüedad: {reporte['antiguedad']}")
        print(f"Valor terreno: {reporte['valor_terreno']}")
        print(f"Valor edificio: {reporte['valor_edificio']}")
        print(f"Gastos comunes: {reporte['gastos_comunes']}")
        print(f"Impuestos anuales: {reporte['impuestos_anuales']}")

        # Imprimir resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El inmueble de {reporte['tipo_inmueble']} ubicado en {reporte['ubicacion']} tiene un precio de {reporte['precio']} y un valor de terreno de {reporte['valor_terreno']}.")
        print(f"Los gastos comunes ascienden a {reporte['gastos_comunes']} y los impuestos anuales a {reporte['impuestos_anuales']}.")

    except (ValueError, IndexError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()