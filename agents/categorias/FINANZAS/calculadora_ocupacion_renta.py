#!/usr/bin/env python3
"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora ocupacion renta
TECNOLOGÍA: Python estándar
"""

import sys
import math
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_ocupacion_renta(precio_alquiler, precio_venta, tasa_interes_anual, gastos_mensuales, impuestos_anuales, seguro_anual):
    try:
        tasa_interes_mensual = tasa_interes_anual / 12
        ocupacion_renta = (precio_alquiler / precio_venta) * 12
        ocupacion_renta_descontada = ocupacion_renta - (gastos_mensuales / precio_venta) * 12 - (impuestos_anuales / precio_venta) - (seguro_anual / precio_venta) / 12
        rentabilidad_anual = precio_alquiler * 12 - gastos_mensuales * 12 - impuestos_anuales - seguro_anual / 12
        return ocupacion_renta, ocupacion_renta_descontada, rentabilidad_anual
    except ZeroDivisionError:
        print("Error: Precio de venta no puede ser cero.")
        return None

def calcular_gastos_totales(gastos_mensuales, meses):
    return gastos_mensuales * meses

def calcular_rentabilidad_total(rentabilidad_anual, meses):
    return rentabilidad_anual * meses

def calcular_pago_mensual(rentabilidad_anual, meses):
    return rentabilidad_anual / meses

def calcular_tasa_rentabilidad(rentabilidad_anual, precio_venta):
    return (rentabilidad_anual / precio_venta) * 100

def main():
    try:
        precio_alquiler = float(sys.argv[1]) if len(sys.argv) > 1 else 15000.0
        precio_venta = float(sys.argv[2]) if len(sys.argv) > 2 else 2000000.0
        tasa_interes_anual = float(sys.argv[3]) if len(sys.argv) > 3 else 8.0
        gastos_mensuales = float(sys.argv[4]) if len(sys.argv) > 4 else 5000.0
        impuestos_anuales = float(sys.argv[5]) if len(sys.argv) > 5 else 20000.0
        seguro_anual = float(sys.argv[6]) if len(sys.argv) > 6 else 10000.0
        meses = int(sys.argv[7]) if len(sys.argv) > 7 else 12

        ocupacion_renta, ocupacion_renta_descontada, rentabilidad_anual = calcular_ocupacion_renta(precio_alquiler, precio_venta, tasa_interes_anual, gastos_mensuales, impuestos_anuales, seguro_anual)

        if ocupacion_renta:
            gastos_totales = calcular_gastos_totales(gastos_mensuales, meses)
            rentabilidad_total = calcular_rentabilidad_total(rentabilidad_anual, meses)
            pago_mensual = calcular_pago_mensual(rentabilidad_anual, meses)
            tasa_rentabilidad = calcular_tasa_rentabilidad(rentabilidad_anual, precio_venta)

            print("Ocupación renta:", ocupacion_renta)
            print("Ocupación renta descontada:", ocupacion_renta_descontada)
            print("Rentabilidad anual:", rentabilidad_anual)
            print("Gastos totales:", gastos_totales)
            print("Rentabilidad total:", rentabilidad_total)
            print("Pago mensual:", pago_mensual)
            print("Tasa de rentabilidad:", tasa_rentabilidad)

            print("\nResumen ejecutivo:")
            print("La inversión en este proyecto tiene una ocupación renta de {:.2f}% y una rentabilidad anual de ${:.2f}.".format(ocupacion_renta, rentabilidad_anual))
            print("Los gastos totales ascienden a ${:.2f} y la rentabilidad total es de ${:.2f}.".format(gastos_totales, rentabilidad_total))
            print("El pago mensual es de ${:.2f} y la tasa de rentabilidad es de {:.2f}%.".format(pago_mensual, tasa_rentabilidad))

    except IndexError:
        print("Error: Faltan argumentos de entrada.")
    except ValueError:
        print("Error: Los argumentos de entrada deben ser números.")

if __name__ == "__main__":
    main()