"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza generador contrato obra
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_contrato_obra(nombre_cliente, nombre_proyecto, ubicacion, fecha_inicio, fecha_final, presupuesto, tipo_contrato):
    try:
        # Validar fecha de inicio y final
        if fecha_inicio > fecha_final:
            raise ValueError("La fecha de inicio no puede ser posterior a la fecha de finalización")

        # Validar presupuesto
        if presupuesto <= 0:
            raise ValueError("El presupuesto debe ser mayor a cero")

        # Generar contrato
        contrato = {
            "nombre_cliente": nombre_cliente,
            "nombre_proyecto": nombre_proyecto,
            "ubicacion": ubicacion,
            "fecha_inicio": str(fecha_inicio),
            "fecha_final": str(fecha_final),
            "presupuesto": str(presupuesto),
            "tipo_contrato": tipo_contrato,
            "fecha_actual": str(datetime.date.today()),
            "total_dias": (fecha_final - fecha_inicio).days,
            "costo_dia": presupuesto / (fecha_final - fecha_inicio).days,
            "costo_total": presupuesto,
            "impuesto": presupuesto * 0.15,
            "total_pago": presupuesto + (presupuesto * 0.15)
        }

        # Imprimir contrato
        print("Contrato de Construcción")
        print("-------------------------")
        print(f"Nombre del cliente: {contrato['nombre_cliente']}")
        print(f"Nombre del proyecto: {contrato['nombre_proyecto']}")
        print(f"Ubicación: {contrato['ubicacion']}")
        print(f"Fecha de inicio: {contrato['fecha_inicio']}")
        print(f"Fecha de finalización: {contrato['fecha_final']}")
        print(f"Presupuesto: {contrato['presupuesto']}")
        print(f"Tipo de contrato: {contrato['tipo_contrato']}")
        print(f"Fecha actual: {contrato['fecha_actual']}")
        print(f"Total de días: {contrato['total_dias']}")
        print(f"Costo por día: {contrato['costo_dia']}")
        print(f"Costo total: {contrato['costo_total']}")
        print(f"Impuesto: {contrato['impuesto']}")
        print(f"Total de pago: {contrato['total_pago']}")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El proyecto tendrá un costo total de {contrato['costo_total']} pesos")
        print(f"El impuesto sobre el proyecto será de {contrato['impuesto']} pesos")
        print(f"El total de pago por el proyecto será de {contrato['total_pago']} pesos")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error desconocido: {e}")

def main():
    if len(sys.argv) != 7:
        print("Uso: python generador_contrato_obra.py <nombre_cliente> <nombre_proyecto> <ubicacion> <fecha_inicio> <fecha_final> <presupuesto> <tipo_contrato>")
        return

    nombre_cliente = sys.argv[1]
    nombre_proyecto = sys.argv[2]
    ubicacion = sys.argv[3]
    fecha_inicio = datetime.datetime.strptime(sys.argv[4], "%Y-%m-%d").date()
    fecha_final = datetime.datetime.strptime(sys.argv[5], "%Y-%m-%d").date()
    presupuesto = float(sys.argv[6])
    tipo_contrato = sys.argv[7]

    generar_contrato_obra(nombre_cliente, nombre_proyecto, ubicacion, fecha_inicio, fecha_final, presupuesto, tipo_contrato)

if __name__ == "__main__":
    main()