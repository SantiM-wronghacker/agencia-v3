"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora forecast mensual
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import random
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcula_forecast_mensual(ventas_anteriores, crecimiento, inflacion, temporada):
    try:
        ventas_anteriores = json.loads(ventas_anteriores)
        if not isinstance(ventas_anteriores, dict):
            raise ValueError("Ventas anteriores deben ser un diccionario")
        if not all(isinstance(ventas, (int, float)) for ventas in ventas_anteriores.values()):
            raise ValueError("Ventas anteriores deben ser números")
        if not all(ventas >= 0 for ventas in ventas_anteriores.values()):
            raise ValueError("Ventas anteriores no pueden ser negativas")
        
        total_ventas = sum(ventas_anteriores.values())
        promedio_ventas = total_ventas / len(ventas_anteriores)
        if promedio_ventas <= 0:
            raise ValueError("Promedio de ventas no puede ser cero o negativo")
        
        forecast = promedio_ventas * (1 + crecimiento) * (1 + inflacion) * (1 + temporada)
        if forecast <= 0:
            raise ValueError("Forecast no puede ser cero o negativo")
        
        return forecast
    except Exception as e:
        print("Error en cálculo:", str(e))
        return None

def main():
    try:
        ventas_anteriores = sys.argv[1] if len(sys.argv) > 1 else '{"Enero": 10000, "Febrero": 12000, "Marzo": 11000}'
        crecimiento = float(sys.argv[2]) if len(sys.argv) > 2 else 0.1
        inflacion = float(sys.argv[3]) if len(sys.argv) > 3 else 0.05
        temporada = float(sys.argv[4]) if len(sys.argv) > 4 else 0.2
        forecast = calcula_forecast_mensual(ventas_anteriores, crecimiento, inflacion, temporada)
        if forecast is not None:
            print("ÁREA: FINANZAS")
            print("DESCRIPCIÓN: Agente que realiza calculadora forecast mensual")
            print("TECNOLOGÍA: Python estándar")
            print("Ventas anteriores:", json.loads(ventas_anteriores))
            print("Crecimiento:", crecimiento)
            print("Inflación:", inflacion)
            print("Temporada:", temporada)
            print("Forecast mensual:", forecast)
            print("Incremento porcentual:", (forecast / sum(json.loads(ventas_anteriores).values()) * len(json.loads(ventas_anteriores))) * 100)
            print("Fecha de cálculo:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print("Resumen ejecutivo:")
            print("  * Ventas proyectadas para el próximo mes:", forecast)
            print("  * Crecimiento proyectado:", (forecast / sum(json.loads(ventas_anteriores).values()) * len(json.loads(ventas_anteriores))) * 100)
            print("  * Incremento porcentual:", (forecast / sum(json.loads(ventas_anteriores).values()) * len(json.loads(ventas_anteriores))) * 100)
            print("  * Fecha de cálculo:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print("  * Resumen de ventas anteriores:")
            for mes, ventas in json.loads(ventas_anteriores).items():
                print(f"    * {mes}: {ventas}")
            print("  * Resumen de crecimiento, inflación y temporada:")
            print(f"    * Crecimiento: {crecimiento}")
            print(f"    * Inflación: {inflacion}")
            print(f"    * Temporada: {temporada}")
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()