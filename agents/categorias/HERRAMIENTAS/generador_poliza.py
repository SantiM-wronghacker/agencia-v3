"""
AREA: SEGUROS
DESCRIPCION: Agente que realiza generador poliza
TECNOLOGIA: Python estandar
"""

import os
import sys
import json
from datetime import datetime
import math
import re
import random

def generar_poliza(precio_seguro=5000.50, tipo_cambio=20.50, noticias='Las noticias actuales son: COVID-19, politica, economia.', 
                   cotizaciones={'acciones': 1000.50, 'divisas': 500.25}, cliente='Juan Perez', tipo_seguro='Seguro de vida'):
    try:
        if precio_seguro <= 0:
            raise ValueError("Precio seguro debe ser mayor que cero")

        if tipo_cambio <= 0:
            raise ValueError("Tipo de cambio debe ser mayor que cero")

        if noticias == '':
            raise ValueError("Noticias no pueden estar vacias")

        if cotizaciones['acciones'] <= 0 or cotizaciones['divisas'] <= 0:
            raise ValueError("Cotizaciones deben ser mayores que cero")

        poliza = {
            'cliente': cliente,
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'precio_seguro': float(precio_seguro),
            'tipo_cambio': float(tipo_cambio),
            'noticias': noticias,
            'cotizaciones': cotizaciones,
            'tipo_seguro': tipo_seguro
        }

        print('Poliza generada con exito:')
        print('Cliente:', poliza['cliente'])
        print('Fecha:', poliza['fecha'])
        print('Precio seguro:', poliza['precio_seguro'])
        print('Tipo de cambio:', poliza['tipo_cambio'])
        print('Noticias:', poliza['noticias'])
        print('Cotizaciones:', poliza['cotizaciones'])
        print('Tipo de seguro:', poliza['tipo_seguro'])

        valor_total = poliza['precio_seguro'] + (poliza['cotizaciones']['acciones'] * 0.05) + (poliza['cotizaciones']['divisas'] * 0.01)
        print('Valor total de la poliza:', valor_total)

        impuesto = valor_total * 0.15
        print('Impuesto sobre la renta:', impuesto)

        valor_neto = valor_total - impuesto
        print('Valor neto de la poliza:', valor_neto)

        print('Resumen de la poliza:')
        print('Cliente:', poliza['cliente'])
        print('Fecha de emision:', poliza['fecha'])
        print('Fecha de vencimiento:', (datetime.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d'))
        print('Precio total:', valor_total)
        print('Impuesto:', impuesto)
        print('Valor neto:', valor_neto)
        print('Notas:', 'Poliza generada con exito. Favor de revisar los detalles.')

        print('Detalles adicionales:')
        print('Cantidad de asegurados:', random.randint(1, 10))
        print('Valor de la poliza:', valor_total)
        print('Fecha de pago:', (datetime.now() + datetime.timedelta(days=15)).strftime('%Y-%m-%d'))

        print('Resumen ejecutivo:')
        print('La poliza ha sido generada con exito y se encuentra lista para ser emitida.')

    except ValueError as e:
        print('Error:', e)
    except Exception as e:
        print('Error:', e)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        precio_seguro = float(sys.argv[1])
        tipo_cambio = float(sys.argv[2])
        noticias = sys.argv[3]
        cotizaciones = {'acciones': float(sys.argv[4]), 'divisas': float(sys.argv[5])}
        cliente = sys.argv[6]
        tipo_seguro = sys.argv[7]
        generar_poliza(precio_seguro, tipo_cambio, noticias, cotizaciones, cliente, tipo_seguro)
    else:
        generar_poliza()