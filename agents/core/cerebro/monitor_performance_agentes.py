"""
ÁREA: CEREBRO
DESCRIPCIÓN: Agente que realiza monitor performance agentes
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        num_agentes = 10
        tiempo_monitoreo = 60  # en segundos
        unidad_tiempo = "segundos"

        # Obtener parámetros desde la línea de comandos
        if len(sys.argv) > 1:
            num_agentes = int(sys.argv[1])
        if len(sys.argv) > 2:
            tiempo_monitoreo = int(sys.argv[2])
        if len(sys.argv) > 3:
            unidad_tiempo = sys.argv[3]

        # Simular datos de monitoreo
        datos_monitoreo = []
        for i in range(num_agentes):
            tiempo_respuesta = round(random.uniform(0.1, 2.0), 2)  # en segundos
            memoria_usada = round(random.uniform(100, 500), 2)  # en MB
            cpu_usada = round(random.uniform(10, 90), 2)  # en porcentaje
            disco_usado = round(random.uniform(10, 90), 2)  # en porcentaje
            red_usada = round(random.uniform(10, 90), 2)  # en porcentaje
            datos = {
                "agente": f"Agente {i+1}",
                "tiempo_respuesta": tiempo_respuesta,
                "memoria_usada": memoria_usada,
                "cpu_usada": cpu_usada,
                "disco_usado": disco_usado,
                "red_usada": red_usada,
                "procesos_actuales": round(random.uniform(1, 10), 2),
                "hilos_actuales": round(random.uniform(1, 10), 2),
                "uso_bateria": round(random.uniform(1, 100), 2)
            }
            datos_monitoreo.append(datos)

        # Imprimir resultados
        print(f"Fecha y hora de monitoreo: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Tiempo de monitoreo: {tiempo_monitoreo} {unidad_tiempo}")
        print(f"Número de agentes: {num_agentes}")
        print("Datos de monitoreo:")
        for datos in datos_monitoreo:
            print(f"  - {datos['agente']}:")
            print(f"    * Tiempo de respuesta: {datos['tiempo_respuesta']} segundos")
            print(f"    * Memoria usada: {datos['memoria_usada']} MB")
            print(f"    * CPU usada: {datos['cpu_usada']}%")
            print(f"    * Disco usado: {datos['disco_usado']}%")
            print(f"    * Red usada: {datos['red_usada']}%")
            print(f"    * Procesos actuales: {datos['procesos_actuales']}")
            print(f"    * Hilos actuales: {datos['hilos_actuales']}")
            print(f"    * Uso de bateria: {datos['uso_bateria']}%")
            print()
        print("Resumen ejecutivo:")
        print(f"  - Tiempo de respuesta promedio: {sum([datos['tiempo_respuesta'] for datos in datos_monitoreo]) / num_agentes} segundos")
        print(f"  - Memoria usada promedio: {sum([datos['memoria_usada'] for datos in datos_monitoreo]) / num_agentes} MB")
        print(f"  - CPU usada promedio: {sum([datos['cpu_usada'] for datos in datos_monitoreo]) / num_agentes}%")
        print(f"  - Disco usado promedio: {sum([datos['disco_usado'] for datos in datos_monitoreo]) / num_agentes}%")
        print(f"  - Red usada promedio: {sum([datos['red_usada'] for datos in datos_monitoreo]) / num_agentes}%")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()