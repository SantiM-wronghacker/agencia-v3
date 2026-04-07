"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza evaluador credito puente
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_credito_puente(monto, plazo, tasa_interes):
    return monto * (tasa_interes / 100) * (1 + tasa_interes / 100) ** plazo / ((1 + tasa_interes / 100) ** plazo - 1)

def calcular_interes_total(cuota, plazo, monto):
    return cuota * plazo - monto

def calcular_pago_total(monto, interes_total):
    return monto + interes_total

def calcular_tasa_mensual(tasa_anual):
    return tasa_anual / 12

def calcular_fecha_vencimiento(plazo):
    fecha_inicio = datetime.date.today()
    fecha_vencimiento = fecha_inicio + datetime.timedelta(days=plazo*30)
    return fecha_vencimiento

def calcular_amortizacion(monto, plazo, tasa_interes):
    cuotas = []
    for i in range(1, plazo + 1):
        interes = monto * (tasa_interes / 100) * (i / 12)
        capital = cuota - interes
        cuotas.append((cuota, interes, capital))
    return cuotas

def calcular_cuota(monto, plazo, tasa_interes):
    return calcular_credito_puente(monto, plazo, tasa_interes)

def calcular_pago_mensual(monto, tasa_interes, plazo):
    return calcular_tasa_mensual(tasa_interes) * (monto + (monto * calcular_tasa_mensual(tasa_interes) * plazo))

def calcular_pago_total_mensual(monto, tasa_interes, plazo):
    return calcular_pago_mensual(monto, tasa_interes, plazo) * plazo

def main():
    try:
        monto = float(sys.argv[1]) if len(sys.argv) > 1 else 1000000.0
        plazo = int(sys.argv[2]) if len(sys.argv) > 2 else 12
        tasa_interes = float(sys.argv[3]) if len(sys.argv) > 3 else 15.0
        
        if monto <= 0:
            raise ValueError("El monto del crédito debe ser mayor a cero")
        if plazo <= 0:
            raise ValueError("El plazo del crédito debe ser mayor a cero")
        if tasa_interes <= 0:
            raise ValueError("La tasa de interés debe ser mayor a cero")
        
        cuota = calcular_cuota(monto, plazo, tasa_interes)
        interes_total = calcular_interes_total(cuota, plazo, monto)
        pago_total = calcular_pago_total(monto, interes_total)
        tasa_mensual = calcular_tasa_mensual(tasa_interes)
        fecha_vencimiento = calcular_fecha_vencimiento(plazo)
        amortizacion = calcular_amortizacion(monto, plazo, tasa_interes)
        
        print("Monto del crédito: $", monto)
        print("Plazo del crédito: ", plazo, "meses")
        print("Tasa de interés anual: ", tasa_interes, "%")
        print("Cuota mensual: $", cuota)
        print("Interés total: $", interes_total)
        print("Pago total: $", pago_total)
        print("Fecha de vencimiento: ", fecha_vencimiento)
        print("Amortización:")
        for i, cuota in enumerate(amortizacion, start=1):
            print("Cuota #", i, ":", cuota)
        print("Resumen ejecutivo:")
        print("El crédito tiene un monto de $", monto, "y un plazo de", plazo, "meses.")
        print("La tasa de interés anual es de", tasa_interes, "%.")
        print("La cuota mensual es de $", cuota, "y el interés total es de $", interes_total)
        print("El pago total es de $", pago_total, "y la fecha de vencimiento es", fecha_vencimiento)
        
    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()