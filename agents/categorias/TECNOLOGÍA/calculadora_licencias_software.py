#!/usr/bin/env python3
"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora licencias software
TECNOLOGÍA: Python estándar
"""

import sys
import json
import math
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por línea de comandos con valores por defecto
        args = sys.argv[1:]
        num_licencias = int(args[0]) if len(args) > 0 else 100
        precio_licencia = float(args[1]) if len(args) > 1 else 1500.0
        descuento = float(args[2]) if len(args) > 2 else 0.15
        iva = float(args[3]) if len(args) > 3 else 0.16

        # Cálculos
        subtotal = num_licencias * precio_licencia
        total_descuento = subtotal * descuento
        total = subtotal - total_descuento
        total_iva = total * iva
        total_final = total + total_iva
        costo_por_licencia = total_final / num_licencias
        ahorro_total = total_descuento
        porcentaje_ahorro = (total_descuento / subtotal) * 100
        costo_por_licencia_sin_iva = total / num_licencias
        costo_por_licencia_sin_descuento_iva = precio_licencia
        total_sin_descuento_iva = subtotal
        total_con_descuento_iva = total_final
        total_sin_iva = total
        total_sin_descuento = subtotal

        # Impresión de resultados
        print("Cálculo de licencias de software para Agencia Santi (México)")
        print("===============================================")
        print(f"Número de licencias: {num_licencias}")
        print(f"Precio por licencia: ${precio_licencia:.2f} MXN")
        print(f"Subtotal: ${subtotal:.2f} MXN")
        print(f"Descuento ({descuento*100}%): ${total_descuento:.2f} MXN")
        print(f"Total sin IVA: ${total_sin_iva:.2f} MXN")
        print(f"IVA ({iva*100}%): ${total_iva:.2f} MXN")
        print(f"Total con IVA ({iva*100}%): ${total_final:.2f} MXN")
        print(f"Costo por licencia con IVA: ${costo_por_licencia:.2f} MXN")
        print(f"Ahorro total por descuento: ${ahorro_total:.2f} MXN")
        print(f"Porcentaje de ahorro: {porcentaje_ahorro:.2f}%")
        print(f"Costo por licencia sin IVA: ${costo_por_licencia_sin_iva:.2f} MXN")
        print(f"Costo por licencia sin descuento IVA: ${costo_por_licencia_sin_descuento_iva:.2f} MXN")
        print(f"Total sin descuento IVA: ${total_sin_descuento_iva:.2f} MXN")
        print(f"Total con descuento IVA: ${total_con_descuento_iva:.2f} MXN")
        print(f"Total sin IVA y descuento: ${total_sin_iva:.2f} MXN")
        print(f"Total sin descuento: ${total_sin_descuento:.2f} MXN")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print("-------------------")
        print(f"El costo total de las licencias de software es de ${total_final:.2f} MXN.")
        print(f"El ahorro total por descuento es de ${ahorro_total:.2f} MXN.")
        print(f"El porcentaje de ahorro es de {porcentaje_ahorro:.2f}%.")

    except ValueError:
        print("Error: Los valores de entrada no son válidos.")
    except IndexError:
        print("Error: Faltan valores de entrada.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()