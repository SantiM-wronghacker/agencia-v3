#!/usr/bin/env python3
# ÁREA: FINANZAS
# DESCRIPCIÓN: Agente que realiza cálculo de impuesto sobre la renta mensual con parámetros realistas para México
# TECNOLOGÍA: Python estándar

import sys
import math

def calculo_impuesto(renta_mensual, deducciones, isr_anterior=0):
    try:
        # Tablas de ISR 2023 para México (simplificadas)
        if renta_mensual <= 7333.33:
            tarifa = 0.0192
            limite_inferior = 0.0
            excedente = 0.0
        elif renta_mensual <= 10552.33:
            tarifa = 0.064
            limite_inferior = 7333.33
            excedente = renta_mensual - limite_inferior
        elif renta_mensual <= 14965.97:
            tarifa = 0.1088
            limite_inferior = 10552.33
            excedente = renta_mensual - limite_inferior
        elif renta_mensual <= 18805.91:
            tarifa = 0.16
            limite_inferior = 14965.97
            excedente = renta_mensual - limite_inferior
        elif renta_mensual <= 25920.36:
            tarifa = 0.1792
            limite_inferior = 18805.91
            excedente = renta_mensual - limite_inferior
        elif renta_mensual <= 38195.55:
            tarifa = 0.2136
            limite_inferior = 25920.36
            excedente = renta_mensual - limite_inferior
        elif renta_mensual <= 73333.33:
            tarifa = 0.2352
            limite_inferior = 38195.55
            excedente = renta_mensual - limite_inferior
        elif renta_mensual <= 97666.67:
            tarifa = 0.30
            limite_inferior = 73333.33
            excedente = renta_mensual - limite_inferior
        elif renta_mensual <= 129800.00:
            tarifa = 0.32
            limite_inferior = 97666.67
            excedente = renta_mensual - limite_inferior
        elif renta_mensual <= 161933.33:
            tarifa = 0.34
            limite_inferior = 129800.00
            excedente = renta_mensual - limite_inferior
        else:
            tarifa = 0.35
            limite_inferior = 161933.33
            excedente = renta_mensual - limite_inferior

        # Cálculo del ISR
        isr = (excedente * tarifa) + isr_anterior
        renta_neta = renta_mensual - deducciones - isr
        return isr, renta_neta
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def main():
    if len(sys.argv) != 4:
        print("Uso: python calculo_impuesto_sobre_renta_mensual.py <renta_mensual> <deducciones> <isr_anterior>")
        return

    try:
        renta_mensual = float(sys.argv[1])
        deducciones = float(sys.argv[2])
        isr_anterior = float(sys.argv[3])

        isr, renta_neta = calculo_impuesto(renta_mensual, deducciones, isr_anterior)

        if isr is not None and renta_neta is not None:
            print(f"ISR: {isr:.2f}")
            print(f"Renta Neta: {renta_neta:.2f}")
            print(f"Renta Mensual: {renta_mensual:.2f}")
            print(f"Deducciones: {deducciones:.2f}")
            print(f"ISR Anterior: {isr_anterior:.2f}")
            print(f"Resumen Ejecutivo: El impuesto sobre la renta mensual es de {isr:.2f} y la renta neta es de {renta_neta:.2f}")
    except ValueError:
        print("Error: Los valores deben ser números")

if __name__ == "__main__":
    main()