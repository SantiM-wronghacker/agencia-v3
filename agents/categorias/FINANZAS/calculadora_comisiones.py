"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora comisiones
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def calculadora_comisiones(venta, comision, descuento, tipo_cambio=None):
    try:
        # Validaciones
        if venta <= 0:
            raise ValueError("Venta no válida")
        if comision < 0 or comision > 100:
            raise ValueError("Comisión no válida")
        if descuento < 0 or descuento > 100:
            raise ValueError("Descuento no válido")

        # Calcula comisión
        comision_calculada = venta * comision / 100

        # Aplica descuento
        comision_descuento = comision_calculada * (1 - descuento / 100)

        # Muestra resultados
        print(f"Fecha: {datetime.date.today()}")
        print(f"Venta: {venta:.2f} MXN")
        print(f"Comisión: {comision_calculada:.2f} MXN")
        print(f"Descuento: {descuento:.2f}%")
        print(f"Comisión con descuento: {comision_descuento:.2f} MXN")
        print(f"Margen de beneficio: {(comision_calculada / venta) * 100:.2f}%")
        print(f"Margen de beneficio con descuento: {(comision_descuento / venta) * 100:.2f}%")
        print(f"Ingresos totales sin comisión: {venta * (1 - comision / 100):.2f} MXN")
        print(f"Ingresos totales con comisión y descuento: {venta - comision_descuento:.2f} MXN")
        print(f"Diferencia entre ingresos totales: {(venta * (1 - comision / 100)) - (venta - comision_descuento):.2f} MXN")
        print(f"Ingresos totales con impuestos (15%): {(venta * 1.15 - comision_descuento):.2f} MXN")
        print(f"Ingresos totales con impuestos y descuento: {(venta * 1.15 - comision_descuento):.2f} MXN")

        # Si hay conexión a internet y tipo de cambio
        if WEB and tipo_cambio:
            # Calcula comisión con datos reales
            comision_calculada = venta * comision / 100 * tipo_cambio

            # Muestra resultados con datos reales
            print(f"Precio venta: {venta:.2f} MXN")
            print(f"Tipo de cambio: {tipo_cambio:.2f}")
            print(f"Comisión con datos reales: {comision_calculada:.2f} MXN")
            print(f"Ingresos totales con comisión y tipo de cambio: {venta * tipo_cambio - comision_calculada:.2f} MXN")

        # Resumen ejecutivo
        print(f"Total de comisiones: {comision_calculada:.2f} MXN")
        print(f"Ingresos totales con comisión y descuento: {venta - comision_descuento:.2f} MXN")
        print(f"Margen de beneficio con descuento: {(comision_descuento / venta) * 100:.2f}%")

    except ValueError as e:
        print(f"Error: {e}")

def main():
    # Obtiene parámetros desde sys.argv
    if len(sys.argv) != 4:
        print("Uso: python calculadora_comisiones.py <venta> <comision> <descuento>")
        return
    venta = float(sys.argv[1])
    comision = float(sys.argv[2])
    descuento = float(sys.argv[3])

    # Llama a la función principal
    calculadora_comisiones(venta, comision, descuento)

if __name__ == "__main__":
    main()