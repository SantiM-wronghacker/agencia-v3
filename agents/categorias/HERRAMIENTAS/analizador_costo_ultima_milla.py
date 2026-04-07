"""
ÁREA: LOGÍSTICA
DESCRIPCIÓN: Agente que realiza analizador costo ultima milla
TECNOLOGÍA: Python estándar
"""

import sys
import os
import math

def main():
    try:
        # Parámetros por defecto
        distancia = float(os.environ.get('DISTANCIA', 10))  # km
        velocidad = float(os.environ.get('VELOCIDAD', 30))  # km/h
        costo_combustible = float(os.environ.get('COSTO_COMBUSTIBLE', 20))  # pesos por litro
        consumo_combustible = float(os.environ.get('CONSUMO_COMBUSTIBLE', 10))  # litros por 100 km
        costo_mano_obra = float(os.environ.get('COSTO_MANO_OBRA', 50))  # pesos por hora
        impuestos = float(os.environ.get('IMPUESTOS', 0.16))  # 16% de impuestos
        seguro = float(os.environ.get('SEGURO', 0.05))  # 5% de seguro

        # Opciones de línea de comandos
        if len(sys.argv) > 1:
            distancia = float(sys.argv[1])
        if len(sys.argv) > 2:
            velocidad = float(sys.argv[2])
        if len(sys.argv) > 3:
            costo_combustible = float(sys.argv[3])
        if len(sys.argv) > 4:
            consumo_combustible = float(sys.argv[4])
        if len(sys.argv) > 5:
            costo_mano_obra = float(sys.argv[5])

        # Cálculo del costo de la última milla
        tiempo_recorrido = distancia / velocidad
        costo_combustible_total = (distancia / 100) * consumo_combustible * costo_combustible
        costo_mano_obra_total = tiempo_recorrido * costo_mano_obra
        costo_impuestos = (costo_combustible_total + costo_mano_obra_total) * impuestos
        costo_seguro = (costo_combustible_total + costo_mano_obra_total) * seguro
        costo_total = costo_combustible_total + costo_mano_obra_total + costo_impuestos + costo_seguro

        # Calculo de consumo de combustible en litros
        consumo_combustible_litros = (distancia / 100) * consumo_combustible

        # Calculo de tiempo de viaje en horas
        tiempo_viaje_horas = distancia / velocidad

        # Calculo de costo de combustible por litro en pesos
        costo_combustible_litro = costo_combustible_total / consumo_combustible_litros

        # Calculo de costo de mano de obra por hora en pesos
        costo_mano_obra_hora = costo_mano_obra_total / tiempo_viaje_horas

        print(f"Distancia recorrida: {distancia} km")
        print(f"Velocidad promedio: {velocidad} km/h")
        print(f"Consumo de combustible: {consumo_combustible_litros} litros")
        print(f"Costo de combustible: {costo_combustible_total} pesos")
        print(f"Costo de mano de obra: {costo_mano_obra_total} pesos")
        print(f"Costo de impuestos: {costo_impuestos} pesos")
        print(f"Costo de seguro: {costo_seguro} pesos")
        print(f"Costo total: {costo_total} pesos")
        print(f"Costo de combustible por litro: {costo_combustible_litro} pesos")
        print(f"Costo de mano de obra por hora: {costo_mano_obra_hora} pesos")
        print(f"Tiempo de viaje: {tiempo_viaje_horas} horas")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El costo total de la última milla es de {costo_total} pesos, lo que incluye un costo de combustible de {costo_combustible_total} pesos, un costo de mano de obra de {costo_mano_obra_total} pesos, un costo de impuestos de {costo_impuestos} pesos y un costo de seguro de {costo_seguro} pesos.")

    except ValueError:
        print("Error: Los parámetros deben ser números.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()