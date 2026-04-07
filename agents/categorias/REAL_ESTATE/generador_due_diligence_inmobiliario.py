#!/usr/bin/env python3
# AREA: REAL ESTATE
# DESCRIPCION: Generador de Due Diligence Inmobiliario para Agencia Santi (Mexico)
# TECNOLOGIA: Python (stdlib)

import sys
import os
import json
import random
from datetime import datetime, timedelta

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        tipo_inmueble = sys.argv[1] if len(sys.argv) > 1 else "departamento"
        ubicacion = sys.argv[2] if len(sys.argv) > 2 else "CDMX"
        precio_min = float(sys.argv[3]) if len(sys.argv) > 3 else 2500000.0
        precio_max = float(sys.argv[4]) if len(sys.argv) > 4 else 5000000.0

        # Generar datos de due diligence
        fecha_actual = datetime.now()
        fecha_registro = (fecha_actual - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")

        precio = round(random.uniform(precio_min, precio_max), 2)
        metros_cuadrados = round(random.uniform(50, 200), 2)
        anos_antiguedad = random.randint(0, 50)
        valor_terreno = round(precio * 0.3, 2)
        valor_edificio = round(precio * 0.7, 2)
        gastos_comunes = round(precio * 0.05, 2)
        impuestos_anuales = round(precio * 0.02, 2)

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
        print(f"Fecha de registro: {reporte['fecha_registro']}")
        print(f"Precio estimado: {reporte['precio']}")
        print(f"Área: {reporte['metros_cuadrados']}")
        print(f"Antigüedad: {reporte['antiguedad']}")
        print(f"Valor del terreno: {reporte['valor_terreno']}")
        print(f"Valor del edificio: {reporte['valor_edificio']}")
        print(f"Gastos comunes: {reporte['gastos_comunes']}")
        print(f"Impuestos anuales: {reporte['impuestos_anuales']}")

        # Resumen ejecutivo
        print("\n=== RESUMEN EJECUTIVO ===")
        print(f"El inmueble {reporte['tipo_inmueble']} ubicado en {reporte['ubicacion']} tiene un precio estimado de {reporte['precio']}.")
        print(f"La antigüedad del inmueble es de {reporte['antiguedad']} años y su área es de {reporte['metros_cuadrados']}.")
        print(f"Los gastos comunes y impuestos anuales ascienden a {reporte['gastos_comunes']} y {reporte['impuestos_anuales']} respectivamente.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()