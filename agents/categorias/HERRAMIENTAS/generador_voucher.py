"""
ÁREA: TURISMO
DESCRIPCIÓN: Agente que realiza generador voucher
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_voucher(precio=10000.00, fecha_inicio="01/03/2024", fecha_fin="31/03/2024", personas=2):
    try:
        if precio <= 0:
            raise ValueError("Precio debe ser mayor a cero")
        if fecha_inicio >= fecha_fin:
            raise ValueError("Fecha de inicio debe ser antes que la fecha de fin")
        if personas <= 0:
            raise ValueError("Número de personas debe ser mayor a cero")

        voucher = {
            "descripcion": f"Voucher turístico para {personas} personas",
            "precio": f"{precio:.2f} MXN",
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
        }

        # Calculo del IVA en México (16% sobre el precio)
        iva = precio * 0.16
        subtotal = precio - iva
        total = precio + iva

        # Calculo del precio por persona
        precio_por_persona = precio / personas

        # Calculo del número de días entre la fecha de inicio y la fecha de fin
        fecha_inicio_date = datetime.datetime.strptime(fecha_inicio, "%d/%m/%Y")
        fecha_fin_date = datetime.datetime.strptime(fecha_fin, "%d/%m/%Y")
        numero_dias = (fecha_fin_date - fecha_inicio_date).days + 1

        # Calculo del monto diario
        monto_diario = precio / numero_dias

        # Calculo del monto mensual
        monto_mensual = precio * 0.0833  # IVA mensual (16% sobre el precio, dividido por 12)

        # Calculo del porcentaje de aumento por persona
        porcentaje_aumento = (precio_por_persona / precio) * 100

        return voucher, iva, subtotal, total, precio_por_persona, numero_dias, monto_diario, monto_mensual, porcentaje_aumento
    except ValueError as e:
        print(f"Error: {str(e)}")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def main():
    try:
        precio = float(sys.argv[1]) if len(sys.argv) > 1 else 10000.00
        fecha_inicio = sys.argv[2] if len(sys.argv) > 2 else "01/03/2024"
        fecha_fin = sys.argv[3] if len(sys.argv) > 3 else "31/03/2024"
        personas = int(sys.argv[4]) if len(sys.argv) > 4 else 2

        voucher, iva, subtotal, total, precio_por_persona, numero_dias, monto_diario, monto_mensual, porcentaje_aumento = generar_voucher(precio, fecha_inicio, fecha_fin, personas)

        if voucher:
            print("Resumen ejecutivo:")
            print(f"Descripción: {voucher['descripcion']}")
            print(f"Precio: {voucher['precio']}")
            print(f"Fecha de inicio: {voucher['fecha_inicio']}")
            print(f"Fecha de fin: {voucher['fecha_fin']}")
            print(f"IVA: {iva:.2f} MXN")
            print(f"Subtotal: {subtotal:.2f} MXN")
            print(f"Total: {total:.2f} MXN")
            print(f"Precio por persona: {precio_por_persona:.2f} MXN")
            print(f"Número de días: {numero_dias}")
            print(f"Monto diario: {monto_diario:.2f} MXN")
            print(f"Monto mensual: {monto_mensual:.2f} MXN")
            print(f"Porcentaje de aumento por persona: {porcentaje_aumento:.2f}%")
        else:
            print("Error al generar voucher.")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if len(sys.argv) > 0:
            print("Uso: python generador_voucher.py <precio> <fecha_inicio> <fecha_fin> <personas>")

if __name__ == "__main__":
    main()