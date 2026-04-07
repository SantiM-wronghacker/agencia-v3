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

def extraer_precios(porcentaje_iva=0.16, cantidad_vinos=10):
    # Datos de ejemplo
    return {
        f'vino{i}': {'nombre': f'Vino Rojo {i}', 'precio': round(random.uniform(300, 1500), 2), 'iva': porcentaje_iva}
        for i in range(1, cantidad_vinos + 1)
    }

def generar_carta_vinos(precios):
    carta = []
    for vino, datos in precios.items():
        try:
            precio_bruto = datos['precio'] * (1 + datos['iva'])
            precio_netos = precio_bruto * 0.8  # 20% descuento
            carta.append(f'{datos["nombre"]}: ${precio_bruto:.2f} MXN (IVA incluido)')
            carta.append(f'Precio neto: ${precio_netos:.2f} MXN (20% descuento)')
            carta.append(f'Porcentaje de IVA: {datos["iva"]*100}%')
            carta.append(f'Precio sin IVA: ${datos["precio"]:.2f} MXN')
        except Exception as e:
            carta.append(f'Error al calcular precio de {datos["nombre"]}: {str(e)}')
    return carta

def calcular_total(precios):
    try:
        total_bruto = sum(precio['precio'] * (1 + precio['iva']) for precio in precios.values())
        total_netos = total_bruto * 0.8  # 20% descuento
        return total_bruto, total_netos
    except Exception as e:
        return None, None

def calcular_iva_total(precios):
    try:
        iva_total = sum(precio['precio'] * precio['iva'] for precio in precios.values())
        return iva_total
    except Exception as e:
        return None

def calcular_descuento_total(precios):
    try:
        total_bruto, _ = calcular_total(precios)
        return total_bruto * 0.2  # 20% descuento
    except Exception as e:
        return None

def generar_resumen_ejecutivo(total_bruto, total_netos, iva_total, descuento_total):
    resumen = f'Resumen ejecutivo:\n'
    resumen += f'Total bruto: ${total_bruto:.2f} MXN\n'
    resumen += f'Total neto: ${total_netos:.2f} MXN\n'
    resumen += f'IVA total: ${iva_total:.2f} MXN\n'
    resumen += f'Descuento total: ${descuento_total:.2f} MXN\n'
    return resumen

def main():
    if len(sys.argv) > 1:
        cantidad_vinos = int(sys.argv[1])
        porcentaje_iva = float(sys.argv[2])
    else:
        cantidad_vinos = 10
        porcentaje_iva = 0.16

    precios = extraer_precios(porcentaje_iva=porcentaje_iva, cantidad_vinos=cantidad_vinos)
    carta = generar_carta_vinos(precios)
    total_bruto, total_netos = calcular_total(precios)
    iva_total = calcular_iva_total(precios)
    descuento_total = calcular_descuento_total(precios)
    resumen = generar_resumen_ejecutivo(total_bruto, total_netos, iva_total, descuento_total)

    print('ÁREA: HERRAMIENTAS')
    print('DESCRIPCIÓN: Agente que realiza generador carta vinos')
    print('TECNOLOGÍA: Python estándar')
    print('\nDatos de precios:')
    for vino, datos in precios.items():
        print(f'{vino}: {datos}')
    print('\nCarta de vinos:')
    for linea in carta:
        print(linea)
    print('\nResumen ejecutivo:')
    print(resumen)

if __name__ == "__main__":
    main()