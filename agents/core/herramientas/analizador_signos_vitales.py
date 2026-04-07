"""
ÁREA: SALUD
DESCRIPCIÓN: Agente que realiza analizador signos vitales
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def analizador_signos_vitales(temperatura, presion_sanguinea, frecuencia_cardiaca, peso=None, altura=None):
    """
    Analiza los signos vitales y devuelve un informe.

    Args:
        temperatura (float): Temperatura en grados Celsius.
        presion_sanguinea (float): Presión sanguinea en milímetros de mercurio.
        frecuencia_cardiaca (int): Frecuencia cardíaca en latidos por minuto.
        peso (float, optional): Peso en kilogramos. Defaults to None.
        altura (float, optional): Altura en metros. Defaults to None.

    Returns:
        dict: Informe con los resultados del análisis.
    """
    try:
        informe = {
            "temperatura": temperatura,
            "presion_sanguinea": presion_sanguinea,
            "frecuencia_cardiaca": frecuencia_cardiaca
        }

        # Análisis de temperatura
        if temperatura < 36.0:
            informe["temperatura"] = "Hipotermia"
        elif temperatura > 38.0:
            informe["temperatura"] = "Fiebre"
        else:
            informe["temperatura"] = "Temperatura normal"

        # Análisis de presión sanguinea
        if presion_sanguinea < 90:
            informe["presion_sanguinea"] = "Hipotensión"
        elif presion_sanguinea > 140:
            informe["presion_sanguinea"] = "Hipertensión"
        else:
            informe["presion_sanguinea"] = "Presión sanguinea normal"

        # Análisis de frecuencia cardíaca
        if frecuencia_cardiaca < 60:
            informe["frecuencia_cardiaca"] = "Bradicardia"
        elif frecuencia_cardiaca > 100:
            informe["frecuencia_cardiaca"] = "Tachicardia"
        else:
            informe["frecuencia_cardiaca"] = "Frecuencia cardíaca normal"

        # Análisis de otros signos vitales
        if peso is not None and altura is not None:
            imc = peso / (altura ** 2)
            if imc < 18.5:
                informe["imc"] = "Peso bajo"
            elif imc < 25:
                informe["imc"] = "Peso normal"
            elif imc < 30:
                informe["imc"] = "Peso sobrepeso"
            else:
                informe["imc"] = "Obesidad"
        else:
            informe["imc"] = "No disponible"

        # Análisis de otros signos vitales
        if temperatura < 36.5:
            informe["signos_vitales"] = "Signos vitales críticos"
        elif temperatura < 37.5:
            informe["signos_vitales"] = "Signos vitales graves"
        elif temperatura < 38.5:
            informe["signos_vitales"] = "Signos vitales moderados"
        else:
            informe["signos_vitales"] = "Signos vitales normales"

        return informe
    except Exception as e:
        return {"error": str(e)}

def main():
    if len(sys.argv) != 5:
        print("Uso: python analizador_signos_vitales.py <temperatura> <presion_sanguinea> <frecuencia_cardiaca> <peso> <altura>")
        return

    temperatura = float(sys.argv[1])
    presion_sanguinea = float(sys.argv[2])
    frecuencia_cardiaca = int(sys.argv[3])
    peso = float(sys.argv[4]) if len(sys.argv) > 4 else None
    altura = float(sys.argv[5]) if len(sys.argv) > 5 else None

    informe = analizador_signos_vitales(temperatura, presion_sanguinea, frecuencia_cardiaca, peso, altura)

    print("Informe de signos vitales:")
    for clave, valor in informe.items():
        print(f"{clave}: {valor}")

    print("\nResumen ejecutivo:")
    print