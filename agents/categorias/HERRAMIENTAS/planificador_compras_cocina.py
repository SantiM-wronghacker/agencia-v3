"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza planificador compras cocina
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
from datetime import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def extraer_precios():
    if WEB:
        return web.extraer_precios()
    else:
        # Permite parametros por sys.argv
        if len(sys.argv) > 1:
            try:
                with open(sys.argv[1], 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Error: El archivo de precios debe ser un JSON válido.")
                return {}
        else:
            # datos de ejemplo hardcodeados
            return {
                "harina": 25.50,
                "azúcar": 18.00,
                "aceite": 40.00,
                "carne": 60.00,
                "verduras": 20.00,
                "pescado": 50.00,
                "frutas": 30.00,
                "huevos": 15.00,
                "leche": 20.00,
                "mantequilla": 35.00
            }

def calcular_costo(precios, cantidad):
    try:
        costo = 0
        for producto, precio in precios.items():
            if producto in cantidad:
                costo += precio * cantidad[producto]
            else:
                print(f"Error: No se encontró la cantidad del producto '{producto}'")
        return costo
    except KeyError as e:
        print(f"Error: No se encontró el producto '{e.args[0]}' en la lista de precios.")
        return None
    except ValueError as e:
        print(f"Error: La cantidad de '{e.args[0]}' debe ser un número entero.")
        return None

def generar_reporte(precios, cantidad):
    reporte = ""
    reporte += "Resumen de compras:\n"
    reporte += "-------------------\n"
    reporte += f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    reporte += f"Total de productos: {len(cantidad)}\n"
    reporte += f"Total de costo: ${calcular_costo(precios, cantidad):.2f}\n"
    reporte += "Productos comprados:\n"
    for producto, cantidad_producto in cantidad.items():
        reporte += f"- {producto}: {cantidad_producto} unidades\n"
    reporte += "-------------------\n"
    reporte += "Resumen ejecutivo:\n"
    reporte += "-------------------\n"
    reporte += f"El total de costo de las compras es de ${calcular_costo(precios, cantidad):.2f}.\n"
    reporte += f"Se compraron {len(cantidad)} productos en total.\n"
    return reporte

def main():
    precios = extraer_precios()
    if precios:
        cantidad = {
            "harina": int(input("Ingrese la cantidad de harina: ")),
            "azúcar": int(input("Ingrese la cantidad de azúcar: ")),
            "aceite": int(input("Ingrese la cantidad de aceite: ")),
            "carne": int(input("Ingrese la cantidad de carne: ")),
            "verduras": int(input("Ingrese la cantidad de verduras: ")),
            "pescado": int(input("Ingrese la cantidad de pescado: ")),
            "frutas": int(input("Ingrese la cantidad de frutas: ")),
            "huevos": int(input("Ingrese la cantidad de huevos: ")),
            "leche": int(input("Ingrese la cantidad de leche: ")),
            "mantequilla": int(input("Ingrese la cantidad de mantequilla: "))
        }
        print(generar_reporte(precios, cantidad))

if __name__ == "__main__":
    main()