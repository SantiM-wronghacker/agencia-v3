"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza generador factura conceptos
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

def generar_factura_conceptos(rfc_emisor, rfc_receptor, conceptos, tasa_iva=0.16, tasa_isr=0.1):
    try:
        # Datos base
        fecha = datetime.datetime.now().strftime("%Y-%m-%d")
        hora = datetime.datetime.now().strftime("%H:%M:%S")

        # Validar RFC
        if not validar_rfc(rfc_emisor) or not validar_rfc(rfc_receptor):
            raise ValueError("RFC inválido")

        # Validar conceptos
        if not conceptos:
            raise ValueError("No se han proporcionado conceptos")

        # Generar subtotal
        subtotal = sum(concepto["cantidad"] * concepto["precio"] for concepto in conceptos)
        iva = subtotal * tasa_iva
        isr = subtotal * tasa_isr
        total = subtotal + iva + isr

        # Crear factura
        factura = {
            "fecha": fecha,
            "hora": hora,
            "rfc_emisor": rfc_emisor,
            "rfc_receptor": rfc_receptor,
            "conceptos": conceptos,
            "subtotal": round(subtotal, 2),
            "iva": round(iva, 2),
            "isr": round(isr, 2),
            "total": round(total, 2)
        }

        return factura
    except Exception as e:
        raise ValueError(f"Error al generar factura: {str(e)}")

def validar_rfc(rfc):
    # Validar formato de RFC
    if len(rfc) != 13:
        return False
    if not rfc[:2].isalpha() or not rfc[2:12].isdigit() or not rfc[12].isalpha():
        return False
    return True

def main():
    try:
        if len(sys.argv) != 5:
            print("Uso: python generador_factura_conceptos.py <rfc_emisor> <rfc_receptor> <tasa_iva> <tasa_isr>", file=sys.stderr)
            sys.exit(1)

        rfc_emisor = sys.argv[1]
        rfc_receptor = sys.argv[2]
        tasa_iva = float(sys.argv[3])
        tasa_isr = float(sys.argv[4])

        conceptos = [
            {"clave": "01", "descripcion": "Consultoría en sistemas", "cantidad": 5, "precio": 1200.50},
            {"clave": "02", "descripcion": "Desarrollo de software", "cantidad": 3, "precio": 1500.00},
            {"clave": "03", "descripcion": "Mantenimiento de sistemas", "cantidad": 2, "precio": 800.00}
        ]

        factura = generar_factura_conceptos(rfc_emisor, rfc_receptor, conceptos, tasa_iva, tasa_isr)
        print("Factura generada con éxito:")
        print(f"Fecha: {factura['fecha']}")
        print(f"Hora: {factura['hora']}")
        print(f"RFC Emisor: {factura['rfc_emisor']}")
        print(f"RFC Receptor: {factura['rfc_receptor']}")
        print("Conceptos:")
        for concepto in factura['conceptos']:
            print(f"Clave: {concepto['clave']}, Descripción: {concepto['descripcion']}, Cantidad: {concepto['cantidad']}, Precio: {concepto['precio']}")
        print(f"Subtotal: {factura['subtotal']}")
        print(f"IVA ({tasa_iva*100}%): {factura['iva']}")
        print(f"ISR ({tasa_isr*100}%): {factura['isr']}")
        print(f"Total: {factura['total']}")
        print("Resumen ejecutivo:")
        print(f"La factura se generó con éxito para el RFC emisor {rfc_emisor} y el RFC receptor {rfc_receptor}. El total de la factura es {factura['total']}.")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()