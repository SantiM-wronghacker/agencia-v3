"""
ÁREA: SOPORTE
DESCRIPCIÓN: Agente que realiza analizador tendencias soporte
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
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def analizar_tendencias_soporte(precios, tipo_de_cambio, noticias, cotizaciones):
    try:
        total_gastado = sum(precios.values())
        promedio_cotizacion = sum(cotizaciones.values()) / len(cotizaciones)
        varianza_cotizaciones = sum((x - promedio_cotizacion) ** 2 for x in cotizaciones.values()) / (len(cotizaciones) - 1)
        desviacion_estandar_cotizaciones = math.sqrt(varianza_cotizaciones)
        tipo_de_cambio_real = tipo_de_cambio * promedio_cotizacion
        noticias = noticias.strip()
    except Exception as e:
        print('Error:', str(e))
        return None

    return {
        'total_gastado': total_gastado,
        'promedio_cotizacion': promedio_cotizacion,
        'varianza_cotizaciones': varianza_cotizaciones,
        'desviacion_estandar_cotizaciones': desviacion_estandar_cotizaciones,
        'tipo_de_cambio_real': tipo_de_cambio_real,
        'cotizaciones': cotizaciones,
        'noticias': noticias
    }

def main():
    if len(sys.argv) > 1:
        precios = {'producto1': float(sys.argv[1]), 'producto2': float(sys.argv[2])}
        tipo_de_cambio = float(sys.argv[3])
        noticias = sys.argv[4]
        cotizaciones = {'producto1': float(sys.argv[5]), 'producto2': float(sys.argv[6])}
    else:
        if WEB:
            precios = web.buscar('precios de productos')
            tipo_de_cambio = web.buscar('tipo de cambio')
            noticias = web.fetch_texto('noticias de último momento')
            cotizaciones = web.extraer_precios()
        else:
            precios = {'producto1': 100.0, 'producto2': 200.0}
            tipo_de_cambio = 20.0
            noticias = 'Noticias de ejemplo'
            cotizaciones = {'producto1': 100.0, 'producto2': 200.0}

    resultado = analizar_tendencias_soporte(precios, tipo_de_cambio, noticias, cotizaciones)
    if resultado:
        print('Área: Soporte')
        print('Descripción: Analizador de tendencias soporte')
        print('Tecnología: Python estándar')
        print('Total gastado:', resultado['total_gastado'], 'MXN')
        print('Promedio de cotización:', resultado['promedio_cotizacion'], 'MXN')
        print('Varianza de cotizaciones:', resultado['varianza_cotizaciones'])
        print('Desviación estandar de cotizaciones:', resultado['desviacion_estandar_cotizaciones'])
        print('Tipo de cambio real:', resultado['tipo_de_cambio_real'], 'MXN/USD')
        print('Cotizaciones:', resultado['cotizaciones'])
        print('Noticias de último momento:', resultado['noticias'])
        print('Resumen ejecutivo:')
        print('El análisis de tendencias soporte muestra que el total gastado es de', resultado['total_gastado'], 'MXN.')
        print('El promedio de cotización es de', resultado['promedio_cotizacion'], 'MXN.')
        print('La varianza de cotizaciones es de', resultado['varianza_cotizaciones'].round(2), '.')
        print('La desviación estandar de cotizaciones es de', resultado['desviacion_estandar_cotizaciones'].round(2), '.')
        print('El tipo de cambio real es de', resultado['tipo_de_cambio_real'], 'MXN/USD.')

if __name__ == "__main__":
    main()