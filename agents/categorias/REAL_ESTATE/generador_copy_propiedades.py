"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Genera variantes de anuncios persuasivos para Facebook e Instagram basados en m2, zona y precio.
TECNOLOGÍA: Python
"""

import sys
import json
import math

def generar_anuncios(m2, zona, precio):
    anuncios = []
    
    anuncio1 = {
        "titulo": f"{m2}m2 en {zona} a un precio inigualable",
        "descripcion": f"¡No te pierdas esta oportunidad de vivir en {zona} con {m2}m2 de espacio! Precio: ${precio:,.2f}. ¡Contáctanos para más información!",
        "llamada_accion": "Contactar ahora",
        "caracteristicas": {
            "m2": m2,
            "zona": zona,
            "precio": precio,
            "precio_m2": precio / m2
        }
    }
    anuncios.append(anuncio1)
    
    anuncio2 = {
        "titulo": f"Vive en el corazón de {zona} a un precio accesible",
        "descripcion": f"¡Descubre la magia de vivir en {zona}! Esta propiedad de {m2}m2 es perfecta para ti. Precio: ${precio:,.2f}. ¡No esperes más!",
        "llamada_accion": "Ver detalles",
        "caracteristicas": {
            "m2": m2,
            "zona": zona,
            "precio": precio,
            "precio_m2": precio / m2
        }
    }
    anuncios.append(anuncio2)
    
    anuncio3 = {
        "titulo": f"Invierte en {zona} con esta propiedad de {m2}m2 a ${precio:,.2f}",
        "descripcion": f"¿Buscas una oportunidad de inversión en {zona}? Esta propiedad de {m2}m2 es ideal. Precio: ${precio:,.2f}. ¡No te arrepentirás!",
        "llamada_accion": "Invertir ahora",
        "caracteristicas": {
            "m2": m2,
            "zona": zona,
            "precio": precio,
            "precio_m2": precio / m2
        }
    }
    anuncios.append(anuncio3)
    
    anuncio4 = {
        "titulo": f"Propiedad en {zona} con {m2}m2 y precio competitivo",
        "descripcion": f"¡No te pierdas esta oportunidad de vivir en {zona} con {m2}m2 de espacio! Precio: ${precio:,.2f}. ¡Contáctanos para más información!",
        "llamada_accion": "Contactar ahora",
        "caracteristicas": {
            "m2": m2,
            "zona": zona,
            "precio": precio,
            "precio_m2": precio / m2
        }
    }
    anuncios.append(anuncio4)
    
    anuncio5 = {
        "titulo": f"{zona}: la mejor zona para vivir con {m2}m2 de espacio",
        "descripcion": f"¡Descubre la magia de vivir en {zona}! Esta propiedad de {m2}m2 es perfecta para ti. Precio: ${precio:,.2f}. ¡No esperes más!",
        "llamada_accion": "Ver detalles",
        "caracteristicas": {
            "m2": m2,
            "zona": zona,
            "precio": precio,
            "precio_m2": precio / m2
        }
    }
    anuncios.append(anuncio5)
    
    return anuncios

def main():
    if len(sys.argv) != 4:
        print("Uso: python generador_copy_propiedades.py <m2> <zona> <precio>")
        sys.exit(1)

    try:
        m2 = int(sys.argv[1])
        zona = sys.argv[2]
        precio = float(sys.argv[3])
    except ValueError:
        print("Error: Los valores de m2 y precio deben ser numéricos.")
        sys.exit(1)

    if m2 <= 0:
        print("Error: El valor de m2 debe ser mayor que cero.")
        sys.exit(1)

    if precio < 0:
        print("Error: El valor de precio no puede ser negativo.")
        sys.exit(1)

    anuncios = generar_anuncios(m2, zona, precio)