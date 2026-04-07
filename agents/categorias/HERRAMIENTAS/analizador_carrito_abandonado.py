import os
import sys
import json
import datetime
import math
import re
import random

def analizador_carrito_abandonado(datos=None, precios=None, texto=None):
    try:
        if datos is None:
            datos = sys.argv[1]
            datos = json.loads(datos)
        if precios is None:
            precios = {
                'MXN/USD': 20.5
            }
        if texto is None:
            texto = 'Datos de ejemplo'

        if not isinstance(datos, dict) or not isinstance(precios, dict):
            raise ValueError("Datos y precios deben ser diccionarios")

        if 'carritos_abandonados' not in datos or 'total_ventas' not in datos or 'promedio_carrito' not in datos:
            raise ValueError("Datos deben contener carritos_abandonados, total_ventas y promedio_carrito")

        if 'MXN/USD' not in precios:
            raise ValueError("Precios deben contener MXN/USD")

        carritos_abandonados = datos['carritos_abandonados']
        total_ventas = datos['total_ventas']
        promedio_carrito = datos['promedio_carrito']
        precio_mxusd = precios['MXN/USD']

        if total_ventas == 0:
            tasa_abandono = 0
        else:
            tasa_abandono = (carritos_abandonados / total_ventas) * 100

        if carritos_abandonados == 0:
            promedio_precio = 0
        else:
            promedio_precio = (total_ventas / carritos_abandonados) * precio_mxusd

        # Calcular tasa de abandono por categoría
        categorias = datos.get('categorias', {})
        tasa_abandono_por_categoria = {}
        for categoria, carritos_abandonados_categoria in categorias.items():
            if total_ventas == 0:
                tasa_abandono_categoria = 0
            else:
                tasa_abandono_categoria = (carritos_abandonados_categoria / total_ventas) * 100
            tasa_abandono_por_categoria[categoria] = tasa_abandono_categoria

        # Calcular promedio de precio por categoría
        promedio_precio_por_categoria = {}
        for categoria, carritos_abandonados_categoria in categorias.items():
            if carritos_abandonados_categoria == 0:
                promedio_precio_categoria = 0
            else:
                promedio_precio_categoria = (total_ventas / carritos_abandonados_categoria) * precio_mxusd
            promedio_precio_por_categoria[categoria] = promedio_precio_categoria

        # Imprimir resultados
        print("ÁREA: ECOMMERCE")
        print("DESCRIPCIÓN: Analizador carrito abandonado")
        print("TECNOLOGÍA: Python estándar")
        print(f"Carritos abandonados: {carritos_abandonados}")
        print(f"Total ventas: {total_ventas} MXN")
        print(f"Promedio carrito: {promedio_carrito}")
        print(f"Tasa de abandono: {tasa_abandono}%")
        print(f"Promedio precio: {promedio_precio} MXN")
        print(f"Tasa de abandono por categoría: {tasa_abandono_por_categoria}")
        print(f"Promedio precio por categoría: {promedio_precio_por_categoria}")
        print(f"Texto: {texto}")

        # Imprimir resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"La tasa de abandono de carritos es del {tasa_abandono}%")
        print(f"El promedio de precio de los carritos es de {promedio_precio} MXN")
        print(f"La tasa de abandono por categoría es la siguiente: {tasa_abandono_por_categoria}")
        print(f"El promedio de precio por categoría es la siguiente: {promedio_precio_por_categoria}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    datos = sys.argv[1]
    datos = json.loads(datos)
    analizador_carrito_abandonado(datos=datos)