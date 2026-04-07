"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza generador comparativa seguros
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios(precio_auto=10000, precio_casa=5000, precio_salud=2000):
    try:
        precios = {
            "seguro_auto": precio_auto,
            "seguro_casa": precio_casa,
            "seguro_salud": precio_salud
        }
        return precios
    except Exception as e:
        print(f"Error: {e}")
        return {
            "seguro_auto": 0,
            "seguro_casa": 0,
            "seguro_salud": 0
        }

def calcular_descuento(precio, porcentaje):
    if porcentaje < 0 or porcentaje > 100:
        raise ValueError("Porcentaje debe estar entre 0 y 100")
    return precio * (porcentaje / 100)

def calcular_impuesto(precio, porcentaje):
    if porcentaje < 0 or porcentaje > 100:
        raise ValueError("Porcentaje debe estar entre 0 y 100")
    return precio * (porcentaje / 100)

def calcular_iva(precio):
    # IVA en México es del 16% pero se aplica a la suma del precio mas impuestos
    # para simplificar se aplica solo al precio
    return precio * 0.16

def calcular_isr(precio):
    # ISR en México es del 10% pero se aplica a la suma del precio mas impuestos
    # para simplificar se aplica solo al precio
    return precio * 0.10

def calcular_total(precios):
    return precios["seguro_auto"] + precios["seguro_casa"] + precios["seguro_salud"]

def calcular_iva_total(precios):
    return calcular_iva(calcular_total(precios))

def calcular_isr_total(precios):
    return calcular_isr(calcular_total(precios))

def generar_comparativa_seguros(precio_auto=10000, precio_casa=5000, precio_salud=2000, descuento_auto=10, descuento_casa=5, impuesto_renta=15):
    print("Comparativa de seguros")
    print("------------------------")
    precios = extraer_precios(precio_auto, precio_casa, precio_salud)
    print("Seguro Auto: ${:.2f}".format(precios["seguro_auto"]))
    print("Seguro Casa: ${:.2f}".format(precios["seguro_casa"]))
    print("Seguro Salud: ${:.2f}".format(precios["seguro_salud"]))
    print("Total: ${:.2f}".format(calcular_total(precios)))
    print("Descuento por seguro auto: ${:.2f}".format(calcular_descuento(precios["seguro_auto"], descuento_auto)))
    print("Descuento por seguro casa: ${:.2f}".format(calcular_descuento(precios["seguro_casa"], descuento_casa)))
    print("Impuesto sobre la renta: ${:.2f}".format(calcular_impuesto(calcular_total(precios), impuesto_renta)))
    print("IVA: ${:.2f}".format(calcular_iva_total(precios)))
    print("ISR: ${:.2f}".format(calcular_isr_total(precios)))
    print("Total con impuestos: ${:.2f}".format(calcular_total(precios) + calcular_iva_total(precios) + calcular_isr_total(precios)))

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--auto", "-a"]:
            precio_auto = int(sys.argv[2])
        elif sys.argv[1] in ["--casa", "-c"]:
            precio_casa = int(sys.argv[2])
        elif sys.argv[1] in ["--salud", "-s"]:
            precio_salud = int(sys.argv[2])
        elif sys.argv[1] in ["--descuento-auto", "-da"]:
            descuento_auto = int(sys.argv[2])
        elif sys.argv[1] in ["--descuento-casa", "-dc"]:
            descuento_casa = int(sys.argv[2])
        elif sys.argv[1] in ["--impuesto-renta", "-ir"]:
            impuesto_renta = int(sys.argv[2])
        else:
            print("Error: Opción desconocida")
            sys.exit(1)
    else:
        precio_auto