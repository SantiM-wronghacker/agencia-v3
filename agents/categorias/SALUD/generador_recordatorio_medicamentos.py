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
    import web_bridge as web
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

        # Procesar argumentos de la línea de comandos
        if len(sys.argv) > 1:
            medicamentos = sys.argv[1].split(",")
            if len(sys.argv) > 2:
                dosis = [int(x) for x in sys.argv[2].split(",")]
                if len(sys.argv) > 3:
                    frecuencia = [int(x) for x in sys.argv[3].split(",")]

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
                print(f"    * Hora de la última dosis: {(hora_actual - frecuencia[i]) % 24}:00 hrs")
                print(f"    * Días de tratamiento recomendados: {math.ceil(30 / (24 / frecuencia[i]))} días")
                print(f"    * Cantidad de tabletas necesarias para un mes: {math.ceil(30 / (24 / frecuencia[i])) * dosis[i]} tabletas")
            except ValueError:
                print(f"Error al calcular la próxima dosis de {medicamentos[i]}")

        # Calcular el costo total de los medicamentos
        costo_total = 0
        for i in range(len(medicamentos)):
            costo_total += dosis[i] * 10  # Asumir un costo de 10 pesos por tableta
        print(f"Costo total de los medicamentos: {costo_total} pesos")

        # Calcular el costo diario de los medicamentos
        costo_diario = costo_total / 30
        print(f"Costo diario de los medicamentos: {costo_diario} pesos")

        print(f"Fecha actual: {datetime.datetime.now().strftime('%Y-%m-%d')}")
        print("Resumen ejecutivo:")
        print(f"El tratamiento con {', '.join(medicamentos)} durante 30 días costará {costo_total} pesos, lo que representa un costo diario de {costo_diario} pesos.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()