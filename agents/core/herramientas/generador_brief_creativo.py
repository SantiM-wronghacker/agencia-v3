"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza generador brief creativo
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_brief_creativo(productos=None, texto=None, precios=None, presupuesto=None):
    try:
        if productos is None:
            productos = ["Producto 1", "Producto 2", "Producto 3"]
        if texto is None:
            texto = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        if precios is None:
            precios = {"Producto 1": 100.50, "Producto 2": 200.25, "Producto 3": 300.75}
        if presupuesto is None:
            presupuesto = sum(precios.values())
    except Exception as e:
        print(f"Error: {e}")
        return ""

    # Procesar datos y generar brief creativo
    brief = f"Brief creativo para campaña de marketing en México\n"
    brief += f"Fecha: {datetime.date.today()}\n"
    brief += f"Productos: {', '.join(productos)}\n"
    brief += f"Precio promedio: {sum(precios.values()) / len(precios):.2f}\n"
    brief += f"Total de productos: {len(productos)}\n"
    brief += f"Total de precios: {sum(precios.values()):.2f}\n"
    brief += f"Mayor precio: {max(precios.values()):.2f}\n"
    brief += f"Menor precio: {min(precios.values()):.2f}\n"
    brief += f"Texto de ejemplo: {texto[:100]}...\n"
    brief += f"Resumen ejecutivo: El brief creativo para la campaña de marketing en México se enfoca en la promoción de los productos {', '.join(productos)} con precios promedio de {sum(precios.values()) / len(precios):.2f}.\n"
    brief += f"Análisis de mercado: La competencia en el mercado mexicano es alta, por lo que se recomienda ofrecer descuentos y promociones para atraer a los clientes.\n"
    brief += f"Estrategia de marketing: La estrategia de marketing se enfocará en la publicidad en redes sociales y en la creación de contenido atractivo para los clientes.\n"
    brief += f"Presupuesto: El presupuesto para la campaña de marketing será de {presupuesto:.2f}\n"
    brief += f"Porcentaje de presupuesto asignado a publicidad: {(presupuesto * 0.7):.2f}\n"
    brief += f"Porcentaje de presupuesto asignado a creación de contenido: {(presupuesto * 0.3):.2f}\n"
    brief += f"Resumen ejecutivo: El brief creativo para la campaña de marketing en México se enfoca en la promoción de los productos {', '.join(productos)} con precios promedio de {sum(precios.values()) / len(precios):.2f}.\n"

    return brief

def main():
    if len(sys.argv) > 1:
        productos = sys.argv[1].split(',')
        texto = sys.argv[2]
        precios = {}
        for producto in productos:
            precios[producto] = float(sys.argv[3 + productos.index(producto)])
        presupuesto = float(sys.argv[len(productos) + 3])
    else:
        productos = ["Producto 1", "Producto 2", "Producto 3"]
        texto = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        precios = {"Producto 1": 100.50, "Producto 2": 200.25, "Producto 3": 300.75}
        presupuesto = sum(precios.values())

    print(generar_brief_creativo(productos, texto, precios, presupuesto))

if __name__ == "__main__":
    main()