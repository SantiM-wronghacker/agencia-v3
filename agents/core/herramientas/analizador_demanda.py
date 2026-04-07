"""
ÁREA: LOGISTICA
DESCRIPCIÓN: Agente que realiza analizador demanda
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def analizador_demanda(precios=None, tipo_de_cambio=None):
    try:
        # Cargar datos de ejemplo hardcodeados como fallback
        if precios is None:
            precios = {
                "materia_prima": float(sys.argv[1]) if len(sys.argv) > 1 else 120.50,
                "energia": float(sys.argv[2]) if len(sys.argv) > 2 else 10.25,
                "transporte": float(sys.argv[3]) if len(sys.argv) > 3 else 5.75
            }
        if tipo_de_cambio is None:
            tipo_de_cambio = float(sys.argv[4]) if len(sys.argv) > 4 else 20.50

        # Calcular indicadores de demanda
        materia_prima_demanda = precios["materia_prima"] * 1000
        energia_demanda = precios["energia"] * 5000
        transporte_demanda = precios["transporte"] * 2000

        # Calcular costo total
        costo_total = materia_prima_demanda + energia_demanda + transporte_demanda

        # Calcular utilidad
        utilidad = costo_total * 0.20

        # Calcular impuestos
        impuestos = costo_total * 0.16

        # Calcular costo total con impuestos
        costo_total_con_impuestos = costo_total + impuestos

        # Imprimir resultados
        print("Materia prima demandada: {:.2f} MXN".format(materia_prima_demanda))
        print("Energía demandada: {:.2f} MXN".format(energia_demanda))
        print("Transporte demandado: {:.2f} MXN".format(transporte_demanda))
        print("Costo total: {:.2f} MXN".format(costo_total))
        print("Utilidad: {:.2f} MXN".format(utilidad))
        print("Impuestos: {:.2f} MXN".format(impuestos))
        print("Costo total con impuestos: {:.2f} MXN".format(costo_total_con_impuestos))
        print("Tipo de cambio: {:.2f}".format(tipo_de_cambio))
        print("Indicadores de demanda:")
        print("  - Materia prima: {:.2f}%".format(materia_prima_demanda / (materia_prima_demanda + energia_demanda + transporte_demanda) * 100))
        print("  - Energía: {:.2f}%".format(energia_demanda / (materia_prima_demanda + energia_demanda + transporte_demanda) * 100))
        print("  - Transporte: {:.2f}%".format(transporte_demanda / (materia_prima_demanda + energia_demanda + transporte_demanda) * 100))
        print("Fecha de análisis: {}".format(datetime.date.today()))

        # Imprimir resumen ejecutivo
        print("\nResumen ejecutivo:")
        print("El análisis de demanda indica que la materia prima es el componente más significativo del costo total, representando {:.2f}% del costo total.".format(materia_prima_demanda / (materia_prima_demanda + energia_demanda + transporte_demanda) * 100))
        print("La utilidad es de {:.2f} MXN, lo que representa una ganancia del {:.2f}% sobre el costo total.".format(utilidad, utilidad / costo_total * 100))
        print("El tipo de cambio es de {:.2f}, lo que puede afectar la competitividad de la empresa en el mercado internacional.".format(tipo_de_cambio))

    except IndexError:
        print("No se proporcionaron suficientes argumentos. Utilice los siguientes argumentos: materia_prima, energia, transporte, tipo_de_cambio")
    except ValueError:
        print("No se proporcionaron valores numéricos. Utilice los siguientes argumentos: materia_prima, energia, transporte, tipo_de_cambio")
    except Exception as e:
        print("Ocurrió un error: {}".format(str(e)))

if __name__ == "__main__":
    analizador_demanda()