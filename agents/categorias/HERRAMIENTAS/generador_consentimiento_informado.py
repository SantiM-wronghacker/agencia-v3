"""
ÁREA: SALUD
DESCRIPCIÓN: Agente que realiza generador consentimiento informado
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
from datetime import datetime
import math
import re
import random

def generar_consentimiento_informado(nombre_paciente, fecha_nacimiento, altura, peso, edad, sexo):
    try:
        # Calcular IMC
        imc = peso / (altura ** 2)

        # Generar consentimiento informado
        consentimiento_informado = f"""
        CONSENTIMIENTO INFORMADO

        Paciente: {nombre_paciente}
        Fecha de nacimiento: {fecha_nacimiento.strftime("%d/%m/%Y")}
        Edad: {edad} años
        Sexo: {sexo}
        Altura: {altura} metros
        Peso: {peso} kilogramos
        IMC: {imc:.2f}

        He leído y comprendido el consentimiento informado y autorizo a que se realicen las pruebas médicas correspondientes.
        """

        return consentimiento_informado

    except Exception as e:
        print(f"Error: {e}")
        return None

def calcular_imc_peso_recomendado(altura, peso):
    try:
        # Peso recomendado para adultos en México
        peso_recomendado = math.ceil(50 + (1.75 - 1.7) * 0.5)
        altura_recomendada = math.ceil(1.65 + (70 - 50) * 0.01)

        return peso_recomendado, altura_recomendada

    except Exception as e:
        print(f"Error: {e}")
        return None

def calcular_edad(fecha_nacimiento):
    try:
        # Calcular edad en años
        edad = datetime.now().year - fecha_nacimiento.year

        return edad

    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    if len(sys.argv) != 6:
        print("Uso: python generador_consentimiento_informado.py <nombre_paciente> <fecha_nacimiento> <altura> <peso> <sexo>")
        sys.exit(1)

    nombre_paciente = sys.argv[1]
    fecha_nacimiento = datetime.strptime(sys.argv[2], "%d/%m/%Y")
    altura = float(sys.argv[3])
    peso = float(sys.argv[4])
    sexo = sys.argv[5]

    consentimiento_informado = generar_consentimiento_informado(nombre_paciente, fecha_nacimiento, altura, peso, calcular_edad(fecha_nacimiento), sexo)

    if consentimiento_informado:
        print(consentimiento_informado)
        print("---------------------------------------------------")
        peso_recomendado, altura_recomendada = calcular_imc_peso_recomendado(altura, peso)
        print(f"Peso recomendado: {peso_recomendado} kg")
        print(f"Altura recomendada: {altura_recomendada} m")
        print("---------------------------------------------------")
        print(f"Fecha de nacimiento: {fecha_nacimiento.strftime('%d/%m/%Y')}")
        print(f"Edad: {calcular_edad(fecha_nacimiento)} años")
        print("---------------------------------------------------")
        print(f"Sexo: {sexo}")
        print(f"IMC: {peso / (altura ** 2):.2f}")
        print("---------------------------------------------------")
        print("RESUMEN EJECUTIVO:")
        print("El paciente tiene un IMC de {:.2f} y se recomienda un peso de {:.0f} kg y una altura de {:.0f} m.".format(peso / (altura ** 2), peso_recomendado, altura_recomendada))

if __name__ == "__main__":
    main()