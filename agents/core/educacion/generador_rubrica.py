"""
ÁREA: EDUCACION
DESCRIPCION: Agente que realiza generador rubrica
TECNOLOGIA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def calcular_precio_pension():
    # Precio de la pensión en México (en pesos mexicanos)
    precio_pension = 10_000.0
    # Tasa de inflación anual (en porcentaje)
    tasa_inflacion = 3.5
    # Tipo de cambio actual (en pesos mexicanos por dólar estadounidense)
    tipo_de_cambio = 20.0
    # Calcula el precio de la pensión con la tasa de inflación y el tipo de cambio
    precio_pension_inflacion = precio_pension * (1 + tasa_inflacion / 100)
    precio_pension_dolares = precio_pension_inflacion / tipo_de_cambio
    return precio_pension_dolares

def calcular_tipodecambio():
    # Tipo de cambio actual (en pesos mexicanos por dólar estadounidense)
    tipo_de_cambio = 20.0
    # Tasa de cambio diario (en porcentaje)
    tasa_cambio_diario = 0.5
    # Calcula el tipo de cambio con la tasa de cambio diario
    tipo_de_cambio_diario = tipo_de_cambio * (1 + tasa_cambio_diario / 100)
    return tipo_de_cambio_diario

def generar_rubrica(precio_pension, tipo_de_cambio, noticias):
    try:
        # Generar rubrica con datos reales o de ejemplo
        rubrica = {
            "Área": "Educación",
            "Precio de la pensión": precio_pension,
            "Tipo de cambio": tipo_de_cambio,
            "Noticias económicas": noticias
        }

        # Imprimir rubrica en formato JSON
        print(json.dumps(rubrica, indent=4))

        # Imprimir datos adicionales con formato específico
        print(f"Precio de la pensión: ${precio_pension:.2f} USD")
        print(f"Tipo de cambio: 1 USD = {tipo_de_cambio:.2f} MXN")
        print("Noticias económicas:")
        for noticia in noticias:
            print(f"- {noticia}")

        # Imprimir datos adicionales
        print(f"Índice de inflación anual: 3.5%")
        print(f"Índice de cambio diario: 0.5%")

        # Imprimir resumen ejecutivo
        print("\nResumen ejecutivo:")
        print("El precio de la pensión en México es de $10,000.00 USD, con un tipo de cambio de 20.00 MXN/USD. Las noticias económicas incluyen:")
        for noticia in noticias:
            print(f"- {noticia}")
        print("Se espera un índice de inflación anual de 3.5% y un índice de cambio diario de 0.5%.")

    except Exception as e:
        print(f"Error: {e}")

def main():
    try:
        # Obtener parámetros por sys.argv
        if len(sys.argv) > 1:
            precio_pension = float(sys.argv[1])
            tipo_de_cambio = float(sys.argv[2])
            noticias = sys.argv[3:]
        else:
            # Datos de ejemplo hardcodeados como fallback
            precio_pension = 10_000.0
            tipo_de_cambio = 20.0
            noticias = ["Noticia 1", "Noticia 2", "Noticia 3"]

        # Calcular precio de la pensión y tipo de cambio
        precio_pension = calcular_precio_pension()
        tipo_de_cambio = calcular_tipodecambio()

        # Generar rubrica
        generar_rubrica(precio_pension, tipo_de_cambio, noticias)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()