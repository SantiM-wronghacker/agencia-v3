#!/usr/bin/env python3
"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora retorno desarrollo obra
TECNOLOGÍA: Python estándar
"""

import sys
import math
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        precio_venta = float(sys.argv[1]) if len(sys.argv) > 1 else 10000000.0  # Precio de venta del inmueble
        costo_construccion = float(sys.argv[2]) if len(sys.argv) > 2 else 8000000.0  # Costo de construcción
        costo_terreno = float(sys.argv[3]) if len(sys.argv) > 3 else 1000000.0  # Costo del terreno
        tasa_interes = float(sys.argv[4]) if len(sys.argv) > 4 else 0.08  # Tasa de interés anual
        plazo = int(sys.argv[5]) if len(sys.argv) > 5 else 2  # Plazo de la inversión en años
        impuestos = float(sys.argv[6]) if len(sys.argv) > 6 else 0.10  # Impuestos sobre la venta
        gastos_administrativos = float(sys.argv[7]) if len(sys.argv) > 7 else 0.05  # Gastos administrativos
        margen_utilidad = float(sys.argv[8]) if len(sys.argv) > 8 else 0.20  # Margen de utilidad

        # Cálculo del retorno de la inversión
        retorno_inversion = (precio_venta - (costo_construccion + costo_terreno)) / (costo_construccion + costo_terreno)
        retorno_inversion_anual = (1 + retorno_inversion) ** (1 / plazo) - 1

        # Cálculo del valor actual neto (VAN)
        van = (precio_venta * (1 - impuestos) / (1 + tasa_interes) ** plazo) - (costo_construccion + costo_terreno) * (1 + gastos_administrativos)

        # Cálculo de la tasa interna de retorno (TIR)
        tir = (precio_venta / (costo_construccion + costo_terreno)) ** (1 / plazo) - 1

        # Cálculo del punto de equilibrio
        punto_equilibrio = (costo_construccion + costo_terreno) / (1 - impuestos)

        # Cálculo del precio de venta mínimo para obtener una rentabilidad del 20%
        precio_venta_minimo = (costo_construccion + costo_terreno) / (1 - margen_utilidad)

        print(f"ÁREA: FINANZAS")
        print(f"DESCRIPCIÓN: Agente que realiza calculadora retorno desarrollo obra")
        print(f"TECNOLOGÍA: Python estándar")
        print(f"Precio de venta: ${precio_venta:,.2f} MXN")
        print(f"Costo de construcción: ${costo_construccion:,.2f} MXN")
        print(f"Costo del terreno: ${costo_terreno:,.2f} MXN")
        print(f"Retorno de la inversión: {retorno_inversion:.2%}")
        print(f"Retorno de la inversión anual: {retorno_inversion_anual:.2%}")
        print(f"Valor actual neto (VAN): ${van:,.2f} MXN")
        print(f"Tasa interna de retorno (TIR): {tir:.2%}")
        print(f"Punto de equilibrio: ${punto_equilibrio:,.2f} MXN")
        print(f"Precio de venta mínimo para obtener una rentabilidad del 20%: ${precio_venta_minimo:,.2f} MXN")
        print(f"Resumen ejecutivo: El desarrollo de la obra tendría una rentabilidad del {retorno_inversion*100:.2f}% y un valor actual neto de ${van:,.2f} MXN.")

    except IndexError:
        print("Error: Faltan parámetros de entrada.")
    except ValueError:
        print("Error: Los parámetros de entrada no son numéricos.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()