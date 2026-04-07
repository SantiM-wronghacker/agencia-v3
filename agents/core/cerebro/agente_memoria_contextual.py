"""
ÁREA: CEREBRO
DESCRIPCIÓN: Agente que realiza agente memoria contextual
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Obtener parámetros de la línea de comandos
        if len(sys.argv) > 1:
            ciudad = sys.argv[1]
            estado = sys.argv[2]
        else:
            ciudad = random.choice(["Ciudad de México", "Guadalajara", "Monterrey"])
            estado = random.choice(["DF", "Jalisco", "Nuevo León"])

        # Simulación de datos de memoria contextual
        datos = {
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temperatura": round(random.uniform(15, 30), 2),
            "humedad": round(random.uniform(40, 80), 2),
            "presion": round(random.uniform(900, 1100), 2),
            "ciudad": ciudad,
            "estado": estado,
            "velocidad_viento": round(random.uniform(5, 20), 2),
            "direccion_viento": random.choice(["Norte", "Sur", "Este", "Oeste"]),
            "nubosidad": round(random.uniform(0, 100), 2)
        }

        # Imprimir datos de memoria contextual
        print("Fecha:", datos["fecha"])
        print("Temperatura (°C):", datos["temperatura"])
        print("Humedad (%):", datos["humedad"])
        print("Presión (hPa):", datos["presion"])
        print("Ciudad:", datos["ciudad"])
        print("Estado:", datos["estado"])
        print("Velocidad del viento (km/h):", datos["velocidad_viento"])
        print("Dirección del viento:", datos["direccion_viento"])
        print("Nubosidad (%):", datos["nubosidad"])

        # Simulación de procesamiento de datos
        procesamiento = {
            "promedio_temperatura": round((datos["temperatura"] + 20) / 2, 2),
            "promedio_humedad": round((datos["humedad"] + 60) / 2, 2),
            "promedio_presion": round((datos["presion"] + 1000) / 2, 2),
            "indice_calor": round(datos["temperatura"] + (0.5555 * (datos["humedad"] - 10)), 2),
            "velocidad_viento_promedio": round(datos["velocidad_viento"] + 5, 2)
        }

        # Imprimir resultados del procesamiento
        print("Promedio Temperatura (°C):", procesamiento["promedio_temperatura"])
        print("Promedio Humedad (%):", procesamiento["promedio_humedad"])
        print("Promedio Presión (hPa):", procesamiento["promedio_presion"])
        print("Índice de calor:", procesamiento["indice_calor"])
        print("Velocidad del viento promedio (km/h):", procesamiento["velocidad_viento_promedio"])

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print("La temperatura promedio es de", procesamiento["promedio_temperatura"], "°C")
        print("La humedad promedio es de", procesamiento["promedio_humedad"], "%")
        print("La presión promedio es de", procesamiento["promedio_presion"], "hPa")
        print("El índice de calor es de", procesamiento["indice_calor"])
        print("La velocidad del viento promedio es de", procesamiento["velocidad_viento_promedio"], "km/h")

    except Exception as e:
        print("Error:", str(e))
    except IndexError:
        print("Error: Parámetros insuficientes")

if __name__ == "__main__":
    main()