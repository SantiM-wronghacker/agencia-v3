"""
AREA: HERRAMIENTAS
DESCRIPCION: Agente que realiza analizador tendencias
TECNOLOGIA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def analizador_tendencias(precios, tipo_cambio):
    # Calcula tendencia de precios
    try:
        tendencia_precios = sum(precios.values()) / len(precios)
        desviacion_estandar = math.sqrt(sum((x - tendencia_precios) ** 2 for x in precios.values()) / len(precios))
        varianza = sum((x - tendencia_precios) ** 2 for x in precios.values()) / len(precios)
        max_precio = max(precios.values())
        min_precio = min(precios.values())
        precio_promedio = sum(precios.values()) / len(precios)
        coeficiente_variacion = desviacion_estandar / precio_promedio
    except ZeroDivisionError:
        print("No hay precios para calcular la tendencia")
        return

    # Calcula tendencia del tipo de cambio
    try:
        tendencia_tipo_cambio = tipo_cambio
    except TypeError:
        print("El tipo de cambio debe ser un número")
        return

    # Imprime resultados
    print(f'Tendencia de precios: {tendencia_precios:.2f} MXN')
    print(f'Desviación estandar: {desviacion_estandar:.2f} MXN')
    print(f'Varianza: {varianza:.2f} MXN^2')
    print(f'Tendencia del tipo de cambio: {tendencia_tipo_cambio:.2f} MXN')
    print(f'Precios: {json.dumps(precios, indent=4)}')
    print(f'Tipo de cambio: {tipo_cambio:.2f} MXN')
    print(f'Datos reales: {WEB}')
    print(f'Fecha de análisis: {datetime.date.today()}')
    print(f'Número de precios: {len(precios)}')
    print(f'Máximo precio: {max_precio:.2f} MXN')
    print(f'Mínimo precio: {min_precio:.2f} MXN')
    print(f'Precio promedio: {precio_promedio:.2f} MXN')
    print(f'Coeficiente de variación: {coeficiente_variacion:.2f}')
    print(f'Porcentaje de variación: {(coeficiente_variacion * 100):.2f}%')
    print(f'Diferencia entre el máximo y el mínimo precio: {(max_precio - min_precio):.2f} MXN')
    print(f'Porcentaje de diferencia entre el máximo y el mínimo precio: {((max_precio - min_precio) / precio_promedio * 100):.2f}%')

    # Resumen ejecutivo
    print(f'Resumen ejecutivo: La tendencia de precios es de {tendencia_precios:.2f} MXN, mientras que la tendencia del tipo de cambio es de {tendencia_tipo_cambio:.2f} MXN. El precio promedio es de {precio_promedio:.2f} MXN con una desviación estandar de {desviacion_estandar:.2f} MXN.')

def main():
    try:
        if len(sys.argv) > 1:
            # Cargar datos desde archivo
            with open(sys.argv[1], 'r') as archivo:
                datos = json.load(archivo)
                precios = datos['precios']
                tipo_cambio = datos['tipo_cambio']
        else:
            # Datos por defecto
            precios = {'producto1': 10.0, 'producto2': 20.0, 'producto3': 30.0}
            tipo_cambio = 1.0
        analizador_tendencias(precios, tipo_cambio)
    except FileNotFoundError:
        print("Archivo no encontrado")
    except json.JSONDecodeError:
        print("Error al parsear el archivo JSON")

if __name__ == "__main__":
    main()