import os
import sys
import json
import datetime
import math
import re
import random

"""
ÁREA: ECOMMERCE
DESCRIPCIÓN: Agente que realiza generador email postventa
TECNOLOGÍA: Python estándar
"""

def generar_email_postventa(nombre_cliente, correo_cliente, fecha_pedido, numero_pedido, subtotal, iva, total, nombre_destinatario, dirección_destinatario, código_postal_destinatario):
    try:
        # Cuerpo del email
        cuerpo_email = f"""
Hola {nombre_cliente},

Gracias por tu compra con nosotros. A continuación, te presentamos los detalles de tu pedido:

* Fecha de pedido: {fecha_pedido}
* Número de pedido: {numero_pedido}
* Subtotal: ${subtotal:.2f}
* IVA (16%): ${iva:.2f}
* Total: ${total:.2f}

Tu pedido se encuentra en proceso de envío. Te informaremos cuando se haya entregado a tu dirección:

* Nombre del destinatario: {nombre_destinatario}
* Dirección del destinatario: {dirección_destinatario}
* Código postal del destinatario: {código_postal_destinatario}

La entrega se estima en un plazo de 3 a 5 días hábiles.

Si tienes alguna pregunta o inquietud, no dudes en hacérmelo saber.

Atentamente,
Tu equipo de servicio al cliente

Resumen ejecutivo:
* Fecha de entrega estimada: {datetime.date.today() + datetime.timedelta(days=5)}
* Método de pago: Tarjeta de crédito
* Estado del pedido: En proceso de envío
        """
        
        return cuerpo_email
    except Exception as e:
        return f"Error al generar email: {str(e)}"

def calcular_iva(subtotal):
    try:
        iva = subtotal * 0.16
        return iva
    except Exception as e:
        return 0

def calcular_total(subtotal, iva):
    try:
        total = subtotal + iva
        return total
    except Exception as e:
        return 0

def main():
    try:
        if len(sys.argv) > 1:
            nombre_cliente = sys.argv[1]
            correo_cliente = sys.argv[2]
            fecha_pedido = sys.argv[3]
            numero_pedido = int(sys.argv[4])
            subtotal = float(sys.argv[5])
            nombre_destinatario = sys.argv[6]
            dirección_destinatario = sys.argv[7]
            código_postal_destinatario = sys.argv[8]
        else:
            nombre_cliente = "Juan Pérez"
            correo_cliente = "juan.perez@example.com"
            fecha_pedido = datetime.date.today().strftime("%Y-%m-%d")
            numero_pedido = 12345
            subtotal = 100.00
            nombre_destinatario = "Juan Pérez"
            dirección_destinatario = "Av. 5 de Mayo 123, Col. Centro"
            código_postal_destinatario = "06000"
        
        iva = calcular_iva(subtotal)
        total = calcular_total(subtotal, iva)
        
        cuerpo_email = generar_email_postventa(nombre_cliente, correo_cliente, fecha_pedido, numero_pedido, subtotal, iva, total, nombre_destinatario, dirección_destinatario, código_postal_destinatario)
        
        print("ÁREA: ECOMMERCE")
        print("DESCRIPCIÓN: Agente que realiza generador email postventa")
        print("TECNOLOGÍA: Python estándar")
        print(f"Cuerpo del email: {cuerpo_email}")
        print(f"Nombre del cliente: {nombre_cliente}")
        print(f"Correo del cliente: {correo_cliente}")
        print(f"Fecha de pedido: {fecha_pedido}")
        print(f"Número de pedido: {numero_pedido}")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"IVA (16%): ${iva:.2f}")
        print(f"Total: ${total:.2f}")
        print(f"Nombre del destinatario: {nombre_destinatario}")
        print(f"Dirección del destinatario: {dirección_destinatario}")
        print(f"Código postal del destinatario: {código_postal_destinatario}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()