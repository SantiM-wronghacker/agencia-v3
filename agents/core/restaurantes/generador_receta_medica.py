"""
AREA: SALUD
DESCRIPCION: Agente que realiza generador receta medica
TECNOLOGIA: Python estandar
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

def calcular_precio_total(precios, dosis, medicamentos):
    precio_total = 0
    for i in range(len(medicamentos)):
        precio_total += precios[medicamentos[i]] * dosis[i]
    return precio_total

def calcular_iva(precio_total):
    iva = 0.16
    return precio_total * iva

def calcular_total_con_iva(precio_total, iva):
    return precio_total + iva

def generar_receta_medica(nombre_paciente, fecha_emision, medicamentos, dosis, frecuencia, precio_unitario=None):
    try:
        precios = extraer_precios()
        if precio_unitario:
            precios = precio_unitario
        precio_total = calcular_precio_total(precios, dosis, medicamentos)
        iva = calcular_iva(precio_total)
        total_con_iva = calcular_total_con_iva(precio_total, iva)

        receta = f"Receta medica para {nombre_paciente} emitida el {fecha_emision}\n"
        receta += "Datos del paciente:\n"
        receta += f"- Nombre: {nombre_paciente}\n"
        receta += f"- Fecha de nacimiento: {datetime.now().strftime('%Y-%m-%d')}\n"
        receta += f"- Edad: {random.randint(20, 80)} años\n"
        receta += f"- Sexo: {random.choice(['Masculino', 'Femenino'])}\n"
        receta += f"- Direccion: {random.choice(['Calle 1', 'Calle 2', 'Calle 3'])}\n"
        receta += f"- Telefono: {random.randint(1000000000, 9999999999)}\n"
        receta += "Medicamentos:\n"
        for i in range(len(medicamentos)):
            receta += f"- {medicamentos[i]}: {dosis[i]} {frecuencia[i]}\n"
            receta += f"Precio unitario: ${precios[medicamentos[i]]:.2f}\n"
            receta += f"Costo total: ${precios[medicamentos[i]] * dosis[i]:.2f}\n"
        receta += f"\nPrecio total: ${precio_total:.2f}\n"
        receta += f"IVA (16%): ${iva:.2f}\n"
        receta += f"Total con IVA: ${total_con_iva:.2f}\n"
        receta += f"Fecha de vencimiento: {datetime.strptime(fecha_emision, '%Y-%m-%d') + timedelta(days=30)}\n"
        receta += f"Resumen ejecutivo: La receta medica para {nombre_paciente} tiene un total de {len(medicamentos)} medicamentos, con un precio total de ${precio_total:.2f} y un total con IVA de ${total_con_iva:.2f}.\n"

        return receta
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    if len(sys.argv)!= 6:
        print("Uso: python generador_receta_medica.py <nombre_paciente> <fecha_emision> <medicamentos> <dosis> <frecuencia>")
        return

    nombre_paciente = sys.argv