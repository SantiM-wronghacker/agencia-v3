"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza planificador contenido mensual
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def planificador_contenido_mensual():
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--help":
            print("Uso: python planificador_contenido_mensual.py [producto1] [precio1] [producto2] [precio2] ... [tipo_de_cambio]")
            print("  - producto1: nombre del primer producto")
            print("  - precio1: precio del primer producto")
            print("  - producto2: nombre del segundo producto")
            print("  - precio2: precio del segundo producto")
            print("  - ...: precio del producto N")
            print("  - tipo_de_cambio: tipo de cambio MXN/USD")
            sys.exit(0)

        if len(sys.argv) < 5:
            print("Error: faltan argumentos")
            sys.exit(1)

        precios = {}
        for i in range(1, len(sys.argv), 2):
            producto = sys.argv[i]
            try:
                precio = float(sys.argv[i+1])
                precios[producto] = precio
            except ValueError:
                print(f"Error: el precio de '{producto}' no es un número")
                sys.exit(1)

        if len(sys.argv) < 6:
            print("Error: tipo de cambio no proporcionado")
            sys.exit(1)

        try:
            tipo_de_cambio = float(sys.argv[-1])
        except ValueError:
            print("Error: tipo de cambio no es un número")
            sys.exit(1)

        # Calcular contenido mensual
        contenido_mensual = {
            "precios": precios,
            "tipo_de_cambio": tipo_de_cambio,
            "noticias": ["Noticia 1", "Noticia 2", "Noticia 3", "Noticia 4", "Noticia 5"],
            "cotizaciones": {"acción1": 100, "acción2": 200, "acción3": 300},
            "ventas": {"producto1": 100, "producto2": 200, "producto3": 300},
            "gastos": {"gasto1": 100, "gasto2": 200, "gasto3": 300}
        }

        # Imprimir resultados
        print("Precios de productos en México:")
        for producto, precio in precios.items():
            print(f"- {producto}: ${precio:.2f}")

        print(f"\nTipo de cambio MXN/USD: {tipo_de_cambio:.2f}")

        print("\nNoticias:")
        for noticia in contenido_mensual["noticias"]:
            print(f"- {noticia}")

        print("\nCotizaciones:")
        for acción, cotización in contenido_mensual["cotizaciones"].items():
            print(f"- {acción}: ${cotización:.2f}")

        print("\nVentas:")
        for producto, venta in contenido_mensual["ventas"].items():
            print(f"- {producto}: ${venta:.2f}")

        print("\nGastos:")
        for gasto, gasto_valor in contenido_mensual["gastos"].items():
            print(f"- {gasto}: ${gasto_valor:.2f}")

        # Calcular indicadores clave
        ventas_totales = sum(contenido_mensual["ventas"].values())
        gastos_totales = sum(contenido_mensual["gastos"].values())
        beneficio = ventas_totales - gastos_totales

        print(f"\nVentas totales: ${ventas_totales:.2f}")
        print(f"Gastos totales: ${gastos_totales:.2f}")
        print(f"Beneficio: ${beneficio:.2f}")

        # Imprimir resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El planificador de contenido mensual indica que las ventas totales son de ${ventas_totales:.2f},"
              f" los gastos totales son de ${gastos_totales:.2f} y el beneficio es de ${beneficio:.2f}.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    planificador_contenido_mensual()