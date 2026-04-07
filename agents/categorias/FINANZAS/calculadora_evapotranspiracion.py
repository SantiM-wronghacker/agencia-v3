#!/usr/bin/env python3
"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora evapotranspiracion
TECNOLOGÍA: Python estándar
"""

import sys
import math
import os

def calcular_evapotranspiracion(temperatura, humedad, velocidad_viento, radiacion_sol, precipitacion):
    try:
        # Constantes para Mexico
        Kc = 0.0028
        Kd = 0.00002
        Ks = 0.000002
        Kr = 0.0000002

        # Validación de valores de entrada
        if temperatura < -20 or temperatura > 40:
            raise ValueError("Temperatura fuera de rango")
        if humedad < 0 or humedad > 100:
            raise ValueError("Humedad fuera de rango")
        if velocidad_viento < 0 or velocidad_viento > 100:
            raise ValueError("Velocidad viento fuera de rango")
        if radiacion_sol < 0 or radiacion_sol > 2000:
            raise ValueError("Radiacion solar fuera de rango")
        if precipitacion < 0 or precipitacion > 100:
            raise ValueError("Precipitacion fuera de rango")

        # Calculo de evapotranspiracion potencial
        ep = (0.408 * radiacion_sol * (temperatura + 273.15)) / (temperatura + 273.15 + 24.9)

        # Calculo de evapotranspiracion real
        es = (0.65 * ep) + (0.35 * (0.5 * radiacion_sol))

        # Calculo de evaporacion real
        ev = es - (Kc * (humedad - 50) * (temperatura + 273.15)) - (Kd * velocidad_viento * (temperatura + 273.15)) - (Ks * (radiacion_sol - 200)) - (Kr * precipitacion)

        # Devuelve evapotranspiracion real
        return ev

    except ValueError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    try:
        # Argumentos de la linea de comandos
        temperatura = float(sys.argv[1]) if len(sys.argv) > 1 else 20
        humedad = float(sys.argv[2]) if len(sys.argv) > 2 else 60
        velocidad_viento = float(sys.argv[3]) if len(sys.argv) > 3 else 2
        radiacion_sol = float(sys.argv[4]) if len(sys.argv) > 4 else 500
        precipitacion = float(sys.argv[5]) if len(sys.argv) > 5 else 0

        # Calcula evapotranspiracion
        evapotranspiracion = calcular_evapotranspiracion(temperatura, humedad, velocidad_viento, radiacion_sol, precipitacion)

        # Imprime resultados
        print("Resultados:")
        print(f"Temperatura: {temperatura}°C")
        print(f"Humedad: {humedad}%")
        print(f"Velocidad viento: {velocidad_viento} km/h")
        print(f"Radiacion solar: {radiacion_sol} W/m²")
        print(f"Precipitacion: {precipitacion} mm")
        print(f"Evapotranspiracion: {evapotranspiracion} mm/día")

        # Imprime resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"La evapotranspiracion en la zona de estudio es de {evapotranspiracion} mm/día.")
        print("Esta cantidad puede variar dependiendo de factores como la temperatura, humedad y radiacion solar.")

    except IndexError:
        print("Error: Faltan argumentos de la linea de comandos.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()