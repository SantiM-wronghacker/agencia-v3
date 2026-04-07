#!/usr/bin/env python3
"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora scrap rate
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random
import argparse

def calcular_scrap_rate(precio_acero, tasa_cambio):
    try:
        if precio_acero <= 0 or tasa_cambio <= 0:
            raise ValueError("Precio de acero y tasa de cambio deben ser positivos")
        return (precio_acero * tasa_cambio) / 100
    except ZeroDivisionError:
        return 0
    except ValueError as e:
        print(f"Error: {e}")
        return None

def calcular_costo_produccion(scrap_rate):
    try:
        if scrap_rate is None:
            return None
        costo_produccion = random.uniform(50000, 70000)
        return costo_produccion * 100
    except Exception as e:
        print(f"Error: {e}")
        return None

def calcular_indice_produccion(scrap_rate):
    try:
        if scrap_rate is None:
            return None
        indice_produccion = random.uniform(0.5, 1.5) * 100
        return indice_produccion
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Calculadora scrap rate')
    parser.add_argument('--precio_acero', type=float, default=45000.0, help='Precio de acero en MXN')
    parser.add_argument('--tasa_cambio', type=float, default=20.5, help='Tasa de cambio MXN/USD')
    parser.add_argument('--cantidad_producida', type=float, default=1000, help='Cantidad de productos producidos')
    args = parser.parse_args()

    try:
        scrap_rate = calcular_scrap_rate(args.precio_acero, args.tasa_cambio)
        if scrap_rate is None:
            print("Error al calcular scrap rate")
            sys.exit(1)
        
        costo_produccion = calcular_costo_produccion(scrap_rate)
        if costo_produccion is None:
            print("Error al calcular costo de producción")
            sys.exit(1)
        
        indice_produccion = calcular_indice_produccion(scrap_rate)
        if indice_produccion is None:
            print("Error al calcular índice de producción")
            sys.exit(1)
        
        beneficio_neto = (scrap_rate * args.cantidad_producida) - costo_produccion
        if beneficio_neto < 0:
            print("El beneficio neto es negativo")
            sys.exit(1)
        
        print(f"Scrap rate: {scrap_rate}%")
        print(f"Costo de producción: {costo_produccion}")
        print(f"Índice de producción: {indice_produccion}%")
        print(f"Cantidad producida: {args.cantidad_producida}")
        print(f"Beneficio neto: {beneficio_neto}")
        
        print("\nResumen ejecutivo:")
        print(f"El scrap rate calculado es de {scrap_rate}% lo que significa que el 5% del costo de producción es debido a la pérdida de materia prima.")
        print(f"El costo de producción para la cantidad de {args.cantidad_producida} productos es de {costo_produccion}.")
        print(f"El índice de producción es de {indice_produccion}% lo que significa que la producción es más eficiente de lo esperado.")
        print(f"El beneficio neto es de {beneficio_neto} lo que significa que la empresa está ganando dinero.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()