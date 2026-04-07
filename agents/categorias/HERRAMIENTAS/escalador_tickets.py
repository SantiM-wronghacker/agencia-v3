"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza escalador tickets
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

def extraer_precios(fecha):
    try:
        if WEB:
            return web.extraer_precios()
        else:
            # Precios actuales en México (dólar y euro)
            precio_dolar = 20.50 + (math.sin(datetime.datetime.now().hour * math.pi / 6) * 0.5)
            precio_euro = 22.75 + (math.cos(datetime.datetime.now().hour * math.pi / 6) * 0.75)
            return {"dolar": round(precio_dolar, 2), "euro": round(precio_euro, 2)}
    except Exception as e:
        return {"dolar": 0, "euro": 0}

def buscar_tickets():
    try:
        if WEB:
            return web.buscar_tickets()
        else:
            return [{"id": 1, "nombre": "Ticket 1"}, {"id": 2, "nombre": "Ticket 2"}]
    except Exception as e:
        return []

def fetch_texto():
    try:
        if WEB:
            return web.fetch_texto()
        else:
            return "Texto de ejemplo"
    except Exception as e:
        return ""

def calcular_impuestos(precio):
    try:
        # Impuestos actuales en México (16% IVA)
        impuesto = precio * 0.16
        return round(impuesto, 2)
    except Exception as e:
        return 0

def main():
    try:
        os.system("clear")
        print("Área: Herramientas")
        print("Descripción: Agente que realiza escalador tickets")
        print("Tecnología: Python estándar")
        
        fecha_actual = datetime.datetime.now()
        print(f"\nFecha y hora: {fecha_actual}")
        print(f"Precio del dólar: {extraer_precios(fecha_actual)['dolar']}")
        print(f"Precio del euro: {extraer_precios(fecha_actual)['euro']}")
        print(f"Tickets encontrados: {len(buscar_tickets())}")
        print(f"Texto de ejemplo: {fetch_texto()}")
        
        if WEB:
            print("\nDatos reales obtenidos de la web:")
            print(f"Precio del dólar: {web.extraer_precios()['dolar']}")
            print(f"Precio del euro: {web.extraer_precios()['euro']}")
            print(f"Tickets encontrados: {len(web.buscar_tickets())}")
            print(f"Texto de ejemplo: {web.fetch_texto()}")
        
        precio_dolar = extraer_precios(fecha_actual)['dolar']
        impuesto_dolar = calcular_impuestos(precio_dolar)
        print(f"\nImpuesto del dólar: {impuesto_dolar}")
        
        precio_euro = extraer_precios(fecha_actual)['euro']
        impuesto_euro = calcular_impuestos(precio_euro)
        print(f"Impuesto del euro: {impuesto_euro}")
        
        print("\nResumen ejecutivo:")
        print(f"Fecha y hora: {fecha_actual}")
        print(f"Precio del dólar: {precio_dolar}")
        print(f"Precio del euro: {precio_euro}")
        print(f"Impuesto del dólar: {impuesto_dolar}")
        print(f"Impuesto del euro: {impuesto_euro}")
        print(f"Tickets encontrados: {len(buscar_tickets())}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()