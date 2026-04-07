"""
ÁREA: TURISMO
DESCRIPCIÓN: Agente que realiza generador itinerario
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
from datetime import datetime, timedelta
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def extraer_precios(pais='México'):
    if WEB:
        return web.extraer_precios()
    else:
        return {
            'hotel': 8000,
            'avión': 3000,
            'comida': 1500,
            'gasolina': 1000,
            'taxi': 500
        }

def generar_itinerario(fecha_salida=None, destino=None, duracion=None, presupuesto=None, transporte=None, alojamiento=None):
    if fecha_salida is None:
        fecha_salida = datetime.now() + timedelta(days=7)
    if destino is None:
        destino = 'Puerto Vallarta'
    if duracion is None:
        duracion = 7
    if presupuesto is None:
        presupuesto = 10000
    if transporte is None:
        transporte = 'avión'
    if alojamiento is None:
        alojamiento = 'hotel'

    return {
        'fecha_salida': fecha_salida.strftime('%Y-%m-%d'),
        'destino': destino,
        'duracion': duracion,
        'presupuesto': presupuesto,
        'transporte': transporte,
        'alojamiento': alojamiento
    }

def main():
    try:
        fecha_salida = datetime.now() + timedelta(days=7)
        destino = 'Puerto Vallarta'
        duracion = 7
        presupuesto = 10000
        transporte = 'avión'
        alojamiento = 'hotel'

        itinerario = generar_itinerario(fecha_salida, destino, duracion, presupuesto, transporte, alojamiento)
        print(f'Fecha de salida: {itinerario["fecha_salida"]}')
        print(f'Destino: {itinerario["destino"]}')
        print(f'Duración: {itinerario["duracion"]} días')
        print(f'Presupuesto: ${itinerario["presupuesto"]}')
        print(f'Transporte: {itinerario["transporte"]}')
        print(f'Alojamiento: {itinerario["alojamiento"]}')
        print(f'Precios: {extraer_precios("México")}')
        print(f'Presupuesto por día: ${itinerario["presupuesto"] / itinerario["duracion"]:.2f}')
        print(f'Presupuesto por persona: ${itinerario["presupuesto"] / 2:.2f}')
        print(f'Costo de gasolina: ${extraer_precios("México")["gasolina"] * duracion:.2f}')
        print(f'Costo de taxi: ${extraer_precios("México")["taxi"] * duracion:.2f}')
        print(f'Resumen ejecutivo: El itinerario para {itinerario["destino"]} durante {itinerario["duracion"]} días tiene un presupuesto de ${itinerario["presupuesto"]:.2f} y un costo de transporte de ${extraer_precios("México")["avión"]:.2f}.')
    except Exception as e:
        print(f'Ocurrió un error: {e}')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fecha_salida = datetime.strptime(sys.argv[1], '%Y-%m-%d')
        destino = sys.argv[2]
        duracion = int(sys.argv[3])
        presupuesto = int(sys.argv[4])
        transporte = sys.argv[5]
        alojamiento = sys.argv[6]
        main(fecha_salida, destino, duracion, presupuesto, transporte, alojamiento)
    else:
        main()