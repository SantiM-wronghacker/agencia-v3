"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora dosis
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def calculadora_dosis(peso, edad, altura, dosis_diaria):
    """
    Calculadora de dosis para medicamentos.
    """
    try:
        # Validaciones
        if peso <= 0 or edad <= 0 or altura <= 0 or dosis_diaria <= 0:
            raise ValueError("Los valores deben ser positivos.")

        if altura < 1.2 or altura > 2.2:
            raise ValueError("La altura debe estar entre 1.2 y 2.2 metros.")

        if edad < 0 or edad > 120:
            raise ValueError("La edad debe estar entre 0 y 120 años.")

        if dosis_diaria < 0:
            raise ValueError("La dosis diaria no puede ser negativa.")

        # Calculos
        area_corporal = peso / (altura ** 2)
        masa_corporal = peso / (altura ** 2)
        dosis_total = dosis_diaria * 30  # 30 días
        dosis_diaria_real = dosis_diaria * (1 + (edad - 35) * 0.01)  # ajuste según edad
        dosis_total_real = dosis_diaria_real * 30  # 30 días
        imc = masa_corporal
        porcentaje_grasa = (masa_corporal - 21) * 100
        peso_ideal = 60 / altura

        # Impresión de resultados
        print(f"Área corporal: {area_corporal:.2f} m²")
        print(f"Masa corporal: {masa_corporal:.2f} kg/m²")
        print(f"Dosis diaria: {dosis_diaria} mg")
        print(f"Dosis diaria real: {dosis_diaria_real:.2f} mg")
        print(f"Dosis total: {dosis_total} mg")
        print(f"Dosis total real: {dosis_total_real:.2f} mg")
        print(f"Fecha y hora: {datetime.datetime.now()}")
        print(f"Peso ideal para altura: {peso_ideal:.2f} kg")
        print(f"Índice de masa corporal (IMC): {imc:.2f}")
        print(f"Porcentaje de grasa corporal: {porcentaje_grasa:.2f}%")
        print(f"Indicador de sobrepeso: {('Sobrepeso' if imc > 25 else 'Normal')}")
        print(f"Indicador de obesidad: {('Obesidad' if imc > 30 else 'Normal')}")
        print(f"Porcentaje de agua corporal: {((1.2 * masa_corporal) - 6.24) * 100}")
        print(f"Indicador de desnutrición: {('Desnutrición' if masa_corporal < 18.5 else 'Normal')}")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"La persona tiene un peso de {peso} kg, una altura de {altura} m y una edad de {edad} años.")
        print(f"Se le recetó una dosis diaria de {dosis_diaria} mg, que se ajustó a {dosis_diaria_real:.2f} mg según su edad.")
        print(f"Se le recomendó un peso ideal de {peso_ideal:.2f} kg para su altura.")

    except ValueError as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) != 5:
        print("Usage: python calculadora_dosis.py <peso> <edad> <altura> <dosis_diaria>")
        sys.exit(1)

    try:
        peso = float(sys.argv[1])
        edad = float(sys.argv[2])
        altura = float(sys.argv[3])
        dosis_diaria = float(sys.argv[4])
        calculadora_dosis(peso, edad, altura, dosis_diaria)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()