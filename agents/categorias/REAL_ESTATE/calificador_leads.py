"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza calificador leads
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def calificar_lead(precios=None, tipo_de_cambio=None, noticias=None, cotizaciones=None):
    try:
        if precios is None:
            precios = {"producto1": 100, "producto2": 200}
        if tipo_de_cambio is None:
            tipo_de_cambio = 1.0
        if noticias is None:
            noticias = "Noticias últimas..."
        if cotizaciones is None:
            cotizaciones = {"acción1": 50.0, "acción2": 75.0}

        calificacion = 0
        if precios["producto1"] > 150:
            calificacion += 10
            print(f"Precio de {precios['producto1']} supera el umbral de $150")
        if tipo_de_cambio > 1.0:
            calificacion += 10
            print(f"Tipo de cambio es superior a 1.0")
        if noticias.find("venta") != -1:
            calificacion += 10
            print(f"Noticias mencionan venta")
        if cotizaciones["acción1"] > 60.0:
            calificacion += 10
            print(f"Cotización de acción 1 supera el umbral de $60.0")
        if cotizaciones["acción2"] > 80.0:
            calificacion += 10
            print(f"Cotización de acción 2 supera el umbral de $80.0")

        return calificacion, precios, tipo_de_cambio, noticias, cotizaciones
    except TypeError as e:
        print(f"Error de tipo: {str(e)}")
    except KeyError as e:
        print(f"Error de clave: {str(e)}")
    except ValueError as e:
        print(f"Error de valor: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")
    return None, None, None, None, None

def main():
    try:
        # Verificar si hay suficientes argumentos
        if len(sys.argv) < 2:
            print("Error: falta el número de lead")
            sys.exit(1)

        # Calificar lead
        lead_id = sys.argv[1]
        precios = None
        tipo_de_cambio = None
        noticias = None
        cotizaciones = None

        if len(sys.argv) > 2:
            precios = json.loads(sys.argv[2])
            tipo_de_cambio = float(sys.argv[3])
            noticias = sys.argv[4]
            cotizaciones = json.loads(sys.argv[5])

        calificacion, precios, tipo_de_cambio, noticias, cotizaciones = calificar_lead(precios, tipo_de_cambio, noticias, cotizaciones)

        # Mostrar resultados
        print(f"Lead {lead_id} calificado con {calificacion} puntos")
        print(f"Precios: {json.dumps(precios)}")
        print(f"Tipo de cambio: {tipo_de_cambio}")
        print(f"Noticias: {noticias}")
        print(f"Cotizaciones: {json.dumps(cotizaciones)}")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El lead {lead_id} ha sido calificado con {calificacion} puntos.")
        print(f"Los precios de los productos están siendo monitoreados y se ajustarán según sea necesario.")
        print(f"El tipo de cambio actual es de {tipo_de_cambio} y se ajustará según sea necesario.")
        print(f"Las noticias actuales son {noticias} y se ajustarán según sea necesario.")
        print(f"Las cotizaciones de las acciones están siendo monitoreadas y se ajustarán según sea necesario.")
    except Exception as e:
        print(f"Error: {str(e)}")
    if __name__ == "__main__":
        main()