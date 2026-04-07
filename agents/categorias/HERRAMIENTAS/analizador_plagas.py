"""
ÁREA: AGRICULTURA
DESCRIPCIÓN: Agente que realiza analizador plagas
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def analizador_plagas(zona, cultivo, plaga):
    # Parámetros por defecto
    fecha = datetime.date.today().strftime("%Y-%m-%d")

    # Obtener datos de la base de datos
    try:
        with open('datos.json', 'r') as f:
            datos = json.load(f)
    except FileNotFoundError:
        print("No se encontró la base de datos.")
        return

    # Verificar si cultivo existe en la base de datos
    if cultivo not in datos['cultivos']:
        print("Cultivo no encontrado.")
        return

    # Analiza datos y genera informe
    informe = f"Informe de plagas para {cultivo} en {zona} el {fecha}:\n"
    informe += f"Plagas detectadas: {', '.join(datos['plagas'])}\n"
    informe += f"Precio de {cultivo}: ${datos['precios'][cultivo]}\n"
    informe += f"Producción de {cultivo}: {datos['producción'][cultivo]} unidades\n"
    informe += f"Consumo de {cultivo}: {datos['consumo'][cultivo]} unidades\n"
    informe += f"Ventas de {cultivo}: ${datos['ventas'][cultivo]}\n"
    informe += f"Índice de producción: {datos['producción'][cultivo] / datos['consumo'][cultivo] * 100}%\n"
    informe += f"Índice de ventas: {datos['ventas'][cultivo] / datos['producción'][cultivo] * 100}%\n"
    informe += f"Índice de rentabilidad: {(datos['ventas'][cultivo] - datos['precios'][cultivo] * datos['producción'][cultivo]) / datos['ventas'][cultivo] * 100}%\n"
    informe += f"Margen de ganancia: {(datos['ventas'][cultivo] - datos['precios'][cultivo] * datos['producción'][cultivo]) / datos['ventas'][cultivo] * 100}%\n"
    informe += f"Costo de producción: ${datos['precios'][cultivo] * datos['producción'][cultivo]}\n"
    informe += f"Beneficio neto: ${datos['ventas'][cultivo] - datos['precios'][cultivo] * datos['producción'][cultivo]}\n"
    informe += f"Utilidad por unidad: ${(datos['ventas'][cultivo] - datos['precios'][cultivo] * datos['producción'][cultivo]) / datos['producción'][cultivo]}\n"
    informe += f"Índice de liquidez: {datos['ventas'][cultivo] / datos['precios'][cultivo]}\n"
    informe += f"Índice de solvencia: {datos['ventas'][cultivo] / datos['precios'][cultivo]}\n"

    # Resumen ejecutivo
    informe += "\nResumen Ejecutivo:\n"
    informe += f"Cultivo: {cultivo}\n"
    informe += f"Zona: {zona}\n"
    informe += f"Fecha: {fecha}\n"
    informe += f"Plagas detectadas: {', '.join(datos['plagas'])}\n"
    informe += f"Producción total: {sum(datos['producción'].values())} unidades\n"
    informe += f"Ventas totales: ${sum(datos['ventas'].values())}\n"
    informe += f"Beneficio neto total: ${sum(datos['ventas'].values()) - sum(datos['precios'].values()) * sum(datos['producción'].values())}\n"

    return informe

def main():
    if len(sys.argv) != 4:
        print("Uso: python analizador_plagas.py <zona> <cultivo> <plaga>")
        return

    zona = sys.argv[1]
    cultivo = sys.argv[2]
    plaga = sys.argv[3]

    print(analizador_plagas(zona, cultivo, plaga))

if __name__ == "__main__":
    main()