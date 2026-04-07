"""
ÁREA: SOPORTE
DESCRIPCIÓN: Agente que realiza generador respuesta ticket
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
        try:
            precios = web.buscar('precios de productos en México')
            return json.loads(precios)
        except Exception as e:
            print(f'Error al obtener precios: {e}')
            return {}
    else:
        return {
            'producto1': 100.50,
            'producto2': 200.75,
            'producto3': 300.25,
            'producto4': 400.90,
            'producto5': 500.15,
            'producto6': 600.30,
            'producto7': 700.45,
            'producto8': 800.60,
            'producto9': 900.75,
            'producto10': 1000.90
        }

def generar_resumen_precios(precios):
    resumen = ''
    for producto, precio in precios.items():
        resumen += f'Producto: {producto}, Precio: ${precio:.2f}\n'
    return resumen

def generar_resumen_tipo_cambio():
    if WEB:
        try:
            tipo_cambio = web.buscar('tipo de cambio MXN/USD')
            return float(tipo_cambio)
        except Exception as e:
            print(f'Error al obtener tipo de cambio: {e}')
            return 20.50
    else:
        return 20.50

def generar_resumen_noticias():
    if WEB:
        try:
            noticias = web.buscar('noticias de México')
            return noticias
        except Exception as e:
            print(f'Error al obtener noticias: {e}')
            return 'No hay noticias disponibles'
    else:
        return 'No hay noticias disponibles'

def generar_resumen_economico():
    tipo_cambio = generar_resumen_tipo_cambio()
    return f'Tipo de cambio: {tipo_cambio:.2f} MXN/USD\nInflación: 3.5%\nPobreza: 20%'

def main():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('ÁREA: SOPORTE')
        print('DESCRIPCIÓN: Agente que realiza generador respuesta ticket')
        print('TECNOLOGÍA: Python estándar, web_bridge (opcional)')

        if len(sys.argv) > 1:
            if sys.argv[1] == 'precios':
                precios = extraer_precios()
                print('Resumen de precios:')
                print(generar_resumen_precios(precios))
            elif sys.argv[1] == 'tipo_cambio':
                print('Tipo de cambio: {}'.format(generar_resumen_tipo_cambio()))
            elif sys.argv[1] == 'noticias':
                print('Noticias de México: {}'.format(generar_resumen_noticias()))
            elif sys.argv[1] == 'resumen':
                print(generar_resumen_economico())
        else:
            precios = extraer_precios()
            resumen_precios = generar_resumen_precios(precios)
            tipo_cambio = generar_resumen_tipo_cambio()
            noticias = generar_resumen_noticias()

            print('Resumen de precios:')
            print(resumen_precios)
            print('Noticias de México:')
            print(noticias)
            print('Resumen económico:')
            print(generar_resumen_economico())

        sys.exit(0)
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)

if __name__ == "__main__":
    main()