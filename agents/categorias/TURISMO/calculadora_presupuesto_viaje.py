"""
ÁREA: TURISMO
DESCRIPCIÓN: Agente que realiza calculadora presupuesto viaje
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcula_presupuesto(duracion_viaje, destino, presupuesto_diario):
    presupuesto_total = duracion_viaje * presupuesto_diario
    return presupuesto_total

def calcula_gastos_transporte(duracion_viaje, destino):
    gastos_transporte = 0
    if destino == "nacional":
        gastos_transporte = duracion_viaje * 500 + 2000  # agregando un costo fijo de transporte
    elif destino == "internacional":
        gastos_transporte = duracion_viaje * 2000 + 5000  # agregando un costo fijo de transporte
    return gastos_transporte

def calcula_gastos_alimentacion(duracion_viaje, presupuesto_diario):
    gastos_alimentacion = duracion_viaje * (presupuesto_diario * 0.3)
    return gastos_alimentacion

def calcula_gastos_otros(duracion_viaje, presupuesto_diario):
    gastos_otros = duracion_viaje * (presupuesto_diario * 0.2)
    return gastos_otros

def main():
    try:
        duracion_viaje = int(sys.argv[1]) if len(sys.argv) > 1 else 7
        destino = sys.argv[2] if len(sys.argv) > 2 else "nacional"
        presupuesto_diario = int(sys.argv[3]) if len(sys.argv) > 3 else 2000

        if duracion_viaje <= 0:
            raise ValueError("La duración del viaje debe ser mayor que cero")

        if presupuesto_diario <= 0:
            raise ValueError("El presupuesto diario debe ser mayor que cero")

        presupuesto_total = calcula_presupuesto(duracion_viaje, destino, presupuesto_diario)
        gastos_transporte = calcula_gastos_transporte(duracion_viaje, destino)
        gastos_alimentacion = calcula_gastos_alimentacion(duracion_viaje, presupuesto_diario)
        gastos_otros = calcula_gastos_otros(duracion_viaje, presupuesto_diario)

        print(f"Duración del viaje: {duracion_viaje} días")
        print(f"Destino: {destino}")
        print(f"Presupuesto diario: ${presupuesto_diario}")
        print(f"Presupuesto total: ${presupuesto_total}")
        print(f"Gastos en transporte: ${gastos_transporte}")
        print(f"Gastos en alimentación: ${gastos_alimentacion}")
        print(f"Gastos en otros: ${gastos_otros}")
        print(f"Fecha de inicio del viaje: {datetime.date.today() + datetime.timedelta(days=7)}")
        print(f"Fecha de fin del viaje: {datetime.date.today() + datetime.timedelta(days=duracion_viaje + 7)}")
        print(f"Tipo de cambio (MXN/USD): {20.0}")
        print(f"Costo de visa (si aplica): ${100.0}")

        print("\nResumen ejecutivo:")
        print(f"El viaje a {destino} durante {duracion_viaje} días tendrá un costo total de ${presupuesto_total}.")
        print(f"Los gastos en transporte representan el {gastos_transporte / presupuesto_total * 100:.2f}% del presupuesto total.")
        print(f"Los gastos en alimentación representan el {gastos_alimentacion / presupuesto_total * 100:.2f}% del presupuesto total.")
        print(f"Los gastos en otros representan el {gastos_otros / presupuesto_total * 100:.2f}% del presupuesto total.")
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()