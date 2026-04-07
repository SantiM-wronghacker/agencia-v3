"""
ÁREA: AGRICULTURA
DESCRIPCIÓN: Agente que realiza planificador siembra
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def planificador_siembra(tipo_semilla, area_cultivo, precio_fertilizante, precio_herbicida):
    try:
        # Obtiene la fecha actual
        fecha_actual = datetime.datetime.now()
        
        # Verifica que el área de cultivo sea un número positivo
        if area_cultivo <= 0:
            raise ValueError("El área de cultivo debe ser un número positivo")
        
        # Verifica que el precio del fertilizante y el herbicida sean números positivos
        if precio_fertilizante < 0 or precio_herbicida < 0:
            raise ValueError("El precio del fertilizante y el herbicida deben ser números positivos")
        
        # Calcula el costo total de la siembra
        costo_total = (precio_fertilizante * area_cultivo) + (precio_herbicida * area_cultivo)
        
        # Calcula el precio por hectárea
        precio_por_hectarea = costo_total / area_cultivo
        
        # Calcula el beneficio por hectárea
        beneficio_por_hectarea = (precio_fertilizante + precio_herbicida) / area_cultivo
        
        # Genera un número aleatorio para simular la cantidad de unidades cosechadas
        unidades_cosechadas = random.randint(1000, 2000)
        
        # Calcula el precio de venta por unidad
        precio_venta_por_unidad = (costo_total + beneficio_por_hectarea * area_cultivo) / unidades_cosechadas
        
        # Imprime los resultados
        print(f"Fecha de siembra: {fecha_actual.strftime('%d/%m/%Y')}")
        print(f"Tipo de semilla: {tipo_semilla}")
        print(f"Área de cultivo: {area_cultivo} hectáreas")
        print(f"Costo total de la siembra: {costo_total:.2f} pesos mexicanos")
        print(f"Precio por hectárea: {precio_por_hectarea:.2f} pesos mexicanos")
        print(f"Beneficio por hectárea: {beneficio_por_hectarea:.2f} pesos mexicanos")
        print(f"Unidades cosechadas: {unidades_cosechadas}")
        print(f"Precio de venta por unidad: {precio_venta_por_unidad:.2f} pesos mexicanos")
        print(f"Tiempo de siembra: {math.ceil(area_cultivo / 10)} días")
        print(f"Costo de mano de obra: {math.ceil((costo_total * 0.2))} pesos mexicanos")
        
        # Imprime un resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El planificador de siembra indica que se puede obtener un beneficio de {beneficio_por_hectarea:.2f} pesos mexicanos por hectárea.")
        print(f"El precio de venta por unidad es de {precio_venta_por_unidad:.2f} pesos mexicanos.")
        print(f"El tiempo de siembra es de aproximadamente {math.ceil(area_cultivo / 10)} días.")
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Error: Faltan argumentos. Utilice la siguiente sintaxis:")
        print("python planificador_siembra.py <tipo_semilla> <area_cultivo> <precio_fertilizante> <precio_herbicida>")
    else:
        tipo_semilla = sys.argv[1]
        area_cultivo = float(sys.argv[2])
        precio_fertilizante = float(sys.argv[3])
        precio_herbicida = float(sys.argv[4])
        planificador_siembra(tipo_semilla, area_cultivo, precio_fertilizante, precio_herbicida)