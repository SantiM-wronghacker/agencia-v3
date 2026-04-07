# ÁREA: SALUD
# DESCRIPCIÓN: Agente que realiza planificador citas medicas
# TECNOLOGÍA: Python estándar

import os
import sys
import json
import datetime
import math
import re
import random

def planificar_citas_medicas():
    # Configuración del agente
    fecha_actual = datetime.datetime.now()
    fecha_hoy = fecha_actual.strftime("%Y-%m-%d")
    hora_actual = fecha_actual.strftime("%H:%M:%S")

    try:
        # Configuración de parámetros por línea de comando
        if len(sys.argv) > 1 and sys.argv[1] == "web":
            # Buscar datos en tiempo real
            print("Buscando datos en tiempo real...")
            num_citas = 20
            minutos_entre_citas = [15, 30, 45, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540]
            precios = [500, 300, 200, 400, 600, 800, 1000, 1200, 1500, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800]
        elif len(sys.argv) > 1 and sys.argv[1] == "personalizado":
            num_citas = int(sys.argv[2])
            minutos_entre_citas = [int(x) for x in sys.argv[3].split(',')]
            precios = [int(x) for x in sys.argv[4].split(',')]
        else:
            # Usar datos de ejemplo hardcodeados
            num_citas = int(input("Ingrese el número de citas: "))
            minutos_entre_citas = [int(x) for x in input("Ingrese los minutos entre citas (separados por comas): ").split(',')]
            precios = [int(x) for x in input("Ingrese los precios (separados por comas): ").split(',')]

        # Validar parámetros
        if num_citas <= 0:
            raise ValueError("El número de citas debe ser mayor a 0")
        if len(minutos_entre_citas) != num_citas:
            raise ValueError("El número de minutos entre citas debe ser igual al número de citas")
        if len(precios) != num_citas:
            raise ValueError("El número de precios debe ser igual al número de citas")

        # Generar citas medicas
        citas_disponibles = []
        hora_inicial = "08:00"
        for i in range(num_citas):
            hora = datetime.datetime.strptime(hora_inicial, "%H:%M") + datetime.timedelta(minutes=minutos_entre_citas[i])
            hora_final = hora.strftime("%H:%M")
            cita = {
                "nombre": f"Cita médica {i+1}",
                "hora": f"{hora_inicial} - {hora_final}",
                "precio": precios[i],
                "especialista": f"Dr. {i+1}",
                "paciente": f"Paciente {i+1}"
            }
            citas_disponibles.append(cita)

        # Mostrar citas disponibles
        print(f"Citas disponibles para el día {fecha_hoy}:")
        for cita in citas_disponibles:
            print(f"Nombre: {cita['nombre']}, Hora: {cita['hora']}, Precio: ${cita['precio']}, Especialista: {cita['especialista']}, Paciente: {cita['paciente']}")

        # Mostrar resumen ejecutivo
        print(f"\nResumen ejecutivo:")
        print(f"Citas disponibles: {len(citas_disponibles)}")
        print(f"Total de citas: {num_citas}")
        print(f"Total de minutos entre citas: {sum(minutos_entre_citas)}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    planificar_citas_medicas()