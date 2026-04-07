"""
ÁREA: SEGUROS
DESCRIPCIÓN: Agente que realiza cotizador seguro hogar
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

def main():
    try:
        # Parámetros por defecto
        valor_casa = 5000000  # Pesos mexicanos
        ubicacion = "Ciudad de México"
        antiguedad = 10  # Años
        tipo_casa = "Departamento"
        seguro_basico = 2500  # Pesos mexicanos
        seguro_adicional = 1000  # Pesos mexicanos
        seguro_defensa = 500  # Pesos mexicanos

        # Argumentos de la línea de comandos
        if len(sys.argv) > 1:
            valor_casa = int(sys.argv[1])
        if len(sys.argv) > 2:
            ubicacion = sys.argv[2]
        if len(sys.argv) > 3:
            antiguedad = int(sys.argv[3])
        if len(sys.argv) > 4:
            tipo_casa = sys.argv[4]

        # Cotización del seguro
        if WEB:
            # Buscar datos en tiempo real
            datos_seguros = web.buscar("seguros de hogar")
            precio_base = web.extraer_precios(datos_seguros)[0]
        else:
            # Datos de ejemplo
            precio_base = 2500  # Pesos mexicanos

        # Cálculo de la cotización
        factor_ubicacion = 1.2 if ubicacion == "Ciudad de México" else 1.0
        factor_antiguedad = 1.1 if antiguedad > 10 else 1.0
        factor_tipo_casa = 1.1 if tipo_casa == "Casa" else 1.0
        precio_seguro = precio_base * factor_ubicacion * factor_antiguedad * factor_tipo_casa * (valor_casa / 1000000)

        # Cálculo del seguro adicional
        seguro_adicional_casa = seguro_adicional * (valor_casa / 1000000)
        seguro_adicional_ubicacion = seguro_adicional * factor_ubicacion
        seguro_adicional_total = seguro_adicional_casa + seguro_adicional_ubicacion

        # Cálculo del seguro de defensa
        seguro_defensa_total = seguro_defensa * factor_ubicacion * factor_antiguedad

        # Impresión de resultados
        print("Resumen de la cotización del seguro de hogar:")
        print(f"Valor de la casa: {valor_casa} pesos mexicanos")
        print(f"Ubicación: {ubicacion}")
        print(f"Antigüedad: {antiguedad} años")
        print(f"Tipo de casa: {tipo_casa}")
        print(f"Precio base del seguro: {precio_base} pesos mexicanos")
        print(f"Factor de ubicación: {factor_ubicacion}")
        print(f"Factor de antigüedad: {factor_antiguedad}")
        print(f"Factor de tipo de casa: {factor_tipo_casa}")
        print(f"Precio del seguro: {precio_seguro} pesos mexicanos")
        print(f"Seguro adicional por casa: {seguro_adicional_casa} pesos mexicanos")
        print(f"Seguro adicional por ubicación: {seguro_adicional_ubicacion} pesos mexicanos")
        print(f"Seguro adicional total: {seguro_adicional_total} pesos mexicanos")
        print(f"Seguro de defensa total: {seguro_defensa_total} pesos mexicanos")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El precio del seguro de hogar para una casa de {valor_casa} pesos mexicanos en {ubicacion} con {antiguedad} años de antigüedad y tipo {tipo_casa} es de {precio_seguro} pesos mexicanos.")
        print(f"El seguro adicional total es de {seguro_adicional_total} pesos mexicanos.")
        print(f"El seguro de defensa total es de {seguro_defensa_total} pesos mexicanos.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main