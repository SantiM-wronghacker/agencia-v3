"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza generador caso exito
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
from datetime import datetime
import math
import re
import random

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def generador_caso_exito(cliente=None, producto=None, precio=None, cantidad=None, fecha=None):
    if cliente is None:
        cliente = "Juan Pérez"
    if producto is None:
        producto = "Laptop HP"
    if precio is None:
        precio = 15000
    if cantidad is None:
        cantidad = 2
    if fecha is None:
        fecha = datetime.now().strftime("%Y-%m-%d")

    if WEB:
        try:
            # Buscar precio actual del producto
            precio_actual = web.buscar(producto)
            # Extraer precio actual
            precio_actual = web.extraer_precios(precio_actual)
            # Generar caso de éxito con datos reales
            print(f"ÁREA: VENTAS")
            print(f"DESCRIPCIÓN: {cliente} compró {cantidad} unidades de {producto} por ${precio_actual:.2f} MXN")
            print(f"FECHA: {fecha}")
            print(f"CLIENTE: {cliente}")
            print(f"PRODUCTO: {producto}")
            print(f"PAGO: ${precio_actual * cantidad:.2f} MXN")
            print(f"DESCUENTO: {random.uniform(0, 10)}%")
            print(f"IMPUESTO: {random.uniform(0, 15)}%")
            print(f"TOTAL: ${precio_actual * cantidad * (1 + random.uniform(0.15, 0.20)) * (1 - random.uniform(0.05, 0.10)):.2f} MXN")
            print(f"FORMA DE PAGO: Tarjeta de crédito")
            print(f"METODO DE ENVÍO: Envío estándar")
            print(f"TIPO DE ENVÍO: DHL")
            print(f"FECHA DE ENTREGA: {datetime.now().strftime('%Y-%m-%d') + ' 2 días'}")
            print(f"VALOR DE ENVÍO: ${random.uniform(500, 1000):.2f} MXN")
            print(f"DESCUENTO DE ENVÍO: {random.uniform(0, 10)}%")
            print(f"TOTAL CON ENVÍO: ${precio_actual * cantidad * (1 + random.uniform(0.15, 0.20)) * (1 - random.uniform(0.05, 0.10)) + random.uniform(500, 1000) * (1 - random.uniform(0, 0.10)):.2f} MXN")
        except Exception as e:
            print(f"Error: {e}")
    else:
        try:
            # Generar caso de éxito con datos de ejemplo
            print(f"ÁREA: VENTAS")
            print(f"DESCRIPCIÓN: {cliente} compró {cantidad} unidades de {producto} por ${precio:.2f} MXN")
            print(f"FECHA: {fecha}")
            print(f"CLIENTE: {cliente}")
            print(f"PRODUCTO: {producto}")
            print(f"PAGO: ${precio * cantidad:.2f} MXN")
            print(f"DESCUENTO: 5%")
            print(f"IMPUESTO: 16%")
            print(f"TOTAL: ${(precio * cantidad * 1.16) * (1 - 0.05):.2f} MXN")
            print(f"FORMA DE PAGO: Efectivo")
            print(f"METODO DE ENVÍO: Envío estándar")
            print(f"TIPO DE ENVÍO: DHL")
            print(f"FECHA DE ENTREGA: {datetime.now().strftime('%Y-%m-%d') + ' 2 días'}")
            print(f"VALOR DE ENVÍO: ${random.uniform(500, 1000):.2f} MXN")
            print(f"DESCUENTO DE ENVÍO: 5%")
            print(f"TOTAL CON ENVÍO: ${(precio * cantidad * 1.16) * (1 - 0.05) + random.uniform(500, 1000) * (1 - 0.05):.2f} MXN")
        except Exception as e:
            print