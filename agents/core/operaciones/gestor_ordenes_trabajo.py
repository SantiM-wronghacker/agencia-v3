"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza gestor ordenes trabajo
TECNOLOGÍA: Python estándar
"""

import sys
import json
import os
from datetime import datetime, timedelta
import random
import math

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def main():
    try:
        # Configuración por defecto
        fecha_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        fecha_fin = datetime.now().strftime('%Y-%m-%d')
        limite_ordenes = 10
        iva = 0.16  # IVA para México

        # Procesar argumentos
        if len(sys.argv) > 1:
            fecha_inicio = sys.argv[1]
        if len(sys.argv) > 2:
            fecha_fin = sys.argv[2]
        if len(sys.argv) > 3:
            limite_ordenes = int(sys.argv[3])
        if len(sys.argv) > 4:
            iva = float(sys.argv[4])

        # Validar fecha inicio y fin
        try:
            datetime.strptime(fecha_inicio, '%Y-%m-%d')
            datetime.strptime(fecha_fin, '%Y-%m-%d')
        except ValueError:
            print("Error: Las fechas deben estar en el formato YYYY-MM-DD")
            sys.exit(1)

        # Validar límite de órdenes
        if limite_ordenes <= 0:
            print("Error: El límite de órdenes debe ser mayor que cero")
            sys.exit(1)

        # Validar IVA
        if iva < 0 or iva > 1:
            print("Error: El IVA debe estar entre 0 y 1")
            sys.exit(1)

        # Generar datos de órdenes de trabajo
        ordenes = []
        for i in range(1, limite_ordenes + 1):
            orden = {
                "id": f"OT-{random.randint(1000, 9999)}",
                "fecha": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d'),
                "cliente": f"Cliente {random.randint(1, 100)}",
                "monto": round(random.uniform(500, 50000), 2),
                "monto_iva": round(random.uniform(500, 50000) * iva, 2),
                "monto_total": round(random.uniform(500, 50000) * (1 + iva), 2),
                "estatus": random.choice(["Pendiente", "En Proceso", "Completado", "Cancelado"]),
                "producto": f"Producto {random.randint(1, 20)}",
                "ciudad": random.choice(["México D.F.", "Guadalajara", "Monterrey", "Puebla", "León"])
            }
            ordenes.append(orden)

        # Filtrar por fechas
        ordenes_filtradas = [o for o in ordenes if fecha_inicio <= o["fecha"] <= fecha_fin]

        # Mostrar resultados
        print("=== REPORTE DE ÓRDENES DE TRABAJO ===")
        print(f"Fecha de inicio: {fecha_inicio}")
        print(f"Fecha de fin: {fecha_fin}")
        print(f"Límite de órdenes: {limite_ordenes}")
        print(f"IVA: {iva * 100}%")
        print("===== ORDENES DE TRABAJO =====")
        for orden in ordenes_filtradas:
            print(f"ID: {orden['id']}")
            print(f"Fecha: {orden['fecha']}")
            print(f"Cliente: {orden['cliente']}")
            print(f"Monto: ${orden['monto']}")
            print(f"Monto IVA: ${orden['monto_iva']}")
            print(f"Monto total: ${orden['monto_total']}")
            print(f"Estatus: {orden['estatus']}")
            print(f"Producto: {orden['producto']}")
            print(f"Ciudad: {orden['ciudad']}")
            print("-------------------------------")

        # Resumen ejecutivo
        print("===== RESUMEN EJECUTIVO =====")
        print(f"Total de órdenes: {len(ordenes_filtradas)}")
        print(f"Monto total: ${sum([orden['monto_total'] for orden in ordenes_filtradas])}")

    except Exception as e:
        print