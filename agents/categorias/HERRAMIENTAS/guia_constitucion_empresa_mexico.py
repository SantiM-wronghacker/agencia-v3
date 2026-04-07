"""
AREA: LEGAL
DESCRIPCION: Agente que realiza guia constitucion empresa mexico
TECNOLOGIA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

def main():
    try:
        nombre_empresa = sys.argv[1] if len(sys.argv) > 1 else "Empresa Mexicana SA de CV"
        fecha_constitucion = sys.argv[2] if len(sys.argv) > 2 else "2022-01-01"
        objeto_social = sys.argv[3] if len(sys.argv) > 3 else "Comercio al por mayor y al por menor"
        capital_social = float(sys.argv[4]) if len(sys.argv) > 4 else 100000.00
        numero_socios = int(sys.argv[5]) if len(sys.argv) > 5 else 2
        domicilio_fiscal = sys.argv[6] if len(sys.argv) > 6 else 'Calle Ficticia 123, Ciudad de México, México'
        rfc = sys.argv[7] if len(sys.argv) > 7 else 'EMEXSA123456'
        clave_identificacion_fiscal = sys.argv[8] if len(sys.argv) > 8 else '1234567890123'

        print(f"Nombre de la empresa: {nombre_empresa}")
        print(f"Fecha de constitución: {fecha_constitucion}")
        print(f"Objeto social: {objeto_social}")
        print(f"Capital social: ${capital_social:,.2f} MXN")
        print(f"Número de socios: {numero_socios}")
        print(f"Fecha de inicio de operaciones: {(datetime.datetime.strptime(fecha_constitucion, '%Y-%m-%d') + datetime.timedelta(days=30)).strftime('%Y-%m-%d')}")
        print(f"Duración de la sociedad: 99 años a partir de la fecha de constitución")
        print(f"Tipo de sociedad: Sociedad Anónima de Capital Variable (SA de CV)")
        print(f"Domicilio fiscal: {domicilio_fiscal}")
        print(f"Registro Federal de Contribuyentes (RFC): {rfc}")
        print(f"Clave de identificación fiscal: {clave_identificacion_fiscal}")
        print(f"Fecha de inicio de obligaciones fiscales: {(datetime.datetime.strptime(fecha_constitucion, '%Y-%m-%d') + datetime.timedelta(days=30)).strftime('%Y-%m-%d')}")
        print(f"Fecha de vencimiento de obligaciones fiscales: {(datetime.datetime.strptime(fecha_constitucion, '%Y-%m-%d') + datetime.timedelta(days=365)).strftime('%Y-%m-%d')}")
        print(f"Impuesto sobre la renta (ISR): {capital_social * 0.25:.2f} MXN")
        print(f"Impuesto al valor agregado (IVA): {capital_social * 0.16:.2f} MXN")
        print(f"Seguro social: {capital_social * 0.05:.2f} MXN")
        print(f"Infonavit: {capital_social * 0.05:.2f} MXN")
        print(f"Total de impuestos y contribuciones: {capital_social * 0.51:.2f} MXN")

        print("\nResumen ejecutivo:")
        print(f"La empresa {nombre_empresa} se constituyó el {fecha_constitucion} con un capital social de ${capital_social:,.2f} MXN y {numero_socios} socios.")
        print(f"El domicilio fiscal es {domicilio_fiscal} y el RFC es {rfc}.")
        print(f"La empresa tiene obligaciones fiscales a partir del {(datetime.datetime.strptime(fecha_constitucion, '%Y-%m-%d') + datetime.timedelta(days=30)).strftime('%Y-%m-%d')} y debe pagar un total de ${capital_social * 0.51:,.2f} MXN en impuestos y contribuciones.")

    except IndexError:
        print("Error: Faltan argumentos. Por favor, proporcione todos los argumentos necesarios.")
    except ValueError:
        print("Error: Valor no válido. Por favor, proporcione valores numéricos para el capital social y el número de socios.")

if __name__ == "__main__":
    main()