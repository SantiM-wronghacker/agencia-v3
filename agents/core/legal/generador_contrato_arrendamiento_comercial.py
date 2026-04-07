# AREA: FINANZAS
# DESCRIPCION: LEGAL/Generador de Contrato de Arrendamiento Comercial/Python
# TECNOLOGIA: Python

import sys
import json
import datetime
import math
import re
import random
import os

def calcular_total_rentas(renta_mensual, duracion_contrato):
    """Calcula el total de rentas a pagar"""
    return renta_mensual * duracion_contrato

def calcular_impuesto_renta(renta_mensual, duracion_contrato):
    """Calcula el impuesto sobre la renta (20%)"""
    total_rentas = calcular_total_rentas(renta_mensual, duracion_contrato)
    return total_rentas * 0.20

def calcular_iva(renta_mensual, duracion_contrato):
    """Calcula el IVA (16%)"""
    total_rentas = calcular_total_rentas(renta_mensual, duracion_contrato)
    return total_rentas * 0.16

def calcular_total_a_pagar(renta_mensual, duracion_contrato):
    """Calcula el total a pagar incluyendo impuestos y IVA"""
    total_rentas = calcular_total_rentas(renta_mensual, duracion_contrato)
    impuesto_renta = calcular_impuesto_renta(renta_mensual, duracion_contrato)
    iva = calcular_iva(renta_mensual, duracion_contrato)
    return total_rentas + impuesto_renta + iva

def main():
    if len(sys.argv) < 6:
        print("Faltan argumentos. Uso: python generador_contrato_arrendamiento_comercial.py <nombre_arrendador> <nombre_arrendatario> <direccion_inmueble> <renta_mensual> <duracion_contrato>")
        return

    nombre_arrendador = sys.argv[1]
    nombre_arrendatario = sys.argv[2]
    direccion_inmueble = sys.argv[3]
    renta_mensual = float(sys.argv[4])
    duracion_contrato = int(sys.argv[5])

    try:
        fecha_inicio = datetime.date.today()
        fecha_fin = fecha_inicio + datetime.timedelta(days=duracion_contrato * 30)

        contrato = {
            "nombre_arrendador": nombre_arrendador,
            "nombre_arrendatario": nombre_arrendatario,
            "direccion_inmueble": direccion_inmueble,
            "renta_mensual": renta_mensual,
            "duracion_contrato": duracion_contrato,
            "fecha_inicio": fecha_inicio.strftime("%d/%m/%Y"),
            "fecha_fin": fecha_fin.strftime("%d/%m/%Y")
        }

        print("Contrato de Arrendamiento Comercial")
        print("------------------------------------")
        print(f"Nombre del Arrendador: {contrato['nombre_arrendador']}")
        print(f"Nombre del Arrendatario: {contrato['nombre_arrendatario']}")
        print(f"Dirección del Inmueble: {contrato['direccion_inmueble']}")
        print(f"Renta Mensual: ${contrato['renta_mensual']:.2f} MXN")
        print(f"Duración del Contrato: {contrato['duracion_contrato']} meses")
        print(f"Fecha de Inicio: {contrato['fecha_inicio']}")
        print(f"Fecha de Fin: {contrato['fecha_fin']}")
        print(f"Total de Rentas: ${calcular_total_rentas(renta_mensual, duracion_contrato):.2f} MXN")
        print(f"Impuesto sobre la Renta (20%): ${calcular_impuesto_renta(renta_mensual, duracion_contrato):.2f} MXN")
        print(f"IVA (16%): ${calcular_iva(renta_mensual, duracion_contrato):.2f} MXN")
        print(f"Total a Pagar: ${calcular_total_a_pagar(renta_mensual, duracion_contrato):.2f} MXN")

        print("\nResumen Ejecutivo:")
        print(f"El contrato de arrendamiento comercial entre {contrato['nombre_arrendador']} y {contrato['nombre_arrendatario']} tiene una duración de {contrato['duracion_contrato']} meses y un total a pagar de ${calcular_total_a_pagar(renta_mensual, duracion_contrato):.2f} MXN.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()