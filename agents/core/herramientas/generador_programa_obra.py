"""
ÁREA: CONSTRUCCIÓN
DESCRIPCIÓN: Agente que realiza generador programa obra
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_programa_obra(nombre_obra="Torre de la Libertad", presupuesto=50000000, fecha_inicio=datetime.date(2024, 3, 1), fecha_fin=datetime.date(2025, 2, 28), peso_total=100000, largo_total=50):
    try:
        # Verificar si la fecha de inicio es anterior a la fecha de fin
        if fecha_inicio > fecha_fin:
            raise ValueError("La fecha de inicio no puede ser posterior a la fecha de fin")

        # Verificar si el presupuesto es suficiente para el peso total y el largo total
        if presupuesto < (peso_total * 100) + (largo_total * 5000):
            raise ValueError("El presupuesto no es suficiente para el peso total y el largo total")

        # Generar programa de obra
        programa_obra = f"""
Nombre de la obra: {nombre_obra}
Presupuesto: {presupuesto} MXN
Fecha de inicio: {fecha_inicio}
Fecha de fin: {fecha_fin}
Peso total: {peso_total} kg
Largo total: {largo_total} m
Costo por kilogramo: {presupuesto / peso_total} MXN/kg
Costo por metro: {presupuesto / largo_total} MXN/m
Número de días de trabajo: {(fecha_fin - fecha_inicio).days + 1}
Resumen ejecutivo:
La obra tendrá un presupuesto de {presupuesto} MXN, con un peso total de {peso_total} kg y un largo total de {largo_total} m. El costo por kilogramo será de {presupuesto / peso_total} MXN/kg y el costo por metro será de {presupuesto / largo_total} MXN/m. La obra durará {fecha_fin - fecha_inicio} días.
"""

        # Imprimir programa de obra
        print(programa_obra)

    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    if len(sys.argv) > 1:
        nombre_obra = sys.argv[1]
    else:
        nombre_obra = "Torre de la Libertad"
    
    if len(sys.argv) > 2:
        try:
            presupuesto = float(sys.argv[2])
        except ValueError:
            print("Error: El presupuesto debe ser un número")
            return
    else:
        presupuesto = 50000000
    
    if len(sys.argv) > 3:
        try:
            fecha_inicio = datetime.datetime.strptime(sys.argv[3], "%Y-%m-%d").date()
        except ValueError:
            print("Error: La fecha de inicio debe ser en formato YYYY-MM-DD")
            return
    else:
        fecha_inicio = datetime.date(2024, 3, 1)
    
    if len(sys.argv) > 4:
        try:
            fecha_fin = datetime.datetime.strptime(sys.argv[4], "%Y-%m-%d").date()
        except ValueError:
            print("Error: La fecha de fin debe ser en formato YYYY-MM-DD")
            return
    else:
        fecha_fin = datetime.date(2025, 2, 28)
    
    if len(sys.argv) > 5:
        try:
            peso_total = float(sys.argv[5])
        except ValueError:
            print("Error: El peso total debe ser un número")
            return
    else:
        peso_total = 100000
    
    if len(sys.argv) > 6:
        try:
            largo_total = float(sys.argv[6])
        except ValueError:
            print("Error: El largo total debe ser un número")
            return
    else:
        largo_total = 50
    
    generar_programa_obra(nombre_obra, presupuesto, fecha_inicio, fecha_fin, peso_total, largo_total)

if __name__ == "__main__":
    main()