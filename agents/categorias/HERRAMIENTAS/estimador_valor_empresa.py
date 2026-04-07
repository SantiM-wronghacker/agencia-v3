"""
AREA: FINANZAS
DESCRIPCION: Agente que realiza estimador valor empresa
TECNOLOGIA: Python estándar
"""

import sys
import json
import math
import random
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def estimador_valor_empresa(ingresos_anuales, gastos_anuales, activos, pasivos, tasa_interes, tasa_inflacion):
    try:
        utilidad_neta = ingresos_anuales - gastos_anuales
        valor_empresa = (utilidad_neta / (tasa_interes - tasa_inflacion)) + activos - pasivos
        if valor_empresa < 0:
            raise ValueError("El valor de la empresa no puede ser negativo")
        return valor_empresa
    except ZeroDivisionError:
        raise ValueError("La tasa de interés no puede ser igual a la tasa de inflación")

def calcular_tasa_interes(tipo_tasa):
    if tipo_tasa == "corta":
        return 0.05
    elif tipo_tasa == "larga":
        return 0.10
    else:
        raise ValueError("Tipo de tasa no válida")

def calcular_tasa_inflacion():
    return 0.03

def calcular_impuesto_sobre_utilidades(utilidad_neta):
    return utilidad_neta * 0.25

def calcular_depreciacion(activos):
    return activos * 0.05

def calcular_intereses_pasivos(pasivos, tasa_interes):
    return pasivos * tasa_interes

def main():
    try:
        ingresos_anuales = float(sys.argv[1]) if len(sys.argv) > 1 else 10000000.0
        gastos_anuales = float(sys.argv[2]) if len(sys.argv) > 2 else 5000000.0
        activos = float(sys.argv[3]) if len(sys.argv) > 3 else 20000000.0
        pasivos = float(sys.argv[4]) if len(sys.argv) > 4 else 5000000.0
        tipo_tasa = sys.argv[5] if len(sys.argv) > 5 else "corta"

        tasa_interes = calcular_tasa_interes(tipo_tasa)
        tasa_inflacion = calcular_tasa_inflacion()

        utilidad_neta = ingresos_anuales - gastos_anuales
        valor_empresa = estimador_valor_empresa(ingresos_anuales, gastos_anuales, activos, pasivos, tasa_interes, tasa_inflacion)
        impuesto_sobre_utilidades = calcular_impuesto_sobre_utilidades(utilidad_neta)
        depreciacion = calcular_depreciacion(activos)
        intereses_pasivos = calcular_intereses_pasivos(pasivos, tasa_interes)

        print(f"Valor de la empresa: {valor_empresa:.2f} MXN")
        print(f"Ingresos anuales: {ingresos_anuales:.2f} MXN")
        print(f"Gastos anuales: {gastos_anuales:.2f} MXN")
        print(f"Activos: {activos:.2f} MXN")
        print(f"Pasivos: {pasivos:.2f} MXN")
        print(f"Utilidad neta: {utilidad_neta:.2f} MXN")
        print(f"Impuesto sobre utilidades: {impuesto_sobre_utilidades:.2f} MXN")
        print(f"Depreciacion: {depreciacion:.2f} MXN")
        print(f"Intereses pasivos: {intereses_pasivos:.2f} MXN")
        print(f"Fecha de evaluacion: {datetime.now().strftime('%Y-%m-%d')}")
        print("Resumen ejecutivo:")
        print(f"La empresa tiene un valor de {valor_empresa:.2f} MXN y una utilidad neta de {utilidad_neta:.2f} MXN.")
        print(f"Los gastos anuales son de {gastos_anuales:.2f} MXN y los activos totales son de {activos:.2f} MXN.")
        print(f"La empresa tiene pasivos por {pasivos:.2f} MXN y paga intereses pasivos de {intereses_pasivos:.2f} MXN.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()