"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza generador contrato servicios
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_contrato_servicios(fecha_contrato=None, nombre_cliente=None, direccion_cliente=None, monto_contrato=None, tipo_cambio=None, precio_unitario=None):
    # Verificar si se proporcionaron argumentos
    if fecha_contrato is None:
        fecha_contrato = datetime.date.today()
    if nombre_cliente is None:
        nombre_cliente = "Juan Pérez"
    if direccion_cliente is None:
        direccion_cliente = "Calle 123, Colonia Centro, Ciudad de México"
    if monto_contrato is None:
        monto_contrato = 100000.0
    if tipo_cambio is None:
        tipo_cambio = float(sys.argv[2]) if len(sys.argv) > 2 else 20.5
    if precio_unitario is None:
        precio_unitario = float(sys.argv[3]) if len(sys.argv) > 3 else 500.0

    # Verificar si los argumentos son validos
    try:
        fecha_contrato = datetime.datetime.strptime(fecha_contrato, "%Y-%m-%d").date()
        monto_contrato = float(monto_contrato)
        tipo_cambio = float(tipo_cambio)
        precio_unitario = float(precio_unitario)
    except ValueError:
        print("Error: Los argumentos deben ser fechas y números.")
        return

    # Calculo del monto total
    try:
        monto_total = monto_contrato * precio_unitario * tipo_cambio
    except TypeError:
        print("Error: El monto total no se puede calcular debido a un tipo de dato incorrecto.")
        return

    # Generación del contrato
    contrato = {
        "fecha_contrato": fecha_contrato,
        "nombre_cliente": nombre_cliente,
        "direccion_cliente": direccion_cliente,
        "monto_contrato": monto_contrato,
        "tipo_cambio": tipo_cambio,
        "precio_unitario": precio_unitario,
        "monto_total": monto_total
    }

    # Imprimir el contrato
    print("CONTRATO DE SERVICIOS")
    print("---------------------")
    print(f"Fecha de contrato: {contrato['fecha_contrato']}")
    print(f"Nombre del cliente: {contrato['nombre_cliente']}")
    print(f"Dirección del cliente: {contrato['direccion_cliente']}")
    print(f"Monto del contrato: {contrato['monto_contrato']} MXN")
    print(f"Tipo de cambio: {contrato['tipo_cambio']} USD/MXN")
    print(f"Precio unitario: {contrato['precio_unitario']} MXN")
    print(f"Monto total: {contrato['monto_total']} MXN")
    print(f"Importe en USD: {contrato['monto_contrato'] / tipo_cambio} USD")
    print(f"Importe en USD (sin tipo de cambio): {contrato['monto_contrato'] / tipo_cambio * 1.1} USD")
    print(f"Importe en USD (con tipo de cambio): {contrato['monto_contrato'] / tipo_cambio * 0.9} USD")
    print("---------------------")
    print("RESUMEN EJECUTIVO")
    print("---------------------")
    print(f"El contrato tiene un monto total de {contrato['monto_total']} MXN, lo que equivale a {contrato['monto_contrato'] / tipo_cambio} USD.")
    print(f"El tipo de cambio utilizado fue de {contrato['tipo_cambio']} USD/MXN.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("Uso: python generador_contrato_servicios.py <tipo_cambio> <precio_unitario>")
        elif len(sys.argv) > 2:
            generar_contrato_servicios(sys.argv[2], sys.argv[3])
        else:
            print("Error: Faltan argumentos.")
    else:
        generar_contrato_servicios()