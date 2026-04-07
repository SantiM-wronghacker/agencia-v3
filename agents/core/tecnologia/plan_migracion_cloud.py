"""
ÁREA: TECNOLOGÍA
DESCRIPCIÓN: Agente que realiza plan migracion cloud
TECNOLOGÍA: Python estándar
"""

import sys
import json
import os
import datetime
import random
import math

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        args = sys.argv[1:]
        if len(args) > 0:
            cloud_provider = args[0]
        else:
            cloud_provider = "AWS"

        if len(args) > 1:
            budget_mxn = int(args[1])
        else:
            budget_mxn = 500000

        if len(args) > 2:
            deadline_days = int(args[2])
        else:
            deadline_days = 90

        # Generar datos de migración
        current_date = datetime.date.today()
        deadline_date = current_date + datetime.timedelta(days=deadline_days)

        # Cálculos ficticios pero realistas para México
        servers = random.randint(10, 30)
        storage_tb = round(random.uniform(50, 200), 2)
        cost_per_server = random.randint(5000, 15000)
        total_cost = servers * cost_per_server
        bandwidth_gb = round(random.uniform(100, 500), 2)
        database_size_gb = round(random.uniform(50, 200), 2)
        security_cost = round(random.uniform(5000, 10000), 2)
        total_cost += security_cost

        # Verificar presupuesto
        if total_cost > budget_mxn:
            budget_status = "SUPERADO"
            budget_diff = total_cost - budget_mxn
        else:
            budget_status = "DENTRO"
            budget_diff = budget_mxn - total_cost

        # Imprimir resultados
        print(f"Plan de Migración a {cloud_provider}")
        print(f"Fecha límite: {deadline_date.strftime('%d/%m/%Y')}")
        print(f"Servidores a migrar: {servers}")
        print(f"Almacenamiento total: {storage_tb} TB")
        print(f"Ancho de banda estimado: {bandwidth_gb} GB")
        print(f"Tamaño de la base de datos: {database_size_gb} GB")
        print(f"Costo estimado por servidor: ${cost_per_server:,.2f} MXN")
        print(f"Costo total estimado: ${total_cost:,.2f} MXN ({budget_status} del presupuesto)")
        print(f"Diferencia presupuestal: ${abs(budget_diff):,.2f} MXN")
        print(f"Costo de seguridad: ${security_cost:,.2f} MXN")
        print(f"Tiempo de migración estimado: {deadline_days} días")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"Se ha generado un plan de migración a {cloud_provider} con un costo total estimado de ${total_cost:,.2f} MXN.")
        print(f"El presupuesto es {budget_status} y la diferencia presupuestal es de ${abs(budget_diff):,.2f} MXN.")
        print(f"Se estima que la migración tomará {deadline_days} días y se necesitarán {servers} servidores.")
        print(f"El ancho de banda estimado es de {bandwidth_gb} GB y el tamaño de la base de datos es de {database_size_gb} GB.")

    except ValueError as e:
        print(f"Error en la conversión de valores: {str(e)}")
    except Exception as e:
        print(f"Error en la planificación: {str(e)}")

if __name__ == "__main__":
    main()