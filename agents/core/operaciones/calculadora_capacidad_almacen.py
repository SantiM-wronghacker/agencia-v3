"""
ÁREA: LOGÍSTICA
DESCRIPCIÓN: Agente que realiza calculadora capacidad almacen
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcular_capacidad_almacen(ancho, largo, alto, capacidad_contenedores):
    area_almacen = ancho * largo
    volumen_almacen = area_almacen * alto
    capacidad_total = volumen_almacen * capacidad_contenedores
    return capacidad_total

def calcular_peso_maximo(capacidad_total, densidad_contenido):
    peso_maximo = capacidad_total * densidad_contenido
    return peso_maximo

def calcular_perimetro(ancho, largo):
    perimetro = 2 * (ancho + largo)
    return perimetro

def calcular_area(ancho, largo):
    area = ancho * largo
    return area

def calcular_volumen(ancho, largo, alto):
    volumen = ancho * largo * alto
    return volumen

def main():
    try:
        ancho = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0
        largo = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0
        alto = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0
        capacidad_contenedores = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
        densidad_contenido = float(sys.argv[5]) if len(sys.argv) > 5 else 0.8

        capacidad_almacen = calcular_capacidad_almacen(ancho, largo, alto, capacidad_contenedores)
        peso_maximo = calcular_peso_maximo(capacidad_almacen, densidad_contenido)
        perimetro = calcular_perimetro(ancho, largo)
        area = calcular_area(ancho, largo)
        volumen = calcular_volumen(ancho, largo, alto)

        print(f"Ancho del almacén: {ancho} metros")
        print(f"Largo del almacén: {largo} metros")
        print(f"Alto del almacén: {alto} metros")
        print(f"Capacidad de los contenedores: {capacidad_contenedores} metros cúbicos")
        print(f"Densidad del contenido: {densidad_contenido} toneladas/metro cúbico")
        print(f"Capacidad total del almacén: {capacidad_almacen} metros cúbicos")
        print(f"Peso máximo que puede soportar el almacén: {peso_maximo} toneladas")
        print(f"Volumen del almacén: {volumen} metros cúbicos")
        print(f"Área del almacén: {area} metros cuadrados")
        print(f"Perímetro del almacén: {perimetro} metros")
        print(f"Relación área/volumen: {area/volumen} metros cuadrados/metros cúbicos")
        print(f"Relación perímetro/área: {perimetro/area} metros/metros cuadrados")
        print(f"Relación volumen/capacidad: {volumen/capacidad_almacen} metros cúbicos/metros cúbicos")

        print("\nResumen Ejecutivo:")
        print(f"El almacén tiene una capacidad total de {capacidad_almacen} metros cúbicos y puede soportar un peso máximo de {peso_maximo} toneladas.")
        print(f"El volumen del almacén es de {volumen} metros cúbicos y su área es de {area} metros cuadrados.")
        print(f"El perímetro del almacén es de {perimetro} metros y la relación área/volumen es de {area/volumen} metros cuadrados/metros cúbicos.")

    except ValueError:
        print("Error: Los parámetros deben ser números.")
    except IndexError:
        print("Error: Faltan parámetros. Por favor, ingrese los siguientes parámetros: ancho, largo, alto, capacidad_contenedores, densidad_contenido.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()