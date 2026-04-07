import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios(precios=None):
    if precios is None:
        precios = {"comida": 50.0, "bebida": 20.0}
    return precios

def buscar_turnos(turnos=None):
    if turnos is None:
        turnos = [
            {"nombre": "Juan", "hora": "10:00"},
            {"nombre": "Maria", "hora": "11:00"},
            {"nombre": "Pedro", "hora": "12:00"},
            {"nombre": "Ana", "hora": "13:00"},
            {"nombre": "Luis", "hora": "14:00"},
            {"nombre": "Jorge", "hora": "15:00"},
            {"nombre": "Eva", "hora": "16:00"},
            {"nombre": "Carlos", "hora": "17:00"}
        ]
    return turnos

def planificar_turnos(turnos=None, precios=None):
    if turnos is None:
        turnos = buscar_turnos()
    if precios is None:
        precios = extraer_precios()
    
    try:
        total_ingresos = 0
        ingresos_por_turno = []
        for turno in turnos:
            hora = datetime.datetime.strptime(turno["hora"], "%H:%M")
            ingresos = (hora.hour + hora.minute / 60) * precios["comida"] + (hora.hour + hora.minute / 60) * precios["bebida"]
            total_ingresos += ingresos
            ingresos_por_turno.append(ingresos)
            print(f"Turno de {turno['nombre']} a las {turno['hora']}: ${ingresos:.2f}")
        
        print(f"Total de ingresos: ${total_ingresos:.2f}")
        print(f"Promedio de ingresos por turno: ${sum(ingresos_por_turno) / len(ingresos_por_turno):.2f}")
        print(f"Turno con mayor ingreso: {max(turnos, key=lambda x: (datetime.datetime.strptime(x['hora'], '%H:%M').hour + datetime.datetime.strptime(x['hora'], '%H:%M').minute / 60) * precios['comida'] + (datetime.datetime.strptime(x['hora'], '%H:%M').hour + datetime.datetime.strptime(x['hora'], '%H:%M').minute / 60) * precios['bebida'])['nombre']} a las {max(turnos, key=lambda x: (datetime.datetime.strptime(x['hora'], '%H:%M').hour + datetime.datetime.strptime(x['hora'], '%H:%M').minute / 60) * precios['comida'] + (datetime.datetime.strptime(x['hora'], '%H:%M').hour + datetime.datetime.strptime(x['hora'], '%H:%M').minute / 60) * precios['bebida'])['hora']}: ${max(ingresos_por_turno):.2f}")
        print(f"Turno con menor ingreso: {min(turnos, key=lambda x: (datetime.datetime.strptime(x['hora'], '%H:%M').hour + datetime.datetime.strptime(x['hora'], '%H:%M').minute / 60) * precios['comida'] + (datetime.datetime.strptime(x['hora'], '%H:%M').hour + datetime.datetime.strptime(x['hora'], '%H:%M').minute / 60) * precios['bebida'])['nombre']} a las {min(turnos, key=lambda x: (datetime.datetime.strptime(x['hora'], '%H:%M').hour + datetime.datetime.strptime(x['hora'], '%H:%M').minute / 60) * precios['comida'] + (datetime.datetime.strptime(x['hora'], '%H:%M').hour + datetime.datetime.strptime(x['hora'], '%H:%M').minute / 60) * precios['bebida'])['hora']}: ${min(ingresos_por_turno):.2f}")
        print(f"Resumen ejecutivo: Se planificaron {len(turnos)} turnos con un total de ingresos de ${total_ingresos:.2f}. El promedio de ingresos por turno fue de ${sum(ingresos_por_turno) / len(ingresos_por_turno):.2f}.")
    except Exception as e:
        print("Error al planificar turnos: ", str(e))

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Uso: python planificador_turnos_restaurante.py [precios_comida] [precios_bebida]")
        sys.exit