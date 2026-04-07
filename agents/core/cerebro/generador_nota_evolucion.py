"""
ÁREA: CEREBRO
DESCRIPCIÓN: Agente que realiza generador nota evolucion
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random
from datetime import date

def extraer_precios(precio_medicamento=150.00, precio_equipo_medico=8000.00, precio_servicio=200.00):
    try:
        with open('precios.json', 'r') as f:
            precios = json.load(f)
        return {
            "precio_medicamento": precios.get("precio_medicamento", precio_medicamento),
            "precio_equipo_medico": precios.get("precio_equipo_medico", precio_equipo_medico),
            "precio_servicio": precios.get("precio_servicio", precio_servicio)
        }
    except FileNotFoundError:
        return {
            "precio_medicamento": precio_medicamento,
            "precio_equipo_medico": precio_equipo_medico,
            "precio_servicio": precio_servicio
        }

def calcular_imc(peso, altura):
    try:
        altura_en_metros = altura / 100
        imc = peso / (altura_en_metros ** 2) * 10000
        if imc < 18.5:
            categoria = "Bajo peso"
        elif imc < 25:
            categoria = "Peso normal"
        elif imc < 30:
            categoria = "Sobrepeso"
        else:
            categoria = "Obesidad"
        return imc, categoria
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def calcular_costo_total(precio_medicamento, cantidad_medicamento):
    try:
        return precio_medicamento * cantidad_medicamento
    except Exception as e:
        print(f"Error: {e}")
        return None

def calcular_costo_total_con_iva(costo_total):
    try:
        return costo_total * 1.16
    except Exception as e:
        print(f"Error: {e}")
        return None

def generar_nota_evolucion(paciente, medicamento, cantidad_medicamento, peso, temperatura, presion_sanguinea, fecha=None):
    try:
        fecha = fecha or date.today()
        precio_medicamento = extraer_precios()["precio_medicamento"]
        nota = f"""
Nota de Evolución del Paciente {paciente}
Fecha: {fecha}
Medicamento: {medicamento} ({precio_medicamento:.2f} MXN por unidad)
Cantidad: {cantidad_medicamento} unidades
Peso: {peso:.2f} kg
Temperatura: {temperatura:.2f}°C
Presión Sanguínea: {presion_sanguinea} mmHg
Costo Total: {calcular_costo_total(precio_medicamento, cantidad_medicamento):.2f} MXN
Costo Total con IVA (16%): {calcular_costo_total_con_iva(calcula_costo_total(precio_medicamento, cantidad_medicamento)):.2f} MXN
IMC: {calcular_imc(peso, 1.70)[0]:.2f} ({calcular_imc(peso, 1.70)[1]})
Peso ideal para sexo masculino: {math.ceil(peso * 0.9)} kg
Peso ideal para sexo femenino: {math.ceil(peso * 0.8)} kg
"""
        return nota
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) != 7:
        print("Uso: python generador_nota_evolucion.py <paciente> <medicamento> <cantidad_medicamento> <peso> <temperatura> <presion_sanguinea>")
        sys.exit(1)

    paciente = sys.argv[1]
    medicamento = sys.argv[2]
    cantidad_medicamento = int(sys.argv[3])
    peso = float(sys.argv[4])
    temperatura = float(sys.argv[5])
    presion_sanguinea = sys.argv[6]

    nota = generar_nota_evolucion(paciente, medicamento, cantidad_medicamento, peso, temperatura, presion_sanguinea)
    print(nota)

if __name__ == "__main__":
    main()