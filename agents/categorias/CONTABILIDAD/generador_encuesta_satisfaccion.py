"""
ÁREA: RECURSOS HUMANOS
DESCRIPCIÓN: Agente que realiza generador encuesta satisfaccion
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Configuración por defecto
        if len(sys.argv) > 1:
            num_empleados = int(sys.argv[1])
            num_preguntas = int(sys.argv[2])
        else:
            num_empleados = 150
            num_preguntas = 5
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        # Generar datos de encuesta
        preguntas = [
            "¿Cómo califica su satisfacción laboral?",
            "¿Qué tan bien se comunica con su supervisor?",
            "¿Qué tan equilibrada es su carga de trabajo?",
            "¿Qué tan satisfecho está con su salario?",
            "¿Qué tan probable es que recomiende esta empresa a otros?"
        ]

        resultados = []
        for i in range(num_empleados):
            empleado = {
                "id": i + 1,
                "fecha": fecha_actual,
                "respuestas": [random.randint(1, 5) for _ in range(num_preguntas)]
            }
            resultados.append(empleado)

        # Calcular estadísticas
        total_satisfaccion = sum(sum(empleado["respuestas"] for empleado in resultados)) / (num_empleados * num_preguntas)
        promedio_superior = sum(1 for empleado in resultados if empleado["respuestas"][1] >= 4) / num_empleados * 100
        promedio_comunicacion = sum(empleado["respuestas"][1] for empleado in resultados) / num_empleados
        promedio_carga_trabajo = sum(empleado["respuestas"][2] for empleado in resultados) / num_empleados
        promedio_salario = sum(empleado["respuestas"][3] for empleado in resultados) / num_empleados
        promedio_recomendacion = sum(empleado["respuestas"][4] for empleado in resultados) / num_empleados

        # Generar salida
        print("Encuesta de Satisfacción Laboral - Agencia Santi")
        print(f"Fecha: {fecha_actual}")
        print(f"Total de empleados encuestados: {num_empleados}")
        print(f"Puntuación promedio general: {total_satisfaccion:.2f}/5")
        print(f"Porcentaje de empleados con comunicación superior a 4/5: {promedio_superior:.1f}%")
        print(f"Promedio de comunicación con supervisor: {promedio_comunicacion:.2f}/5")
        print(f"Promedio de equilibrio en la carga de trabajo: {promedio_carga_trabajo:.2f}/5")
        print(f"Promedio de satisfacción con el salario: {promedio_salario:.2f}/5")
        print(f"Promedio de probabilidad de recomendación: {promedio_recomendacion:.2f}/5")
        print("Datos generados correctamente.")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"La encuesta muestra un promedio de satisfacción general de {total_satisfaccion:.2f}/5.")
        print(f"El {promedio_superior:.1f}% de los empleados tienen una comunicación superior a 4/5 con su supervisor.")
        print(f"El promedio de equilibrio en la carga de trabajo es de {promedio_carga_trabajo:.2f}/5.")
        print(f"El promedio de satisfacción con el salario es de {promedio_salario:.2f}/5.")
        print(f"El promedio de probabilidad de recomendación es de {promedio_recomendacion:.2f}/5.")

        # Guardar en archivo JSON
        with open("encuesta_satisfaccion.json", "w") as f:
            json.dump(resultados, f, indent=2)

    except ValueError as e:
        print(f"Error al convertir los argumentos: {str(e)}")
    except Exception as e:
        print(f"Error al generar la encuesta: {str(e)}")

if __name__ == "__main__":
    main()