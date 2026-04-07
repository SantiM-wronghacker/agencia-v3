"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza chatbot faq
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

def extraer_precios(dolar=20.50, euro=22.80, peso=1.00, fuente='banco', fecha=None):
    if WEB:
        return web.extraer_precios()
    else:
        if fecha is None:
            fecha = datetime.date.today()
        if fuente == 'banco':
            return {
                "dólar": 20.50,
                "euro": 22.80,
                "peso": 1.00
            }
        elif fuente == 'api':
            return {
                "dólar": 21.20,
                "euro": 23.50,
                "peso": 0.95
            }
        else:
            return {
                "dólar": 0.0,
                "euro": 0.0,
                "peso": 0.0
            }

def buscar_datos(preguntas=["¿Qué es Agencia Santi?", "¿Cómo puedo registrarme en Agencia Santi?", "¿Qué beneficios ofrece Agencia Santi?"]):
    if WEB:
        return web.buscar("preguntas frecuentes")
    else:
        return preguntas

def fetch_texto(url="https://www.agenciasanti.com.mx"):
    if WEB:
        return web.fetch_texto(url)
    else:
        return "Bienvenido a Agencia Santi, su agencia de viajes y turismo."

def calcular_cambio(precio_dolar, tipo_cambio):
    return precio_dolar * tipo_cambio

def main():
    try:
        print("Área: Herramientas")
        print("Descripción: Agente que realiza chatbot faq")
        print("Tecnología: Python estándar")
        
        print("Fecha y hora actual:", datetime.datetime.now())
        
        print("Precios actuales:")
        print("Dólar:", extraer_precios()["dólar"])
        print("Euro:", extraer_precios()["euro"])
        print("Peso:", extraer_precios()["peso"])
        
        tipo_cambio = extraer_precios()["dólar"]
        print("Tipo de cambio actual (MXN/USD):", tipo_cambio)
        print("Valor de 100 dólares en pesos mexicanos:", calcular_cambio(100, tipo_cambio))
        
        print("Preguntas frecuentes:")
        for pregunta in buscar_datos():
            print(pregunta)
        
        print("Información adicional:")
        print("Dirección:", fetch_texto())
        print("Teléfono:", "01 800 123 4567")
        print("Correo electrónico:", "info@agenciasanti.com.mx")
        
        print("Resumen ejecutivo:")
        print("El chatbot de Agencia Santi ofrece información sobre precios de divisas, preguntas frecuentes y detalles de contacto.")
        
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--dolar":
            print("Precio del dólar:", extraer_precios(dolar=float(sys.argv[2])))
        elif sys.argv[1] == "--euro":
            print("Precio del euro:", extraer_precios(euro=float(sys.argv[2])))
        elif sys.argv[1] == "--peso":
            print("Precio del peso:", extraer_precios(peso=float(sys.argv[2])))
    else:
        main()