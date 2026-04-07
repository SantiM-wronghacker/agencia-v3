import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Definir zonas de inversión en la CDMX con datos más reales
        zonas = {
            "Polanco": {"precio_m2": 250000, "renta_mensual": 50000},
            "Reforma": {"precio_m2": 200000, "renta_mensual": 40000},
            "Condesa": {"precio_m2": 180000, "renta_mensual": 35000},
            "Roma": {"precio_m2": 150000, "renta_mensual": 30000},
            "Juárez": {"precio_m2": 120000, "renta_mensual": 25000},
        }

        # Definir argumentos por defecto
        zona1 = "Polanco"
        zona2 = "Reforma"

        # Verificar argumentos
        if len(sys.argv) > 1:
            zona1 = sys.argv[1]
        if len(sys.argv) > 2:
            zona2 = sys.argv[2]

        # Verificar si las zonas existen
        if zona1 not in zonas:
            print(f"Error: La zona '{zona1}' no existe")
            return
        if zona2 not in zonas:
            print(f"Error: La zona '{zona2}' no existe")
            return

        # Calcular diferencia de precio por metro cuadrado
        diff_precio_m2 = zonas[zona1]["precio_m2"] - zonas[zona2]["precio_m2"]

        # Calcular diferencia de renta mensual
        diff_renta_mensual = zonas[zona1]["renta_mensual"] - zonas[zona2]["renta_mensual"]

        # Calcular relación precio-renta
        relacion_precio_renta1 = zonas[zona1]["precio_m2"] / zonas[zona1]["renta_mensual"]
        relacion_precio_renta2 = zonas[zona2]["precio_m2"] / zonas[zona2]["renta_mensual"]

        # Imprimir resultados
        print(f"Comparación de zonas: {zona1} vs {zona2}")
        print(f"Precio por metro cuadrado en {zona1}: {zonas[zona1]['precio_m2']} MXN")
        print(f"Precio por metro cuadrado en {zona2}: {zonas[zona2]['precio_m2']} MXN")
        print(f"Diferencia de precio por metro cuadrado: {diff_precio_m2} MXN")
        print(f"Renta mensual en {zona1}: {zonas[zona1]['renta_mensual']} MXN")
        print(f"Renta mensual en {zona2}: {zonas[zona2]['renta_mensual']} MXN")
        print(f"Diferencia de renta mensual: {diff_renta_mensual} MXN")
        print(f"Relación precio-renta en {zona1}: {relacion_precio_renta1:.2f}")
        print(f"Relación precio-renta en {zona2}: {relacion_precio_renta2:.2f}")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        if diff_precio_m2 > 0:
            print(f"La zona {zona1} tiene un precio por metro cuadrado más alto que la zona {zona2}")
        elif diff_precio_m2 < 0:
            print(f"La zona {zona2} tiene un precio por metro cuadrado más alto que la zona {zona1}")
        else:
            print(f"Las zonas {zona1} y {zona2} tienen el mismo precio por metro cuadrado")
        if diff_renta_mensual > 0:
            print(f"La zona {zona1} tiene una renta mensual más alta que la zona {zona2}")
        elif diff_renta_mensual < 0:
            print(f"La zona {zona2} tiene una renta mensual más alta que la zona {zona1}")
        else:
            print(f"Las zonas {zona1} y {zona2} tienen la misma renta mensual")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()