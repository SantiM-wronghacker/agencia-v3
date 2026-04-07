"""
ÁREA: TURISMO
DESCRIPCIÓN: Agente que realiza generador descripcion tour
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_descripcion_tour(nombre_tour, descripcion_tour, precios, fecha_inicio, fecha_fin):
    try:
        # Generar descripción del tour
        descripcion = f"Nombre: {nombre_tour}\n"
        descripcion += f"Descripción: {descripcion_tour}\n"
        descripcion += f"Precio adulto: {precios['adulto']} MXN\n"
        descripcion += f"Precio niño: {precios['niño']} MXN\n"
        descripcion += f"Fecha de inicio: {fecha_inicio}\n"
        descripcion += f"Fecha de fin: {fecha_fin}\n"
        descripcion += f"Duración: {random.randint(5, 10)} días\n"
        descripcion += f"Lugar de inicio: Ciudad de México\n"
        descripcion += f"Lugar de destino: Cancún\n"
        descripcion += f"Actividades incluidas: Visita a la Ciudad de México, Guadalajara y Cancún\n"
        descripcion += f"Servicios incluidos: Transporte, alojamiento y comidas\n"
        descripcion += f"Resumen ejecutivo: Este tour te llevará a los lugares más emblemáticos de México, disfrutando de la cultura y la naturaleza del país.\n"
        descripcion += f"Distancia recorrida: {random.randint(1000, 2000)} km\n"
        descripcion += f"Altitud máxima: {random.randint(2000, 3000)} msnm\n"
        descripcion += f"Temperatura promedio: {random.randint(20, 30)} °C\n"
        descripcion += f"Presión atmosférica: {random.randint(900, 1100)} hPa\n"

        return descripcion

    except TypeError as e:
        return f"Error: {str(e)}"
    except KeyError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def calcular_distancia(lat1, lon1, lat2, lon2):
    try:
        # Calcular distancia entre dos puntos en la Tierra
        R = 6371  # Radio de la Tierra en km
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distancia = R * c
        return distancia
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    if len(sys.argv) != 7:
        print("Uso: python generador_descripcion_tour.py <nombre_tour> <descripcion_tour> <precio_adulto> <precio_niño> <latitud_inicio> <longitud_inicio> <latitud_fin> <longitud_fin>")
        sys.exit(1)

    nombre_tour = sys.argv[1]
    descripcion_tour = sys.argv[2]
    precios = {
        "adulto": int(sys.argv[3]),
        "niño": int(sys.argv[4])
    }
    latitud_inicio = float(sys.argv[5])
    longitud_inicio = float(sys.argv[6])
    latitud_fin = float(sys.argv[7])
    longitud_fin = float(sys.argv[8])

    distancia = calcular_distancia(latitud_inicio, longitud_inicio, latitud_fin, longitud_fin)
    fecha_inicio = datetime.date.today()
    fecha_fin = fecha_inicio + datetime.timedelta(days=random.randint(5, 10))
    descripcion = generar_descripcion_tour(nombre_tour, descripcion_tour, precios, fecha_inicio, fecha_fin)
    descripcion += f"Distancia recorrida: {distancia:.2f} km\n"
    print(descripcion)
    with open("descripcion_tour.txt", "w") as f:
        f.write(descripcion)

if __name__ == "__main__":
    main()