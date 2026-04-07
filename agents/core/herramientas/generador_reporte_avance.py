# ARCHIVO: generador_reporte_avance.py
# AREA: HERRAMIENTAS
# DESCRIPCION: Generador Reporte Avance
# TECNOLOGIA: Python

import os
import sys
import json
import datetime
import math
import re
import random

def calcula_monto_total(precio_m2, cantidad_m2):
    return precio_m2 * cantidad_m2

def calcula_monto_gastado(monto_total, avance):
    return monto_total * avance

def calcula_monto_restante(monto_total, monto_gastado):
    return monto_total - monto_gastado

def calcula_porcentaje_gastado(avance):
    return avance * 100

def calcula_porcentaje_restante(avance):
    return (1 - avance) * 100

def calcula_intereses_mora(precio_m2, cantidad_m2, avance, tasa_interes, plazo_meses):
    monto_total = calcula_monto_total(precio_m2, cantidad_m2)
    monto_gastado = calcula_monto_gastado(monto_total, avance)
    intereses_mora = monto_gastado * tasa_interes * plazo_meses / 12
    return intereses_mora

def generador_reporte_avance():
    try:
        if len(sys.argv) > 1:
            fecha_actual = sys.argv[1]
            presupuesto = float(sys.argv[2])
            avance = float(sys.argv[3])
            precio_m2 = float(sys.argv[4])
            cantidad_m2 = float(sys.argv[5])
            tasa_interes = float(sys.argv[6])
            plazo_meses = int(sys.argv[7])
        else:
            fecha_actual = datetime.date.today()
            presupuesto = 1000000
            avance = 0.5
            precio_m2 = 5000
            cantidad_m2 = 100
            tasa_interes = 0.05
            plazo_meses = 12

        cantidad_total_m2 = cantidad_m2
        monto_total = calcula_monto_total(precio_m2, cantidad_total_m2)
        monto_gastado = calcula_monto_gastado(monto_total, avance)
        monto_restante = calcula_monto_restante(monto_total, monto_gastado)
        porcentaje_gastado = calcula_porcentaje_gastado(avance)
        porcentaje_restante = calcula_porcentaje_restante(avance)
        intereses_mora = calcula_intereses_mora(precio_m2, cantidad_m2, avance, tasa_interes, plazo_meses)

        print(f"Fecha Actual: {fecha_actual}")
        print(f"Presupuesto: ${presupuesto:,.2f}")
        print(f"Precio por m2: ${precio_m2:,.2f}")
        print(f"Cantidad total de m2: {cantidad_total_m2} m2")
        print(f"Avance: {avance*100}%")
        print(f"Monto Total: ${monto_total:,.2f}")
        print(f"Monto Gastado: ${monto_gastado:,.2f}")
        print(f"Monto Restante: ${monto_restante:,.2f}")
        print(f"Porcentaje Gastado: {porcentaje_gastado}%")
        print(f"Porcentaje Restante: {porcentaje_restante}%")
        print(f"Intereses por Mora: ${intereses_mora:,.2f}")
        print(f"Plazo en Meses: {plazo_meses} meses")
        print(f"Tasa de Interes: {tasa_interes*100}%")
        print("Resumen Ejecutivo:")
        print(f"El proyecto tiene un avance del {porcentaje_gastado}% y un monto gastado de ${monto_gastado:,.2f}.")
        print(f"El monto restante es de ${monto_restante:,.2f} y los intereses por mora ascienden a ${intereses_mora:,.2f}.")
        print(f"Es importante tener en cuenta que el plazo para la finalizacion del proyecto es de {plazo_meses} meses y la tasa de interes es del {tasa_interes*100}%.") 

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    generador_reporte_avance()