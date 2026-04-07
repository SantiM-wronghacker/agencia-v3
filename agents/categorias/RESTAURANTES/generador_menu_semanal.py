import os
import sys
import json
import datetime
import math
import re
import random

def generar_menu_semanal(precios=None, noticias=None, cotizaciones=None):
    if precios is None:
        precios = {
            "plato1": 100.0,
            "plato2": 200.0,
            "plato3": 300.0,
            "plato4": 110.0,
            "plato5": 240.0
        }
    if noticias is None:
        noticias = "Noticias de restaurantes: nuevo restaurante en la ciudad"
    if cotizaciones is None:
        cotizaciones = "Cotizaciones actuales: 1 USD = 20 MXN"

    # Generar menu semanal
    menu = {
        "platos": [
            {"nombre": "Plato 1", "precio": precios["plato1"]},
            {"nombre": "Plato 2", "precio": precios["plato2"]},
            {"nombre": "Plato 3", "precio": precios["plato3"]},
            {"nombre": "Plato 4", "precio": precios["plato4"]},
            {"nombre": "Plato 5", "precio": precios["plato5"]}
        ],
        "noticias": noticias,
        "cotizaciones": cotizaciones
    }

    # Calcular promedio de precios
    try:
        promedio = sum(precio['precio'] for precio in menu['platos']) / len(menu['platos'])
        menu['promedio'] = f"Promedio de precios: {promedio:.2f}"
    except ZeroDivisionError:
        menu['promedio'] = "No hay platos para calcular el promedio"

    # Calcular platos más caros
    try:
        platos_caro = sorted(menu['platos'], key=lambda x: x['precio'], reverse=True)[:3]
        menu['platos_caro'] = platos_caro
    except Exception as e:
        menu['platos_caro'] = f"Error al calcular los platos más caros: {str(e)}"

    # Calcular platos más baratos
    try:
        platos_barato = sorted(menu['platos'], key=lambda x: x['precio'])[:3]
        menu['platos_barato'] = platos_barato
    except Exception as e:
        menu['platos_barato'] = f"Error al calcular los platos más baratos: {str(e)}"

    # Calcular el total de ventas
    try:
        total_ventas = sum(precio['precio'] for precio in menu['platos'])
        menu['total_ventas'] = f"Total de ventas: {total_ventas:.2f}"
    except Exception as e:
        menu['total_ventas'] = f"Error al calcular el total de ventas: {str(e)}"

    return menu

def main():
    try:
        precios = {}
        if len(sys.argv) > 1:
            for arg in sys.argv[1:]:
                if "=" in arg:
                    clave, valor = arg.split("=")
                    precios[clave] = float(valor)

        menu = generar_menu_semanal(precios=precios)
        print("ÁREA: RESTAURANTES")
        print("DESCRIPCIÓN: Agente que realiza generador menu semanal")
        print("TECNOLOGÍA: Python estándar")
        print("\nMenu Semanal:")
        print(json.dumps(menu, indent=4))
        print("\nResumen Ejecutivo:")
        print(f"Promedio de precios: {menu['promedio']}")
        print(f"Total de ventas: {menu['total_ventas']}")
        print(f"Platos más caros: {[plato['nombre'] for plato in menu['platos_caro']]}")
        print(f"Platos más baratos: {[plato['nombre'] for plato in menu['platos_barato']]}")
        print(f"Noticias: {menu['noticias']}")
        print(f"Cotizaciones: {menu['cotizaciones']}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()