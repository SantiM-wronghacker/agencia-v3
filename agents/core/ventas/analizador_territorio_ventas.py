#!/usr/bin/env python3
"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza analizador territorio ventas
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def analizador_territorio_ventas():
    try:
        datos = {
            "ciudad": "México D.F.",
            "region": "Centro",
            "ventas": 1000000,
            "precios": {
                "producto1": 500,
                "producto2": 200,
                "producto3": 300,
                "producto4": 400
            }
        }
        texto = "Texto de ejemplo"

        if len(sys.argv) > 1:
            datos["ciudad"] = sys.argv[1]
            datos["region"] = sys.argv[2]
            datos["ventas"] = int(sys.argv[3])
            datos["precios"] = {
                "producto1": int(sys.argv[4]),
                "producto2": int(sys.argv[5]),
                "producto3": int(sys.argv[6]),
                "producto4": int(sys.argv[7])
            }

        total_ventas = datos["ventas"]
        promedio_precio = sum(datos["precios"].values()) / len(datos["precios"])
        max_precio = max(datos["precios"].values())
        min_precio = min(datos["precios"].values())
        total_precios = sum(datos["precios"].values())
        cantidad_productos = len(datos["precios"])
        porcentaje_utilidad = (promedio_precio * 0.25)
        utilidad_total = total_ventas * porcentaje_utilidad
        gastos_operativos = 100000
        beneficio_neto = total_ventas - gastos_operativos - utilidad_total

        # Imprimir resultados
        print(f"ÁREA: VENTAS")
        print(f"DESCRIPCIÓN: Agente que realiza analizador territorio ventas")
        print(f"TECNOLOGÍA: Python estándar")
        print(f"\nTotal de ventas: {total_ventas:,.2f} MXN")
        print(f"Promedio de precio: {promedio_precio:,.2f} MXN")
        print(f"Máximo de precio: {max_precio:,.2f} MXN")
        print(f"Mínimo de precio: {min_precio:,.2f} MXN")
        print(f"Total de precios: {total_precios:,.2f} MXN")
        print(f"Cantidad de productos: {cantidad_productos}")
        print(f"Texto: {texto}")
        print(f"Fecha actual: {datetime.date.today()}")
        print(f"Random: {random.randint(1, 100)}")
        print(f"Porcentaje de utilidad: {porcentaje_utilidad*100:.2f}%")
        print(f"Utilidad total: {utilidad_total:,.2f} MXN")
        print(f"Gastos operativos: {gastos_operativos:,.2f} MXN")
        print(f"Beneficio neto: {beneficio_neto:,.2f} MXN")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El análisis de las ventas en {datos['ciudad']} en la región {datos['region']} muestra que el total de ventas es de {total_ventas:,.2f} MXN, con un promedio de precio de {promedio_precio:,.2f} MXN.")
        print(f"Se estima que la utilidad total es de {utilidad_total:,.2f} MXN, lo que representa un porcentaje de utilidad de {porcentaje_utilidad*100:.2f}%.")
        print(f"El beneficio neto es de {beneficio_neto:,.2f} MXN, después de considerar los gastos operativos de {gastos_operativos:,.2f} MXN.")

    except IndexError:
        print("Faltan argumentos de entrada")
    except ValueError:
        print("Error de valor")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    analizador_territorio_ventas()