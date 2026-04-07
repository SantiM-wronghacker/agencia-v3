"""
ÁREA: LEGAL
DESCRIPCIÓN: Agente que realiza validador cfdi
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def calcular_iva(total):
    try:
        iva = total * 0.16
        return iva
    except Exception as e:
        print(f"Error al calcular IVA: {str(e)}")
        return 0.0

def calcular_isr(total):
    try:
        isr = total * 0.10
        return isr
    except Exception as e:
        print(f"Error al calcular ISR: {str(e)}")
        return 0.0

def calcular_total_con_impuestos(total):
    try:
        iva = calcular_iva(total)
        isr = calcular_isr(total)
        total_con_impuestos = total + iva + isr
        return total_con_impuestos
    except Exception as e:
        print(f"Error al calcular total con impuestos: {str(e)}")
        return 0.0

def calcular_descuento(total, porcentaje):
    try:
        descuento = total * (porcentaje / 100)
        return descuento
    except Exception as e:
        print(f"Error al calcular descuento: {str(e)}")
        return 0.0

def calcular_subtotal(total, descuento):
    try:
        subtotal = total - descuento
        return subtotal
    except Exception as e:
        print(f"Error al calcular subtotal: {str(e)}")
        return 0.0

def main():
    try:
        if len(sys.argv) > 1:
            fecha = sys.argv[1]
            total = float(sys.argv[2])
            emisor = sys.argv[3]
            receptor = sys.argv[4]
            tipo_cambio = float(sys.argv[5])
            descuento_porcentaje = float(sys.argv[6])
        else:
            fecha = "2022-01-01"
            total = 1000.0
            emisor = "Empresa Ejemplo"
            receptor = "Cliente Ejemplo"
            tipo_cambio = 20.0
            descuento_porcentaje = 5.0

        noticias = "No hay noticias disponibles"

        print("Validador CFDI")
        print("----------------")
        print(f"Fecha: {fecha}")
        print(f"Total: ${total:.2f} MXN")
        print(f"Tipo de cambio: 1 USD = {tipo_cambio:.2f} MXN")
        print(f"Noticias: {noticias}")
        print(f"Emisor: {emisor}")
        print(f"Receptor: {receptor}")
        print(f"Descuento ({descuento_porcentaje}%): ${calcular_descuento(total, descuento_porcentaje):.2f} MXN")
        print(f"Subtotal: ${calcular_subtotal(total, calcular_descuento(total, descuento_porcentaje)):.2f} MXN")
        print(f"IVA (16%): ${calcular_iva(total):.2f} MXN")
        print(f"ISR (10%): ${calcular_isr(total):.2f} MXN")
        print(f"Total con impuestos: ${calcular_total_con_impuestos(total):.2f} MXN")
        print(f"Total con impuestos y descuento: ${calcular_total_con_impuestos(calcular_subtotal(total, calcular_descuento(total, descuento_porcentaje))):.2f} MXN")

        print("\nResumen Ejecutivo:")
        print("--------------------")
        print(f"El total de la factura es de ${total:.2f} MXN.")
        print(f"El monto total con impuestos es de ${calcular_total_con_impuestos(total):.2f} MXN.")
        print(f"El monto total con impuestos y descuento es de ${calcular_total_con_impuestos(calcular_subtotal(total, calcular_descuento(total, descuento_porcentaje))):.2f} MXN.")
        print(f"El descuento aplicado es de {descuento_porcentaje}%.")
        print(f"El tipo de cambio utilizado es de 1 USD = {tipo_cambio:.2f} MXN.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()