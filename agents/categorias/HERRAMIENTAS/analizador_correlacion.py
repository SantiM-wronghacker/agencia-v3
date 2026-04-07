#!/usr/bin/env python3
# ÁREA: HERRAMIENTAS
# DESCRIPCIÓN: Agente que realiza analizador correlacion
# TECNOLOGÍA: Python estándar

import os
import sys
import json
import datetime
import math
import re
import random
import statistics

def analizador_correlacion(data):
    try:
        correlacion = statistics.correlation_coefficient(data['columna1'], data['columna2'])
        return correlacion
    except KeyError as e:
        print(f"Error en cálculo de correlación: Faltan datos en la columna '{e.args[0]}'")
        return None
    except statistics.StatisticsError:
        print(f"Error en cálculo de correlación: No se pueden calcular correlaciones con menos de 2 puntos")
        return None
    except Exception as e:
        print(f"Error en cálculo de correlación: {e}")
        return None

def obtener_datos(sys_args):
    if len(sys_args) > 20:
        datos = {
            'columna1': [int(sys_args[1]), int(sys_args[2]), int(sys_args[3]), int(sys_args[4]), int(sys_args[5]),
                         int(sys_args[6]), int(sys_args[7]), int(sys_args[8]), int(sys_args[9]), int(sys_args[10]),
                         int(sys_args[11]), int(sys_args[12]), int(sys_args[13]), int(sys_args[14]), int(sys_args[15]),
                         int(sys_args[16]), int(sys_args[17]), int(sys_args[18]), int(sys_args[19]), int(sys_args[20])],
            'columna2': [int(sys_args[21]), int(sys_args[22]), int(sys_args[23]), int(sys_args[24]), int(sys_args[25]),
                         int(sys_args[26]), int(sys_args[27]), int(sys_args[28]), int(sys_args[29]), int(sys_args[30]),
                         int(sys_args[31]), int(sys_args[32]), int(sys_args[33]), int(sys_args[34]), int(sys_args[35]),
                         int(sys_args[36]), int(sys_args[37]), int(sys_args[38]), int(sys_args[39]), int(sys_args[40])]
        }
    else:
        datos = {
            'columna1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            'columna2': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
        }
    return datos

def obtener_precios_web():
    try:
        texto = "Precio de la gasolina: 25.50\nPrecio del petróleo: 70.20"
        precios = texto.split('\n')
        return precios
    except Exception as e:
        print(f"Error al obtener precios en tiempo real: {e}")
        return []

def obtener_precio_gasolina():
    try:
        # Simulación de precio de la gasolina en tiempo real
        return random.uniform(20, 30)
    except Exception as e:
        print(f"Error al obtener precio de la gasolina: {e}")
        return None

def obtener_precio_petróleo():
    try:
        # Simulación de precio del petróleo en tiempo real
        return random.uniform(60, 80)
    except Exception as e:
        print(f"Error al obtener precio del petróleo: {e}")
        return None

def obtener_resumen_ejecutivo(correlacion):
    try:
        if correlacion > 0.7:
            return "La correlación entre las dos columnas es alta y positiva."
        elif correlacion < -0.7:
            return "La correlación entre las dos columnas es alta y negativa."
        elif correlacion > 0.3:
            return "La correlación entre las dos columnas es moderada y positiva."
        elif correlacion < -0.3:
            return "La correlación entre las dos columnas es moderada y negativa."
        else:
            return "La correlación entre las dos columnas es baja."
    except Exception as e:
        print(f"Error al obtener resumen ejecutivo: {e}")
        return None