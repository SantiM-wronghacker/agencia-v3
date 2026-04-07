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
    import agencia.agents.herramientas.web_bridge as web
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

    # Calcula costos totales
    precios = extraer_precios(pais)
    costos = {
        'hotel': precios['hotel'] * duracion,
        'avión': precios['avión'],
        'comida': precios['comida'] * duracion,
        'gasolina': precios['gasolina'] * duracion,
        'taxi': precios['taxi'] * duracion
    }

    # Verifica si el presupuesto es suficiente
    if sum(costos.values()) > presupuesto:
        raise ValueError('El presupuesto es insuficiente')

    return {
        'fecha_salida': fecha_salida.strftime('%Y-%m-%d'),
        'destino': destino,
        'duracion': duracion,
        'presupuesto': presupuesto,
        'transporte': transporte,
        'alojamiento': alojamiento,
        'costos': costos,
        'resumen': f'Presupuesto: ${presupuesto}, Costos totales: ${sum(costos.values())}'
    }

def main():
    try:
        if len(sys.argv) > 1:
            fecha_salida = datetime.strptime(sys.argv[1], '%Y-%m-%d')
        else:
            fecha_salida = datetime.now() + timedelta(days=7)
        if len(sys.argv) > 2:
            destino = sys.argv[2]
        else:
            destino = 'Puerto Vallarta'
        if len(sys.argv) > 3:
            duracion = int(sys.argv[3])
        else:
            duracion = 7
        if len(sys.argv) > 4:
            presupuesto = int(sys.argv[4])
        else:
            presupuesto = 10000
        if len(sys.argv) > 5:
            transporte = sys.argv[5]
        else:
            transporte = 'avión'
        if len(sys.argv) > 6:
            alojamiento = sys.argv[6]
        else:
            alojamiento = 'hotel'

        itinerario = generar_itinerario(fecha_salida, destino, duracion, presupuesto, transporte, alojamiento)
        print(f'Fecha de salida: {itinerario["fecha_salida"]}')
        print(f'Destino: {itinerario["destino"]}')
        print(f'Duración: {itinerario["duracion"]} días')
        print(f'Presupuesto: ${itinerario["presupuesto"]}')
        print(f'Transporte: {itinerario["transporte"]}')
        print(f'Alojamiento: {itinerario["alojamiento"]}')
        print('Costos totales:')
        for costo, valor in itinerario['costos'].items():
            print(f'{costo}: ${valor}')
        print(itinerario['resumen'])
    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    main()