#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import datetime
import math
import re
import random

def generar_carta_presentacion(nombre_cliente, empresa, fecha, monto, tipo_cambio, tipo_cambio_eur, precio_dolar, precio_euro, precio_peso_mexicano, precio_gasolina, precio_diesel, inflacion_anual, tasa_interes_bancaria):
    try:
        texto = os.popen(f"curl -s https://www.banxico.org.mx/estadisticas-y-publicaciones/banco-de-datos-economicos/banco-de-datos-economico/banxico-api").read()
        precios = json.loads(texto)["bmx"]["series"][0]["datos"][0]["valor"]
        monto = float(precios)
    except Exception as e:
        print(f"Error al obtener tipos de cambio y precios: {e}")
        monto = 100000.00

    carta = f"""
    Carta de presentación

    Fecha: {fecha}
    Cliente: {nombre_cliente}
    Empresa: {empresa}

    El monto de la transacción es de ${monto:.2f} MXN, lo que equivale a ${monto / tipo_cambio:.2f} USD y ${monto * tipo_cambio_eur:.2f} EUR.

    Tipos de cambio:
    - MXN/USD: {tipo_cambio}
    - MXN/EUR: {tipo_cambio_eur}

    Precios actuales en México:
    - Peso mexicano: ${precio_peso_mexicano:.2f}
    - Gasolina: ${precio_gasolina:.2f}
    - Diesel: ${precio_diesel:.2f}
    - Dólar en el mercado libre: ${precio_dolar:.2f}
    - Euro en el mercado libre: ${precio_euro:.2f}
    - Inflación anual: {inflacion_anual}%
    - Tasa de interés bancaria: {tasa_interes_bancaria}%
    """

    # Agregar resumen ejecutivo
    carta += f"""
    Resumen ejecutivo:
    - El monto de la transacción es significativo, lo que sugiere una operación importante.
    - El tipo de cambio utilizado es {tipo_cambio}.
    - Los precios de los activos se han mantenido estables en el mercado.
    """

    # Agregar datos adicionales
    carta += f"""
    Datos adicionales:
    - Precio del dólar en el mercado libre: ${precio_dolar:.2f}
    - Precio del euro en el mercado libre: ${precio_euro:.2f}
    - Inflación anual: {inflacion_anual}%
    - Tasa de interés bancaria: {tasa_interes_bancaria}%
    """

    # Agregar resumen ejecutivo final
    carta += f"""
    Resumen ejecutivo final:
    - La transacción es significativa y sugiere una operación importante.
    - El tipo de cambio utilizado es {tipo_cambio}.
    - Los precios de los activos se han mantenido estables en el mercado.
    """

    return carta

if __name__ == "__main__":
    if len(sys.argv) != 8:
        print("Uso: python generador_carta_presentacion.py <nombre_cliente> <empresa> <fecha> <monto> <tipo_cambio> <tipo_cambio_eur> <precio_dolar> <precio_euro>")
        sys.exit(1)

    nombre_cliente = sys.argv[1]
    empresa = sys.argv[2]
    fecha = sys.argv[3]
    monto = float(sys.argv[4])
    tipo_cambio = float(sys.argv[5])
    tipo_cambio_eur = float(sys.argv[6])
    precio_dolar = float(sys.argv[7])
    precio_euro = float(sys.argv[8])
    precio_peso_mexicano = 20.50
    precio_gasolina = 25.00
    precio_diesel = 22.00
    inflacion_anual = 4.2
    tasa_interes_bancaria = 8.5

    print(generar_carta_presentacion(nombre_cliente, empresa, fecha, monto, tipo_cambio, tipo_cambio_eur, precio_dolar, precio_euro, precio_peso_mexicano, precio_gasolina, precio_diesel, inflacion_anual, tasa_interes_bancaria))