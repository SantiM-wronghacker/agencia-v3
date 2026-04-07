"""
ÁREA: EDUCACION
DESCRIPCIÓN: Agente que realiza generador material didactico
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_material_didactico(titulo, descripcion, precios, texto):
    try:
        # Validar entrada
        if not titulo:
            raise ValueError("Titulo vacio")
        if not descripcion:
            raise ValueError("Descripcion vacia")
        if not precios:
            raise ValueError("Precios vacios")
        if not texto:
            raise ValueError("Texto vacio")

        # Validar precios
        if not isinstance(precios, dict):
            raise ValueError("Precios no son un diccionario")
        for precio in precios.values():
            if precio <= 0:
                raise ValueError("Precio no valido")

        # Generar material didactico
        material_didactico = {
            "titulo": titulo,
            "descripcion": descripcion,
            "precios": precios,
            "texto": texto
        }

        # Imprimir material didactico
        print("Material didactico:")
        print("Titulo:", material_didactico["titulo"])
        print("Descripcion:", material_didactico["descripcion"])
        print("Precios:")
        for clave, valor in material_didactico["precios"].items():
            print(f"{clave}: ${valor:.2f}")
        print("Texto:")
        print(material_didactico["texto"])

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El material didactico {material_didactico['titulo']} tiene un costo total de ${sum(material_didactico['precios'].values()):.2f}")
        print(f"El texto del material didactico tiene {len(texto.split())} palabras")
        print(f"El material didactico tiene un peso de {len(material_didactico['texto'].encode('utf-8')) / 1024:.2f} KB")
        print(f"El material didactico tiene un costo por palabra de ${sum(material_didactico['precios'].values()) / len(texto.split()):.2f}")
        print(f"El material didactico tiene un costo por caracter de ${sum(material_didactico['precios'].values()) / len(material_didactico['texto']):.2f}")

        # Imprimir porcentaje de precios
        precios_total = sum(material_didactico['precios'].values())
        porcentajes = {}
        for clave, valor in material_didactico['precios'].items():
            porcentajes[clave] = (valor / precios_total) * 100
        print("\nPorcentaje de precios:")
        for clave, valor in porcentajes.items():
            print(f"{clave}: {valor:.2f}%")

    except ValueError as e:
        print("Error:", str(e))
    except Exception as e:
        print("Error:", str(e))

def main():
    if len(sys.argv) != 5:
        print("Uso: python generador_material_didactico.py <titulo> <descripcion> <precio_libro> <precio_material> <texto>")
    else:
        titulo = sys.argv[1]
        descripcion = sys.argv[2]
        precio_libro = float(sys.argv[3])
        precio_material = float(sys.argv[4])
        texto = sys.argv[5]
        generar_material_didactico(titulo, descripcion, {"libro": precio_libro, "material": precio_material}, texto)

if __name__ == "__main__":
    main()