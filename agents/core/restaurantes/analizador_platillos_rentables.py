"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza analizador platillos rentables
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
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def extraer_precios(json_data):
    try:
        precios = {}
        for platillo in json_data['platillos']:
            precios[platillo['nombre']] = platillo['precio']
        return precios
    except KeyError as e:
        print(f"Error: {e}")
        return {}

def calcula_margen(precio_venta, costo):
    try:
        if costo == 0:
            return 0
        margen = (precio_venta - costo) / costo * 100
        return margen
    except ZeroDivisionError:
        print("Error: Costo no puede ser cero")
        return 0

def analizador_platillos_rentables(precios=None, url=None, costos=None):
    if WEB and url:
        try:
            datos = web.buscar(url)
            texto = web.fetch_texto(datos['url'])
            json_data = json.loads(texto)
            precios = extraer_precios(json_data)
        except Exception as e:
            print(f"Error al obtener datos de la URL: {e}")
    
    if precios is None:
        # Datos de ejemplo hardcodeados como fallback
        if len(sys.argv) > 1:
            try:
                precios = json.loads(sys.argv[1])
            except json.JSONDecodeError:
                print("Error: Argumento no es un JSON válido")
                sys.exit(1)
        else:
            precios = {
                'Tacos de carne': 25.50,
                'Enchiladas rojas': 20.25,
                'Sopes de chorizo': 22.75,
                'Tortas de milanesa': 18.00,
                'Chiles rellenos': 19.50,
                'Enchiladas verdes': 21.00,
                'Chilaquiles': 17.50,
                'Sopa de tortilla': 15.00,
                'Tostadas de carnitas': 20.00,
                'Tortas de carne': 19.00
            }
    
    if costos is None:
        if len(sys.argv) > 2:
            try:
                costos = float(sys.argv[2])
            except ValueError:
                print("Error: Argumento no es un número válido")
                sys.exit(1)
        else:
            costos = random.uniform(10, 20)
    
    resultados = []
    for nombre, precio in precios.items():
        margen = calcula_margen(precio, costos)
        resultados.append((nombre, precio, costos, margen))
    
    resultados.sort(key=lambda x: x[3], reverse=True)
    
    print("Platillos rentables:")
    for i, (nombre, precio, costo, margen) in enumerate(resultados):
        print(f"{i+1}. {nombre}: ${precio:.2f}, Costo: ${costo:.2f}, Margen: {margen:.2f}%")
    
    print("\nResumen Ejecutivo:")
    print(f"Total de platillos: {len(precios)}")
    print(f"Platillo más rentable: {resultados[0][0]} con un margen de {resultados[0][3]:.2f}%")
    print(f"Platillo menos rentable: {resultados[-1][0]} con un margen de {resultados[-1][3]:.2f}%")
    print(f"Margen promedio: {sum(x[3] for x in resultados) / len(resultados):.2f}%")

if __name__ == "__main__":
    analizador_platillos_rentables()