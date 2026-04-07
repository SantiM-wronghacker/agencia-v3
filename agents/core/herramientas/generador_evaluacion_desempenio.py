"""
ÁREA: RECURSOS HUMANOS
DESCRIPCIÓN: Agente que realiza generador evaluacion desempenio
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        num_empleados = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        rango_evaluacion = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        fecha_inicio = sys.argv[3] if len(sys.argv) > 3 else "2022-01-01"
        fecha_fin = sys.argv[4] if len(sys.argv) > 4 else "2022-12-31"

        # Validar fechas
        try:
            datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")
            datetime.datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            print("Error: Fecha inválida. Debe ser en formato YYYY-MM-DD")
            return

        # Generar evaluación de desempeño
        evaluacion = []
        for i in range(num_empleados):
            empleado = {
                "nombre": f"Empleado {i+1}",
                "evaluacion": random.randint(1, rango_evaluacion),
                "fecha": datetime.date.today().strftime("%Y-%m-%d"),
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "promedio_anual": random.uniform(10000, 50000),
                "bono": random.uniform(0, 10000)
            }
            evaluacion.append(empleado)

        # Imprimir resultados
        print("Evaluación de Desempeño:")
        for empleado in evaluacion:
            print(f"Nombre: {empleado['nombre']}, Evaluación: {empleado['evaluacion']}, Fecha: {empleado['fecha']}, Fecha de inicio: {empleado['fecha_inicio']}, Fecha de fin: {empleado['fecha_fin']}, Promedio anual: {empleado['promedio_anual']:.2f}, Bono: {empleado['bono']:.2f}")

        # Estadísticas
        promedio_evaluacion = sum([empleado['evaluacion'] for empleado in evaluacion]) / len(evaluacion)
        empleado_mejor_evaluacion = max(evaluacion, key=lambda x: x['evaluacion'])
        empleado_peor_evaluacion = min(evaluacion, key=lambda x: x['evaluacion'])
        promedio_promedio_anual = sum([empleado['promedio_anual'] for empleado in evaluacion]) / len(evaluacion)
        total_bono = sum([empleado['bono'] for empleado in evaluacion])

        print(f"Promedio de evaluación: {promedio_evaluacion:.2f}")
        print(f"Empleado con mejor evaluación: {empleado_mejor_evaluacion['nombre']} con {empleado_mejor_evaluacion['evaluacion']}")
        print(f"Empleado con peor evaluación: {empleado_peor_evaluacion['nombre']} con {empleado_peor_evaluacion['evaluacion']}")
        print(f"Promedio anual promedio: {promedio_promedio_anual:.2f}")
        print(f"Total de bonos: {total_bono:.2f}")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"Se evaluaron {num_empleados} empleados con un promedio de evaluación de {promedio_evaluacion:.2f}.")
        print(f"El empleado con mejor evaluación fue {empleado_mejor_evaluacion['nombre']} con una evaluación de {empleado_mejor_evaluacion['evaluacion']}.")
        print(f"El empleado con peor evaluación fue {empleado_peor_evaluacion['nombre']} con una evaluación de {empleado_peor_evaluacion['evaluacion']}.")
        print(f"El promedio anual promedio fue de {promedio_promedio_anual:.2f} y el total de bonos fue de {total_bono:.2f}.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()