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

    # Verificar si zona existe en la base de datos
    if zona not in datos['zonas']:
        print("Zona no encontrada.")
        return

    # Verificar si plaga existe en la base de datos
    if plaga not in datos['plagas']:
        print("Plaga no encontrada.")
        return

    # Analiza datos y genera informe
    informe = f"Informe de plagas para {cultivo} en {zona} el {fecha}:\n"
    informe += f"Plagas detectadas: {', '.join(datos['plagas'])}\n"
    informe += f"Precio de {cultivo}: ${datos['precios'][cultivo]:.2f}\n"
    informe += f"Producción de {cultivo}: {datos['producción'][cultivo]:.2f} unidades\n"
    informe += f"Consumo de {cultivo}: {datos['consumo'][cultivo]:.2f} unidades\n"
    informe += f"Ventas de {cultivo}: ${datos['ventas'][cultivo]:.2f}\n"
    informe += f"Índice de producción: {(datos['producción'][cultivo] / datos['consumo'][cultivo] * 100):.2f}%\n"
    informe += f"Índice de ventas: {(datos['ventas'][cultivo] / datos['producción'][cultivo] * 100):.2f}%\n"
    informe += f"Índice de rentabilidad: {((datos['ventas'][cultivo] - datos['precios'][cultivo] * datos['producción'][cultivo]) / datos['ventas'][cultivo] * 100):.2f}%\n"
    informe += f"Margen de ganancia: {((datos['ventas'][cultivo] - datos['precios'][cultivo] * datos['producción'][cultivo]) / datos['ventas'][cultivo] * 100):.2f}%\n"
    informe += f"Costo de producción: ${datos['precios'][cultivo] * datos['producción'][cultivo]:.2f}\n"
    informe += f"Beneficio neto: ${datos['ventas'][cultivo] - datos['precios'][cultivo] * datos['producción'][cultivo]:.2f}\n"
    informe += f"Utilidad por unidad: ${(datos['ventas'][cultivo] - datos['precios'][cultivo] * datos['producción'][cultivo]) / datos['producción'][cultivo]:.2f}\n"
    informe += f"Costo de control de plagas: ${datos['costo_control_plagas'][plaga]:.2f}\n"
    informe += f"Beneficio neto después de control de plagas: ${datos['ventas'][cultivo] - datos['precios'][cultivo] * datos['producción'][cultivo] - datos['costo_control_plagas'][plaga]:.2f}\n"

    # Resumen ejecutivo
    informe += "\nResumen ejecutivo:\n"
    informe += f"La producción de {cultivo} en {zona} ha sido afectada por la plaga {plaga}.\n"
    informe += f"El beneficio neto después de controlar la plaga es de ${datos['ventas'][cultivo] - datos['precios'][cultivo] * datos['producción'][cultivo] - datos['costo_control_plagas'][plaga]:.2f}.\n"
    informe += f"Se recomienda tomar medidas para controlar la plaga y reducir el costo de producción.\n"