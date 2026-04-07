"""
ÁREA: LOGISTICA
DESCRIPCIÓN: Agente que realiza tracker inventario
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def obtener_precios(precios=None):
    if precios is None:
        precios = {
            'producto1': 100.00,
            'producto2': 200.00,
            'producto3': 300.00
        }
    return precios

def calcular_inventario(precios, inventario):
    total = 0
    for producto, cantidad in inventario.items():
        total += cantidad * precios[producto]
    return total

def calcular_costo_unitario(precios, inventario):
    return calcular_inventario(precios, inventario) / sum(inventario.values())

def calcular_utilidad(inventario, precios):
    return calcular_inventario(precios, inventario) - sum(inventario.values()) * 10.00

def main():
    try:
        if len(sys.argv) > 1:
            precios = json.loads(sys.argv[1])
        else:
            precios = obtener_precios()
        
        if 'producto1' not in precios or 'producto2' not in precios or 'producto3' not in precios:
            raise ValueError("Precios deben tener los productos 'producto1', 'producto2' y 'producto3'")
        
        if len(sys.argv) > 2:
            inventario = json.loads(sys.argv[2])
        else:
            inventario = {
                'producto1': 100,
                'producto2': 200,
                'producto3': 300
            }
        
        if 'producto1' not in inventario or 'producto2' not in inventario or 'producto3' not in inventario:
            raise ValueError("Inventario debe tener los productos 'producto1', 'producto2' y 'producto3'")
        
        total = calcular_inventario(precios, inventario)
        costo_unitario = calcular_costo_unitario(precios, inventario)
        utilidad = calcular_utilidad(inventario, precios)
        
        print(f"Inventario total: {total:.2f} MXN")
        print(f"Productos: {', '.join(precios.keys())}")
        print(f"Cantidad de productos: {', '.join(map(str, [inventario['producto1'], inventario['producto2'], inventario['producto3']]))}")
        print(f"Valor de cada producto: {', '.join(map(str, [precios['producto1'], precios['producto2'], precios['producto3']]))}")
        print(f"Fecha y hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Random número: {random.randint(0, 100)}")
        print(f"Costo unitario: {costo_unitario:.2f} MXN")
        print(f"Utilidad: {utilidad:.2f} MXN")
        print("Resumen ejecutivo:")
        print(f"Inventario total: {total:.2f} MXN")
        print(f"Costo unitario: {costo_unitario:.2f} MXN")
        print(f"Utilidad: {utilidad:.2f} MXN")
    except json.JSONDecodeError:
        print("Error al leer los precios o el inventario. Por favor, asegúrese de que sean formatos JSON válidos.")
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].startswith('{') and sys.argv[1].endswith('}'):
        main()
    else:
        print("Por favor, proporcione los precios y el inventario como argumentos de la línea de comandos en formato JSON.")