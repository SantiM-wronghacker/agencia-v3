"""
ÁREA: MICRO_TAREAS
DESCRIPCIÓN: extractor números texto
TECNOLOGÍA: Python estándar
"""

import os
import sys
import re
import json
import datetime
import math
import random

def extractor_numeros_texto(entrada, patron_numeros=r"[-+]?\d*\.\d+|[-+]?\d+"):
    """Función pura, sin prints, sin side effects."""
    try:
        numeros = re.findall(patron_numeros, entrada)
        if numeros:
            return json.dumps(numeros)
        else:
            return "INVALIDO:no_numeros"
    except re.error as e:
        return f"ERROR: Patrón de números inválido. {str(e)}"
    except Exception as e:
        return f"ERROR: {str(e)}"

def calcular_promedio(numeros):
    try:
        return math.fsum(map(float, numeros)) / len(numeros)
    except ZeroDivisionError:
        return "ERROR: No se pueden calcular promedios con ceros"
    except ValueError:
        return "ERROR: No se pueden calcular promedios con valores no numéricos"

def calcular_maximo(numeros):
    try:
        return max(map(float, numeros))
    except ValueError:
        return "ERROR: No se pueden encontrar máximos con valores no numéricos"

def calcular_minimo(numeros):
    try:
        return min(map(float, numeros))
    except ValueError:
        return "ERROR: No se pueden encontrar mínimos con valores no numéricos"

def calcular_desviacion_estandar(numeros):
    try:
        promedio = calcular_promedio(numeros)
        varianza = sum((float(num) - promedio) ** 2 for num in numeros) / len(numeros)
        return math.sqrt(varianza)
    except (ZeroDivisionError, ValueError):
        return "ERROR: No se pueden calcular desviaciones estandar con ceros o valores no numéricos"

def calcular_media_mensual(numeros):
    try:
        return math.fsum(map(float, numeros)) / len(numeros) * 12
    except (ZeroDivisionError, ValueError):
        return "ERROR: No se pueden calcular medias mensuales con ceros o valores no numéricos"

def calcular_maximo_anual(numeros):
    try:
        return max(map(float, numeros)) * 12
    except ValueError:
        return "ERROR: No se pueden encontrar máximos anuales con valores no numéricos"

def calcular_minimo_anual(numeros):
    try:
        return min(map(float, numeros)) * 12
    except ValueError:
        return "ERROR: No se pueden encontrar mínimos anuales con valores no numéricos"

def main():
    entrada = sys.argv[1] if len(sys.argv) > 1 else "default_value"
    patron_numeros = sys.argv[2] if len(sys.argv) > 2 else r"[-+]?\d*\.\d+|[-+]?\d+"
    resultado = extractor_numeros_texto(entrada, patron_numeros)
    numeros = json.loads(resultado)
    print(f"Resultado: {resultado}")
    print(f"Entrada: {entrada}")
    print(f"Patrón de números: {patron_numeros}")
    print(f"Fecha y hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Número de números encontrados: {len(numeros)}")
    print(f"Promedio: {calcular_promedio(numeros)}")
    print(f"Maximo: {calcular_maximo(numeros)}")
    print(f"Minimo: {calcular_minimo(numeros)}")
    print(f"Desviación estandar: {calcular_desviacion_estandar(numeros)}")
    print(f"Media mensual: {calcular_media_mensual(numeros)}")
    print(f"Maximo anual: {calcular_maximo_anual(numeros)}")
    print(f"Minimo anual: {calcular_minimo_anual(numeros)}")
    print(f"Resumen ejecutivo: Se han encontrado {len(numeros)} números en la entrada, con un promedio de {calcular_promedio(numeros)} y una desviación estandar de {calcular_desviacion_estandar(numeros)}")

if __name__ == "__main__":
    main()