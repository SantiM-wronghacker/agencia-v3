"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que genera cotizaciones y correos electrónicos para ventas
TECNOLOGÍA: Python estándar
"""

import sys
import os
import json
from datetime import datetime, timedelta
import random
import math

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def generar_cotizacion(cliente=None, vendedor=None, productos=None):
    productos = productos or [
        {"nombre": "Laptop HP", "precio": 12999.99, "cantidad": 1},
        {"nombre": "Monitor Dell", "precio": 4999.50, "cantidad": 2},
        {"nombre": "Teclado Logitech", "precio": 899.99, "cantidad": 3},
        {"nombre": "Mouse Logitech", "precio": 399.99, "cantidad": 2},
        {"nombre": "Bocinas JBL", "precio": 1999.99, "cantidad": 1},
    ]

    try:
        subtotal = sum(item["precio"] * item["cantidad"] for item in productos)
        iva = subtotal * 0.16
        total = subtotal + iva

        return {
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "productos": productos,
            "subtotal": round(subtotal, 2),
            "iva": round(iva, 2),
            "total": round(total, 2),
            "cliente": cliente or "Empresa XYZ S.A. de C.V.",
            "vendedor": vendedor or "Juan Pérez",
            "numero_cotizacion": f"COT-{random.randint(1000, 9999)}",
            "validez": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),
            "condiciones": "Pago al contado con 5% de descuento. 30 días para pago con tarjeta."
        }
    except Exception as e:
        raise ValueError(f"Error al calcular cotización: {e}")

def generar_email(cotizacion):
    try:
        fecha = cotizacion["fecha"]
        productos = "\n".join(
            f"- {item['nombre']}: ${item['precio']:.2f} x {item['cantidad']} = ${item['precio'] * item['cantidad']:.2f}"
            for item in cotizacion["productos"]
        )
        mensaje = f"""
        Estimado/a {cotizacion["cliente"]},

        Adjunto encontrará la cotización {cotizacion["numero_cotizacion"]} con fecha {fecha}, válida hasta {cotizacion["validez"]}.

        Detalle de productos:
        {productos}

        Resumen:
        Subtotal: ${cotizacion["subtotal"]:.2f}
        IVA (16%): ${cotizacion["iva"]:.2f}
        Total: ${cotizacion["total"]:.2f}

        Condiciones comerciales:
        {cotizacion["condiciones"]}

        Resumen ejecutivo:
        - Cotización válida por 15 días naturales
        - Opción de pago al contado con 5% de descuento
        - Entrega estimada: 7-10 días hábiles
        - Garantía de 1 año en todos los productos

        Atentamente,
        {cotizacion["vendedor"]}
        Agencia Santi
        Tel: 55-1234-5678
        Email: ventas@agenciasanti.com
        """

        return mensaje
    except Exception as e:
        raise ValueError(f"Error al generar email: {e}")

def main():
    try:
        # Procesar argumentos de línea de comandos
        args = sys.argv[1:]
        cliente = args[0] if len(args) > 0 else None
        vendedor = args[1] if len(args) > 1 else None

        cotizacion = generar_cotizacion(cliente, vendedor)
        email = generar_email(cotizacion)
        print(email)
    except Exception as e:
        print(f"Error al generar la cotización: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()