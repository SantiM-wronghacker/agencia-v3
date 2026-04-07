"""
ÁREA: SALUD
DESCRIPCIÓN: Agente que realiza generador receta medica
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
from datetime import datetime, timedelta
import random
import math

def extraer_precios(precios_archivo='precios.json'):
    try:
        with open(precios_archivo, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "Ibuprofeno": 10.50,
            "Paracetamol": 20.75,
            "Aspirina": 30.25,
            "Amlodipino": 40.50,
            "Atorvastatina": 50.75,
            "Simvastatina": 60.25
        }
    except json.JSONDecodeError:
        return {
            "Ibuprofeno": 10.50,
            "Paracetamol": 20.75,
            "Aspirina": 30.25,
            "Amlodipino": 40.50,
            "Atorvastatina": 50.75,
            "Simvastatina": 60.25
        }

def calcular_precio_total(precios, dosis):
    return sum(precio * dosis for precio, dosis in zip(precios.values(), dosis))

def generar_receta_medica(nombre_paciente, fecha_emision, medicamentos, dosis, frecuencia, precio_unitario=None):
    precios = extraer_precios()
    if precio_unitario:
        precios = precio_unitario
    precio_total = calcular_precio_total(precios, dosis)

    receta = f"Receta médica para {nombre_paciente} emitida el {fecha_emision}\n"
    receta += "Datos del paciente:\n"
    receta += f"- Nombre: {nombre_paciente}\n"
    receta += f"- Fecha de nacimiento: {datetime.now().strftime('%Y-%m-%d')}\n"
    receta += f"- Edad: {random.randint(20, 80)} años\n"
    receta += f"- Sexo: {random.choice(['Masculino', 'Femenino'])}\n"
    receta += "Medicamentos:\n"
    for i in range(len(medicamentos)):
        receta += f"- {medicamentos[i]}: {dosis[i]} {frecuencia[i]}\n"
        receta += f"Precio unitario: ${precios[medicamentos[i]]:.2f}\n"
        receta += f"Costo total: ${precios[medicamentos[i]] * dosis[i]:.2f}\n"
    receta += f"\nPrecio total: ${precio_total:.2f}\n"
    receta += f"Fecha de vencimiento: {(datetime.now() + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')}\n"
    receta += f"\nResumen ejecutivo:\n"
    receta += f"- El paciente {nombre_paciente} ha sido prescrito los siguientes medicamentos:\n"
    for i in range(len(medicamentos)):
        receta += f"- {medicamentos[i]}\n"
    receta += f"- El precio total de la receta es de ${precio_total:.2f}\n"

    return receta

def main():
    if len(sys.argv) != 6:
        print("Error: Faltan argumentos")
        return
    nombre_paciente = sys.argv[1]
    fecha_emision = sys.argv[2]
    medicamentos = sys.argv[3].split(',')
    dosis = [int(x) for x in sys.argv[4].split(',')]
    frecuencia = sys.argv[5].split(',')
    receta = generar_receta_medica(nombre_paciente, fecha_emision, medicamentos, dosis, frecuencia)
    print(receta)

if __name__ == "__main__":
    main()