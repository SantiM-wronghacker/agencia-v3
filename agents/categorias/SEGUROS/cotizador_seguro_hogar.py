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
    import web_bridge as web
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
        seguro_defensa_total = seguro_defensa * (valor_casa / 1000000)

        # Imprimir resultados
        print(f"Valor de la casa: {valor_casa} pesos mexicanos")
        print(f"Ubicación: {ubicacion}")
        print(f"Antiguedad: {antiguedad} años")
        print(f"Tipo de casa: {tipo_casa}")
        print(f"Precio del seguro básico: {precio_base} pesos mexicanos")
        print(f"Precio del seguro adicional: {seguro_adicional_total:.2f} pesos mexicanos")
        print(f"Precio del seguro de defensa: {seguro_defensa_total:.2f} pesos mexicanos")
        print(f"Precio total del seguro: {precio_seguro + seguro_adicional_total + seguro_defensa_total:.2f} pesos mexicanos")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El seguro hogar para una casa de valor {valor_casa} pesos mexicanos en {ubicacion} con {antiguedad} años de antigüedad y tipo de casa {tipo_casa} tiene un precio total de {precio_seguro + seguro_adicional_total + seguro_defensa_total:.2f} pesos mexicanos.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()