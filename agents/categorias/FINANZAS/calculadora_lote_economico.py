import os
import sys
import json
import datetime
import math
import re
import random

def calcular_lote_economico(costo_unitario, precio_venta, descuento, cantidad):
    try:
        if costo_unitario <= 0 or precio_venta <= 0 or descuento < 0 or cantidad <= 0:
            raise ValueError("Valores inválidos")

        costo_total = costo_unitario * cantidad
        precio_venta_total = precio_venta * cantidad
        descuento_total = costo_total * descuento
        beneficio = precio_venta_total - costo_total - descuento_total
        impuesto = costo_total * 0.16  # Impuesto al valor agregado (IVA) en México
        beneficio_neto = beneficio - impuesto
        margen_ganancia = (precio_venta - costo_unitario) / costo_unitario * 100
        punto_equilibrio = costo_total / (1 - (descuento + 0.16))

        return {
            "costo_total": costo_total,
            "precio_venta_total": precio_venta_total,
            "descuento_total": descuento_total,
            "beneficio": beneficio,
            "impuesto": impuesto,
            "beneficio_neto": beneficio_neto,
            "margen_ganancia": margen_ganancia,
            "punto_equilibrio": punto_equilibrio
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    try:
        if len(sys.argv) > 6:
            costo_unitario = float(sys.argv[1])
            precio_venta = float(sys.argv[2])
            descuento = float(sys.argv[3])
            cantidad = int(sys.argv[4])
            fecha = sys.argv[5]
            tecnologia = sys.argv[6]
        else:
            costo_unitario = 100.0
            precio_venta = 120.0
            descuento = 0.10
            cantidad = 1000
            fecha = datetime.datetime.now().strftime("%Y-%m-%d")
            tecnologia = "Python estándar"

        resultado = calcular_lote_economico(costo_unitario, precio_venta, descuento, cantidad)
        if resultado:
            print(f"ÁREA: FINANZAS")
            print(f"DESCRIPCIÓN: Agente que realiza cálculos de lote económico")
            print(f"TECNOLOGÍA: {tecnologia}")
            print(f"FECHA: {fecha}")
            print(f"COSTO UNITARIO: ${costo_unitario:.2f}")
            print(f"PRECIO DE VENTA: ${precio_venta:.2f}")
            print(f"DESCUENTO: {descuento*100:.2f}%")
            print(f"CANTIDAD: {cantidad} unidades")
            print(f"COSTO TOTAL: ${resultado['costo_total']:.2f}")
            print(f"PRECIO DE VENTA TOTAL: ${resultado['precio_venta_total']:.2f}")
            print(f"DESCUENTO TOTAL: ${resultado['descuento_total']:.2f}")
            print(f"BENEFICIO: ${resultado['beneficio']:.2f}")
            print(f"IMPUESTO: ${resultado['impuesto']:.2f}")
            print(f"BENEFICIO NETO: ${resultado['beneficio_neto']:.2f}")
            print(f"MARGEN DE GANANCIA: {resultado['margen_ganancia']:.2f}%")
            print(f"PUNTO DE EQUILIBRIO: ${resultado['punto_equilibrio']:.2f}")
            print(f"RESUMEN EJECUTIVO: El lote económico con un costo unitario de ${costo_unitario:.2f}, precio de venta de ${precio_venta:.2f}, descuento de {descuento*100:.2f}%, y una cantidad de {cantidad} unidades, genera un beneficio neto de ${resultado['beneficio_neto']:.2f} y un margen de ganancia de {resultado['margen_ganancia']:.2f}%")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()