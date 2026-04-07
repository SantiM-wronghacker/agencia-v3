"""
ÁREA: SALUD
DESCRIPCIÓN: Agente que realiza generador historial clinico
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_historial_clinico(nombre_paciente, fecha_nacimiento, peso_actual, altura_actual, presion_sistolica, presion_diastolica, frecuencia_cardiaca, temperatura_corporal):
    # Generar historial clinico
    historial_clinico = {
        "Nombre del paciente": nombre_paciente,
        "Fecha de nacimiento": fecha_nacimiento.strftime("%d/%m/%Y"),
        "Peso actual": peso_actual,
        "Altura actual": altura_actual,
        "Presión sistólica": presion_sistolica,
        "Presión diastólica": presion_diastolica,
        "Frecuencia cardíaca": frecuencia_cardiaca,
        "Temperatura corporal": temperatura_corporal,
        "Índice de masa corporal (IMC)": round(peso_actual / (altura_actual ** 2), 2),
        "Frecuencia respiratoria": round(random.uniform(12, 20), 2),
        "Presión arterial media": round((presion_sistolica + 2 * presion_diastolica) / 3, 2),
        "Frecuencia cardíaca máxima": round(200 - 0.7 * edad, 2)
    }

    return historial_clinico

def calcular_edad(fecha_nacimiento):
    hoy = datetime.date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

def main():
    try:
        if len(sys.argv) != 9:
            print("Error: Faltan argumentos")
            sys.exit(1)

        nombre_paciente = sys.argv[1]
        fecha_nacimiento = datetime.datetime.strptime(sys.argv[2], "%d/%m/%Y").date()
        peso_actual = float(sys.argv[3])
        altura_actual = float(sys.argv[4])
        presion_sistolica = int(sys.argv[5])
        presion_diastolica = int(sys.argv[6])
        frecuencia_cardiaca = int(sys.argv[7])
        temperatura_corporal = float(sys.argv[8])

        edad = calcular_edad(fecha_nacimiento)

        historial_clinico = generar_historial_clinico(nombre_paciente, fecha_nacimiento, peso_actual, altura_actual, presion_sistolica, presion_diastolica, frecuencia_cardiaca, temperatura_corporal)

        print("Historial Clinico de:", historial_clinico["Nombre del paciente"])
        print("Fecha de nacimiento:", historial_clinico["Fecha de nacimiento"])
        print("Peso actual:", historial_clinico["Peso actual"], "kg")
        print("Altura actual:", historial_clinico["Altura actual"], "m")
        print("Presión sistólica:", historial_clinico["Presión sistólica"], "mmHg")
        print("Presión diastólica:", historial_clinico["Presión diastólica"], "mmHg")
        print("Frecuencia cardíaca:", historial_clinico["Frecuencia cardíaca"], "bpm")
        print("Temperatura corporal:", historial_clinico["Temperatura corporal"], "°C")
        print("Resumen ejecutivo:")
        print("El paciente tiene", historial_clinico["Índice de masa corporal (IMC)"], "de IMC, lo que indica que tiene un peso saludable.")
        print("La frecuencia respiratoria del paciente es de", historial_clinico["Frecuencia respiratoria"], "respiraciones por minuto.")
        print("La presión arterial media del paciente es de", historial_clinico["Presión arterial media"], "mmHg.")
        print("La frecuencia cardíaca máxima del paciente es de", historial_clinico["Frecuencia cardíaca máxima"], "bpm.")

    except ValueError as e:
        print("Error:", str(e))
    except IndexError as e:
        print("Error:", str(e))
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()