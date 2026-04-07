"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza generador propuesta comercial
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime, timedelta
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por línea de comandos con defaults
        args = sys.argv[1:]
        if not args:
            args = ["Propuesta_Comercial_2023", "50000", "10", "2023-12-31"]

        nombre_propuesta = args[0]
        monto_inicial = float(args[1])
        meses = int(args[2])
        fecha_limite = args[3]

        # Generar datos de propuesta
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        fecha_entrega = (datetime.now() + timedelta(days=random.randint(1, 15))).strftime("%Y-%m-%d")
        descuento = random.uniform(0.05, 0.20)
        iva = 0.16
        total = monto_inicial * (1 - descuento) * (1 + iva)

        # Generar datos de contacto
        contactos = [
            {"nombre": "Juan Pérez", "puesto": "Gerente de Compras", "telefono": "5512345678"},
            {"nombre": "María López", "puesto": "Directora de Ventas", "telefono": "5587654321"}
        ]

        # Generar propuesta
        propuesta = {
            "nombre": nombre_propuesta,
            "fecha_creacion": fecha_actual,
            "fecha_entrega": fecha_entrega,
            "monto_inicial": monto_inicial,
            "descuento": descuento,
            "iva": iva,
            "total": total,
            "contactos": contactos,
            "condiciones": [
                "Pago al contado 5% de descuento",
                "Pago en 30 días sin descuento",
                "Garantía de 1 año"
            ]
        }

        # Calcular subtotal y total con más precisión
        subtotal = monto_inicial * (1 - descuento)
        impuestos = subtotal * iva
        total = subtotal + impuestos

        # Generar resumen ejecutivo
        resumen_ejecutivo = f"Se propone la adquisición de {nombre_propuesta} por un monto total de {total:.2f} pesos, con un descuento del {descuento*100:.2f}% y un impuesto del {iva*100:.2f}%."

        # Mostrar propuesta
        print("Propuesta Comercial Generada")
        print(f"Nombre: {propuesta['nombre']}")
        print(f"Fecha de Creación: {propuesta['fecha_creacion']}")
        print(f"Fecha de Entrega: {propuesta['fecha_entrega']}")
        print(f"Monto Inicial: {propuesta['monto_inicial']:.2f} pesos")
        print(f"Descuento: {propuesta['descuento']*100:.2f}%")
        print(f"IVA: {propuesta['iva']*100:.2f}%")
        print(f"Total: {propuesta['total']:.2f} pesos")
        print(f"Contactos:")
        for contacto in propuesta['contactos']:
            print(f"  - {contacto['nombre']} ({contacto['puesto']}) - {contacto['telefono']}")
        print(f"Condiciones:")
        for condicion in propuesta['condiciones']:
            print(f"  - {condicion}")
        print(f"Resumen Ejecutivo:\n{resumen_ejecutivo}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()