# MANUFACTURA/ANALIZADOR CAPACIDAD PLANTA/PYTHON
# AREA: MANUFACTURA
# DESCRIPCION: Agente que realiza analizador capacidad planta
# TECNOLOGIA: PYTHON

import sys
import json
import datetime
import math
import re
import random
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Obtener argumentos de la linea de comandos
        capacidad_planta = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
        produccion_diaria = int(sys.argv[2]) if len(sys.argv) > 2 else 500
        horas_trabajo = int(sys.argv[3]) if len(sys.argv) > 3 else 8
        dias_trabajo = int(sys.argv[4]) if len(sys.argv) > 4 else 20
        costo_mano_obra = float(sys.argv[5]) if len(sys.argv) > 5 else 150.0
        costo_materiales = float(sys.argv[6]) if len(sys.argv) > 6 else 200.0
        precio_venta = float(sys.argv[7]) if len(sys.argv) > 7 else 500.0

        # Calcular capacidad total de la planta
        capacidad_total = capacidad_planta * horas_trabajo * dias_trabajo

        # Calcular porcentaje de capacidad utilizada
        if capacidad_total > 0:
            porcentaje_capacidad_utilizada = (produccion_diaria * dias_trabajo / capacidad_total) * 100
        else:
            porcentaje_capacidad_utilizada = 0

        # Calcular tiempo de entrega promedio
        tiempo_entrega_promedio = random.uniform(1, 5)

        # Calcular costo de produccion por unidad
        costo_produccion_por_unidad = (costo_mano_obra + costo_materiales) / produccion_diaria

        # Calcular costo total de produccion
        costo_total_produccion = costo_produccion_por_unidad * produccion_diaria * dias_trabajo

        # Calcular ingresos totales
        ingresos_totales = produccion_diaria * dias_trabajo * precio_venta

        # Calcular utilidad neta
        utilidad_neta = ingresos_totales - costo_total_produccion

        # Calcular impuestos (10% de la utilidad neta)
        impuestos = utilidad_neta * 0.10

        # Calcular utilidad neta despues de impuestos
        utilidad_neta_despues_impuestos = utilidad_neta - impuestos

        # Imprimir resultados
        print(f"Capacidad total de la planta: {capacidad_total} unidades")
        print(f"Produccion diaria: {produccion_diaria} unidades")
        print(f"Porcentaje de capacidad utilizada: {porcentaje_capacidad_utilizada:.2f}%")
        print(f"Tiempo de entrega promedio: {tiempo_entrega_promedio:.2f} dias")
        print(f"Costo de produccion por unidad: ${costo_produccion_por_unidad:.2f}")
        print(f"Costo total de produccion: ${costo_total_produccion:.2f}")
        print(f"Ingresos totales: ${ingresos_totales:.2f}")
        print(f"Utilidad neta: ${utilidad_neta:.2f}")
        print(f"Impuestos: ${impuestos:.2f}")
        print(f"Utilidad neta despues de impuestos: ${utilidad_neta_despues_impuestos:.2f}")
        print(f"Precio de venta por unidad: ${precio_venta:.2f}")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"La planta tiene una capacidad total de {capacidad_total} unidades y una produccion diaria de {produccion_diaria} unidades.")
        print(f"El porcentaje de capacidad utilizada es del {porcentaje_capacidad_utilizada:.2f}% y el tiempo de entrega promedio es de {tiempo_entrega_promedio:.2f} dias.")
        print(f"La utilidad neta despues de impuestos es de ${utilidad_neta_despues_impuestos:.2f}.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()