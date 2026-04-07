"""
AREA: HERRAMIENTAS
DESCRIPCION: Agente que realiza planificador capacitacion
TECNOLOGIA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def planificador_capacitacion():
    try:
        # Obtener datos desde argumentos
        if len(sys.argv) < 7:
            raise ValueError("Falta de argumentos")
        
        datos = {
            "capacitaciones": [
                {"nombre": sys.argv[1], "fecha": sys.argv[2], "precios": float(sys.argv[3])},
                {"nombre": sys.argv[4], "fecha": sys.argv[5], "precios": float(sys.argv[6])}
            ]
        }
        
        # Procesar datos
        capacitaciones = datos["capacitaciones"]
        total_precios = sum([capacitacion['precios'] for capacitacion in capacitaciones])
        promedio_precios = total_precios / len(capacitaciones)
        max_precio = max([capacitacion['precios'] for capacitacion in capacitaciones])
        min_precio = min([capacitacion['precios'] for capacitacion in capacitaciones])
        fecha_proxima_capacitacion = min([datetime.datetime.strptime(capacitacion['fecha'], '%Y-%m-%d') for capacitacion in capacitaciones])
        
        # Calcular indicadores financieros
        tasa_de_retorno_promedio = (promedio_precios / max_precio) * 100
        return_on_investment = (total_precios / max_precio) * 100
        cost_benefit_ratio = (total_precios / (max_precio + min_precio)) * 100
        
        # Calcular impuestos y descuentos
        impuesto_iva = total_precios * 0.16
        descuento_promocional = total_precios * 0.05
        
        # Imprimir resultados
        print("Capacitaciones:")
        for i, capacitacion in enumerate(capacitaciones):
            print(f"- {capacitacion['nombre']} ({capacitacion['fecha']}) - {capacitacion['precios']} MXN")
        print(f"Total de precios: {total_precios} MXN")
        print(f"Promedio de precios: {promedio_precios} MXN")
        print(f"Precio máximo: {max_precio} MXN")
        print(f"Precio mínimo: {min_precio} MXN")
        print(f"Fecha de la próxima capacitación: {fecha_proxima_capacitacion.strftime('%Y-%m-%d')}")
        print(f"Impuesto IVA: {impuesto_iva} MXN")
        print(f"Descuento promocional: {descuento_promocional} MXN")
        print(f"Tasa de retorno promedio: {tasa_de_retorno_promedio}%")
        print(f"Return on Investment (ROI): {return_on_investment}%")
        print(f"Cost-Benefit Ratio: {cost_benefit_ratio}%")
        print(f"Total con impuestos y descuentos: {total_precios + impuesto_iva - descuento_promocional} MXN")
        
        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"La próxima capacitación es {fecha_proxima_capacitacion.strftime('%Y-%m-%d')} con un precio de {min_precio} MXN.")
        print(f"El total de precios es {total_precios} MXN, con un promedio de {promedio_precios} MXN.")
        print(f"Se recomienda considerar un descuento promocional de {descuento_promocional} MXN y un impuesto IVA de {impuesto_iva} MXN.")
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    planificador_capacitacion()