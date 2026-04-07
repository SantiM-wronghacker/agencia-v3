"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza analizador funnel conversion
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
from datetime import datetime
import math
import re
import random

def analizador_funnel_conversion(usuario, visita, venta, precio_producto1, tipo_de_cambio):
    try:
        if usuario < 0:
            raise ValueError("El número de usuarios no puede ser negativo")
        if visita < 0:
            raise ValueError("El número de visitas no puede ser negativo")
        if venta < 0:
            raise ValueError("El número de ventas no puede ser negativo")
        if precio_producto1 < 0:
            raise ValueError("El precio del producto no puede ser negativo")
        if tipo_de_cambio < 0:
            raise ValueError("El tipo de cambio no puede ser negativo")
        if tipo_de_cambio == 0:
            raise ValueError("El tipo de cambio no puede ser cero")

        # Analizar datos
        conversion = (venta / visita) * 100 if visita != 0 else 0
        rentabilidad = (venta / (usuario * precio_producto1)) * 100 if usuario != 0 and precio_producto1 != 0 else 0
        rentabilidad_mexico = (venta / (usuario * precio_producto1 * tipo_de_cambio)) * 100 if usuario != 0 and precio_producto1 != 0 and tipo_de_cambio != 0 else 0
        ingresos = venta * precio_producto1
        ingresos_mexico = ingresos * tipo_de_cambio
        usuarios_repetidos = (usuario / visita) * 100 if visita != 0 else 0
        visitas_repetidas = (visita / usuario) * 100 if usuario != 0 else 0
        ventas_repetidas = (venta / usuario) * 100 if usuario != 0 else 0
        margen_utilidad = (ingresos - (usuario * precio_producto1)) / ingresos * 100 if ingresos != 0 else 0

        # Mostrar resultados
        print(f"Área: Marketing")
        print(f"Descripción: Analizador Funnel Conversion")
        print(f"Tecnología: Python estándar")
        print(f"Conversion: {conversion:.2f}%")
        print(f"Rentabilidad: {rentabilidad:.2f}%")
        print(f"Rentabilidad en México: {rentabilidad_mexico:.2f}%")
        print(f"Ingresos: ${ingresos:.2f}")
        print(f"Ingresos en México: ${ingresos_mexico:.2f}")
        print(f"Tipo de cambio: {tipo_de_cambio}")
        print(f"Usuarios: {usuario}")
        print(f"Visitas: {visita}")
        print(f"Ventas: {venta}")
        print(f"Precio del producto 1: ${precio_producto1:.2f}")
        print(f"Usuarios repetidos: {usuarios_repetidos:.2f}%")
        print(f"Visitas repetidas: {visitas_repetidas:.2f}%")
        print(f"Ventas repetidas: {ventas_repetidas:.2f}%")
        print(f"Margen de utilidad: {margen_utilidad:.2f}%")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El análisis de funnel conversion muestra que la conversión es de {conversion:.2f}%")
        print(f"La rentabilidad es de {rentabilidad:.2f}% y la rentabilidad en México es de {rentabilidad_mexico:.2f}%")
        print(f"Los ingresos totales son de ${ingresos:.2f} y los ingresos en México son de ${ingresos_mexico:.2f}")
        print(f"El margen de utilidad es de {margen_utilidad:.2f}%")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Error: Faltan argumentos")
    else:
        usuario = int(sys.argv[1])
        visita = int(sys.argv[2])
        venta = int(sys.argv[3])
        precio_producto1 = float(sys.argv[4])
        tipo_de_cambio = float(sys.argv[5])
        analizador_funnel_conversion(usuario, visita, venta, precio_producto1, tipo_de_cambio)