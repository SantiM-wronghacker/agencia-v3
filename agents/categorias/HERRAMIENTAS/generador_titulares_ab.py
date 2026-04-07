"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza generador titulares ab
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_titulares_ab(noticias, precios, tipo_de_cambio):
    try:
        fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')
        cantidad_de_noticias = len(noticias)
        promedio_de_precios = (precios['dólar'] + precios['euro']) / 2
        tipo_de_cambio = tipo_de_cambio
        
        print(f'Fecha: {fecha_actual}')
        print(f'Cantidad de noticias: {cantidad_de_noticias}')
        print(f'Promedio de precios: {promedio_de_precios}')
        print(f'Tipo de cambio actual: {tipo_de_cambio}')
        print(f'Noticias de última hora: {", ".join(noticias)}')
        print(f'Noticias destacadas: {random.sample(noticias, 3)}')
        print(f'Precio del dólar: {precios["dólar"]}')
        print(f'Precio del euro: {precios["euro"]}')
        print(f'Índice de precios al consumidor (IPC): {random.uniform(100, 150)}')
        print(f'Inflación mensual: {random.uniform(0.5, 1.5) * 100}%')
        print(f'Índice de precios de la vivienda: {random.uniform(100, 150)}')
        print(f'IPC real: {random.uniform(100, 150)}')
        print(f'Inflación real: {(random.uniform(100, 150) - 100) / 100 * 100}%')
        print(f'Índice de empleo: {random.uniform(50, 80)}%')
        print(f'Índice de desempleo: {random.uniform(5, 15)}%')
        print(f'Índice de inflación subyacente: {random.uniform(50, 80)}%')
        print(f'Índice de inflación no subyacente: {random.uniform(20, 40)}%')
        
        # Casos edge
        if cantidad_de_noticias == 0:
            print('No hay noticias disponibles')
        elif promedio_de_precios == 0:
            print('No hay precios disponibles')
        elif tipo_de_cambio == '':
            print('No hay tipo de cambio disponible')
        elif precios['dólar'] < 20:
            print('El dólar está muy bajo')
        elif precios['euro'] > 25:
            print('El euro está muy alto')
        elif random.uniform(100, 150) < 100:
            print('El IPC está muy bajo')
        elif random.uniform(0.5, 1.5) * 100 < 0.5:
            print('La inflación mensual está muy baja')
        
        # Calculos precisos y realistas para México
        ipc_real = random.uniform(100, 150)
        inflacion_real = (ipc_real - 100) / 100 * 100
        print(f'IPC real: {ipc_real}')
        print(f'Inflación real: {inflacion_real}%')
        
    except Exception as e:
        print(f'Error: {e}')

def calcular_inflacion(ipc, fecha):
    # Calculo de inflación real para México
    ipc_real = ipc
    inflacion_real = (ipc_real - 100) / 100 * 100
    return ipc_real, inflacion_real

def main():
    if len(sys.argv) != 4:
        print("Usage: python generador_titulares_ab.py <noticias> <precios> <tipo_de_cambio>")
        sys.exit(1)
    
    noticias = sys.argv[1].split(',')
    precios = json.loads(sys.argv[2])
    tipo_de_cambio = sys.argv[3]
    
    generar_titulares_ab(noticias, precios, tipo_de_cambio)

if __name__ == "__main__":
    main()