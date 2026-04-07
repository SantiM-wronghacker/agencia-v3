"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Clasificador de viviendas según su precio y características en México
TECNOLOGÍA: Python
"""

import sys
import time
from datetime import datetime
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

class ClasificadorViviendas:
    def __init__(self, precio, ubicacion, tipo, metros_cuadrados=0, habitaciones=0, banos=0):
        self.precio = precio
        self.ubicacion = ubicacion
        self.tipo = tipo
        self.metros_cuadrados = metros_cuadrados
        self.habitaciones = habitaciones
        self.banos = banos

    def clasificar(self):
        # Clasificación por precio
        if self.precio < 200000:
            return 'Interes Social'
        elif self.precio < 500000:
            return 'Residencial'
        elif self.precio < 1500000:
            return 'Residencial Plus'
        else:
            return 'Premium'

    def calcular_precio_m2(self):
        if self.metros_cuadrados > 0:
            return self.precio / self.metros_cuadrados
        return 0

    def get_precio(self):
        return self.precio

    def set_precio(self, nuevo_precio):
        self.precio = nuevo_precio

    def get_ubicacion(self):
        return self.ubicacion

    def get_tipo(self):
        return self.tipo

    def get_metros_cuadrados(self):
        return self.metros_cuadrados

    def get_habitaciones(self):
        return self.habitaciones

    def get_banos(self):
        return self.banos

def main():
    try:
        if len(sys.argv) > 3:
            precio = float(sys.argv[1])
            ubicacion = sys.argv[2]
            tipo = sys.argv[3]
            metros_cuadrados = float(sys.argv[4]) if len(sys.argv) > 4 else 0
            habitaciones = int(sys.argv[5]) if len(sys.argv) > 5 else 0
            banos = int(sys.argv[6]) if len(sys.argv) > 6 else 0
        else:
            precio = 300000
            ubicacion = 'Ciudad de México'
            tipo = 'Departamento'
            metros_cuadrados = 60
            habitaciones = 2
            banos = 1
            print(f"Usando valores por defecto: precio: {precio}, ubicación: {ubicacion}, tipo: {tipo}, m²: {metros_cuadrados}, habitaciones: {habitaciones}, baños: {banos}")

        clasificador = ClasificadorViviendas(precio, ubicacion, tipo, metros_cuadrados, habitaciones, banos)

        print(f"Clasificación de propiedad en {clasificador.get_ubicacion()}")
        print(f"Tipo de propiedad: {clasificador.get_tipo()}")
        print(f"Precio: ${clasificador.get_precio():,.2f} MXN")
        print(f"Metros cuadrados: {clasificador.get_metros_cuadrados()} m²")
        print(f"Habitaciones: {clasificador.get_habitaciones()}")
        print(f"Baños: {clasificador.get_banos()}")
        print(f"Precio por m²: ${clasificador.calcular_precio_m2():,.2f} MXN")
        print(f"Categoría: {clasificador.clasificar()}")
        print(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Resumen ejecutivo: Propiedad {clasificador.get_tipo()} en {clasificador.get_ubicacion()} con {clasificador.get_metros_cuadrados()} m², {clasificador.get_habitaciones()} habitaciones y {clasificador.get_banos()} baños, valorada en ${clasificador.get_precio():,.2f} MXN, clasificada como {clasificador.clasificar()}.")
        time.sleep(2)
    except ValueError as e:
        print(f"Error: Datos inválidos - {str(e)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()