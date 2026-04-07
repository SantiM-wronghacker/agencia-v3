import json
import os
import sys
import math
import random
from datetime import datetime

HABILIDADES_PATH = os.path.join(os.path.expanduser('~'), 'habilidades.json')
TMP_PATH = HABILIDADES_PATH + ".tmp"

ARGS_NOT_NEEDED = 0

def obtener_habilidades(path):
    try:
        with open(path, 'r') as f:
            habilidades = json.load(f)
            return habilidades
    except json.JSONDecodeError as e:
        print(f"Error al leer archivo de habilidades: {e}")
        return []
    except FileNotFoundError:
        print("Archivo de habilidades no encontrado")
        return []

def calcular_promedio(habilidades):
    try:
        total = sum(habilidad['puntuacion'] for habilidad in habilidades)
        count = len(habilidades)
        return total / count
    except ZeroDivisionError:
        return 0

def calcular_media(habilidades):
    try:
        total = sum(habilidad['puntuacion'] for habilidad in habilidades)
        count = len(habilidades)
        return total / count
    except ZeroDivisionError:
        return 0

def calcular_desviacion_estandar(habilidades):
    try:
        promedio = calcular_promedio(habilidades)
        total = sum((habilidad['puntuacion'] - promedio) ** 2 for habilidad in habilidades)
        count = len(habilidades)
        return math.sqrt(total / count)
    except ZeroDivisionError:
        return 0

def obtener_resumen_ejecutivo(habilidades):
    promedio = calcular_promedio(habilidades)
    media = calcular_media(habilidades)
    desviacion_estandar = calcular_desviacion_estandar(habilidades)
    return f"Promedio: {promedio:.2f}, Media: {media:.2f}, Desviación Estándar: {desviacion_estandar:.2f}"

def obtener_mayor_puntuacion(habilidades):
    try:
        return max(habilidad['puntuacion'] for habilidad in habilidades)
    except ValueError:
        return 0

def obtener_menor_puntuacion(habilidades):
    try:
        return min(habilidad['puntuacion'] for habilidad in habilidades)
    except ValueError:
        return 0

def obtener_cantidad_habilidades(habilidades):
    return len(habilidades)

def obtener_area_con_mayor_puntuacion(habilidades):
    try:
        area_con_mayor_puntuacion = max(habilidades, key=lambda x: x['puntuacion'])['area']
        return area_con_mayor_puntuacion
    except ValueError:
        return "No hay habilidades"

def obtener_tecnologia_con_mayor_puntuacion(habilidades):
    try:
        tecnologia_con_mayor_puntuacion = max(habilidades, key=lambda x: x['puntuacion'])['tecnologia']
        return tecnologia_con_mayor_puntuacion
    except ValueError:
        return "No hay habilidades"

def main():
    if len(sys.argv) > 1:
        HABILIDADES_PATH = sys.argv[1]
    habilidades = obtener_habilidades(HABILIDADES_PATH)
    if habilidades:
        print("AREA\tDESCRIPCION\tTECNOLOGIA\tPUNTUACION")
        for habilidad in habilidades:
            print(f"{habilidad['area']}\t{habilidad['descripcion']}\t{habilidad['tecnologia']}\t{habilidad['puntuacion']}")
        print("\n")
        print(obtener_resumen_ejecutivo(habilidades))
        print(f"Cantidad de habilidades: {obtener_cantidad_habilidades(habilidades)}")
        print(f"Mayor puntuación: {obtener_mayor_puntuacion(habilidades)}")
        print(f"Menor puntuación: {obtener_menor_puntuacion(habilidades)}")
        print(f"Área con mayor puntuación: {obtener_area_con_mayor_puntuacion(habilidades)}")
        print(f"Tecnología con mayor puntuación: {obtener_tecnologia_con_mayor_puntuacion(habilidades)}")
        print(f"Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("No hay habilidades disponibles")

if __name__ == "__main__":
    main()