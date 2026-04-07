import sys
import json
import datetime
import math
import re
import random
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        fecha_inicio = datetime.date.today() - datetime.timedelta(days=30)
        fecha_fin = datetime.date.today()
        num_registros = 10
        moneda = "MXN"
        tipo_cambio = 1.0
        area = "CEREBRO"
        descripcion = "Agente que realiza resumen ejecutivo"
        tecnologia = "Python estándar"

        # Parámetros de la línea de comandos
        if len(sys.argv) > 1:
            fecha_inicio = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        if len(sys.argv) > 2:
            fecha_fin = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
        if len(sys.argv) > 3:
            num_registros = int(sys.argv[3])
        if len(sys.argv) > 4:
            moneda = sys.argv[4]
        if len(sys.argv) > 5:
            tipo_cambio = float(sys.argv[5])
        if len(sys.argv) > 6:
            area = sys.argv[6]
        if len(sys.argv) > 7:
            descripcion = sys.argv[7]
        if len(sys.argv) > 8:
            tecnologia = sys.argv[8]

        # Validar parámetros
        if num_registros <= 0:
            raise ValueError("Número de registros debe ser positivo")
        if tipo_cambio <= 0:
            raise ValueError("Tipo de cambio debe ser positivo")

        # Generar datos aleatorios
        registros = []
        total = 0.0
        max_valor = 0.0
        min_valor = float('inf')
        promedio_valor = 0.0
        for _ in range(num_registros):
            fecha = fecha_inicio + datetime.timedelta(days=random.randint(0, (fecha_fin - fecha_inicio).days))
            valor = round(random.uniform(1000, 100000), 2)
            registros.append({"fecha": fecha.strftime("%Y-%m-%d"), "valor": valor})
            total += valor
            max_valor = max(max_valor, valor)
            min_valor = min(min_valor, valor)

        # Calculos precisos y realistas para México
        promedio_valor = round(total / num_registros, 2)
        total_pesos = round(total * tipo_cambio, 2)
        total_dolares = round(total / tipo_cambio, 2)

        # Encabezado
        print(f"AREA: {area}")
        print(f"DESCRIPCION: {descripcion}")
        print(f"TECNOLOGIA: {tecnologia}")

        # Datos concretos
        print(f"Fecha inicio: {fecha_inicio.strftime('%Y-%m-%d')}")
        print(f"Fecha fin: {fecha_fin.strftime('%Y-%m-%d')}")
        print(f"Número de registros: {num_registros}")
        print(f"Moneda: {moneda}")
        print(f"Tipo de cambio: {tipo_cambio}")
        print(f"Total: {total}")
        print(f"Total pesos: {total_pesos} {moneda}")
        print(f"Total dólares: {total_dolares} USD")
        print(f"Promedio: {promedio_valor}")
        print(f"Maximo: {max_valor}")
        print(f"Minimo: {min_valor}")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El total de la operación es de {total} {moneda}, equivalente a {total_pesos} {moneda} o {total_dolares} USD.")
        print(f"El promedio de la operación es de {promedio_valor} {moneda}.")
        print(f"El máximo y mínimo valores de la operación son respectivamente de {max_valor} {moneda} y {min_valor} {moneda}.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Fin del programa")

if __name__ == "__main__":
    main()