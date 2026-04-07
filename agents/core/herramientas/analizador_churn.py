"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza analizador churn
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

def analizador_churn(clientes=1000, ventas=5000, retorno=0.2, precio_promedio=100, descuento=0.1, tipo_de_cambio=20):
    try:
        if WEB:
            # Buscar datos reales con web_bridge
            datos = web.buscar("datos_churn")
            precios = web.extraer_precios(datos)
            tipo_de_cambio = web.fetch_texto("tipo_de_cambio")
        else:
            # Datos de ejemplo hardcodeados
            datos = {
                "clientes": clientes,
                "ventas": ventas,
                "retorno": retorno
            }
            precios = {
                "precio_promedio": precio_promedio,
                "descuento": descuento
            }

        # Calcular churn
        churn = clientes * retorno
        ventas_reales = ventas * (1 - descuento)
        ingresos_reales = ventas_reales * precio_promedio
        tipo_de_cambio_real = tipo_de_cambio / 20  # Tipo de cambio real (1 USD = 20 MXN)

        # Calcular ingresos por cliente
        ingresos_por_cliente = ingresos_reales / clientes

        # Calcular churn porcentual
        churn_porcentual = (churn / clientes) * 100

        # Calcular ingresos por mes
        ingresos_por_mes = ingresos_reales / 12

        # Calcular churn mensual
        churn_mensual = churn / 12

        # Calcular rentabilidad
        rentabilidad = ingresos_reales - (churn * precio_promedio)

        # Imprimir resultados
        print(f"Área: Ventas")
        print(f"Descripción: Analizador Churn")
        print(f"Fecha y hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Clientes: {clientes}")
        print(f"Ventas: {ventas} MXN")
        print(f"Retorno: {retorno * 100}%")
        print(f"Churn: {churn:.2f} clientes")
        print(f"Precio promedio: {precio_promedio} MXN")
        print(f"Descuento: {descuento * 100}%")
        print(f"Ingresos reales: {ingresos_reales} MXN")
        print(f"Tipo de cambio real: {tipo_de_cambio_real} MXN/USD")
        print(f"Ingresos por cliente: {ingresos_por_cliente:.2f} MXN")
        print(f"Churn porcentual: {churn_porcentual:.2f}%")
        print(f"Ingresos por mes: {ingresos_por_mes:.2f} MXN")
        print(f"Churn mensual: {churn_mensual:.2f} clientes")
        print(f"Rentabilidad: {rentabilidad:.2f} MXN")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        if churn_porcentual < 10:
            print("El nivel de churn es bajo y la empresa está en buen estado.")
        elif churn_porcentual < 20:
            print("El nivel de churn es moderado y la empresa debe tomar medidas para mejorar la retención de clientes.")
        else:
            print("El nivel de churn es alto y la empresa está en riesgo de perder clientes y afectar sus ingresos.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        clientes = int(sys.argv[1])
        ventas = int(sys.argv[2])
        retorno = float(sys.argv[3])
        precio_promedio = float(sys.argv[4])
        descuento = float(sys.argv[5])
        tipo_de_cambio = int(sys.argv[6])
        analizador_churn(clientes, ventas, retorno, precio_promedio, descuento, tipo_de_cambio)
    else:
        analizador_churn()