"""
ÁREA: LOGISTICA
DESCRIPCIÓN: Agente que realiza generador guia envio
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random
import argparse

def generar_guia_envio(remitente=None, destinatario=None, peso=None, volumen=None, tipo_envio="estandar"):
    try:
        if remitente is None or destinatario is None:
            raise ValueError("Faltan datos de remitente o destinatario.")
        if peso is None or volumen is None:
            raise ValueError("Faltan datos de peso o volumen.")

        # Calcula costo de envío con fórmula realista para México
        if tipo_envio == "estandar":
            costo_envio = 100.0 + (peso * 10) + (volumen * 5)
        elif tipo_envio == "express":
            costo_envio = 200.0 + (peso * 15) + (volumen * 10)
        else:
            raise ValueError("Tipo de envío no válido.")

        # Genera guía de envío
        guia_envio = {
            "remitente": remitente,
            "destinatario": destinatario,
            "peso": peso,
            "volumen": volumen,
            "costo_envio": costo_envio,
            "fecha_envio": datetime.date.today(),
            "estado": "En proceso de envío",
            "modalidad": tipo_envio,
            "duracion": "3-5 días hábiles" if tipo_envio == "estandar" else "1-2 días hábiles"
        }

        # Imprime guía de envío
        print("Guía de Envío:")
        print("----------------")
        print(f"Remitente: {guia_envio['remitente']}")
        print(f"Destinatario: {guia_envio['destinatario']}")
        print(f"Peso: {guia_envio['peso']} kg")
        print(f"Volumen: {guia_envio['volumen']} m³")
        print(f"Costo de envío: ${guia_envio['costo_envio']:.2f}")
        print(f"Fecha de envío: {guia_envio['fecha_envio']}")
        print(f"Estado: {guia_envio['estado']}")
        print(f"Modalidad: {guia_envio['modalidad']}")
        print(f"Duración: {guia_envio['duracion']}")
        print(f"Tipo de envío: {tipo_envio}")
        print(f"Fecha estimada de entrega: {(guia_envio['fecha_envio'] + datetime.timedelta(days=3)) if tipo_envio == 'estandar' else (guia_envio['fecha_envio'] + datetime.timedelta(days=1))}")

        # Imprime resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print("-------------------")
        print(f"El costo de envío es de ${guia_envio['costo_envio']:.2f}")
        print(f"El peso del paquete es de {guia_envio['peso']} kg")
        print(f"El volumen del paquete es de {guia_envio['volumen']} m³")
        print(f"La modalidad de envío es {guia_envio['modalidad']}")
        print(f"La duración del envío es de {guia_envio['duracion']}")

    except ValueError as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) < 5:
        print("Uso: python generador_guia_envio.py <remitente> <destinatario> <peso> <volumen> <tipo_envio>")
        return

    remitente = sys.argv[1]
    destinatario = sys.argv[2]
    peso = float(sys.argv[3])
    volumen = float(sys.argv[4])
    tipo_envio = sys.argv[5] if len(sys.argv) > 5 else "estandar"

    generar_guia_envio(remitente, destinatario, peso, volumen, tipo_envio)

if __name__ == "__main__":
    main()