"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza generador acta constitutiva
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def main():
    try:
        nombre_empresa = sys.argv[1] if len(sys.argv) > 1 else "Empresa Ejemplo"
        objeto_social = sys.argv[2] if len(sys.argv) > 2 else "Comercio al por mayor"
        fecha_constitucion = sys.argv[3] if len(sys.argv) > 3 else datetime.date.today().strftime("%Y-%m-%d")
        monto_autorizado = float(sys.argv[4]) if len(sys.argv) > 4 else 1000000.0
        numero_acciones = int(sys.argv[5]) if len(sys.argv) > 5 else 1000
        tipo_cambio = float(sys.argv[6]) if len(sys.argv) > 6 else 20.0
        tipo_empresa = sys.argv[7] if len(sys.argv) > 7 else "Sociedad Anónima"
        domicilio_empresa = sys.argv[8] if len(sys.argv) > 8 else "Calle 123, Colonia Centro, Ciudad de México"
        razon_social = sys.argv[9] if len(sys.argv) > 9 else "Empresa Ejemplo S.A. de C.V."
        nombre_tesorero = sys.argv[10] if len(sys.argv) > 10 else "Juan Pérez"
        nombre_secretario = sys.argv[11] if len(sys.argv) > 11 else "María Gómez"

        if monto_autorizado <= 0 or numero_acciones <= 0 or tipo_cambio <= 0:
            print("Error: Valores no válidos")
            return

        valor_accion = monto_autorizado / numero_acciones
        valor_accion_usd = valor_accion / tipo_cambio
        capital_social = monto_autorizado
        impuesto_al_capital = capital_social * 0.02
        registro_publico = 500.0
        notario = 2000.0
        gastos_constitucion = impuesto_al_capital + registro_publico + notario

        print(f"Acta Constitutiva de {nombre_empresa}")
        print(f"Objeto Social: {objeto_social}")
        print(f"Fecha de Constitución: {fecha_constitucion}")
        print(f"Monto Autorizado: ${monto_autorizado:.2f} MXN")
        print(f"Valor de la Acción: ${valor_accion:.2f} MXN (${valor_accion_usd:.2f} USD)")
        print(f"Número de Acciones: {numero_acciones}")
        print(f"Capital Social: ${capital_social:.2f} MXN")
        print(f"Impuesto al Capital: ${impuesto_al_capital:.2f} MXN")
        print(f"Gastos de Constitución: ${gastos_constitucion:.2f} MXN")
        print(f"Registro Público: ${registro_publico:.2f} MXN")
        print(f"Notario: ${notario:.2f} MXN")
        print(f"Tipo de Cambio: {tipo_cambio} MXN/USD")
        print(f"Tipo de Empresas: {tipo_empresa}")
        print(f"Domicilio de la Empresa: {domicilio_empresa}")
        print(f"Razón Social: {razon_social}")
        print(f"Nombre del Tesorero: {nombre_tesorero}")
        print(f"Nombre del Secretario: {nombre_secretario}")

        print("\nResumen Ejecutivo:")
        print(f"La empresa {nombre_empresa} se constituyó el {fecha_constitucion} con un monto autorizado de ${monto_autorizado:.2f} MXN.")
        print(f"El capital social es de ${capital_social:.2f} MXN y se dividirá en {numero_acciones} acciones de valor ${valor_accion:.2f} MXN cada una.")
        print(f"El impuesto al capital es de ${impuesto_al_capital:.2f} MXN y los gastos de constitución ascienden a ${gastos_constitucion:.2f} MXN.")

    except IndexError:
        print("Error: Faltan argumentos")
    except ValueError:
        print("Error: Valores no válidos")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()