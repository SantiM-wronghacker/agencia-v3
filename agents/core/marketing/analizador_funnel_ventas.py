"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza analizador funnel ventas
TECNOLOGÍA: Python estándar
"""

import sys
import json
import os
from datetime import datetime
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
        mes = sys.argv[1] if len(sys.argv) > 1 else "2023-10"
        archivo = sys.argv[2] if len(sys.argv) > 2 else "ventas.json"

        # Datos simulados de funnel de ventas (MXN)
        datos = {
            "prospectos": random.randint(500, 1000),
            "contactados": random.randint(300, 600),
            "cotizaciones": random.randint(150, 300),
            "ofertas": random.randint(100, 200),
            "ventas": random.randint(50, 100),
            "ingresos": random.randint(500000, 1000000)
        }

        # Guardar datos en archivo JSON
        with open(archivo, 'w') as f:
            json.dump({mes: datos}, f)

        # Análisis
        conversion_prospecto = (datos["ventas"] / datos["prospectos"]) * 100 if datos["prospectos"] > 0 else 0
        conversion_contactado = (datos["ventas"] / datos["contactados"]) * 100 if datos["contactados"] > 0 else 0
        conversion_cotizacion = (datos["ventas"] / datos["cotizaciones"]) * 100 if datos["cotizaciones"] > 0 else 0
        conversion_oferta = (datos["ventas"] / datos["ofertas"]) * 100 if datos["ofertas"] > 0 else 0

        # Resultados
        print(f"Análisis de funnel de ventas para {mes}")
        print(f"1. Prospectos: {datos['prospectos']} | Contactados: {datos['contactados']} (Conversión: {conversion_prospecto:.2f}%)")
        print(f"2. Cotizaciones: {datos['cotizaciones']} | Ofertas: {datos['ofertas']} (Conversión: {conversion_contactado:.2f}%)")
        print(f"3. Ventas realizadas: {datos['ventas']} | Ingresos: ${datos['ingresos']:,.2f} MXN")
        print(f"4. Tasa de conversión final: {conversion_oferta:.2f}%")
        print(f"5. Archivo guardado: {os.path.abspath(archivo)}")
        print(f"6. Promedio de ingresos por venta: ${datos['ingresos'] / datos['ventas'] if datos['ventas'] > 0 else 0:,.2f} MXN")
        print(f"7. Tasa de crecimiento de ventas: {(datos['ventas'] / datos['prospectos']) * 100 if datos['prospectos'] > 0 else 0:.2f}%")
        print(f"8. Número de prospectos que no se convirtieron en ventas: {datos['prospectos'] - datos['ventas']}")
        print(f"9. Número de contactados que no se convirtieron en ofertas: {datos['contactados'] - datos['ofertas']}")
        print(f"10. Número de cotizaciones que no se convirtieron en ventas: {datos['cotizaciones'] - datos['ventas']}")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El análisis de funnel de ventas para {mes} muestra un total de {datos['prospectos']} prospectos, de los cuales {datos['ventas']} se convirtieron en ventas.")
        print(f"La tasa de conversión final es del {conversion_oferta:.2f}% y el promedio de ingresos por venta es de ${datos['ingresos'] / datos['ventas'] if datos['ventas'] > 0 else 0:,.2f} MXN.")
        print(f"Es importante destacar que {datos['prospectos'] - datos['ventas']} prospectos no se convirtieron en ventas y que {datos['cotizaciones'] - datos['ventas']} cotizaciones no se convirtieron en ventas.")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()