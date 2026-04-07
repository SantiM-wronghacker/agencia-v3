"""
ÁREA: LEGAL
DESCRIPCIÓN: Agente que realiza calculadora penalizaciones
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random
import os

def calcular_penalizacion(monto, dias_retraso, tasa_interes=0.05):
    try:
        if dias_retraso < 0:
            raise ValueError("Días de retraso no puede ser negativo")
        if monto < 0:
            raise ValueError("Monto no puede ser negativo")
        if tasa_interes < 0:
            raise ValueError("Tasa de interés no puede ser negativa")
        penalizacion = monto * tasa_interes * (dias_retraso / 365)
        return penalizacion
    except Exception as e:
        print(f"Error en calcular_penalizacion: {str(e)}")
        return None

def calcular_monto_total(monto, penalizacion):
    try:
        if monto < 0:
            raise ValueError("Monto no puede ser negativo")
        if penalizacion < 0:
            raise ValueError("Penalización no puede ser negativa")
        monto_total = monto + penalizacion
        return monto_total
    except Exception as e:
        print(f"Error en calcular_monto_total: {str(e)}")
        return None

def calcular_iva(monto_total, tasa_iva=0.16):
    try:
        if monto_total < 0:
            raise ValueError("Monto total no puede ser negativo")
        if tasa_iva < 0:
            raise ValueError("Tasa de IVA no puede ser negativa")
        iva = monto_total * tasa_iva
        return iva
    except Exception as e:
        print(f"Error en calcular_iva: {str(e)}")
        return None

def calcular_total_con_iva(monto_total, iva):
    try:
        if monto_total < 0:
            raise ValueError("Monto total no puede ser negativo")
        if iva < 0:
            raise ValueError("IVA no puede ser negativo")
        total_con_iva = monto_total + iva
        return total_con_iva
    except Exception as e:
        print(f"Error en calcular_total_con_iva: {str(e)}")
        return None

def main():
    try:
        if len(sys.argv) > 1:
            monto = float(sys.argv[1])
            dias_retraso = int(sys.argv[2])
        else:
            monto = 1000.0  # Monto original
            dias_retraso = 30  # Días de retraso

        # Calcular penalización
        penalizacion = calcular_penalizacion(monto, dias_retraso)

        # Calcular monto total
        monto_total = calcular_monto_total(monto, penalizacion)

        # Calcular IVA
        iva = calcular_iva(monto_total)

        # Calcular total con IVA
        total_con_iva = calcular_total_con_iva(monto_total, iva)

        # Imprimir resultados
        print(f"Monto original: ${monto:.2f} MXN")
        print(f"Días de retraso: {dias_retraso} días")
        print(f"Penalización: ${penalizacion:.2f} MXN")
        print(f"Monto total: ${monto_total:.2f} MXN")
        print(f"IVA (16%): ${iva:.2f} MXN")
        print(f"Total con IVA: ${total_con_iva:.2f} MXN")
        print(f"Fecha de cálculo: {datetime.date.today()}")
        print(f"Hora de cálculo: {datetime.datetime.now().time()}")
        print("Resumen ejecutivo:")
        print(f"El monto total con penalización y IVA es de ${total_con_iva:.2f} MXN")
        print(f"La penalización es de ${penalizacion:.2f} MXN")
        print(f"El IVA es de ${iva:.2f} MXN")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()