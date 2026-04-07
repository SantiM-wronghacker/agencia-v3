"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Generador de clave de producto
TECNOLOGÍA: Python estándar
"""

import sys
import json
import math
import random
import datetime
import os
import re

def generador_clave_producto(entrada, *args):
    """Función pura, sin prints, sin side effects."""
    try:
        # Procesar 'entrada' (el primer parámetro recibido)
        if not entrada or len(entrada) != 10:
            raise ValueError("Longitud inválida")
        # Validar que entrada sea un número entero
        if not re.match("^[0-9]+$", entrada):
            raise ValueError("Entrada no es un número entero")
        # Validar que entrada sea un número positivo
        if float(entrada) <= 0:
            raise ValueError("Entrada no es un número positivo")
        # Generar clave de producto aleatoria
        clave_producto = str(random.randint(100000000, 999999999))
        # Calcular impuesto (al 16% para México)
        impuesto = math.ceil((float(entrada) * 0.16) * 100) / 100
        # Calcular subtotal
        subtotal = float(entrada) + impuesto
        # Calcular total con impuesto incluido
        total = math.ceil((float(entrada) + impuesto) * 1.16) / 1.16
        # Calcular descuento (10% si el subtotal es mayor a 1000)
        descuento = 0
        if subtotal > 1000:
            descuento = math.ceil(subtotal * 0.10) / 100
        # Calcular total con descuento incluido
        total_descuento = math.ceil((subtotal - descuento) * 1.16) / 1.16
        # Generar fecha de emisión
        fecha_emision = datetime.datetime.now().strftime("%Y-%m-%d")
        # Generar hora de emisión
        hora_emision = datetime.datetime.now().strftime("%H:%M:%S")
        # Generar código de respuesta
        respuesta_codigo = os.environ.get("RESPONSE_CODE", "200")
        # Generar mensaje de respuesta
        respuesta_mensaje = os.environ.get("RESPONSE_MESSAGE", "Operación exitosa")
        # Generar detalles de pago
        detalles_pago = {
            "moneda": "MXN",
            "metodo_pago": "Tarjeta de crédito",
            "direccion_pago": "Calle 123, Colonia 456, Ciudad 789"
        }
        # Generar resumen ejecutivo
        resumen_ejecutivo = {
            "clave_producto": clave_producto,
            "subtotal": subtotal,
            "impuesto": impuesto,
            "total": total,
            "descuento": descuento,
            "total_descuento": total_descuento
        }
        # Devolver resultado en formato JSON
        return json.dumps({
            "clave_producto": clave_producto,
            "subtotal": subtotal,
            "impuesto": impuesto,
            "total": total,
            "descuento": descuento,
            "total_descuento": total_descuento,
            "fecha_emision": fecha_emision,
            "hora_emision": hora_emision,
            "respuesta_codigo": respuesta_codigo,
            "respuesta_mensaje": respuesta_mensaje,
            "detalles_pago": detalles_pago,
            "resumen_ejecutivo": resumen_ejecutivo
        })
    except ValueError as e:
        return json.dumps({"error": str(e)})
    except Exception as e:
        return json.dumps({"error": "Ocurrió un error inesperado: " + str(e)})

def main():
    if len(sys.argv) > 1:
        entrada = sys.argv[1]
    else:
        entrada = "1000000000"
    print(generador_clave_producto(entrada))

if __name__ == "__main__":
    main()