# CEREBRO - Agente de Fact Checking - Python
# AREA: CEREBRO
# DESCRIPCION: Agente que realiza agente fact checking
# TECNOLOGIA: Python

import sys
import json
import datetime
import math
import re
import random
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Configuracion por defecto
        pais = sys.argv[1] if len(sys.argv) > 1 else 'Mexico'
        poblacion = int(sys.argv[2]) if len(sys.argv) > 2 else 127575529
        pib = float(sys.argv[3]) if len(sys.argv) > 3 else 1334.78  # Billones de pesos mexicanos
        superficie = int(sys.argv[4]) if len(sys.argv) > 4 else 1964375  # km^2
        tasa_crecimiento_poblacional = float(sys.argv[5]) if len(sys.argv) > 5 else 1.05  # Porcentaje
        tasa_inflacion = float(sys.argv[6]) if len(sys.argv) > 6 else 3.5  # Porcentaje

        # Mostrar datos concretos
        print(f"Pais: {pais}")
        print(f"Poblacion: {poblacion}")
        print(f"PIB (billones de pesos mexicanos): {pib}")
        print(f"Fecha actual: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Numero aleatorio entre 1 y 100: {random.randint(1, 100)}")
        print(f"Superficie (km^2): {superficie}")
        print(f"Tasa de crecimiento poblacional: {tasa_crecimiento_poblacional}%")
        print(f"Tasa de inflacion: {tasa_inflacion}%")

        # Calculos adicionales
        densidad_poblacional = poblacion / superficie  # Densidad poblacional por km^2
        pib_per_capita = pib * 1000000000 / poblacion
        print(f"Densidad poblacional (hab/km^2): {densidad_poblacional:.2f}")
        print(f"PIB per capita (pesos mexicanos): {pib_per_capita:.2f}")
        print(f"Porcentaje de poblacion urbana (aproximado): {70:.2f}%")
        print(f"Porcentaje de poblacion rural (aproximado): {30:.2f}%")
        print(f"Edad promedio de la poblacion (aproximado): {28:.2f} años")
        print(f"Poblacion urbana (aproximado): {poblacion * 0.7:.2f} habitantes")
        print(f"Poblacion rural (aproximado): {poblacion * 0.3:.2f} habitantes")
        print(f"PIB con inflacion (billones de pesos mexicanos): {pib * (1 + tasa_inflacion / 100):.2f}")
        print(f"Poblacion con crecimiento (aproximado): {poblacion * (1 + tasa_crecimiento_poblacional / 100):.2f} habitantes")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El pais de {pais} tiene una poblacion de {poblacion} habitantes y un PIB de {pib} billones de pesos mexicanos.")
        print(f"La densidad poblacional es de {densidad_poblacional:.2f} habitantes por km^2 y el PIB per capita es de {pib_per_capita:.2f} pesos mexicanos.")
        print(f"La tasa de crecimiento poblacional es del {tasa_crecimiento_poblacional}% y la tasa de inflacion es del {tasa_inflacion}%.")

    except Exception as e:
        print(f"Error: {str(e)}")
    except IndexError:
        print("Error: No se proporcionaron suficientes argumentos.")
    except ValueError:
        print("Error: Valor no valido.")
    except ZeroDivisionError:
        print("Error: Division por cero.")

if __name__ == "__main__":
    main()