# TRANSPORTE/Generador de bitacora de vehiculos/Python
# AREA: TRANSPORTE
# DESCRIPCION: Agente que realiza generador bitacora vehiculos
# TECNOLOGIA: Python

import sys
import json
import datetime
import math
import re
import random
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Definir variables
        num_vehiculos = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        vehiculos = ["Chevrolet", "Ford", "Toyota", "Volkswagen", "Nissan", "Honda", "Kia", "Hyundai", "Mazda", "BMW"]
        placas = [f"MX-{random.randint(1000, 9999)}" for _ in range(num_vehiculos)]
        kilometrajes = [random.randint(0, 200000) for _ in range(num_vehiculos)]
        fechas = [datetime.date.today() - datetime.timedelta(days=random.randint(0, 365)) for _ in range(num_vehiculos)]
        combustibles = ["Gasolina", "Diesel", "Gas", "Electrico"]
        tipos_vehiculos = ["Automovil", "Camioneta", "Camion", "Motocicleta"]
        modelo_vehiculos = [random.randint(2010, 2022) for _ in range(num_vehiculos)]

        # Generar bitacora
        print("Bitacora de vehiculos:")
        for i in range(num_vehiculos):
            print(f"Vehiculo: {vehiculos[i % len(vehiculos)]}, Placa: {placas[i]}, Kilometraje: {kilometrajes[i]} km, Fecha: {fechas[i]}, Combustible: {random.choice(combustibles)}, Tipo: {random.choice(tipos_vehiculos)}, Modelo: {modelo_vehiculos[i]}")

        # Calcular estadisticas
        total_kilometraje = sum(kilometrajes)
        promedio_kilometraje = total_kilometraje / num_vehiculos
        max_kilometraje = max(kilometrajes)
        min_kilometraje = min(kilometrajes)
        promedio_modelo = sum(modelo_vehiculos) / num_vehiculos

        # Imprimir estadisticas
        print("\nEstadisticas:")
        print(f"Total kilometraje: {total_kilometraje} km")
        print(f"Promedio kilometraje: {promedio_kilometraje:.2f} km")
        print(f"Maximo kilometraje: {max_kilometraje} km")
        print(f"Minimo kilometraje: {min_kilometraje} km")
        print(f"Promedio modelo: {promedio_modelo:.2f}")

        # Imprimir resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"Se generaron {num_vehiculos} vehiculos con un total de {total_kilometraje} km recorridos.")
        print(f"El promedio de kilometraje es de {promedio_kilometraje:.2f} km y el promedio de modelo es {promedio_modelo:.2f}.")
        print(f"El maximo kilometraje registrado es de {max_kilometraje} km y el minimo es de {min_kilometraje} km.")

        # Guardar bitacora en archivo
        with open("bitacora_vehiculos.json", "w") as archivo:
            json.dump({
                "vehiculos": [vehiculos[i % len(vehiculos)] for i in range(num_vehiculos)],
                "placas": placas,
                "kilometrajes": kilometrajes,
                "fechas": [fecha.isoformat() for fecha in fechas],
                "combustibles": [random.choice(combustibles) for _ in range(num_vehiculos)],
                "tipos": [random.choice(tipos_vehiculos) for _ in range(num_vehiculos)],
                "modelos": modelo_vehiculos
            }, indent=4)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()