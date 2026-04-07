"""
AREA: HERRAMIENTAS
DESCRIPCION: Agente que realiza coordinador pipeline datos
TECNOLOGIA: Python estándar
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
        # Configuración por defecto
        num_transacciones = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        monto_min = float(sys.argv[2]) if len(sys.argv) > 2 else 100
        monto_max = float(sys.argv[3]) if len(sys.argv) > 3 else 1000
        tasa_iva = float(sys.argv[4]) if len(sys.argv) > 4 else 0.16
        tasa_isr = float(sys.argv[5]) if len(sys.argv) > 5 else 0.10

        datos = {
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "monto_total": 0,
            "monto_total_con_iva": 0,
            "monto_total_con_isr": 0,
            "transacciones": []
        }

        # Simulación de transacciones
        for _ in range(num_transacciones):
            monto = round(random.uniform(monto_min, monto_max), 2)
            datos["monto_total"] += monto
            datos["monto_total_con_iva"] += monto * (1 + tasa_iva)
            datos["monto_total_con_isr"] += monto * (1 + tasa_isr)
            datos["transacciones"].append({
                "monto": monto,
                "descripcion": f"Transacción {random.randint(1, 100)}",
                "iva": round(monto * tasa_iva, 2),
                "isr": round(monto * tasa_isr, 2)
            })

        # Imprimir resultados
        print(f"Fecha: {datos['fecha']}")
        print(f"Monto total sin IVA ni ISR: ${datos['monto_total']:.2f} MXN")
        print(f"Monto total con IVA: ${datos['monto_total_con_iva']:.2f} MXN")
        print(f"Monto total con ISR: ${datos['monto_total_con_isr']:.2f} MXN")
        print(f"Número de transacciones: {len(datos['transacciones'])}")
        print(f"Transacción promedio: ${datos['monto_total'] / len(datos['transacciones']):.2f} MXN")
        print(f"Transacción máxima: ${max(transaccion['monto'] for transaccion in datos['transacciones']):.2f} MXN")
        print(f"Transacción mínima: ${min(transaccion['monto'] for transaccion in datos['transacciones']):.2f} MXN")
        print(f"Desviación estándar de las transacciones: {math.sqrt(sum((x['monto'] - datos['monto_total'] / len(datos['transacciones'])) ** 2 for x in datos['transacciones']) / len(datos['transacciones'])):.2f} MXN")
        print(f"Impuesto total sobre la renta (ISR): ${sum(transaccion['isr'] for transaccion in datos['transacciones']):.2f} MXN")
        print(f"Impuesto al valor agregado (IVA) total: ${sum(transaccion['iva'] for transaccion in datos['transacciones']):.2f} MXN")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El monto total de las transacciones es de ${datos['monto_total']:.2f} MXN.")
        print(f"El monto total con IVA es de ${datos['monto_total_con_iva']:.2f} MXN.")
        print(f"El monto total con ISR es de ${datos['monto_total_con_isr']:.2f} MXN.")
        print(f"El número de transacciones es de {len(datos['transacciones'])}.")
        print(f"La transacción promedio es de ${datos['monto_total'] / len(datos['transacciones']):.2f} MXN.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()