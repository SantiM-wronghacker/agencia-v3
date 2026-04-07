import os
import sys
import json
import datetime
import math
import re
import random
from datetime import date

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def calcular_costo(costo_unidad, cantidad_unidades):
    return costo_unidad * cantidad_unidades

def calcular_recaudacion(precio_venta, cantidad_unidades):
    return precio_venta * cantidad_unidades

def calcular_utilidad(costo_total, recaudacion_total):
    return recaudacion_total - costo_total

def planificar_produccion(fecha_actual, cantidad_unidades, duracion_produccion, horas_produccion_por_dia):
    return cantidad_unidades * duracion_produccion * horas_produccion_por_dia

def calcular_costo_material(costo_material_unidad, cantidad_material_unidades):
    return costo_material_unidad * cantidad_material_unidades

def calcular_costo_mantenimiento(costo_mantenimiento_unidad, cantidad_unidades):
    return costo_mantenimiento_unidad * cantidad_unidades

def calcular_costo_total(costo_material, costo_mantenimiento):
    return costo_material + costo_mantenimiento

def calcular_precio_venta(costo_unidad, margen_ganancia):
    return costo_unidad * (1 + margen_ganancia)

def main():
    if len(sys.argv) > 9:
        costo_unidad = float(sys.argv[1])
        cantidad_unidades = int(sys.argv[2])
        duracion_produccion = int(sys.argv[3])
        horas_produccion_por_dia = int(sys.argv[4])
        costo_material_unidad = float(sys.argv[5])
        cantidad_material_unidades = int(sys.argv[6])
        costo_mantenimiento_unidad = float(sys.argv[7])
        margen_ganancia = float(sys.argv[8])
    else:
        costo_unidad = 150.0
        cantidad_unidades = 1000
        duracion_produccion = 5
        horas_produccion_por_dia = 8
        costo_material_unidad = 20.0
        cantidad_material_unidades = 500
        costo_mantenimiento_unidad = 10.0
        margen_ganancia = 0.3

    if WEB:
        # Buscar datos reales con web_bridge
        pass
    else:
        fecha_actual = date.today()
        costo_total = calcular_costo(costo_unidad, cantidad_unidades)
        costo_material = calcular_costo_material(costo_material_unidad, cantidad_material_unidades)
        costo_mantenimiento = calcular_costo_mantenimiento(costo_mantenimiento_unidad, cantidad_unidades)
        costo_total_real = calcular_costo_total(costo_material, costo_mantenimiento)
        recaudacion_total = calcular_recaudacion(calcular_precio_venta(costo_unidad, margen_ganancia), cantidad_unidades)
        utilidad_total = calcular_utilidad(costo_total_real, recaudacion_total)
        unidades_producidas = planificar_produccion(fecha_actual, cantidad_unidades, duracion_produccion, horas_produccion_por_dia)

    print("ÁREA: MANUFACTURA")
    print("DESCRIPCIÓN: Agente que realiza planificador produccion semanal")
    print("TECNOLOGÍA: Python estándar")

    print("\nResumen Ejecutivo:")
    print("--------------------")
    print(f"Cantidad de unidades a producir: {cantidad_unidades}")
    print(f"Cantidad total de unidades producidas: {unidades_producidas}")
    print(f"Costo total de producción: ${costo_total:.2f}")
    print(f"Costo total real: ${costo_total_real:.2f}")
    print(f"Recaudación total: ${recaudacion_total:.2f}")
    print(f"Utilidad total: ${utilidad_total:.2f}")
    print(f"Precio de venta: ${calcular_precio_venta(costo_unidad, margen_ganancia):.2f}")
    print("\nResumen de Costos:")
    print("-------------------")
    print(f"Costo de materiales: ${costo_material:.2f}")
    print(f"Costo de mantenimiento: ${costo_mantenimiento:.2f}")
    print(f"Costo de mano de obra: ${costo_total - costo_material - costo_mantenimiento:.2f}")

if __name__ == "__main__":
    main()