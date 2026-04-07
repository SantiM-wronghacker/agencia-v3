"""
ÁREA: SEGUROS
DESCRIPCIÓN: Agente que realiza generador dictamen siniestro
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def obtener_datos_siniestro():
    try:
        fecha = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().strftime("%Y-%m-%d")
        lugar = sys.argv[2] if len(sys.argv) > 2 else "Ciudad de México"
        descripcion = sys.argv[3] if len(sys.argv) > 3 else "Siniestro de incendio en un edificio"
        costo = float(sys.argv[4]) if len(sys.argv) > 4 else 1000000.0
        afectados = int(sys.argv[5]) if len(sys.argv) > 5 else 10
    except IndexError:
        fecha = "2022-01-01"
        lugar = "Ciudad de México"
        descripcion = "Siniestro de incendio en un edificio"
        costo = 1000000.0
        afectados = 10
    except ValueError:
        print("Error: valores de entrada no válidos")
        sys.exit(1)
    return {
        "fecha": fecha,
        "lugar": lugar,
        "descripcion": descripcion,
        "costo": costo,
        "afectados": afectados
    }

def calcular_dictamen_siniestro(datos):
    dictamen = {
        "fecha": datos["fecha"],
        "lugar": datos["lugar"],
        "descripcion": datos["descripcion"],
        "costo": datos["costo"],
        "afectados": datos["afectados"],
        "recomendaciones": [
            "Revisar instalaciones eléctricas",
            "Capacitar personal en prevención de incendios",
            "Verificar estado de los sistemas de seguridad",
            "Realizar un estudio de la causa raíz del siniestro"
        ]
    }
    return dictamen

def calcular_perdidas_economicas(costo, afectados):
    # Calcula las pérdidas económicas considerando un valor por afectado
    valor_por_afectado = 100000.0
    perdidas_economicas = costo + (afectados * valor_por_afectado)
    return perdidas_economicas

def calcular_dias_de_paralización(afectados, costo):
    # Calcula los días de paralización considerando un valor por afectado y costo
    valor_por_afectado = 1000.0
    dias_de_paralización = (afectados * valor_por_afectado) + (costo / 1000.0)
    return dias_de_paralización

def main():
    try:
        datos_siniestro = obtener_datos_siniestro()
        dictamen_siniestro = calcular_dictamen_siniestro(datos_siniestro)
        perdidas_economicas = calcular_perdidas_economicas(datos_siniestro["costo"], datos_siniestro["afectados"])
        dias_de_paralización = calcular_dias_de_paralización(datos_siniestro["afectados"], datos_siniestro["costo"])
        print("Dictamen de siniestro:")
        print("Fecha:", dictamen_siniestro["fecha"])
        print("Lugar:", dictamen_siniestro["lugar"])
        print("Descripción:", dictamen_siniestro["descripcion"])
        print("Costo:", dictamen_siniestro["costo"])
        print("Afectados:", dictamen_siniestro["afectados"])
        print("Recomendaciones:")
        for recomendacion in dictamen_siniestro["recomendaciones"]:
            print("-", recomendacion)
        print("Perdidas económicas:", perdidas_economicas)
        print("Días de paralización:", dias_de_paralización)
        print("Resumen ejecutivo:")
        print("El siniestro ha causado pérdidas económicas significativas y ha afectado a la comunidad.")
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()