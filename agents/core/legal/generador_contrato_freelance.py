"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza generador contrato freelance
TECNOLOGÍA: Python estándar
"""

import os
import sys
from datetime import datetime
import math
import re
import random

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def generar_contrato(nombre_cliente, nombre_freelance, fecha_inicio, fecha_fin, monto_total, descuento, iva):
    try:
        # Calculo del subtotal y total
        subtotal = monto_total - (monto_total * descuento)
        total = subtotal + (subtotal * iva)

        # Verificar si el descuento es válido
        if descuento < 0 or descuento > 1:
            raise ValueError("Descuento no válido")

        # Verificar si el IVA es válido
        if iva < 0 or iva > 1:
            raise ValueError("IVA no válido")

        # Verificar si el monto total es válido
        if monto_total <= 0:
            raise ValueError("Monto total no válido")

        # Verificar si la fecha de inicio es anterior a la fecha de fin
        if datetime.strptime(fecha_inicio, "%Y-%m-%d") >= datetime.strptime(fecha_fin, "%Y-%m-%d"):
            raise ValueError("Fecha de inicio no puede ser igual o posterior a la fecha de fin")

        # Obtener el precio unitario desde la API si se tiene conexión
        if WEB:
            try:
                precios = web.extraer_precios()
                if precios:
                    total = float(precios["precio_unitario"]) * subtotal
                else:
                    print("No se pudo obtener el precio unitario")
            except Exception as e:
                print(f"Error: {str(e)}")

        # Imprimir el contrato
        print(f"CONTRATO DE FREELANCE")
        print(f"---------------------")
        print(f"Nombre del cliente: {nombre_cliente}")
        print(f"Nombre del freelance: {nombre_freelance}")
        print(f"Fecha de inicio: {fecha_inicio}")
        print(f"Fecha de fin: {fecha_fin}")
        print(f"Monto total: {monto_total:.2f} MXN")
        print(f"Descuento: {descuento*100:.2f}%")
        print(f"Subtotal: {subtotal:.2f} MXN")
        print(f"IVA (16%): {iva*100:.2f}%")
        print(f"Total: {total:.2f} MXN")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El contrato de freelance tiene un monto total de {monto_total:.2f} MXN y un descuento del {descuento*100:.2f}%.")
        print(f"El subtotal es de {subtotal:.2f} MXN y el IVA es del {iva*100:.2f}%.")
        print(f"El total a pagar es de {total:.2f} MXN.")

        # Impuestos adicionales
        print("\nImpuestos Adicionales:")
        print(f"El IVA es del {iva*100:.2f}% y el subtotal es de {subtotal:.2f} MXN.")
        print(f"El total a pagar es de {total:.2f} MXN.")

        # Plazo de pago
        print("\nPlazo de Pago:")
        print(f"El plazo de pago es de 30 días hábiles a partir de la fecha de inicio del contrato.")
        print(f"El pago debe ser realizado en efectivo o mediante transferencia bancaria.")

    except ValueError as e:
        print(f"Error: {str(e)}")

def main():
    if len(sys.argv) != 7:
        print("Error: Faltan argumentos. Utilice: python generador_contrato_freelance.py <nombre_cliente> <nombre_freelance> <fecha_inicio> <fecha_fin> <monto_total> <descuento> <iva>")
        sys.exit(1)

    nombre_cliente = sys.argv[1]
    nombre_freelance = sys.argv[2]
    fecha_inicio = sys.argv[3]
    fecha_fin = sys.argv[4]
    monto_total = float(sys.argv[5])
    descuento = float(sys.argv[6])
    iva = float(sys.argv[7])

    generar_contrato(nombre_cliente, nombre_freelance, fecha_inicio, fecha_fin, monto_total, descuento, iva)

if __name__ == "__main__":
    main()