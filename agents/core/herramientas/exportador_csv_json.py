"""
ÁREA: DATOS
DESCRIPCIÓN: Agente que realiza exportador csv json
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random
import csv

def extraer_datos(debug=False):
    if sys.argv[1] == '--debug':
        texto = 'Texto de ejemplo'
        precios = {
            'precio1': 100.50,
            'precio2': 200.75,
            'precio3': 300.25
        }
    else:
        try:
            texto = sys.argv[1]
            precios = {
                'precio1': float(sys.argv[2]),
                'precio2': float(sys.argv[3]),
                'precio3': float(sys.argv[4])
            }
        except (IndexError, ValueError):
            print('Faltan parámetros. Uso: python exportador_csv_json.py <texto> <precio1> <precio2> <precio3>')
            sys.exit(1)
    
    try:
        # Buscar datos en tiempo real
        texto_api = web.fetch_texto('https://api.example.com/datos')
        try:
            precios_api = web.extraer_precios(texto_api)
        except ValueError as e:
            print(f'Error al extraer precios: {e}')
            precios_api = {}
        
        # Combinar datos de API y hardcoded
        precios = {**precios, **precios_api}
    except ImportError:
        pass
    
    return texto, precios

def crear_csv(texto, precios):
    try:
        with open('datos.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Fecha', 'Precio1', 'Precio2', 'Precio3'])
            writer.writerow([datetime.date.today(), precios['precio1'], precios['precio2'], precios['precio3']])
            writer.writerow(['Total', precios['precio1'] + precios['precio2'] + precios['precio3']])
    except Exception as e:
        print(f'Error al crear CSV: {e}')

def crear_json(texto, precios):
    try:
        with open('datos.json', 'w') as jsonfile:
            json.dump({
                'fecha': str(datetime.date.today()),
                'precios': precios
            }, jsonfile, indent=4)
    except Exception as e:
        print(f'Error al crear JSON: {e}')

def crear_excel(texto, precios):
    try:
        import xlsxwriter
        workbook = xlsxwriter.Workbook('datos.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, 'Fecha')
        worksheet.write(0, 1, 'Precio1')
        worksheet.write(0, 2, 'Precio2')
        worksheet.write(0, 3, 'Precio3')
        worksheet.write(1, 0, datetime.date.today())
        worksheet.write(1, 1, precios['precio1'])
        worksheet.write(1, 2, precios['precio2'])
        worksheet.write(1, 3, precios['precio3'])
        worksheet.write(2, 0, 'Total')
        worksheet.write(2, 1, precios['precio1'] + precios['precio2'] + precios['precio3'])
        workbook.close()
    except Exception as e:
        print(f'Error al crear Excel: {e}')

def resumen_ejecutivo(texto, precios):
    print(f'Resumen ejecutivo: El texto es "{texto}" y los precios son {precios}')

def main():
    texto, precios = extraer_datos(debug=True)
    print(f'Texto: {texto}')
    print(f'Precios: {precios}')
    crear_csv(texto, precios)
    crear_json(texto, precios)
    crear_excel(texto, precios)
    resumen_ejecutivo(texto, precios)

if __name__ == "__main__":
    main()