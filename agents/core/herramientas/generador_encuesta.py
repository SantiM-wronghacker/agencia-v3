"""
AREA: HERRAMIENTAS
DESCRIPCION: Agente que realiza generador encuesta
TECNOLOGIA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random
from datetime import date

def extraer_precios(ciudad, año=None):
    try:
        # Simulación de extracción de precios
        if año is None:
            año = date.today().year
        if ciudad == "México D.F.":
            precios = {
                "gasolina": round(random.uniform(20, 30), 2),
                "diesel": round(random.uniform(18, 25), 2),
                "electricidad": round(random.uniform(2, 5), 2)
            }
        else:
            precios = {
                "gasolina": round(random.uniform(25, 35), 2),
                "diesel": round(random.uniform(22, 30), 2),
                "electricidad": round(random.uniform(3, 6), 2)
            }
        return precios
    except Exception as e:
        print("Error al extraer precios:", str(e))
        return {
            "gasolina": 25.50,
            "diesel": 22.20,
            "electricidad": 3.50
        }

def buscar_datos(ciudad, año=None):
    try:
        # Simulación de búsqueda de datos
        if año is None:
            año = date.today().year
        datos = {
            "ciudad": ciudad,
            "estado": "Distrito Federal" if ciudad == "México D.F." else "Otro estado",
            "población": round(random.uniform(500000, 10000000)),
            "año": año
        }
        return datos
    except Exception as e:
        print("Error al buscar datos:", str(e))
        return {
            "ciudad": ciudad,
            "estado": "Distrito Federal",
            "población": 9000000,
            "año": date.today().year
        }

def generar_encuesta(ciudad, año=None):
    precios = extraer_precios(ciudad, año)
    datos = buscar_datos(ciudad, año)
    encuesta = {
        "nombre": "Encuesta de precios",
        "fecha": date.today(),
        "precios": {
            "gasolina": precios["gasolina"],
            "diesel": precios["diesel"],
            "electricidad": precios["electricidad"]
        },
        "datos": {
            "ciudad": datos["ciudad"],
            "estado": datos["estado"],
            "población": datos["población"],
            "año": datos["año"]
        }
    }
    return encuesta

def main():
    if __name__ == "__main__":
        try:
            ciudad = sys.argv[1] if len(sys.argv) > 1 else "México D.F."
            año = sys.argv[2] if len(sys.argv) > 2 else None
            encuesta = generar_encuesta(ciudad, año)
            print("Nombre:", encuesta["nombre"])
            print("Fecha:", encuesta["fecha"])
            print("Precios:")
            print("  Gasolina:", encuesta["precios"]["gasolina"])
            print("  Diesel:", encuesta["precios"]["diesel"])
            print("  Electricidad:", encuesta["precios"]["electricidad"])
            print("Datos:")
            print("  Ciudad:", encuesta["datos"]["ciudad"])
            print("  Estado:", encuesta["datos"]["estado"])
            print("  Población:", encuesta["datos"]["población"])
            print("  Año:", encuesta["datos"]["año"])
            print("\nResumen ejecutivo:")
            print("La encuesta de precios muestra que el gasolina en", encuesta["datos"]["ciudad"], "tiene un precio promedio de", encuesta["precios"]["gasolina"], "por litro.")
            print("El diesel en", encuesta["datos"]["ciudad"], "tiene un precio promedio de", encuesta["precios"]["diesel"], "por litro.")
            print("La electricidad en", encuesta["datos"]["ciudad"], "tiene un precio promedio de", encuesta["precios"]["electricidad"], "por kilowatt hora.")
        except Exception as e:
            print("Error:", str(e))

if __name__ == "__main__":
    main()