#!/usr/bin/env python3
"""
AREA: TURISMO
DESCRIPCION: Agente que realiza comparador hospedaje
TECNOLOGIA: Python estandar
"""
import sys
import json
import datetime
import math
import re
import random
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Definir opciones por defecto
        ciudad = sys.argv[1] if len(sys.argv) > 1 else "Cancun"
        num_hoteles = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        precio_maximo = float(sys.argv[3]) if len(sys.argv) > 3 else 10000.0
        num_estrellas = int(sys.argv[4]) if len(sys.argv) > 4 else 5

        # Simular datos de hospedaje
        hoteles = [
            {"nombre": "Hyatt Zilara Cancun", "precio": 4500.0, "calificacion": 4.8, "estrellas": 5},
            {"nombre": "Secrets The Vine Cancun", "precio": 3800.0, "calificacion": 4.7, "estrellas": 5},
            {"nombre": "Moon Palace Cancun", "precio": 3200.0, "calificacion": 4.5, "estrellas": 5},
            {"nombre": "Iberostar Cancun", "precio": 4000.0, "calificacion": 4.6, "estrellas": 5},
            {"nombre": "The Grand Park Royal Cancun", "precio": 3500.0, "calificacion": 4.4, "estrellas": 4},
            {"nombre": "Fiesta Americana Grand Coral Beach", "precio": 4200.0, "calificacion": 4.5, "estrellas": 4},
            {"nombre": "The Westin Lagunamar Ocean Resort Villas", "precio": 3000.0, "calificacion": 4.3, "estrellas": 4},
            {"nombre": "Riu Cancun", "precio": 2800.0, "calificacion": 4.2, "estrellas": 4},
            {"nombre": "Barcelo Maya Palace", "precio": 2500.0, "calificacion": 4.1, "estrellas": 5},
            {"nombre": "Occidental at Xcaret Destination", "precio": 2200.0, "calificacion": 4.0, "estrellas": 5},
        ]

        # Filtrar hoteles por precio maximo
        hoteles_filtrados = [hotel for hotel in hoteles if hotel["precio"] <= precio_maximo]

        # Filtrar hoteles por numero de estrellas
        hoteles_filtrados_estrellas = [hotel for hotel in hoteles_filtrados if hotel["estrellas"] >= num_estrellas]

        # Seleccionar los mejores hoteles
        mejores_hoteles = sorted(hoteles_filtrados_estrellas, key=lambda x: x["calificacion"], reverse=True)[:num_hoteles]

        # Imprimir resultados
        print("Mejores hoteles en {} con precio maximo de {} y {} estrellas o mas:".format(ciudad, precio_maximo, num_estrellas))
        for i, hotel in enumerate(mejores_hoteles):
            print("{}. {} - Precio: {} - Calificacion: {} - Estrellas: {}".format(i+1, hotel["nombre"], hotel["precio"], hotel["calificacion"], hotel["estrellas"]))

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print("Ciudad: {}".format(ciudad))
        print("Precio maximo: {}".format(precio_maximo))
        print("Numero de estrellas: {}".format(num_estrellas))
        print("Numero de hoteles seleccionados: {}".format(num_hoteles))
        print("Mejor hotel: {}".format(mejores_hoteles[0]["nombre"]))
        print("Peor hotel: {}".format(mejores_hoteles[-1]["nombre"]))

    except IndexError:
        print("Error: No se proporcionaron suficientes argumentos.")
    except ValueError:
        print("Error: Los argumentos proporcionados no son validos.")

if __name__ == "__main__":
    main()