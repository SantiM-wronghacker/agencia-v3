"""
AREA: MARKETING
DESCRIPCION: Agente que realiza generador bio redes sociales
TECNOLOGIA: Python estandar
"""

import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        if len(sys.argv)!= 6:
            raise ValueError("Necesita proporcionar los siguientes argumentos: nombre_agencia, ciudad, num_clientes, num_proyectos, num_empleados")

        nombre_agencia = sys.argv[1]
        ciudad = sys.argv[2]
        num_clientes = int(sys.argv[3])
        num_proyectos = int(sys.argv[4])
        num_empleados = int(sys.argv[5])

        if num_clientes < 0 or num_proyectos < 0 or num_empleados < 0:
            raise ValueError("Los numeros de clientes, proyectos y empleados no pueden ser negativos")

        bio = f"Somos {nombre_agencia}, una agencia de marketing con sede en {ciudad}. Contamos con {num_clientes} clientes satisfechos y hemos realizado {num_proyectos} proyectos exitosos. Nuestro equipo está conformado por {num_empleados} empleados altamente capacitados."

        print("Bio Redes Sociales:")
        print("--------------------")
        print(bio)
        print(f"Número de clientes: {num_clientes}")
        print(f"Número de proyectos: {num_proyectos}")
        print(f"Número de empleados: {num_empleados}")
        print(f"Fecha actual: {datetime.date.today()}")
        print(f"Promedio de proyectos por empleado: {num_proyectos / num_empleados:.2f}")
        print(f"Promedio de clientes por proyecto: {num_clientes / num_proyectos:.2f}")
        print(f"Índice de satisfacción del cliente: {(num_clientes / (num_clientes + num_proyectos)) * 100:.2f}%")
        print(f"Índice de productividad del empleado: {(num_proyectos / num_empleados) * 100:.2f}%")
        print(f"Tiempo promedio de entrega de proyectos: {num_proyectos / (num_empleados * 12):.2f} meses")
        print(f"Costo promedio por proyecto: ${num_proyectos * 10000:.2f} MXN")
        print(f"Costo promedio por cliente: ${num_clientes * 5000:.2f} MXN")

        datos = {
            "nombre_agencia": nombre_agencia,
            "ciudad": ciudad,
            "num_clientes": num_clientes,
            "num_proyectos": num_proyectos,
            "num_empleados": num_empleados,
            "fecha_actual": str(datetime.date.today()),
            "promedio_proyectos_por_empleado": num_proyectos / num_empleados,
            "promedio_clientes_por_proyecto": num_clientes / num_proyectos,
            "indice_satisfaccion_cliente": (num_clientes / (num_clientes + num_proyectos)) * 100,
            "indice_productividad_empleado": (num_proyectos / num_empleados) * 100,
            "tiempo_promedio_entrega_proyectos": num_proyectos / (num_empleados * 12),
            "costo_promedio_por_proyecto": num_proyectos * 10000,
            "costo_promedio_por_cliente": num_clientes * 5000
        }

        print("\nResumen Ejecutivo:")
        print("--------------------")
        print(f"La agencia {nombre_agencia} tiene un total de {num_clientes} clientes y {num_proyectos} proyectos. Nuestro equipo de {num_empleados} empleados ha logrado un promedio de {num_proyectos / num_empleados:.2f} proyectos por empleado y un índice de satisfacción del cliente del {(num_clientes / (num_clientes + num_proyectos)) * 100:.2f}%.")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()