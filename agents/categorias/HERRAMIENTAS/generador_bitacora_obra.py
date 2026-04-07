"""
ÁREA: CONSTRUCCIÓN
DESCRIPCIÓN: Agente que realiza generador bitacora obra
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
from datetime import datetime
import math
import re
import random

def generar_bitacora_obra():
    try:
        # Crea un objeto datetime para obtener la fecha actual
        fecha_actual = datetime.now()
        
        # Obtiene el monto de la obra en pesos mexicanos
        monto = float(sys.argv[1]) if len(sys.argv) > 1 else 1000000.0
        
        # Obtiene el porcentaje de avance de la obra
        porcentaje_avance = float(sys.argv[2]) if len(sys.argv) > 2 else 50.0
        
        # Obtiene el número de trabajadores en la obra
        num_trabajadores = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        
        # Obtiene el costo por hora de cada trabajador
        costo_hora = float(sys.argv[4]) if len(sys.argv) > 4 else 50.0
        
        # Obtiene los precios de los materiales
        precios_materiales = {
            'cemento': float(sys.argv[5]) if len(sys.argv) > 5 else 25.0,
            'acero': float(sys.argv[6]) if len(sys.argv) > 6 else 30.0,
            'madera': float(sys.argv[7]) if len(sys.argv) > 7 else 20.0
        }
        
        # Obtiene las cotizaciones de la obra
        cotizaciones = {
            'cotizacion1': float(sys.argv[8]) if len(sys.argv) > 8 else 10000.0,
            'cotizacion2': float(sys.argv[9]) if len(sys.argv) > 9 else 20000.0
        }
        
        # Calcula el costo total de la obra
        costo_total = monto * (porcentaje_avance / 100)
        
        # Calcula el tiempo total de trabajo
        tiempo_trabajo = costo_total / (num_trabajadores * costo_hora)
        
        # Obtiene el costo total de los materiales
        costo_materiales = sum(precios_materiales.values())
        
        # Obtiene el costo total de las cotizaciones
        costo_cotizaciones = sum(cotizaciones.values())
        
        # Imprime los datos en la bitacora
        print(f'Fecha: {fecha_actual}')
        print(f'Monto: {monto} pesos')
        print(f'Porcentaje avance: {porcentaje_avance}%')
        print(f'Número de trabajadores: {num_trabajadores}')
        print(f'Costo hora: {costo_hora} pesos')
        print(f'Costo total: {costo_total} pesos')
        print(f'Tiempo trabajo: {tiempo_trabajo} horas')
        print(f'Costo materiales: {costo_materiales} pesos')
        print(f'Cotizaciones: {cotizaciones}')
        print(f'Resumen ejecutivo:')
        print(f'  - El costo total de la obra es de {costo_total} pesos')
        print(f'  - El tiempo total de trabajo es de {tiempo_trabajo} horas')
        print(f'  - El costo total de los materiales es de {costo_materiales} pesos')
        print(f'  - El costo total de las cotizaciones es de {costo_cotizaciones} pesos')
        
    except ValueError as e:
        print(f'Ocurrió un error de valor: {str(e)}')
    except IndexError as e:
        print(f'Ocurrió un error de índice: {str(e)}')
    except Exception as e:
        print(f'Ocurrió un error: {str(e)}')

def main():
    if len(sys.argv) < 10:
        print('Faltan argumentos. Utilice el comando con los siguientes argumentos:')
        print('  - monto')
        print('  - porcentaje_avance')
        print('  - num_trabajadores')
        print('  - costo_hora')
        print('  - precio_cemento')
        print('  - precio_acero')
        print('  - precio_madera')
        print('  - cotizacion1')
        print('  - cotizacion2')
    else:
        generar_bitacora_obra()

if __name__ == "__main__":
    main()