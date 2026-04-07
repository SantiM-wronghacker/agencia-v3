#!/usr/bin/env python3
# AREA: FINANZAS
# DESCRIPCIÓN: Agente que realiza simulador de inversión en CETES con cálculos precisos para México
# TECNOLOGÍA: Python estándar

import sys
import math
from datetime import datetime, timedelta

def calcular_intereses(monto, tasa, dias):
    # Cálculo de intereses con redondeo a 4 decimales para mayor precisión
    intereses = monto * (tasa / 365) * dias
    return round(intereses, 4)

def calcular_iva(intereses):
    # Cálculo del IVA sobre intereses (16% en México)
    return intereses * 0.16

def calcular_neto(intereses, iva):
    # Cálculo del monto neto después de impuestos
    return intereses - iva

def calcular_rentabilidad(monto, neto):
    # Cálculo de la rentabilidad
    return (neto / monto) * 100

def calcular_tasa_efectiva(tasa_anual, dias):
    # Cálculo de la tasa efectiva
    return (1 + tasa_anual / 365) ** dias - 1

def calcular_monto_total(monto, neto):
    # Cálculo del monto total
    return monto + neto

def calcular_plazo_efectivo(dias):
    # Cálculo del plazo efectivo
    return f"{dias} días"

def calcular_fecha_vencimiento(fecha_inicio, dias):
    # Cálculo de la fecha de vencimiento
    fecha_vencimiento = fecha_inicio + timedelta(days=dias)
    return fecha_vencimiento.strftime("%Y-%m-%d")

def main():
    try:
        # Parámetros por defecto
        monto = float(sys.argv[1]) if len(sys.argv) > 1 else 10000.0
        tasa_anual = float(sys.argv[2]) if len(sys.argv) > 2 else 0.07  # 7%
        dias = int(sys.argv[3]) if len(sys.argv) > 3 else 28

        # Validaciones
        if monto <= 0 or tasa_anual <= 0 or dias <= 0:
            print("Error: Valores deben ser positivos")
            return

        if tasa_anual > 1:
            print("Error: Tasa anual debe ser menor o igual a 1 (100%)")
            return

        if dias > 365:
            print("Error: Plazo máximo es 1 año")
            return

        # Cálculos
        intereses = calcular_intereses(monto, tasa_anual, dias)
        iva = calcular_iva(intereses)
        neto = calcular_neto(intereses, iva)
        total = calcular_monto_total(monto, neto)
        rentabilidad = calcular_rentabilidad(monto, neto)
        tasa_efectiva = calcular_tasa_efectiva(tasa_anual, dias)
        plazo_efectivo = calcular_plazo_efectivo(dias)
        fecha_vencimiento = calcular_fecha_vencimiento(datetime.now(), dias)

        # Resultados
        print("=== SIMULADOR DE INVERSIÓN EN CETES ===")
        print(f"Fecha de inicio: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"Fecha de vencimiento: {fecha_vencimiento}")
        print(f"Monto inicial: ${monto:.2f}")
        print(f"Tasa anual: {tasa_anual*100:.2f}%")
        print(f"Plazo: {dias} días ({plazo_efectivo})")
        print(f"Intereses: ${intereses:.2f}")
        print(f"IVA: ${iva:.2f}")
        print(f"Monto neto: ${neto:.2f}")
        print(f"Monto total: ${total:.2f}")
        print(f"Rentabilidad: {rentabilidad:.2f}%")
        print(f"Tasa efectiva: {tasa_efectiva*100:.2f}%")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print("El simulador de inversión en CETES calcula el monto neto y total después de impuestos, así como la rentabilidad y tasa efectiva de la inversión.")

    except IndexError:
        print("Error: Faltan parámetros")
    except ValueError:
        print("Error: Valores no numéricos")