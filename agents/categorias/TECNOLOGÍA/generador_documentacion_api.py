"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza generador documentación api
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
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_estadisticas(numeros_aleatorios):
    promedio_numeros = sum(numeros_aleatorios) / len(numeros_aleatorios)
    maximo_numero = max(numeros_aleatorios)
    minimo_numero = min(numeros_aleatorios)
    media_aritmetica = sum(numeros_aleatorios) / len(numeros_aleatorios)
    desviacion_estandar = math.sqrt(sum((x - media_aritmetica) ** 2 for x in numeros_aleatorios) / len(numeros_aleatorios))
    return {
        "promedio_numeros": promedio_numeros,
        "maximo_numero": maximo_numero,
        "minimo_numero": minimo_numero,
        "media_aritmetica": media_aritmetica,
        "desviacion_estandar": desviacion_estandar
    }

def main():
    try:
        # Configuración por defecto
        if len(sys.argv) > 1:
            nombre_agencia = sys.argv[1]
        else:
            nombre_agencia = "Agencia Santi"

        if len(sys.argv) > 2:
            ubicacion = sys.argv[2]
        else:
            ubicacion = "México"

        if len(sys.argv) > 3:
            num_numeros_aleatorios = int(sys.argv[3])
        else:
            num_numeros_aleatorios = 10

        if len(sys.argv) > 4:
            minimo_numero_aleatorio = int(sys.argv[4])
        else:
            minimo_numero_aleatorio = 1

        if len(sys.argv) > 5:
            maximo_numero_aleatorio = int(sys.argv[5])
        else:
            maximo_numero_aleatorio = 100

        fecha_actual = datetime.datetime.now()
        numeros_aleatorios = [random.randint(minimo_numero_aleatorio, maximo_numero_aleatorio) for _ in range(num_numeros_aleatorios)]

        # Generar documentación API
        documentacion = {
            "agencia": nombre_agencia,
            "ubicacion": ubicacion,
            "fecha": fecha_actual.strftime("%Y-%m-%d %H:%M:%S"),
            "numeros": numeros_aleatorios,
            "informacion": [
                {"id": 1, "nombre": "Servicio 1", "descripcion": "Descripción del servicio 1"},
                {"id": 2, "nombre": "Servicio 2", "descripcion": "Descripción del servicio 2"},
                {"id": 3, "nombre": "Servicio 3", "descripcion": "Descripción del servicio 3"}
            ],
            "estadisticas": calcular_estadisticas(numeros_aleatorios)
        }

        # Imprimir documentación API
        print("Nombre de la agencia:", documentacion["agencia"])
        print("Ubicación:", documentacion["ubicacion"])
        print("Fecha actual:", documentacion["fecha"])
        print("Números aleatorios:", documentacion["numeros"])
        print("Información de servicios:")
        for servicio in documentacion["informacion"]:
            print(f"ID: {servicio['id']}, Nombre: {servicio['nombre']}, Descripción: {servicio['descripcion']}")
        print("Estadísticas:")
        for estadistica in documentacion["estadisticas"]:
            print(f"{estadistica}: {documentacion['estadisticas'][estadistica]}")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"La agencia {documentacion['agencia']} se encuentra ubicada en {documentacion['ubicacion']} y ha generado {len(documentacion['numeros'])} números aleatorios entre {min(documentacion['numeros'])} y {max(documentacion['numeros'])}.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()