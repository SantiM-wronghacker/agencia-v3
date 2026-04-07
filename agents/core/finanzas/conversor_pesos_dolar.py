"""
ÁREA: FINANZAS
DESCRIPCIÓN: Convierte precios de propiedades de pesos a dólares
TECNOLOGÍA: Python, requests
"""

import requests
import sys
import time
import json
import math

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def obtener_tipo_cambio_actual():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        datos = respuesta.json()
        return datos["rates"]["COP"]
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el tipo de cambio: {e}")
        return None

def convertir_pesos_a_dolares(precios_pesos, tipo_cambio):
    try:
        if tipo_cambio is None:
            raise ValueError("Tipo de cambio no disponible")
        precios_dolares = [precio / tipo_cambio for precio in precios_pesos]
        return precios_dolares
    except ValueError as e:
        print(f"Error al convertir precios: {e}")
        return None

def calcular_estadisticas(precios_dolares):
    try:
        if precios_dolares is None:
            raise ValueError("Precios en dólares no disponibles")
        mayor_precio = max(precios_dolares)
        menor_precio = min(precios_dolares)
        promedio_precio = sum(precios_dolares) / len(precios_dolares)
        desviacion_estandar = math.sqrt(sum((x - promedio_precio) ** 2 for x in precios_dolares) / len(precios_dolares))
        return mayor_precio, menor_precio, promedio_precio, desviacion_estandar
    except ValueError as e:
        print(f"Error al calcular estadísticas: {e}")
        return None, None, None, None

def main():
    if len(sys.argv) > 1:
        try:
            precios_pesos = [float(arg) for arg in sys.argv[1:]]
        except ValueError:
            print("Valores no válidos. Usando valores por defecto")
            precios_pesos = [100000000, 200000000, 300000000, 400000000, 500000000]
            print("Precios en pesos por defecto:", precios_pesos)
    else:
        print("Usando valores por defecto")
        precios_pesos = [100000000, 200000000, 300000000, 400000000, 500000000]
        print("Precios en pesos por defecto:", precios_pesos)
    
    tipo_cambio_actual = obtener_tipo_cambio_actual()
    if tipo_cambio_actual is not None:
        print(f"Tipo de cambio actual: 1 USD = {tipo_cambio_actual} COP")
        
        time.sleep(2)
        
        precios_dolares = convertir_pesos_a_dolares(precios_pesos, tipo_cambio_actual)
        if precios_dolares is not None:
            print("Precios en dólares:", precios_dolares)
            mayor_precio, menor_precio, promedio_precio, desviacion_estandar = calcular_estadisticas(precios_dolares)
            if mayor_precio is not None:
                print("Resumen:")
                print(f"Mayor precio en dólares: {mayor_precio}")
                print(f"Menor precio en dólares: {menor_precio}")
                print(f"Promedio de precios en dólares: {promedio_precio}")
                print(f"Desviación estándar de precios en dólares: {desviacion_estandar}")
                print("Resumen ejecutivo:")
                print(f"El precio promedio de las propiedades es de {promedio_precio} dólares, con una desviación estándar de {desviacion_estandar} dólares.")
                print(f"El mayor precio es de {mayor_precio} dólares y el menor precio es de {menor_precio} dólares.")

if __name__ == "__main__":
    main()