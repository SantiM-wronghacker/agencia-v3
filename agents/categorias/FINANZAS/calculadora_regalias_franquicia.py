# FRANQUICIAS / Calculadora de Regalias Franquicia / Python
# AREA: FINANZAS
# DESCRIPCION: FRANQUICIAS / Calculadora de Regalias Franquicia / Python
# TECNOLOGIA: Python

import sys
import json
import datetime
import math
import re

def calcular_regalias(ventas, porcentaje_regalia, iva=0.16, isr=0.1):
    try:
        regalia = ventas * porcentaje_regalia / 100
        iva_regalia = regalia * iva
        isr_regalia = regalia * isr
        total_regalia = regalia + iva_regalia + isr_regalia
        return regalia, iva_regalia, isr_regalia, total_regalia
    except ZeroDivisionError:
        print("Error: No se puede calcular regalia con porcentaje de 0%")
        return None

def calcular_margenes(ventas, total_regalia):
    try:
        margen_utilidad = (ventas - total_regalia) / ventas * 100
        margen_regalia = total_regalia / ventas * 100
        return margen_utilidad, margen_regalia
    except ZeroDivisionError:
        print("Error: No se puede calcular margen con ventas de 0")
        return None

def calcular_impuestos(ventas, iva=0.16, isr=0.1):
    try:
        iva_venta = ventas * iva
        isr_venta = ventas * isr
        return iva_venta, isr_venta
    except ZeroDivisionError:
        print("Error: No se puede calcular impuestos con ventas de 0")
        return None

def calcular_utilidad_neta(ventas, total_regalia, iva_venta, isr_venta):
    try:
        return ventas - total_regalia - iva_venta - isr_venta
    except TypeError:
        print("Error: No se pueden calcular utilidades con valores no numéricos")
        return None

def main():
    try:
        ventas = float(sys.argv[1]) if len(sys.argv) > 1 else 100000.0
        porcentaje_regalia = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
        iva = float(sys.argv[3]) if len(sys.argv) > 3 else 0.16
        isr = float(sys.argv[4]) if len(sys.argv) > 4 else 0.1
        regalia, iva_regalia, isr_regalia, total_regalia = calcular_regalias(ventas, porcentaje_regalia, iva, isr)
        margen_utilidad, margen_regalia = calcular_margenes(ventas, total_regalia)
        iva_venta, isr_venta = calcular_impuestos(ventas, iva, isr)
        utilidad_neta = calcular_utilidad_neta(ventas, total_regalia, iva_venta, isr_venta)
        print(f"Fecha de calculo: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Ventas: ${ventas:,.2f} MXN")
        print(f"Porcentaje de regalia: {porcentaje_regalia}%")
        print(f"Regalia: ${regalia:,.2f} MXN")
        print(f"IVA ({iva*100}%): ${iva_regalia:,.2f} MXN")
        print(f"ISR ({isr*100}%): ${isr_regalia:,.2f} MXN")
        print(f"Total de regalia: ${total_regalia:,.2f} MXN")
        print(f"Total a pagar: ${ventas - total_regalia:,.2f} MXN")
        print(f"Utilidad: ${utilidad_neta:,.2f} MXN")
        print(f"Margen de utilidad: {margen_utilidad}%")
        print(f"Margen de regalia: {margen_regalia}%")
        print("Resumen ejecutivo:")
        print(f"La empresa tiene una utilidad neta de ${utilidad_neta:,.2f} MXN")
        print(f"El margen de utilidad es de {margen_utilidad}%")
        print(f"El margen de regalia es de {margen_regalia}%")
    except IndexError:
        print("Error: No se proporcionaron suficientes argumentos")
    except ValueError:
        print("Error: Los argumentos proporcionados no son numéricos")

if __name__ == "__main__":
    main()