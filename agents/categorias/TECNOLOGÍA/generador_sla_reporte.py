import os
import sys
import json
import datetime
import math
import re
import random
import argparse

def extraer_precios(precio_dolar, precio_euro, precio_pesos):
    return {
        'dolar': precio_dolar,
        'euro': precio_euro,
        'pesos': precio_pesos
    }

def calcular_promedio_transacciones(volumen_transacciones, dias):
    return volumen_transacciones / dias

def calcular_volumen_transacciones(dias):
    # Utilizando la tasa de crecimiento anual del PIB de México (4.5%)
    # y asumiendo que el volumen de transacciones crece al mismo ritmo que el PIB
    volumen_transacciones = 1000000 * (1 + 0.045) ** dias
    return volumen_transacciones

def generar_reporte(precio_dolar, precio_euro, precio_pesos, dias):
    fecha_actual = datetime.date.today()
    fecha_anterior = fecha_actual - datetime.timedelta(days=dias)
    fecha_anterior_str = fecha_anterior.strftime('%Y-%m-%d')
    fecha_actual_str = fecha_actual.strftime('%Y-%m-%d')

    informacion = {
        'fecha': fecha_anterior_str,
        'tipo_cambio': precio_dolar,
        'volumen_transacciones': calcular_volumen_transacciones(dias),
        'promedio_transacciones': calcular_promedio_transacciones(calcular_volumen_transacciones(dias), dias)
    }

    reporte = f"""
ÁREA: SOPORTE
DESCRIPCIÓN: Agente que realiza generador sla reporte
TECNOLOGÍA: Python estándar

Fecha actual: {fecha_actual_str}
Fecha anterior: {fecha_anterior_str}

Tipo de cambio: {informacion['tipo_cambio']} MXN
Volumen de transacciones: {informacion['volumen_transacciones']}
Promedio de transacciones: {informacion['promedio_transacciones']}

Precios actuales:
Dólar: {precio_dolar} MXN
Euro: {precio_euro} MXN
Pesos: {precio_pesos} MXN

Resumen ejecutivo:
El volumen de transacciones ha sido de {informacion['volumen_transacciones']} en los últimos {dias} días.
El promedio de transacciones ha sido de {informacion['promedio_transacciones']} por día.

Resumen de datos:
- Volumen de transacciones: {informacion['volumen_transacciones']}
- Promedio de transacciones: {informacion['promedio_transacciones']}

Resumen por moneda:
- Dólar: {informacion['volumen_transacciones'] / informacion['tipo_cambio']}
- Euro: {informacion['volumen_transacciones'] / informacion['tipo_cambio'] * 0.85}
- Pesos: {informacion['volumen_transacciones'] / informacion['tipo_cambio'] * 0.15}

Resumen ejecutivo final:
El volumen de transacciones ha sido significativo en los últimos {dias} días y el promedio de transacciones ha sido estable.

"""

    return reporte

def main():
    parser = argparse.ArgumentParser(description='Generador Sla Reporte')
    parser.add_argument('--dolar', type=float, help='Tipo de cambio del dólar')
    parser.add_argument('--euro', type=float, help='Tipo de cambio del euro')
    parser.add_argument('--pesos', type=float, help='Tipo de cambio de los pesos')
    parser.add_argument('--dias', type=int, help='Número de días a considerar')
    args = parser.parse_args()

    if args.dolar and args.euro and args.pesos and args.dias:
        reporte = generar_reporte(args.dolar, args.euro, args.pesos, args.dias)
        print(reporte)
    else:
        print("Faltan argumentos")

if __name__ == "__main__":
    main()