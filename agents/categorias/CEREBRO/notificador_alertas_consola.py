"""
ÁREA: CEREBRO
DESCRIPCIÓN: Agente que realiza notificador alertas consola
TECNOLOGÍA: Python estándar
"""

import sys
import json
import os
from datetime import datetime
import math
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_porcentaje(parcial, total):
    if total == 0:
        return 0
    return round((parcial / total) * 100, 2)

def calcular_iva(monto):
    return round(monto * 0.16, 2)

def calcular_margen(monto_ventas, monto_gastos):
    return round(monto_ventas - monto_gastos, 2)

def calcular_porcentaje_margen(margen, monto_ventas):
    if monto_ventas == 0:
        return 0
    return round((margen / monto_ventas) * 100, 2)

def calcular_utilidad(monto_ventas, monto_gastos, iva):
    return round(monto_ventas - monto_gastos - iva, 2)

def main():
    try:
        # Configuración por defecto
        alertas = [
            {"id": 1, "tipo": "VENTAS", "mensaje": "Ventas diarias: $15,250.00 MXN", "prioridad": "ALTA"},
            {"id": 2, "tipo": "INVENTARIO", "mensaje": "Stock crítico: 35 unidades de producto XYZ", "prioridad": "MEDIA"},
            {"id": 3, "tipo": "FINANZAS", "mensaje": "Gasto mensual: $48,750.00 MXN", "prioridad": "BAJA"},
            {"id": 4, "tipo": "LOGISTICA", "mensaje": "Envíos pendientes: 12", "prioridad": "ALTA"},
            {"id": 5, "tipo": "SOPORTE", "mensaje": "Tickets abiertos: 7", "prioridad": "MEDIA"}
        ]

        # Procesar argumentos
        if len(sys.argv) > 1:
            try:
                archivo = sys.argv[1]
                if os.path.exists(archivo):
                    with open(archivo, 'r') as f:
                        alertas = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error al leer el archivo: {e}")
                sys.exit(1)

        # Datos adicionales calculados
        total_ventas = float(sys.argv[2]) if len(sys.argv) > 2 else 15250.00
        total_gastos = float(sys.argv[3]) if len(sys.argv) > 3 else 48750.00
        iva = calcular_iva(total_ventas)
        margen = calcular_margen(total_ventas, total_gastos)
        porcentaje_margen = calcular_porcentaje_margen(margen, total_ventas)
        utilidad = calcular_utilidad(total_ventas, total_gastos, iva)

        print("Alertas del sistema:")
        for alerta in alertas:
            print(f"ID: {alerta['id']}, Tipo: {alerta['tipo']}, Mensaje: {alerta['mensaje']}, Prioridad: {alerta['prioridad']}")

        print("\nResumen financiero:")
        print(f"Total ventas: ${total_ventas:.2f} MXN")
        print(f"Total gastos: ${total_gastos:.2f} MXN")
        print(f"IVA: ${iva:.2f} MXN")
        print(f"Márgen: ${margen:.2f} MXN")
        print(f"Porcentaje de margen: {porcentaje_margen:.2f}%")
        print(f"Utilidad: ${utilidad:.2f} MXN")

        print("\nResumen ejecutivo:")
        print(f"El sistema tiene {len(alertas)} alertas pendientes.")
        print(f"El total de ventas es de ${total_ventas:.2f} MXN.")
        print(f"El total de gastos es de ${total_gastos:.2f} MXN.")
        print(f"La utilidad es de ${utilidad:.2f} MXN.")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()