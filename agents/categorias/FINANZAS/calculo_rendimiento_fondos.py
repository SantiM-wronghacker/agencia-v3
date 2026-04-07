import sys
import json
import datetime
import math
import os

# AREA: FINANZAS
# DESCRIPCION: Agente que realiza calculo rendimiento fondos
# TECNOLOGIA: Python

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calculo_rendimiento_fondos(inversion, tasa_interes, plazo):
    """Calcula el rendimiento total de una inversión"""
    return inversion * (1 + tasa_interes/100) ** plazo

def calculo_rendimiento_anual(rendimiento, inversion, plazo):
    """Calcula el rendimiento anual de una inversión"""
    return (rendimiento - inversion) / plazo

def calculo_tasa_inflacion(rendimiento, tasa_inflacion, plazo):
    """Calcula el rendimiento real ajustado por inflación"""
    return rendimiento / (1 + tasa_inflacion/100) ** plazo

def calculo_ganancia(inversion, rendimiento):
    """Calcula la ganancia en porcentaje"""
    return (rendimiento - inversion) / inversion * 100

def calculo_pago_mensual(rendimiento, plazo):
    """Calcula el pago mensual de una inversión"""
    return rendimiento / plazo

def main():
    try:
        if len(sys.argv) < 5:
            print("Error: Faltan argumentos. Ejemplo de uso: python calculo_rendimiento_fondos.py 100000 6.5 5 3.5")
            return

        inversion = float(sys.argv[1])
        tasa_interes = float(sys.argv[2])
        plazo = int(sys.argv[3])
        tasa_inflacion = float(sys.argv[4])

        if inversion < 0:
            raise ValueError("La inversión inicial no puede ser negativa")

        if tasa_interes < 0 or tasa_interes > 100:
            raise ValueError("La tasa de interés debe estar entre 0 y 100")

        if plazo < 0:
            raise ValueError("El plazo no puede ser negativo")

        if tasa_inflacion < 0 or tasa_inflacion > 100:
            raise ValueError("La tasa de inflación debe estar entre 0 y 100")

        rendimiento = calculo_rendimiento_fondos(inversion, tasa_interes, plazo)
        rendimiento_anual = calculo_rendimiento_anual(rendimiento, inversion, plazo)
        rendimiento_real = calculo_tasa_inflacion(rendimiento, tasa_inflacion, plazo)
        ganancia = calculo_ganancia(inversion, rendimiento)
        pago_mensual = calculo_pago_mensual(rendimiento, plazo)

        print(f"Inversión inicial: ${inversion:,.2f} MXN")
        print(f"Tasa de interés: {tasa_interes}%")
        print(f"Plazo: {plazo} años")
        print(f"Tasa de inflación: {tasa_inflacion}%")
        print(f"Rendimiento total: ${rendimiento:,.2f} MXN")
        print(f"Rendimiento anual: ${rendimiento_anual:,.2f} MXN")
        print(f"Rendimiento real (ajustado por inflación): ${rendimiento_real:,.2f} MXN")
        print(f"Ganancia en porcentaje: {ganancia:.2f}%")
        print(f"Pago mensual: ${pago_mensual:,.2f} MXN")
        print(f"Fecha de cálculo: {datetime.date.today()}")
        print(f"Resumen ejecutivo: La inversión inicial de ${inversion:,.2f} MXN con una tasa de interés de {tasa_interes}% y un plazo de {plazo} años ha generado un rendimiento total de ${rendimiento:,.2f} MXN")
        print(f"Resumen ejecutivo: La inversión ha generado una ganancia de {ganancia:.2f}% y un pago mensual de ${pago_mensual:,.2f} MXN")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()