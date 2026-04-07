"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza generador copy google ads
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
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def calcular_descuento(precio, descuento):
    """Calcula el descuento aplicado al precio"""
    return precio * descuento

def calcular_precio_original(precio, descuento):
    """Calcula el precio original con descuento"""
    return precio / (1 - descuento)

def generar_copy_google_ads(url=None, texto=None, precio=None, descuento=None):
    try:
        if WEB:
            # Buscar datos reales con web_bridge
            datos = web.buscar("google ads copy")
            texto = web.fetch_texto(datos['url'])
            precios = web.extraer_precios(texto)
        else:
            # Datos de ejemplo hardcodeados como fallback
            if url is None:
                url = 'https://www.example.com/google-ads-copy'
            if texto is None:
                texto = 'Este es un ejemplo de texto para Google Ads'
            if precio is None:
                precio = 1000.00
            if descuento is None:
                descuento = 0.10

        # Generar copy Google Ads
        copy = f"¡Descubre la mejor forma de aumentar tus ventas con nuestros {precio} MXN de descuento exclusivo!\n"
        copy += f"No te pierdas esta oportunidad de {math.ceil(descuento * 100)}% de descuento en nuestros productos.\n"
        copy += f"¡Registra ahora y aprovecha de esta oferta limitada! {datetime.datetime.now().strftime('%Y-%m-%d')}\n"
        copy += f"Oferta válida solo para el mes de {datetime.datetime.now().strftime('%B')} y hasta agotar existencias.\n"
        copy += f"Precio original: {calcular_precio_original(precio, descuento):.2f} MXN. Ahorra {math.ceil((descuento * 100))}%.\n"
        copy += f"La oferta incluye: {random.choice(['servicio de asesoría', 'asesoría de marketing', 'análisis de mercado'])}.\n"
        copy += f"¡No esperes más! Registra ahora y aprovecha de esta oferta exclusiva.\n"
        copy += f"Precio normal: {precio:.2f} MXN. Descuento: {math.ceil(descuento * 100)}%.\n"
        copy += f"Precio final: {precio - (precio * descuento):.2f} MXN.\n"
        copy += f"Oferta válida solo para clientes nuevos. No se aplica a pedidos anteriores.\n"

        # Resumen ejecutivo
        resumen = f"Resumen ejecutivo:\n"
        resumen += f"Oferta: {precio} MXN de descuento exclusivo.\n"
        resumen += f"Descuento: {math.ceil(descuento * 100)}%.\n"
        resumen += f"Precio original: {calcular_precio_original(precio, descuento):.2f} MXN.\n"
        resumen += f"La oferta incluye: {random.choice(['servicio de asesoría', 'asesoría de marketing', 'análisis de mercado'])}.\n"

        return copy + "\n" + resumen

    except Exception as e:
        return f"Error: {str(e)}"

def main():
    if __name__ == "__main__":
        url = sys.argv[1] if len(sys.argv) > 1 else None
        texto = sys.argv[2] if len(sys.argv) > 2 else None
        precio = float(sys.argv[3]) if len(sys.argv) > 3 else None
        descuento = float(sys.argv[4]) if len(sys.argv) > 4 else None

        print(generar_copy_google_ads(url, texto, precio, descuento))

if __name__ == "__main__":
    main()