"""
ÁREA: LOGÍSTICA
DESCRIPCIÓN: Agente que realiza generador manifiesto carga
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
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        fecha_inicial = datetime.date.today()
        fecha_final = datetime.date.today() + datetime.timedelta(days=7)
        cantidad_cargas = 10
        impuesto = 0.16  # IVA en México

        # Parámetros desde línea de comandos
        if len(sys.argv) > 1:
            fecha_inicial = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        if len(sys.argv) > 2:
            fecha_final = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
        if len(sys.argv) > 3:
            cantidad_cargas = int(sys.argv[3])
        if len(sys.argv) > 4:
            impuesto = float(sys.argv[4])

        # Generar manifiesto de carga
        manifiesto = []
        for i in range(cantidad_cargas):
            carga = {
                "id": i+1,
                "fecha": (fecha_inicial + datetime.timedelta(days=random.randint(0, (fecha_final - fecha_inicial).days))).isoformat(),
                "origen": random.choice(["Ciudad de México", "Guadalajara", "Monterrey"]),
                "destino": random.choice(["Ciudad de México", "Guadalajara", "Monterrey"]),
                "peso": round(random.uniform(100, 1000), 2),
                "valor": round(random.uniform(1000, 10000), 2),
                "impuesto": round(random.uniform(1000, 10000) * impuesto, 2),
                "total": round(random.uniform(1000, 10000) + random.uniform(1000, 10000) * impuesto, 2),
                "descripcion": f"Carga de {random.choice(['electrónicos', 'textiles', 'alimentos'])} con un peso de {round(random.uniform(100, 1000), 2)} kg"
            }
            manifiesto.append(carga)

        # Imprimir manifiesto
        print("Manifiesto de Carga:")
        for carga in manifiesto:
            print(f"ID: {carga['id']}")
            print(f"Fecha: {carga['fecha']}")
            print(f"Origen: {carga['origen']}")
            print(f"Destino: {carga['destino']}")
            print(f"Peso: {carga['peso']} kg")
            print(f"Valor: ${carga['valor']:.2f} MXN")
            print(f"Impuesto ({impuesto*100}%): ${carga['impuesto']:.2f} MXN")
            print(f"Total: ${carga['total']:.2f} MXN")
            print(f"Descripción: {carga['descripcion']}")
            print("-" * 50)

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"Total de cargas: {len(manifiesto)}")
        print(f"Total de valor: ${sum(carga['valor'] for carga in manifiesto):.2f} MXN")
        print(f"Total de impuesto: ${sum(carga['impuesto'] for carga in manifiesto):.2f} MXN")
        print(f"Total general: ${sum(carga['total'] for carga in manifiesto):.2f} MXN")

    except ValueError as e:
        print(f"Error de formato: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()