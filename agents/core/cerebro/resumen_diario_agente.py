"""
ÁREA: CEREBRO
DESCRIPCIÓN: Genera un reporte de texto con todas las tareas que el sistema completó durante el día.
TECNOLOGÍA: Python, datetime, sys
"""

import os
import sys
import time
import datetime
import math
import json

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

class Tarea:
    def __init__(self, descripcion, tiempo_inicio, tiempo_fin):
        self.descripcion = descripcion
        self.tiempo_inicio = tiempo_inicio
        self.tiempo_fin = tiempo_fin

class ResumenDiarioAgente:
    def __init__(self):
        self.tareas = []
        self.total_tiempo = datetime.timedelta(0)

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)
        self.total_tiempo += tarea.tiempo_fin - tarea.tiempo_inicio

    def generar_reporte(self):
        reporte = "ÁREA: CEREBRO\nDESCRIPCIÓN: Genera un reporte de texto con todas las tareas que el sistema completó durante el día.\nTECNOLOGÍA: Python, datetime, sys\n\n"
        reporte += "Resumen diario de tareas\n"
        reporte += "-------------------------\n"
        for i, tarea in enumerate(self.tareas):
            reporte += f"Tarea {i+1}: {tarea.descripcion}\n"
            reporte += f"Tiempo de inicio: {tarea.tiempo_inicio.strftime('%Y-%m-%d %H:%M:%S')}\n"
            reporte += f"Tiempo de fin: {tarea.tiempo_fin.strftime('%Y-%m-%d %H:%M:%S')}\n"
            reporte += f"Duración: {(tarea.tiempo_fin - tarea.tiempo_inicio).total_seconds() / 60:.2f} minutos\n"
            reporte += f"Tiempo de trabajo efectivo: {(tarea.tiempo_fin - tarea.tiempo_inicio).total_seconds() / 60 - (tarea.tiempo_fin - tarea.tiempo_inicio).total_seconds() / 60 * 0.1:.2f} minutos\n" # descuento 10% por distracciones
            reporte += "-------------------------\n"
        reporte += f"Total de tiempo: {self.total_tiempo.total_seconds() / 60:.2f} minutos\n"
        reporte += f"Promedio de tiempo por tarea: {(self.total_tiempo.total_seconds() / 60) / len(self.tareas):.2f} minutos\n"
        reporte += "-------------------------\n"
        reporte += "Resumen ejecutivo:\n"
        reporte += f"El sistema completó un total de {len(self.tareas)} tareas durante el día.\n"
        reporte += f"El tiempo total invertido en estas tareas fue de {self.total_tiempo.total_seconds() / 60:.2f} minutos.\n"
        reporte += f"La duración promedio por tarea fue de {self.total_tiempo.total_seconds() / 60 / len(self.tareas):.2f} minutos.\n"
        reporte += f"La productividad diaria fue de {len(self.tareas) / (self.total_tiempo.total_seconds() / 3600):.2f} tareas/hora.\n"
        reporte += f"El tiempo de trabajo efectivo diario fue de {(self.total_tiempo.total_seconds() / 60 - (self.total_tiempo.total_seconds() / 60) * 0.1):.2f} minutos.\n"
        reporte += "-------------------------\n"
        return reporte

def main():
    if len(sys.argv) > 1:
        try:
            archivo = sys.argv[1]
            with open(archivo, 'r') as f:
                tareas = json.load(f)
                agente = ResumenDiarioAgente()
                for tarea in tareas:
                    agente.agregar_tarea(Tarea(tarea['descripcion'], datetime.datetime.strptime(tarea['tiempo_inicio'], '%Y-%m-%d %H:%M:%S'), datetime.datetime.strptime(tarea['tiempo_fin'], '%Y-%m-%d %H:%M:%S')))
                print(agente.generar_reporte())
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Error: Faltan argumentos")

if __name__ == "__main__":
    main()