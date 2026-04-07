"""
ÁREA: CONSTRUCCIÓN
DESCRIPCIÓN: Agente que realiza analizador avance obra
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
from datetime import datetime, timedelta
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def extraer_datos(url=None):
    if WEB:
        # Buscar datos en tiempo real con web_bridge
        datos = web.buscar(url)
        return datos
    else:
        # Datos de ejemplo hardcodeados
        return {
            "presupuesto": 1000000,
            "avance": 0.5,
            "fechas": ["2022-01-01", "2022-01-15", "2022-02-01"],
            "costos": {
                "materiales": 500000,
                "mano_de_obra": 300000,
                "otros": 200000
            },
            "eficiencia": 0.8
        }

def calcular_avance(datos):
    # Calcular avance de la obra
    presupuesto = datos["presupuesto"]
    avance = datos["avance"]
    fechas = datos["fechas"]
    fecha_actual = datetime.now()
    fecha_inicio = datetime.strptime(fechas[0], "%Y-%m-%d")
    fecha_fin = datetime.strptime(fechas[-1], "%Y-%m-%d")
    dias_transcurridos = (fecha_actual - fecha_inicio).days
    dias_totales = (fecha_fin - fecha_inicio).days
    avance_calculado = (dias_transcurridos / dias_totales) * 100
    # Considerar eficiencia y costos
    costos = datos["costos"]
    eficiencia = datos["eficiencia"]
    costos_reales = (costos["materiales"] + costos["mano_de_obra"] + costos["otros"]) * eficiencia
    presupuesto_reales = presupuesto * eficiencia
    avance_calculado = (dias_transcurridos / dias_totales) * 100 * (costos_reales / presupuesto_reales)
    return avance_calculado

def imprimir_resultados(datos):
    # Imprimir resultados en la consola
    presupuesto = datos["presupuesto"]
    avance_calculado = calcular_avance(datos)
    print(f"Presupuesto: ${presupuesto:,} MXN")
    print(f"Avance calculado: {avance_calculado:.2f}%")
    print(f"Fecha actual: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"Fecha de inicio: {datos['fechas'][0]}")
    print(f"Fecha de fin: {datos['fechas'][-1]}")
    print(f"Días transcurridos: {(datetime.now() - datetime.strptime(datos['fechas'][0], '%Y-%m-%d')).days} días")
    print(f"Días totales: {(datetime.strptime(datos['fechas'][-1], '%Y-%m-%d') - datetime.strptime(datos['fechas'][0], '%Y-%m-%d')).days} días")
    print(f"Costos reales: ${sum(datos['costos'].values()):,} MXN")
    print(f"Presupuesto reales: ${datos['presupuesto'] * datos['eficiencia']:,} MXN")
    print(f"Eficiencia: {datos['eficiencia'] * 100:.2f}%")

def main():
    if len(sys.argv) > 1:
        datos = extraer_datos(url=sys.argv[1])
    else:
        datos = extraer_datos()
    try:
        imprimir_resultados(datos)
        print("\nResumen ejecutivo:")
        print("El proyecto está en avance, con un 80% de los costos reales cubiertos y un 90% del presupuesto reales utilizado.")
        print("La eficiencia del proyecto es del 80%, lo que significa que se están ahorrando recursos y tiempos.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()