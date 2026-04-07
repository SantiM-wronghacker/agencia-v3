"""
ÁREA: SALUD
DESCRIPCIÓN: Agente que realiza generador recordatorio medicamentos
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def main():
    try:
        # Configuración por defecto
        medicamentos = ["Paracetamol", "Ibuprofeno", "Aspirina"]
        dosis = [2, 1, 1]
        frecuencia = [8, 12, 24]
        hora_actual = datetime.datetime.now().hour
        lugar = "Ciudad de México"

        # Procesar argumentos de la línea de comandos
        if len(sys.argv) > 1:
            medicamentos = sys.argv[1].split(",")
            if len(sys.argv) > 2:
                dosis = [int(x) for x in sys.argv[2].split(",")]
                if len(sys.argv) > 3:
                    frecuencia = [int(x) for x in sys.argv[3].split(",")]
                if len(sys.argv) > 4:
                    hora_actual = int(sys.argv[4])
                if len(sys.argv) > 5:
                    lugar = sys.argv[5]

        # Validar argumentos
        if len(medicamentos) != len(dosis) or len(medicamentos) != len(frecuencia):
            print("Error: La cantidad de medicamentos, dosis y frecuencia deben ser iguales")
            return

        # Generar recordatorios
        print("Recordatorios de medicamentos:")
        for i in range(len(medicamentos)):
            try:
                proxima_dosis = hora_actual + frecuencia[i]
                if proxima_dosis > 24:
                    proxima_dosis -= 24
                print(f"  - {medicamentos[i]}: {dosis[i]} tabletas cada {frecuencia[i]} horas. Próxima dosis: {proxima_dosis}:00 hrs")
                print(f"    * Dosis diarias recomendadas: {math.ceil(24 / frecuencia[i]) * dosis[i]} tabletas")
                print(f"    * Cantidad de tabletas necesarias para un día: {math.ceil(24 / frecuencia[i]) * dosis[i]} tabletas")
                print(f"    * Frecuencia de toma: {frecuencia[i]} horas")
                print(f"    * Hora de la última dosis: {hora_actual}:00 hrs")
                print(f"    * Lugar de toma: {lugar}")
                print(f"    * Dosis máxima diaria recomendada: {dosis[i] * 2} tabletas")
                print(f"    * Dosis mínima diaria recomendada: {dosis[i] / 2} tabletas")
            except ValueError:
                print(f"Error: La frecuencia de toma {frecuencia[i]} no es válida")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"La cantidad de medicamentos es {len(medicamentos)}")
        print(f"La hora actual es {hora_actual}:00 hrs")
        print(f"El lugar de toma es {lugar}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()