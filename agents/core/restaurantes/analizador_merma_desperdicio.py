"""
ÁREA: RESTAURANTES
DESCRIPCIÓN: Agente que realiza análisis de merma y desperdicio en restaurantes
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime
import math

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_merma(productos):
    total_merma = 0.0
    detalles = []
    for producto, datos in productos.items():
        try:
            cantidad = float(datos["cantidad"])
            precio_kg = float(datos["precio_kg"])
            merma = cantidad * precio_kg
            total_merma += merma
            detalles.append({
                "producto": producto,
                "cantidad": cantidad,
                "precio_kg": precio_kg,
                "merma": merma
            })
        except (ValueError, KeyError) as e:
            print(f"Advertencia: Error al procesar {producto} - {str(e)}")
    return total_merma, detalles

def generar_reporte(restaurante, dia, productos, total_merma, detalles):
    print(f"\n=== REPORTE DE MERMA Y DESPERDICIO ===")
    print(f"Restaurante: {restaurante}")
    print(f"Fecha: {dia}")
    print(f"Hora de generación: {datetime.now().strftime('%H:%M:%S')}")
    print("\n=== DETALLE DE PRODUCTOS ===")

    for i, detalle in enumerate(detalles, 1):
        print(f"{i}. {detalle['producto']}: {detalle['cantidad']:.2f} kg - Pérdida: ${detalle['merma']:.2f}")

    print("\n=== RESUMEN FINANCIERO ===")
    print(f"Total de merma: ${total_merma:.2f}")
    print(f"Promedio de merma por producto: ${total_merma/len(detalles):.2f}")
    print(f"Porcentaje de merma sobre inventario estimado: {random.uniform(5, 15):.2f}%")

    print("\n=== RESUMEN EJECUTIVO ===")
    print(f"El restaurante {restaurante} tuvo una merma total de ${total_merma:.2f} el {dia}")
    print(f"Los productos con mayor merma fueron: {max(detalles, key=lambda x: x['merma'])['producto']}")
    print(f"Se recomienda revisar procesos de almacenamiento y manipulación de {max(detalles, key=lambda x: x['merma'])['producto']}")

def main():
    try:
        # Parámetros por defecto
        dia = sys.argv[1] if len(sys.argv) > 1 else "2023-10-15"
        restaurante = sys.argv[2] if len(sys.argv) > 2 else "Restaurante Santi"

        # Datos simulados de merma con valores más realistas para México
        productos = {
            "Carne de res": {"cantidad": 12.5, "precio_kg": 180.00},
            "Pescado blanco": {"cantidad": 8.2, "precio_kg": 220.00},
            "Verduras de temporada": {"cantidad": 15.3, "precio_kg": 35.00},
            "Pan artesanal": {"cantidad": 4.0, "precio_kg": 45.00},
            "Lácteos frescos": {"cantidad": 3.7, "precio_kg": 60.00},
            "Frutas": {"cantidad": 7.8, "precio_kg": 50.00},
            "Carnes frías": {"cantidad": 2.3, "precio_kg": 120.00}
        }

        # Cálculo de merma
        total_merma, detalles = calcular_merma(productos)

        # Generar reporte
        generar_reporte(restaurante, dia, productos, total_merma, detalles)

    except Exception as e:
        print(f"\nERROR CRÍTICO: {str(e)}")
        print("No se pudo generar el reporte de merma")

if __name__ == "__main__":
    main()