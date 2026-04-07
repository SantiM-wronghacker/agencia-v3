"""
ÁREA: CEREBRO
DESCRIPCIÓN: Agente que realiza agente validacion resultados
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
        # Configuración por defecto
        resultados_por_defecto = {
            "ventas": 100000,
            "clientes": 500,
            "productos": 200,
            "tasa_iva": 0.16,
            "tasa_isr": 0.10
        }

        # Obtener argumentos de la línea de comandos
        if len(sys.argv) > 1:
            resultados = json.loads(sys.argv[1])
        else:
            resultados = resultados_por_defecto

        # Validar resultados
        if resultados["ventas"] < 0 or resultados["clientes"] < 0 or resultados["productos"] < 0:
            print("Error: Resultados no pueden ser negativos")
            return

        if resultados["clientes"] == 0:
            print("Error: No se pueden calcular estadísticas con cero clientes")
            return

        # Calcular estadísticas
        promedio_ventas_por_cliente = resultados["ventas"] / resultados["clientes"]
        promedio_productos_por_cliente = resultados["productos"] / resultados["clientes"]
        total_iva = resultados["ventas"] * resultados["tasa_iva"]
        total_isr = resultados["ventas"] * resultados["tasa_isr"]
        utilidad_neta = resultados["ventas"] - total_iva - total_isr

        # Imprimir resultados
        print(f"Fecha: {datetime.date.today()}")
        print(f"Ventas: ${resultados['ventas']:.2f} MXN")
        print(f"Clientes: {resultados['clientes']}")
        print(f"Productos: {resultados['productos']}")
        print(f"Promedio de ventas por cliente: ${promedio_ventas_por_cliente:.2f} MXN")
        print(f"Promedio de productos por cliente: {promedio_productos_por_cliente:.2f}")
        print(f"Total IVA: ${total_iva:.2f} MXN")
        print(f"Total ISR: ${total_isr:.2f} MXN")
        print(f"Utilidad neta: ${utilidad_neta:.2f} MXN")
        print(f"Tasa de crecimiento de ventas: {(resultados['ventas'] / resultados['clientes']) * 100:.2f}%")
        print(f"Tasa de satisfacción del cliente: {(resultados['clientes'] / resultados['productos']) * 100:.2f}%")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"La empresa ha obtenido ${resultados['ventas']:.2f} MXN en ventas, con un promedio de ${promedio_ventas_por_cliente:.2f} MXN por cliente.")
        print(f"El total de IVA y ISR es de ${total_iva + total_isr:.2f} MXN, lo que representa una utilidad neta de ${utilidad_neta:.2f} MXN.")
        print(f"La tasa de crecimiento de ventas es del {(resultados['ventas'] / resultados['clientes']) * 100:.2f}% y la tasa de satisfacción del cliente es del {(resultados['clientes'] / resultados['productos']) * 100:.2f}%.")

    except Exception as e:
        print(f"Error: {str(e)}")

    except ZeroDivisionError:
        print("Error: No se pueden calcular estadísticas con cero clientes")

    except json.JSONDecodeError:
        print("Error: El formato del JSON es incorrecto")

if __name__ == "__main__":
    main()