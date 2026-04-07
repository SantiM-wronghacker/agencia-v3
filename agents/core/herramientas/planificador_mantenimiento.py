"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza planificador mantenimiento
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def calcular_mantenimiento(costo_mantenimiento, frecuencia_mantenimiento, costo_reparacion):
    try:
        if frecuencia_mantenimiento <= 0:
            raise ValueError("Frecuencia de mantenimiento no puede ser cero o negativo.")
        if costo_mantenimiento < 0:
            raise ValueError("Costo de mantenimiento no puede ser negativo.")
        if costo_reparacion < 0:
            raise ValueError("Costo de reparación no puede ser negativo.")
        if costo_reparacion == 0:
            raise ZeroDivisionError("Costo de reparación no puede ser cero.")
        mantenimiento_diario = costo_mantenimiento + (costo_reparacion / frecuencia_mantenimiento)
        mantenimiento_anual = mantenimiento_diario * 365
        mantenimiento_diario_por_hora = mantenimiento_diario / 24
        mantenimiento_anual_por_hora = mantenimiento_anual / (24 * 365)
        return mantenimiento_diario, mantenimiento_anual, mantenimiento_diario_por_hora, mantenimiento_anual_por_hora
    except ValueError as e:
        print(f"Error: {e}")
        return None, None, None, None
    except ZeroDivisionError:
        print("Error: Frecuencia de mantenimiento no puede ser cero.")
        return None, None, None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None, None

def planificar_mantenimiento():
    # Permitir parametros por sys.argv
    if len(sys.argv) > 1:
        try:
            costo_mantenimiento = float(sys.argv[1])
            frecuencia_mantenimiento = int(sys.argv[2])
            costo_reparacion = float(sys.argv[3])
        except ValueError:
            print("Error: Los parametros deben ser numericos.")
            return
    else:
        costo_mantenimiento = 10000.0
        frecuencia_mantenimiento = 30  # Días
        costo_reparacion = 50000.0

    # Calcular mantenimiento
    mantenimiento_diario, mantenimiento_anual, mantenimiento_diario_por_hora, mantenimiento_anual_por_hora = calcular_mantenimiento(costo_mantenimiento, frecuencia_mantenimiento, costo_reparacion)

    # Imprimir resultados
    if mantenimiento_diario is not None:
        print(f"Mantenimiento diario: ${mantenimiento_diario:.2f} MXN")
        print(f"Mantenimiento anual: ${mantenimiento_anual:.2f} MXN")
        print(f"Mantenimiento diario por hora: ${mantenimiento_diario_por_hora:.2f} MXN")
        print(f"Mantenimiento anual por hora: ${mantenimiento_anual_por_hora:.2f} MXN")
        print(f"Costo de reparación: ${costo_reparacion:.2f} MXN")
        print(f"Frecuencia de mantenimiento: {frecuencia_mantenimiento} días")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El plan de mantenimiento recomendado es realizar un mantenimiento diario de ${mantenimiento_diario:.2f} MXN, "
              f"lo que equivale a un mantenimiento anual de ${mantenimiento_anual:.2f} MXN. "
              f"El mantenimiento diario por hora es de ${mantenimiento_diario_por_hora:.2f} MXN, "
              f"lo que equivale a un mantenimiento anual por hora de ${mantenimiento_anual_por_hora:.2f} MXN.")

if __name__ == "__main__":
    planificar_mantenimiento()