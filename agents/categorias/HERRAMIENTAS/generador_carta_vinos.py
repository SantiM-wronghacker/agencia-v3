# ÁREA: HERRAMIENTAS
# DESCRIPCIÓN: Agente que realiza generador carta vinos
# TECNOLOGÍA: Python estándar

import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios(porcentaje_iva=0.16):
    # Datos de ejemplo
    return {
        'vino1': {'nombre': 'Vino Rojo', 'precio': 500.0, 'iva': porcentaje_iva},
        'vino2': {'nombre': 'Vino Blanco', 'precio': 300.0, 'iva': porcentaje_iva},
        'vino3': {'nombre': 'Vino Tinto', 'precio': 800.0, 'iva': porcentaje_iva},
        'vino4': {'nombre': 'Vino Rosado', 'precio': 400.0, 'iva': porcentaje_iva},
        'vino5': {'nombre': 'Vino Espumoso', 'precio': 1200.0, 'iva': porcentaje_iva},
        'vino6': {'nombre': 'Vino Verde', 'precio': 600.0, 'iva': porcentaje_iva},
        'vino7': {'nombre': 'Vino Rosé', 'precio': 700.0, 'iva': porcentaje_iva},
        'vino8': {'nombre': 'Vino Blanco Seco', 'precio': 350.0, 'iva': porcentaje_iva},
        'vino9': {'nombre': 'Vino Tinto Intenso', 'precio': 900.0, 'iva': porcentaje_iva},
        'vino10': {'nombre': 'Vino Espumoso Brut', 'precio': 1300.0, 'iva': porcentaje_iva}
    }

def generar_carta_vinos(precios):
    carta = []
    for vino, datos in precios.items():
        precio_bruto = datos['precio'] * (1 + datos['iva'])
        precio_netos = precio_bruto * 0.8  # 20% descuento
        carta.append(f'{datos["nombre"]}: ${precio_bruto:.2f} MXN (IVA incluido)')
        carta.append(f'Precio neto: ${precio_netos:.2f} MXN (20% descuento)')
        carta.append(f'Porcentaje de IVA: {datos["iva"]*100}%')
        carta.append(f'Precio sin IVA: ${datos["precio"]:.2f} MXN')
    return carta

def calcular_total(precios):
    total_bruto = sum(precio['precio'] * (1 + precio['iva']) for precio in precios.values())
    total_netos = total_bruto * 0.8  # 20% descuento
    return total_bruto, total_netos

def calcular_iva_total(precios):
    iva_total = sum(precio['precio'] * precio['iva'] for precio in precios.values())
    return iva_total

def calcular_descuento_total(precios):
    descuento_total = sum(precio['precio'] * 0.2 for precio in precios.values())
    return descuento_total

def main():
    try:
        if len(sys.argv) > 1:
            porcentaje_iva = float(sys.argv[1])
        else:
            porcentaje_iva = 0.16
        precios = extraer_precios(porcentaje_iva=porcentaje_iva)
        carta = generar_carta_vinos(precios)
        total_bruto, total_netos = calcular_total(precios)
        iva_total = calcular_iva_total(precios)
        descuento_total = calcular_descuento_total(precios)
        print('**Carta de Vinos**')
        for vino in carta:
            print(vino)
        print(f'Total bruto: ${total_bruto:.2f} MXN')
        print(f'Total neto: ${total_netos:.2f} MXN')
        print(f'IVA total: ${iva_total:.2f} MXN')
        print(f'Descuento total: ${descuento_total:.2f} MXN')
        print(f'Resumen ejecutivo: La carta de vinos incluye 10 opciones con un total bruto de ${total_bruto:.2f} MXN, un total neto de ${total_netos:.2f} MXN, un IVA total de ${iva_total:.2f} MXN y un descuento total de ${descuento_total:.2f} MXN.')
    except ValueError:
        print