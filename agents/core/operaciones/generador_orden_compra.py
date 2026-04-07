import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios(precio_unitario=12.50, impuesto=0.16):
    return {
        "precio_unitario": precio_unitario,
        "impuesto": impuesto,
        "total": precio_unitario + (precio_unitario * impuesto)
    }

def calcular_impuesto_total(subtotal, impuesto):
    return subtotal * impuesto

def calcular_total(subtotal, impuesto_total):
    return subtotal + impuesto_total

def calcular_total_compra_mexico(cantidad, precio_unitario, impuesto):
    subtotal = cantidad * precio_unitario
    impuesto_total = subtotal * impuesto
    total = subtotal + impuesto_total
    return total

def generar_orden_compra(cantidad, precio_unitario, impuesto):
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    hora = datetime.datetime.now().strftime("%H:%M:%S")
    subtotal = float(cantidad) * precio_unitario
    impuesto_total = calcular_impuesto_total(subtotal, impuesto)
    total = calcular_total(subtotal, impuesto_total)
    total_mexico = calcular_total_compra_mexico(cantidad, precio_unitario, impuesto)
    orden_compra = {
        "fecha": fecha,
        "hora": hora,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "subtotal": subtotal,
        "impuesto": impuesto,
        "impuesto_total": impuesto_total,
        "total": total,
        "total_mexico": total_mexico
    }
    return orden_compra

def main():
    try:
        if len(sys.argv) > 4:
            cantidad = float(sys.argv[1])
            precio_unitario = float(sys.argv[2])
            impuesto = float(sys.argv[3])
        else:
            cantidad = float(sys.argv[1]) if len(sys.argv) > 1 else random.uniform(1, 10)
            precio_unitario = float(sys.argv[2]) if len(sys.argv) > 2 else extraer_precios()["precio_unitario"]
            impuesto = float(sys.argv[3]) if len(sys.argv) > 3 else extraer_precios()["impuesto"]
        
        orden_compra = generar_orden_compra(cantidad, precio_unitario, impuesto)
        
        print("ÁREA: HERRAMIENTAS")
        print("DESCRIPCIÓN: Agente que realiza generador orden compra")
        print("TECNOLOGÍA: Python estándar")
        print(f"Fecha: {orden_compra['fecha']}")
        print(f"Hora: {orden_compra['hora']}")
        print(f"Cantidad: {orden_compra['cantidad']}")
        print(f"Precio unitario: ${orden_compra['precio_unitario']:.2f}")
        print(f"Subtotal: ${orden_compra['subtotal']:.2f}")
        print(f"Impuesto: {orden_compra['impuesto'] * 100:.2f}%")
        print(f"Impuesto total: ${orden_compra['impuesto_total']:.2f}")
        print(f"Total: ${orden_compra['total']:.2f}")
        print(f"Total (México): ${orden_compra['total_mexico']:.2f}")
        print("Resumen ejecutivo:")
        print(f"La orden de compra incluye {orden_compra['cantidad']} unidades a ${orden_compra['precio_unitario']:.2f} cada una, con un subtotal de ${orden_compra['subtotal']:.2f} y un impuesto total de ${orden_compra['impuesto_total']:.2f}. El total de la orden es ${orden_compra['total']:.2f}.")
    
    except ValueError:
        print("Error: Los valores ingresados no son válidos.")
    except IndexError:
        print("Error: Faltan argumentos de línea de comandos.")

if __name__ == "__main__":
    main()