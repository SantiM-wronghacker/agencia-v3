import os
import sys
import json
from datetime import datetime
import math
import re
import random

"""
ÁREA: TURISMO
DESCRIPCIÓN: Agente que realiza generador de reseña de destino
TECNOLOGÍA: Python estándar
"""

def extraer_precios(precio_hotel=1500.0, precio_transporte=500.0, precio_comida=200.0):
    return {
        "hotel": precio_hotel,
        "transporte": precio_transporte,
        "comida": precio_comida
    }

def get_caracteristicas(lugar):
    if lugar == "playa":
        return "con aguas cristalinas y playas de ensueño"
    elif lugar == "ciudad":
        return "con una rica historia y cultura"

def get_distancia(lugar):
    if lugar == "playa":
        return 200
    elif lugar == "ciudad":
        return 100

def get_tiempo_viaje(distancia):
    return distancia / 60

def get_actividades(lugar):
    if lugar == "playa":
        return "nadar, surfear, pasear en caballo"
    elif lugar == "ciudad":
        return "visitar museos, ir a teatro, explorar mercados"

def get_mejores_epocas(lugar):
    if lugar == "playa":
        return "de diciembre a abril"
    elif lugar == "ciudad":
        return "de enero a marzo"

def get_consejos(lugar):
    if lugar == "playa":
        return "no olvidar protector solar y sombrero"
    elif lugar == "ciudad":
        return "no olvidar llevar dinero en efectivo"

def generar_resena_destino():
    try:
        lugar = sys.argv[1] if len(sys.argv) > 1 else "playa"
        if lugar not in ["playa", "ciudad"]:
            print("Lugar no válido")
            return
        resena = f"La {lugar} es una de las más hermosas de México, con {get_caracteristicas(lugar)}."
        precio_hotel = float(sys.argv[2]) if len(sys.argv) > 2 else 1500.0
        precio_transporte = float(sys.argv[3]) if len(sys.argv) > 3 else 500.0
        precio_comida = float(sys.argv[4]) if len(sys.argv) > 4 else 200.0
        distancia = get_distancia(lugar)
        tiempo_viaje = get_tiempo_viaje(distancia)
        print(f"Reseña del destino: {resena}")
        print(f"Precio del hotel: {precio_hotel} pesos mexicanos")
        print(f"Precio del transporte: {precio_transporte} pesos mexicanos")
        print(f"Precio de la comida: {precio_comida} pesos mexicanos")
        print(f"Distancia desde la capital: {distancia} km")
        print(f"Tiempo de viaje: {tiempo_viaje} horas")
        print(f"Fecha de la visita: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"Calificación del destino: {random.randint(1, 5)}/5")
        print(f"Resumen ejecutivo: La {lugar} es un destino ideal para aquellos que buscan relajación y aventura.")
        print(f"Actividades recomendadas: {get_actividades(lugar)}")
        print(f"Mejores épocas para visitar: {get_mejores_epocas(lugar)}")
        print(f"Consejos para viajar: {get_consejos(lugar)}")
        print(f"Resumen de gastos:")
        print(f"Precio del hotel: {precio_hotel} pesos mexicanos")
        print(f"Precio del transporte: {precio_transporte} pesos mexicanos")
        print(f"Precio de la comida: {precio_comida} pesos mexicanos")
        print(f"Total de gastos: {precio_hotel + precio_transporte + precio_comida} pesos mexicanos")
    except IndexError:
        print("Falta de argumentos")
    except ValueError:
        print("Valor no válido")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    generar_resena_destino()