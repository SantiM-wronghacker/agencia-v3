"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza generador argumentario ventas
TECNOLOGÍA: Python estándar
"""

import sys
import random
from datetime import datetime
import math

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_precio_mensual(precio_base, meses, descuento):
    precio_mensual = precio_base * meses * (1 - descuento / 100)
    return precio_mensual

def calcular_impuestos(precio_mensual, meses, descuento):
    precio_mensual_total = calcular_precio_mensual(precio_mensual, meses, descuento)
    impuestos = precio_mensual_total * 0.16
    return impuestos

def calcular_precio_total_con_impuestos(precio_mensual, meses, descuento):
    precio_mensual_total = calcular_precio_mensual(precio_mensual, meses, descuento)
    impuestos = calcular_impuestos(precio_mensual, meses, descuento)
    precio_total = precio_mensual_total * 1.16
    return precio_total

def main():
    try:
        # Parámetros por defecto
        producto = sys.argv[1] if len(sys.argv) > 1 else "Seguro de Auto"
        cliente = sys.argv[2] if len(sys.argv) > 2 else "Cliente Premium"
        meses = int(sys.argv[3]) if len(sys.argv) > 3 else 12
        descuento = float(sys.argv[4]) if len(sys.argv) > 4 else 15.5
        coberturas = sys.argv[5] if len(sys.argv) > 5 else "Básica, Ampliada, Total"

        # Generación de argumentario
        print(f"Argumentario para {producto} - {cliente}")
        print(f"1. Oferta especial: {descuento}% de descuento en {meses} meses")
        print(f"2. Coberturas disponibles: {coberturas}")
        precio_base = random.randint(500, 2000)
        print(f"3. Precio base estimado: ${precio_base:,.2f} MXN")
        print(f"4. Beneficio adicional: {random.choice(['Asistencia vial 24/7', 'Protección legal', 'Reembolso de gastos médicos'])}")
        fecha_inicial = datetime.now().strftime('%d/%m/%Y')
        fecha_final = datetime.now().replace(year=datetime.now().year + 1).strftime('%d/%m/%Y')
        print(f"5. Fecha de vigencia: {fecha_inicial} a {fecha_final}")
        precio_mensual = calcular_precio_mensual(precio_base, meses, descuento)
        print(f"6. Precio mensual estimado: ${precio_mensual:,.2f} MXN")
        print(f"7. Ahorro estimado con descuento: ${precio_base * meses * (descuento / 100):,.2f} MXN")
        print(f"8. Precio total estimado: ${precio_mensual * meses:,.2f} MXN")
        print(f"9. Impuestos aplicables (16% IVA): ${calcular_impuestos(precio_base, meses, descuento):,.2f} MXN")
        print(f"10. Precio total con impuestos: ${calcular_precio_total_con_impuestos(precio_base, meses, descuento):,.2f} MXN")
        print(f"11. Tasa de interés anual: {math.pow(1 + descuento / 100, meses):,.2f}")
        print(f"12. Resumen ejecutivo: El seguro de auto ofrece una excelente opción para proteger tus bienes y tu familia. Con un descuento del {descuento}% en {meses} meses, puedes ahorrar {precio_base * meses * (descuento / 100):,.2f} MXN y pagar un precio total de {calcular_precio_total_con_impuestos(precio_base, meses, descuento):,.2f} MXN.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()