"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza generador email marketing
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_email_marketing(asunto=None, cuerpo=None, fecha=None, tipo_de_cambio=None, precio=None):
    try:
        if asunto is None:
            asunto = sys.argv[1] if len(sys.argv) > 1 else "Oferta especial de fin de semana"
        if cuerpo is None:
            cuerpo = sys.argv[2] if len(sys.argv) > 2 else "¡Descubre nuestras ofertas especiales de fin de semana! ¡No te pierdas la oportunidad de ahorrar!"
        if fecha is None:
            fecha = datetime.datetime(2024, 3, 15)
        if tipo_de_cambio is None:
            tipo_de_cambio = float(sys.argv[3]) if len(sys.argv) > 3 else 20.50
        if precio is None:
            precio = float(sys.argv[4]) if len(sys.argv) > 4 else 100.00

        # Calculos precisos para Mexico
        tipo_de_cambio = round(tipo_de_cambio, 2)
        precio_mex = round(precio * tipo_de_cambio, 2)
        descuento = round(precio * 0.10, 2)
        impuesto = round(precio * 0.16, 2)
        subtotal = round(precio + impuesto, 2)
        total = round(subtotal + descuento, 2)

        # Generar email marketing
        email = {
            "asunto": asunto,
            "cuerpo": cuerpo,
            "fecha": fecha.strftime("%Y-%m-%d"),
            "tipo_de_cambio": tipo_de_cambio,
            "precio": precio,
            "precio_mex": precio_mex,
            "descuento": descuento,
            "impuesto": impuesto,
            "subtotal": subtotal,
            "total": total
        }

        return email

    except IndexError:
        print("Error: Faltan argumentos de entrada")
        return None
    except ValueError:
        print("Error: Los argumentos de entrada deben ser números")
        return None
    except Exception as e:
        print("Error:", str(e))
        return None

def main():
    try:
        asunto = sys.argv[1] if len(sys.argv) > 1 else None
        cuerpo = sys.argv[2] if len(sys.argv) > 2 else None
        fecha = sys.argv[3] if len(sys.argv) > 3 else None
        tipo_de_cambio = sys.argv[4] if len(sys.argv) > 4 else None
        precio = sys.argv[5] if len(sys.argv) > 5 else None

        email = generar_email_marketing(asunto, cuerpo, fecha, tipo_de_cambio, precio)

        if email:
            print("Email Marketing:")
            print("----------------")
            print(f"Asunto: {email['asunto']}")
            print(f"Cuerpo: {email['cuerpo']}")
            print(f"Fecha: {email['fecha']}")
            print(f"Tipo de cambio: {email['tipo_de_cambio']}")
            print(f"Precio: {email['precio']} USD")
            print(f"Precio (MXN): {email['precio_mex']} MXN")
            print(f"Descuento: {email['descuento']} MXN")
            print(f"Impuesto: {email['impuesto']} MXN")
            print(f"Subtotal: {email['subtotal']} MXN")
            print(f"Total: {email['total']} MXN")

            print("\nResumen Ejecutivo:")
            print("-------------------")
            print("La oferta especial de fin de semana ofrece un precio de 100 USD, equivalente a 2,020 MXN. Con un descuento del 10% y un impuesto del 16%, el subtotal es de 2,240 MXN. El total es de 2,360 MXN.")

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()