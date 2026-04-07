"""
ÁREA: MANUFACTURA
DESCRIPCIÓN: Agente que realiza analizador defectos
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

def analizador_defectos(area, produccion, costo_unitario, defectos, precio_unitario=None, precio_total=None):
    try:
        if WEB:
            # Buscar datos reales con web_bridge
            texto = web.fetch_texto("https://www.example.com/datos_defectos")
            precios = web.extraer_precios(texto)
        else:
            # Datos de ejemplo hardcodeados
            precios = {
                "precio_unitario": precio_unitario or 50,
                "precio_total": precio_total or 50000
            }

        # Procesar datos y calcular resultados
        defectos_porcentaje = (defectos / produccion) * 100
        costo_total = produccion * costo_unitario
        beneficio = precios["precio_total"] - costo_total
        margen_ganancia = (beneficio / costo_total) * 100

        # Imprimir resultados
        print(f"Área: {area}")
        print(f"Producción: {produccion} unidades")
        print(f"Costo unitario: ${costo_unitario:.2f}")
        print(f"Costo total: ${costo_total:.2f}")
        print(f"Beneficio: ${beneficio:.2f}")
        print(f"Defectos porcentaje: {defectos_porcentaje:.2f}%")
        print(f"Margen de ganancia: {margen_ganancia:.2f}%")
        print(f"Defectos: {defectos} unidades")
        print(f"Precio unitario: ${precios['precio_unitario']:.2f}")
        print(f"Precio total: ${precios['precio_total']:.2f}")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"La producción de {area} ha tenido un costo total de ${costo_total:.2f} y un beneficio de ${beneficio:.2f}.")
        print(f"El margen de ganancia es de {margen_ganancia:.2f}%.")

        # Información adicional
        print("\nInformación adicional:")
        print(f"El nivel de calidad de la producción es {defectos_porcentaje:.2f}%.")

        # Información sobre el análisis
        print("\nInformación sobre el análisis:")
        print(f"El análisis se realizó con los siguientes datos:")
        print(f"  - Área: {area}")
        print(f"  - Producción: {produccion} unidades")
        print(f"  - Costo unitario: ${costo_unitario:.2f}")
        print(f"  - Defectos: {defectos} unidades")
        print(f"  - Precio unitario: ${precios['precio_unitario']:.2f}")
        print(f"  - Precio total: ${precios['precio_total']:.2f}")

    except ZeroDivisionError:
        print("Error: No se puede dividir entre cero.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) != 5 and len(sys.argv) != 7:
        print("Error: El número de argumentos es incorrecto.")
        return

    area = sys.argv[1]
    produccion = int(sys.argv[2])
    costo_unitario = float(sys.argv[3])
    defectos = int(sys.argv[4])

    if len(sys.argv) == 7:
        precio_unitario = float(sys.argv[5])
        precio_total = float(sys.argv[6])

    analizador_defectos(area, produccion, costo_unitario, defectos, precio_unitario, precio_total)

if __name__ == "__main__":
    main()