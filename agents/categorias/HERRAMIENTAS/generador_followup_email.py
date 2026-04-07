"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza generador followup email
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_email(nombre_cliente, producto, precio, fecha_venta, fecha_envío):
    # Calcula IVA y impuestos según la ley mexicana
    iva = precio * 0.16
    impuestos = precio * 0.08
    monto_total = precio + iva + impuestos

    # Generar cuerpo del email
    cuerpo_email = f"Hola {nombre_cliente},\n\n\
Se acerca la fecha de envío de tu {producto}.\n\
El precio final es de {precio:.2f} pesos mexicanos.\n\
La fecha de envío es {fecha_envío}.\n\
La fecha de venta fue {fecha_venta}.\n\
El monto de IVA es de {iva:.2f} pesos mexicanos.\n\
El monto de impuestos es de {impuestos:.2f} pesos mexicanos.\n\
El monto total es de {monto_total:.2f} pesos mexicanos.\n\
\n\
Un saludo,\n\
Tu agente"

    # Generar asunto del email
    asunto_email = f"Seguimiento de tu pedido de {producto}"

    # Devolver datos del email
    return {
        "nombre_cliente": nombre_cliente,
        "producto": producto,
        "precio": precio,
        "fecha_venta": fecha_venta,
        "fecha_envío": fecha_envío,
        "cuerpo_email": cuerpo_email,
        "asunto_email": asunto_email
    }

def main():
    try:
        if len(sys.argv) != 7:
            print("Error: Faltan argumentos")
            sys.exit(1)

        nombre_cliente = sys.argv[1]
        producto = sys.argv[2]
        precio = float(sys.argv[3])
        anio_venta = int(sys.argv[4])
        mes_venta = int(sys.argv[5])
        anio_envio = int(sys.argv[6])

        if precio <= 0:
            print("Error: Precio debe ser mayor a cero")
            sys.exit(1)

        if not (1 <= mes_venta <= 12):
            print("Error: Mes de venta debe estar entre 1 y 12")
            sys.exit(1)

        if not (1 <= anio_venta <= 9999):
            print("Error: Año de venta debe estar entre 1 y 9999")
            sys.exit(1)

        if not (1 <= anio_envio <= 9999):
            print("Error: Año de envío debe estar entre 1 y 9999")
            sys.exit(1)

        fecha_venta = datetime.date(anio_venta, mes_venta, 1)
        fecha_envío = datetime.date(anio_envio, 1, 1)

        datos_email = generar_email(nombre_cliente, producto, precio, fecha_venta, fecha_envío)

        print(f"Nombre cliente: {datos_email['nombre_cliente']}")
        print(f"Producto: {datos_email['producto']}")
        print(f"Precio: {datos_email['precio']:.2f} pesos mexicanos")
        print(f"Fecha venta: {datos_email['fecha_venta']}")
        print(f"Fecha envío: {datos_email['fecha_envío']}")
        print(f"Cuerpo email: {datos_email['cuerpo_email']}")
        print(f"Asunto email: {datos_email['asunto_email']}")

        print("Resumen ejecutivo:")
        print(f"El cliente {datos_email['nombre_cliente']} ha pedido un {datos_email['producto']} por un precio de {datos_email['precio']:.2f} pesos mexicanos.")
        print(f"La fecha de venta fue {datos_email['fecha_venta']} y la fecha de envío es {datos_email['fecha_envío']}.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()