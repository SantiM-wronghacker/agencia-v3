"""
ÁREA: ECOMMERCE
DESCRIPCIÓN: Agente que realiza generador faq producto
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def extraer_precios(tipo_moneda="MXN"):
    if WEB:
        precios = web.extraer_precios()
    else:
        # Precios realistas para México
        precio_unitario = 100.00
        precio_total = 1000.00
        descuento = 10.00
        if tipo_moneda == "USD":
            # Conversión aproximada al tipo de cambio actual
            tipo_cambio = 20.00
            precio_unitario_usd = precio_unitario / tipo_cambio
            precio_total_usd = precio_total / tipo_cambio
            descuento_usd = descuento / tipo_cambio
            return {
                "precio_unitario": precio_unitario_usd,
                "precio_total": precio_total_usd,
                "descuento": descuento_usd
            }
        return {
            "precio_unitario": precio_unitario,
            "precio_total": precio_total,
            "descuento": descuento
        }
    return precios

def generar_faq_producto(tipo_moneda="MXN"):
    try:
        faq = {
            "pregunta1": "¿Cuál es el precio del producto?",
            "respuesta1": "El precio del producto es ${:.2f} {}".format(extraer_precios(tipo_moneda)["precio_unitario"], tipo_moneda),
            "pregunta2": "¿Cuál es el descuento disponible?",
            "respuesta2": "El descuento disponible es de ${:.2f} {}".format(extraer_precios(tipo_moneda)["descuento"], tipo_moneda),
            "pregunta3": "¿Cuál es el precio total con descuento?",
            "respuesta3": "El precio total con descuento es ${:.2f} {}".format(extraer_precios(tipo_moneda)["precio_total"], tipo_moneda),
            "pregunta4": "¿Cuál es el tipo de cambio actual?",
            "respuesta4": "El tipo de cambio actual es de 1 {} = {:.2f} USD".format(tipo_moneda, extraer_precios(tipo_moneda)["precio_unitario"] / 20.00),
            "pregunta5": "¿Cuál es el monto del impuesto?",
            "respuesta5": "El monto del impuesto es de {:.2f}% del precio total".format(random.uniform(10.0, 20.0)),
            "pregunta6": "¿Cuál es el tiempo de entrega?",
            "respuesta6": "El tiempo de entrega es de {:.2f} días hábiles".format(random.uniform(5.0, 15.0)),
            "pregunta7": "¿Cuál es el método de pago disponible?",
            "respuesta7": "Los métodos de pago disponibles son: PayPal, Tarjeta de Crédito, Transferencia Bancaria",
            "pregunta8": "¿Cuál es el proceso de devolución?",
            "respuesta8": "El proceso de devolución es el siguiente: 1. Contactar con el servicio al cliente, 2. Devolver el producto en su estado original, 3. Recibir el reembolso"
        }
        return faq
    except Exception as e:
        return {"error": str(e)}

def main():
    if len(sys.argv) > 1:
        tipo_moneda = sys.argv[1]
    else:
        tipo_moneda = "MXN"

    faq = generar_faq_producto(tipo_moneda)
    print("ÁREA: ECOMMERCE")
    print("DESCRIPCIÓN: Agente que realiza generador faq producto")
    print("TECNOLOGÍA: Python estándar")
    print("Tipo de moneda: {}".format(tipo_moneda))
    print("FAQ del producto:")
    for pregunta, respuesta in faq.items():
        print("{}: {}".format(pregunta, respuesta))
    print("\nResumen ejecutivo:")
    print("El producto ofrece un precio competitivo y un proceso de devolución claro y fácil de seguir.")

if __name__ == "__main__":
    main()