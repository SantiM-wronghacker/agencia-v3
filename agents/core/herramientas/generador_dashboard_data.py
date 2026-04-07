#!/usr/bin/env python3
"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza generador dashboard data
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios(precio_petroleo=120.50, precio_gasolina=25.20, precio_dolar=20.50):
    return {
        "petróleo": precio_petroleo,
        "gasolina": precio_gasolina,
        "dólar": precio_dolar
    }

def extraer_noticias():
    return [
        "Noticia 1",
        "Noticia 2",
        "Noticia 3",
        "Noticia 4",
        "Noticia 5",
        "Noticia 6",
        "Noticia 7",
        "Noticia 8",
        "Noticia 9",
        "Noticia 10"
    ]

def extraer_cotizaciones():
    return {
        "EUR/USD": 20.50,
        "USD/JPY": 150.20,
        "GBP/USD": 1.35,
        "AUD/USD": 0.75,
        "CAD/USD": 1.10
    }

def extraer_economicas():
    return {
        "inflación": round(random.uniform(3.5, 4.5), 2),
        "tasa_de_interés": round(random.uniform(15.5, 18.5), 2),
        "empleo": round(random.uniform(55.5, 65.5), 2)
    }

def generar_dashboard_data(precio_petroleo=120.50, precio_gasolina=25.20, precio_dolar=20.50, tipo_de_cambio=20.50, cotizaciones=1500):
    try:
        precios = extraer_precios(precio_petroleo, precio_gasolina, precio_dolar)
        noticias = extraer_noticias()
        cotizaciones = extraer_cotizaciones()
        economicas = extraer_economicas()
        datos = {
            "precios": precios,
            "noticias": noticias,
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo_de_cambio": tipo_de_cambio,
            "cotizaciones": cotizaciones,
            "economicas": economicas
        }
        return datos
    except Exception as e:
        return {
            "error": str(e)
        }

def main():
    try:
        if len(sys.argv) > 1:
            precio_petroleo = float(sys.argv[1])
            precio_gasolina = float(sys.argv[2])
            precio_dolar = float(sys.argv[3])
            tipo_de_cambio = float(sys.argv[4])
            cotizaciones = int(sys.argv[5])
        else:
            precio_petroleo = 120.50
            precio_gasolina = 25.20
            precio_dolar = 20.50
            tipo_de_cambio = 20.50
            cotizaciones = 1500
        
        datos = generar_dashboard_data(precio_petroleo, precio_gasolina, precio_dolar, tipo_de_cambio, cotizaciones)
        
        print("ÁREA: HERRAMIENTAS")
        print("DESCRIPCIÓN: Agente que realiza generador dashboard data")
        print("TECNOLOGÍA: Python estándar")
        print()
        print("Datos generados:")
        print(json.dumps(datos, indent=4))
        print()
        print("Resumen ejecutivo:")
        print("El precio del petróleo se encuentra en $", datos["precios"]["petróleo"])
        print("La inflación se encuentra en", datos["economicas"]["inflación"], "%")
        print("La tasa de interés se encuentra en", datos["economicas"]["tasa_de_interés"], "%")
        print("El empleo se encuentra en", datos["economicas"]["empleo"], "%")
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()