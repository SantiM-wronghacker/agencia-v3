import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios(dolar=20.50, euro=22.75, peso=1.00):
    return {
        "dólar": dolar,
        "euro": euro,
        "peso": peso
    }

def buscar_datos(ventas=1000, compras=500, utilidad=500):
    return {
        "ventas": ventas,
        "compras": compras,
        "utilidad": utilidad
    }

def fetch_texto(texto="Texto de ejemplo"):
    return texto

def generar_reporte_kpi(dolar, euro, peso, ventas, compras, utilidad, texto):
    try:
        print("\nÁREA: DATOS")
        print("DESCRIPCIÓN: Agente que realiza generador reporte kpi")
        print("TECNOLOGÍA: Python estándar")
        print(f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\nDATOS FINANCIEROS")
        print(f"Precio dólar: {dolar:.2f}")
        print(f"Precio euro: {euro:.2f}")
        print(f"Precio peso: {peso:.2f}")
        print(f"Ventas: {ventas:.2f}")
        print(f"Compras: {compras:.2f}")
        print(f"Utilidad: {utilidad:.2f}")
        print(f"Ingresos totales: {ventas + utilidad:.2f}")
        print(f"Gastos totales: {compras:.2f}")
        print(f"Margen de utilidad: {(utilidad / ventas) * 100:.2f}%")
        print(f"Índice de ventas: {ventas / (compras + ventas):.2f}")
        print(f"Margen de ganancia: {(utilidad / compras) * 100:.2f}%")
        print(f"Índice de liquidez: {(ventas / compras):.2f}")
        print(f"Costo de ventas: {(compras / ventas) * 100:.2f}%")
        print(f"Margen de contribución: {(utilidad / (ventas - compras)) * 100:.2f}%")
        
        print("\nRESUMEN EJECUTIVO")
        print(f"El reporte muestra un aumento en las ventas y una reducción en las compras.")
        print(f"La utilidad se ha incrementado en un {((utilidad - 500) / 500) * 100:.2f}%.")
        print(f"El margen de ganancia se mantiene en un {((utilidad / compras) * 100):.2f}%.")
        
        print("\nRESUMEN FINANCIERO")
        print(f"Ingresos totales: {ventas + utilidad:.2f}")
        print(f"Gastos totales: {compras:.2f}")
        
        print("\nSEMAFORO DE CUMPLIMIENTO")
        if utilidad > 0:
            print("Cumplimiento: Alto")
        elif utilidad == 0:
            print("Cumplimiento: Moderado")
        else:
            print("Cumplimiento: Bajo")
        
        print("\nRESUMEN EJECUTIVO FINAL")
        print(f"El reporte muestra un aumento en las ventas y una reducción en las compras.")
        print(f"La utilidad se ha incrementado en un {((utilidad - 500) / 500) * 100:.2f}%.")
        print(f"El margen de ganancia se mantiene en un {((utilidad / compras) * 100):.2f}%.")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    if len(sys.argv) > 1:
        try:
            dolar = float(sys.argv[1])
            euro = float(sys.argv[2])
            peso = float(sys.argv[3])
            ventas = float(sys.argv[4])
            compras = float(sys.argv[5])
            utilidad = float(sys.argv[6])
            texto = sys.argv[7]
        except ValueError:
            print("Error: Los valores deben ser números o texto.")
            return
    else:
        dolar = 20.50
        euro = 22.75
        peso = 1.00
        ventas = 1000
        compras = 500
        utilidad = 500
        texto = "Texto de ejemplo"