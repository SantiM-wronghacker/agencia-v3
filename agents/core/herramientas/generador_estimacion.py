"""
ÁREA: CONSTRUCCION
DESCRIPCIÓN: Agente que realiza generador estimacion
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random
import argparse

def generador_estimacion(precios=None):
    if precios is None:
        try:
            # Buscar datos reales con web_bridge
            datos_reales = web.buscar("precios de materiales de construcción en México")
            precios = web.extraer_precios(datos_reales)
        except ImportError:
            # Datos de ejemplo hardcodeados como fallback
            precios = {
                "madera": 100.50,
                "acero": 80.25,
                "cemento": 50.75,
                "ladrillo": 20.00,
                "pintura": 30.00,
                "tarima": 40.00,
                "puertas": 60.00,
                "ventanas": 70.00
            }
        except Exception as e:
            print(f"Error: {e}")
            return

    # Calcular estimación
    estimacion = math.sqrt(
        precios["madera"] * precios["acero"] * precios["cemento"] *
        precios["ladrillo"] * precios["pintura"] * precios["tarima"] *
        precios["puertas"] * precios["ventanas"]
    )

    # Imprimir resultados
    print("Precios de materiales de construcción en México:")
    print(f"Madera: ${precios['madera']:.2f} MXN")
    print(f"Acero: ${precios['acero']:.2f} MXN")
    print(f"Cemento: ${precios['cemento']:.2f} MXN")
    print(f"Ladrillo: ${precios['ladrillo']:.2f} MXN")
    print(f"Pintura: ${precios['pintura']:.2f} MXN")
    print(f"Tarima: ${precios['tarima']:.2f} MXN")
    print(f"Puertas: ${precios['puertas']:.2f} MXN")
    print(f"Ventanas: ${precios['ventanas']:.2f} MXN")
    print(f"Estimación: ${estimacion:.2f} MXN")

def main():
    try:
        parser = argparse.ArgumentParser(description='Generador de estimación de costos de construcción')
        parser.add_argument('--precio-madera', type=float, default=100.50, help='Precio de la madera')
        parser.add_argument('--precio-acero', type=float, default=80.25, help='Precio del acero')
        parser.add_argument('--precio-cemento', type=float, default=50.75, help='Precio del cemento')
        parser.add_argument('--precio-ladrillo', type=float, default=20.00, help='Precio del ladrillo')
        parser.add_argument('--precio-pintura', type=float, default=30.00, help='Precio de la pintura')
        parser.add_argument('--precio-tarima', type=float, default=40.00, help='Precio de la tarima')
        parser.add_argument('--precio-puertas', type=float, default=60.00, help='Precio de las puertas')
        parser.add_argument('--precio-ventanas', type=float, default=70.00, help='Precio de las ventanas')
        args = parser.parse_args()
        precios = {
            "madera": args.precio_madera,
            "acero": args.precio_acero,
            "cemento": args.precio_cemento,
            "ladrillo": args.precio_ladrillo,
            "pintura": args.precio_pintura,
            "tarima": args.precio_tarima,
            "puertas": args.precio_puertas,
            "ventanas": args.precio_ventanas
        }
        generador_estimacion(precios)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()