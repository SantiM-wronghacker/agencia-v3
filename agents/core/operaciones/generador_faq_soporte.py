"""
ÁREA: SOPORTE
DESCRIPCIÓN: Agente que realiza generador faq soporte
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

def extraer_precios(tipo_cambio=None):
    if WEB:
        return web.extraer_precios()
    else:
        if tipo_cambio:
            return {
                "dolar": 19.40,
                "euro": 21.50,
                "peso": 1.00,
                tipo_cambio: 1.00
            }
        else:
            return {
                "dolar": 19.40,
                "euro": 21.50,
                "peso": 1.00
            }

def generar_faq():
    faq = {
        "¿Qué es un FAQ?": "Un FAQ es una lista de preguntas y respuestas que se utilizan para proporcionar información sobre un tema en particular.",
        "¿Cómo puedo acceder a mi cuenta?": "Puedes acceder a tu cuenta ingresando tu nombre de usuario y contraseña en la sección de inicio de sesión.",
        "¿Qué sucede si olvido mi contraseña?": "Si olvidas tu contraseña, puedes recuperarla ingresando tu nombre de usuario y siguiendo las instrucciones que se te presentarán.",
        "¿Cómo puedo cambiar mi contraseña?": "Puedes cambiar tu contraseña ingresando tu nombre de usuario y contraseña actuales, y luego ingresando tu nueva contraseña.",
        "¿Qué es un soporte técnico?": "Un soporte técnico es un equipo de profesionales que se encarga de ayudarte a resolver problemas técnicos relacionados con nuestros productos o servicios.",
        "¿Cómo puedo realizar una reserva?": "Puedes realizar una reserva ingresando tu información de contacto y seleccionando la fecha y hora deseada.",
        "¿Qué es un código de descuento?": "Un código de descuento es un código que puedes utilizar para obtener un descuento en tus compras.",
        "¿Cómo puedo cancelar una reserva?": "Puedes cancelar una reserva ingresando tu información de contacto y seleccionando la reserva que deseas cancelar.",
        "¿Qué es un préstamo?": "Un préstamo es una cantidad de dinero prestada por una institución financiera para ser devuelta con intereses.",
        "¿Cómo puedo calcular el interés de un préstamo?": "Puedes calcular el interés de un préstamo utilizando la fórmula: interés = monto * tasa * tiempo.",
        "¿Qué es la tasa de interés?": "La tasa de interés es el porcentaje de interés que se cobra sobre un préstamo.",
        "¿Cómo puedo calcular el monto de un préstamo?": "Puedes calcular el monto de un préstamo utilizando la fórmula: monto = interés / (tasa * tiempo)."
    }
    return faq

def calcular_interes(tasa, monto, tiempo, tipo_cambio=None):
    try:
        if tipo_cambio:
            return monto * (tasa / 100) * tiempo * tipo_cambio
        else:
            return monto * (tasa / 100) * tiempo
    except ZeroDivisionError:
        return "Error: No se puede dividir por cero."

def main():
    tipo_cambio = sys.argv[1] if len(sys.argv) > 1 else None
    faq = generar_faq()
    precios = extraer_precios(tipo_cambio)
    interes = calcular_interes(10, 1000, 12, tipo_cambio)
    print("ÁREA: SOPORTE")
    print("DESCRIPCIÓN: Agente que realiza generador faq soporte")
    print("TECNOLOGÍA: Python estándar")
    print("Precios de cambio:")
    for tipo, precio in precios.items():
        print(f"{tipo}: {precio}")
    print("FAQ:")
    for pregunta, respuesta in faq.items():
        print(f"{pregunta}: {respuesta}")
    print("Interés de un préstamo:")
    print(f"Interés = {interes}")

if __name__ == "__main__":
    main()