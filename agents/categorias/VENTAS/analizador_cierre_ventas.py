"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza analizador cierre ventas
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def analizar_cierre_ventas(total, ventas_semana, crecimiento, mayor_venta, menor_venta):
    try:
        # Verificar que los valores sean numéricos
        if not all(isinstance(x, (int, float)) for x in [total, ventas_semana, crecimiento, mayor_venta, menor_venta]):
            raise ValueError("Todos los valores deben ser numéricos")

        # Verificar que el crecimiento sea un valor entre 0 y 100
        if not 0 <= crecimiento <= 100:
            raise ValueError("El crecimiento debe ser un valor entre 0 y 100")

        # Calcular porcentaje de crecimiento realista para México
        crecimiento_real = (crecimiento / 100) + 1
        ventas_anuales = ventas_semana * 52
        ventas_proyectadas = ventas_anuales * crecimiento_real

        # Calcular mayor y menor venta del mes
        mayor_venta_mensual = mayor_venta * 4
        menor_venta_mensual = menor_venta * 4

        # Calcular promedio de ventas diarias
        promedio_ventas_diarias = ventas_semana / 7

        # Calcular ganancia total
        ganancia_total = total * 0.2  # suponiendo una tasa de ganancia del 20%

        # Calcular ganancia por semana
        ganancia_semanal = ventas_semana * 0.2

        # Calcular ganancia por mes
        ganancia_mensual = ventas_anuales * 0.2

        # Calcular ventas por día de la semana
        ventas_lunes = ventas_semana * 0.2
        ventas_martes = ventas_semana * 0.2
        ventas_miercoles = ventas_semana * 0.2
        ventas_jueves = ventas_semana * 0.2
        ventas_viernes = ventas_semana * 0.2
        ventas_sabado = ventas_semana * 0.1
        ventas_domingo = ventas_semana * 0.1

        # Calcular ventas totales por mes
        ventas_totales_mensual = ventas_anuales * 4

        print(f"Cierre de ventas: {total:.2f} MXN")
        print(f"Ventas de la semana: {ventas_semana:.2f} MXN")
        print(f"Porcentaje de crecimiento: {crecimiento}%")
        print(f"Mayor venta del día: {mayor_venta:.2f} MXN")
        print(f"Menor venta del día: {menor_venta:.2f} MXN")
        print(f"Mayor venta del mes: {mayor_venta_mensual:.2f} MXN")
        print(f"Menor venta del mes: {menor_venta_mensual:.2f} MXN")
        print(f"Promedio de ventas diarias: {promedio_ventas_diarias:.2f} MXN")
        print(f"Ventas por día de la semana: Lunes: {ventas_lunes:.2f} MXN, Martes: {ventas_martes:.2f} MXN, Miércoles: {ventas_miercoles:.2f} MXN, Jueves: {ventas_jueves:.2f} MXN, Viernes: {ventas_viernes:.2f} MXN, Sábado: {ventas_sabado:.2f} MXN, Domingo: {ventas_domingo:.2f} MXN")
        print(f"Ventas totales por mes: {ventas_totales_mensual:.2f} MXN")
        print(f"Ganancia total: {ganancia_total:.2f} MXN")
        print(f"Ganancia por semana: {ganancia_semanal:.2f} MXN")
        print(f"Ganancia por mes: {ganancia_mensual:.2f} MXN")
        print(f"Ventas proyectadas: {ventas_proyectadas:.2f} MXN")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) != 6:
        print("Uso: python analizador_cierre_ventas.py <total> <ventas_semana> <crecimiento> <mayor_venta> <menor_venta>")
        return