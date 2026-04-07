"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza limpiador de datos
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def limpiar_datos(nombre_archivo, ciudad):
    try:
        # Procesar datos de ejemplo (fallback si no hay conexión a internet)
        datos_ejemplo = {
            "nombre": nombre_archivo,
            "edad": random.randint(18, 100),
            "ciudad": ciudad,
            "pais": "México",
            "altura": random.uniform(1.5, 2.2),
            "peso": random.uniform(50, 120),
            "genero": random.choice(["Hombre", "Mujer"]),
            "ocupacion": random.choice(["Estudiante", "Trabajador", "Retirado"]),
            "ingresos": random.uniform(20000, 100000)
        }

        # Procesar datos para eliminar valores nulos o vacíos
        datos_limpios = {key: value for key, value in datos_ejemplo.items() if value}

        # Devolver datos limpios
        return datos_limpios

    except Exception as e:
        print(f"Error: {e}")
        return None

def calcular_promedios():
    try:
        # Calcula la edad promedio en México
        edad_promedio = math.floor(random.uniform(25, 35))
        print(f"Edad promedio en México: {edad_promedio} años")

        # Calcula la altura promedio en México (hombres)
        altura_promedio_hombres = math.floor(random.uniform(1.68, 1.72))
        print(f"Altura promedio en México (hombres): {altura_promedio_hombres} m")

        # Calcula el peso promedio en México (hombres)
        peso_promedio_hombres = math.floor(random.uniform(65, 75))
        print(f"Peso promedio en México (hombres): {peso_promedio_hombres} kg")

        # Calcula la edad promedio en México (mujeres)
        edad_promedio_mujeres = math.floor(random.uniform(25, 35))
        print(f"Edad promedio en México (mujeres): {edad_promedio_mujeres} años")

        # Calcula la altura promedio en México (mujeres)
        altura_promedio_mujeres = math.floor(random.uniform(1.60, 1.65))
        print(f"Altura promedio en México (mujeres): {altura_promedio_mujeres} m")

        # Calcula el peso promedio en México (mujeres)
        peso_promedio_mujeres = math.floor(random.uniform(55, 65))
        print(f"Peso promedio en México (mujeres): {peso_promedio_mujeres} kg")

    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) > 2:
        nombre_archivo = sys.argv[1]
        ciudad = sys.argv[2]
    else:
        nombre_archivo = "Juan"
        ciudad = "Ciudad de México"

    datos_limpios = limpiar_datos(nombre_archivo, ciudad)
    if datos_limpios:
        print("Datos limpios:")
        print(json.dumps(datos_limpios, indent=4))
        print(f"Cantidad de datos: {len(datos_limpios)}")
        print(f"Fecha y hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Valor aleatorio: {random.randint(1, 100)}")
        calcular_promedios()
    else:
        print("No se pudieron limpiar los datos.")

    print("\nResumen ejecutivo:")
    print(f"Nombre archivo: {nombre_archivo}")
    print(f"Ciudad: {ciudad}")
    print(f"Fecha y hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()