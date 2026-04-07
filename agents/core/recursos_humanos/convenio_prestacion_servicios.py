"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza convenio prestacion servicios
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import random
import os
import math

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def generar_convenio(monto_min=50000, monto_max=500000, duracion_min=3, duracion_max=24):
    try:
        datos = {
            "fecha": datetime.datetime.now().strftime("%d/%m/%Y"),
            "numero_convenio": f"CONV-{random.randint(1000, 9999)}",
            "monto": round(random.uniform(monto_min, monto_max), 2),
            "duracion_meses": random.randint(duracion_min, duracion_max),
            "partes": ["Agencia Santi", "Cliente " + str(random.randint(1, 1000))],
            "impuesto": round(datos["monto"] * 0.16, 2),  # IVA 16%
            "total": round(datos["monto"] + datos["impuesto"], 2),
            "monto_mensual": round(datos["monto"] / datos["duracion_meses"], 2),
            "monto_mensual_con_impuesto": round((datos["monto"] + datos["impuesto"]) / datos["duracion_meses"], 2),
            "intereses": round(datos["monto"] * 0.05, 2),  # Intereses 5%
            "fecha_pago": (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%d/%m/%Y"),
            "descripcion": f"Convenio de prestacion de servicios por un monto de ${datos['monto']:.2f} para un plazo de {datos['duracion_meses']} meses"
        }
        return datos
    except Exception as e:
        print(f"Error al generar convenio: {str(e)}")
        return None

def main():
    try:
        args = sys.argv[1:] if len(sys.argv) > 1 else ["--default"]
        if len(args) > 0 and args[0] == "--help":
            print("Uso: python convenio_prestacion_servicios.py [monto_min] [monto_max] [duracion_min] [duracion_max]")
            print("Ejemplo: python convenio_prestacion_servicios.py 50000 500000 3 24")
            sys.exit(0)

        monto_min = int(args[0]) if len(args) > 0 else 50000
        monto_max = int(args[1]) if len(args) > 1 else 500000
        duracion_min = int(args[2]) if len(args) > 2 else 3
        duracion_max = int(args[3]) if len(args) > 3 else 24

        convenio = generar_convenio(monto_min, monto_max, duracion_min, duracion_max)

        if convenio:
            print("=== CONVENIO DE PRESTACIÓN DE SERVICIOS ===")
            print(f"Número: {convenio['numero_convenio']}")
            print(f"Fecha: {convenio['fecha']}")
            print(f"Monto: ${convenio['monto']:.2f}")
            print(f"Duración: {convenio['duracion_meses']} meses")
            print(f"Intereses: ${convenio['intereses']:.2f} (5% anual)")
            print(f"Fecha de pago: {convenio['fecha_pago']}")
            print(f"Descripción: {convenio['descripcion']}")
            print("\nResumen ejecutivo:")
            print(f"El convenio de prestación de servicios tiene un monto de ${convenio['monto']:.2f} y una duración de {convenio['duracion_meses']} meses.")
            print(f"El cliente pagará un monto de ${convenio['monto_mensual']:.2f} al mes, incluyendo un interés del 5% anual.")
            print(f"El pago final será de ${convenio['total']:.2f} en la fecha de pago {convenio['fecha_pago']}.")
            print(f"La descripción del convenio es: {convenio['descripcion']}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()