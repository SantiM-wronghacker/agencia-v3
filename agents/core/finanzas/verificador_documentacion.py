#!/usr/bin/env python3
"""
ÁREA: FINANZAS
DESCRIPCIÓN: Verifica la documentación requerida para procesos de renta
TECNOLOGÍA: Python
"""

import sys
import os
import time
import json
import math
from datetime import datetime

def calcular_imponible(valor):
    # Es un porcentaje del 16% sobre el valor
    return valor * 0.16

def calcular_retencion(valor):
    # Es un porcentaje del 15% sobre el valor
    return valor * 0.15

def verificar_documentacion(ine=False, comprobante=False, aval=False, valor_ingresos=0):
    print("Verificador de Documentación para Renta")
    print("-----------------------------------------")
    print("ÁREA: FINANZAS")
    print("DESCRIPCIÓN: Verifica la documentación requerida para procesos de renta")
    print("TECNOLOGÍA: Python")
    print("Fecha de inicio:", os.path.basename(__file__))
    print("Fecha de inicio:", time.strftime("%Y-%m-%d %H:%M:%S"))
    print("")

    documentos = {
        "INE": ine,
        "Comprobante de Ingresos": comprobante,
        "Aval": aval
    }

    while True:
        print("\nDocumentos:")
        for documento, tiene in documentos.items():
            if tiene:
                print(f"- {documento}: Si")
            else:
                print(f"- {documento}: No")

        print("\nValor de ingresos:", valor_ingresos)
        print("Imponible:", calcular_imponible(valor_ingresos))
        print("Retención:", calcular_retencion(valor_ingresos))

        print("\n¿Qué deseas hacer?")
        print("1. Agregar documento")
        print("2. Quitar documento")
        print("3. Finalizar")

        if len(sys.argv) > 1:
            accion = sys.argv[1]
            valor_ingresos = float(sys.argv[2]) if len(sys.argv) > 2 else 0
        else:
            accion = "3"

        if accion == "1":
            if len(sys.argv) > 3:
                documento_agregar = sys.argv[3]
            else:
                documento_agregar = "1"

            if documento_agregar == "1":
                documentos["INE"] = True
            elif documento_agregar == "2":
                documentos["Comprobante de Ingresos"] = True
            elif documento_agregar == "3":
                documentos["Aval"] = True
            else:
                print("Opción inválida. Por favor, selecciona una opción válida.")
        elif accion == "2":
            if len(sys.argv) > 3:
                documento_quitar = sys.argv[3]
            else:
                documento_quitar = "1"

            if documento_quitar == "1":
                documentos["INE"] = False
            elif documento_quitar == "2":
                documentos["Comprobante de Ingresos"] = False
            elif documento_quitar == "3":
                documentos["Aval"] = False
            else:
                print("Opción inválida. Por favor, selecciona una opción válida.")
        elif accion == "3":
            break
        else:
            print("Opción inválida. Por favor, selecciona una opción válida.")

    resumen_ejecutivo = ""
    if documentos["INE"]:
        resumen_ejecutivo += "El contribuyente tiene un INE válido.\n"
    else:
        resumen_ejecutivo += "El contribuyente no tiene un INE válido.\n"

    if documentos["Comprobante de Ingresos"]:
        resumen_ejecutivo += "El contribuyente tiene un comprobante de ingresos válido.\n"
    else:
        resumen_ejecutivo += "El contribuyente no tiene un comprobante de ingresos válido.\n"

    if documentos["Aval"]:
        resumen_ejecutivo += "El contribuyente tiene un aval válido.\n"
    else:
        resumen_ejecutivo += "El contribuyente no tiene un aval válido.\n"

    print("\nResumen Ejecutivo:")
    print(resumen_ejecutivo)

if __name__ == "__main__":
    verificar_documentacion()