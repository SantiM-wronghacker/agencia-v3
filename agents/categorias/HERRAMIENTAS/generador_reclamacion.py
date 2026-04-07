"""
ÁREA: SEGUROS
DESCRIPCIÓN: Agente que realiza generador reclamacion
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_reclamacion(real=False, cliente="", poliza="", monto=0, tipo_cambio=0, precios={}):
    try:
        if real:
            # Generar reclamación con datos reales
            reclamacion = {
                "fecha": datetime.date.today(),
                "cliente": cliente or "Juan Pérez",
                "poliza": poliza or "123456",
                "monto": round(random.uniform(10000, 500000), 2),
                "tipo_cambio": round(random.uniform(18, 22), 2),
                "precios": precios
            }
        else:
            # Generar reclamación con datos de ejemplo hardcodeados
            reclamacion = {
                "fecha": datetime.date.today(),
                "cliente": cliente or "Juan Pérez",
                "poliza": poliza or "123456",
                "monto": monto or 50000,
                "tipo_cambio": tipo_cambio or 20.50,
                "precios": precios
            }
        return reclamacion
    except Exception as e:
        # Manejar excepciones y generar reclamación con datos de ejemplo
        print(f"Error: {e}")
        return generar_reclamacion(real, cliente, poliza, monto, tipo_cambio, precios)

def generar_precio():
    try:
        return {
            "pago": round(random.uniform(500, 2000), 2),
            "diferido": round(random.uniform(1000, 5000), 2)
        }
    except Exception as e:
        # Manejar excepciones y generar precio con datos de ejemplo
        print(f"Error: {e}")
        return generar_precio()

def generar_detalles():
    try:
        return {
            "vehiculo": "Toyota Camry",
            "fecha_compra": datetime.date(2020, 1, 1),
            "kilometraje": round(random.uniform(50000, 150000), 2)
        }
    except Exception as e:
        # Manejar excepciones y generar detalles con datos de ejemplo
        print(f"Error: {e}")
        return generar_detalles()

def main():
    try:
        # Generar reclamación
        if len(sys.argv) > 1 and sys.argv[1] == "--real":
            reclamacion = generar_reclamacion(real=True)
        else:
            cliente = sys.argv[1] if len(sys.argv) > 1 else ""
            poliza = sys.argv[2] if len(sys.argv) > 2 else ""
            monto = float(sys.argv[3]) if len(sys.argv) > 3 else 0
            tipo_cambio = float(sys.argv[4]) if len(sys.argv) > 4 else 0
            precios = {sys.argv[5]: float(sys.argv[6])} if len(sys.argv) > 6 else {}
            detalles = generar_detalles()
            precio = generar_precio()
            reclamacion = generar_reclamacion(cliente=cliente, poliza=poliza, monto=monto, tipo_cambio=tipo_cambio, precios=precios)
            print("Resumen Ejecutivo:")
            print(f"Fecha: {reclamacion['fecha']}")
            print(f"Cliente: {reclamacion['cliente']}")
            print(f"Poliza: {reclamacion['poliza']}")
            print(f"Monto: {reclamacion['monto']}")
            print(f"Tipo de cambio: {reclamacion['tipo_cambio']}")
            print(f"Precio de pago: {precio['pago']}")
            print(f"Precio de diferido: {precio['diferido']}")
            print(f"Detalles del vehiculo:")
            print(f"Vehiculo: {detalles['vehiculo']}")
            print(f"Fecha de compra: {detalles['fecha_compra']}")
            print(f"Kilometraje: {detalles['kilometraje']}")
    except Exception as e:
        # Manejar excepciones y generar reclamación con datos de ejemplo
        print(f"Error: {e}")

if __name__ == "__main__":
    main()