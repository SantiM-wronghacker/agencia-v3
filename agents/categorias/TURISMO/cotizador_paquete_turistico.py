"""
ÁREA: TURISMO
DESCRIPCIÓN: Agente que realiza cotizador paquete turistico
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def cotizar_paquete_turistico(precio1, precio2, precio3, descuento):
    # Calcular impuestos y total con descuento
    total_sin_descuento = precio1 + precio2 + precio3
    impuestos = total_sin_descuento * 0.16
    total_con_descuento = total_sin_descuento * (1 - descuento)
    descuento_total = descuento * 100
    porcentaje_impuestos = impuestos / total_sin_descuento * 100
    total_con_impuestos = total_sin_descuento + impuestos
    total_con_descuento_y_impuestos = total_con_descuento + impuestos
    cantidad_de_dias = 7  # dias de estancia en el paquete
    costo_de_alimentos = 100  # costo de alimentos por dia
    costo_de_transporte = 50  # costo de transporte por dia
    costo_de_acomodacion = 200  # costo de acomodacion por dia
    costo_total_de_alimentos = cantidad_de_dias * costo_de_alimentos
    costo_total_de_transporte = cantidad_de_dias * costo_de_transporte
    costo_total_de_acomodacion = cantidad_de_dias * costo_de_acomodacion
    costo_total_adicional = costo_total_de_alimentos + costo_total_de_transporte + costo_total_de_acomodacion

    return precio1, precio2, precio3, total_sin_descuento, total_con_descuento, impuestos, descuento_total, porcentaje_impuestos, total_con_impuestos, total_con_descuento_y_impuestos, costo_total_adicional

def main():
    try:
        if len(sys.argv) != 5:
            print("Error: Numero de argumentos invalido")
            sys.exit(1)

        precio1 = float(sys.argv[1])
        precio2 = float(sys.argv[2])
        precio3 = float(sys.argv[3])
        descuento = float(sys.argv[4])

        if descuento < 0 or descuento > 1:
            print("Error: Descuento invalido. Debe ser un valor entre 0 y 1")
            sys.exit(1)

        if precio1 < 0 or precio2 < 0 or precio3 < 0:
            print("Error: Precios invalidos. Deben ser valores positivos")
            sys.exit(1)

        precio1, precio2, precio3, total_sin_descuento, total_con_descuento, impuestos, descuento_total, porcentaje_impuestos, total_con_impuestos, total_con_descuento_y_impuestos, costo_total_adicional = cotizar_paquete_turistico(precio1, precio2, precio3, descuento)

        print("Precios de los paquetes turísticos:")
        print(f"Paquete 1: ${precio1:.2f} MXN")
        print(f"Paquete 2: ${precio2:.2f} MXN")
        print(f"Paquete 3: ${precio3:.2f} MXN")
        print(f"Total sin descuento: ${total_sin_descuento:.2f} MXN")
        print(f"Total con descuento: ${total_con_descuento:.2f} MXN")
        print(f"Impuestos: ${impuestos:.2f} MXN")
        print(f"Descuento total: {descuento_total:.2f}%")
        print(f"Porcentaje de impuestos: {porcentaje_impuestos:.2f}%")
        print(f"Total con impuestos: ${total_con_impuestos:.2f} MXN")
        print(f"Total con descuento y impuestos: ${total_con_descuento_y_impuestos:.2f} MXN")
        print(f"Costo total adicional: ${costo_total_adicional:.2f} MXN")
        print("Resumen ejecutivo:")
        print(f"El paquete turístico con descuento y impuestos es el más económico, con un costo total de ${total_con_descuento_y_impuestos:.2f} MXN")

    except ValueError:
        print("Error: Los argumentos deben ser números")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()