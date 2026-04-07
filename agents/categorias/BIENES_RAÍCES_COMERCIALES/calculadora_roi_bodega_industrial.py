"""
ÁREA: BIENES RAÍCES COMERCIALES
DESCRIPCIÓN: Agente que realiza calculadora roi bodega industrial
TECNOLOGÍA: Python estándar
"""

import sys
import math
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto realistas para México
        precio_compra = float(sys.argv[1]) if len(sys.argv) > 1 else 5000000.0  # $5,000,000 MXN
        renta_mensual = float(sys.argv[2]) if len(sys.argv) > 2 else 150000.0    # $150,000 MXN/mes
        gastos_mensuales = float(sys.argv[3]) if len(sys.argv) > 3 else 30000.0  # $30,000 MXN/mes
        años_inversión = float(sys.argv[4]) if len(sys.argv) > 4 else 5.0        # 5 años
        tasa_interes = float(sys.argv[5]) if len(sys.argv) > 5 else 0.06         # 6% anual
        tasa_inflacion = float(sys.argv[6]) if len(sys.argv) > 6 else 0.03       # 3% anual

        # Cálculos
        flujo_anual = (renta_mensual - gastos_mensuales) * 12
        flujo_total = flujo_anual * años_inversión
        roi = (flujo_total / precio_compra) * 100

        # Proyección de valor futuro (con tasa de apreciación anual)
        valor_futuro = precio_compra * math.pow(1 + tasa_inflacion, años_inversión)
        ganancia_total = valor_futuro - precio_compra + flujo_total

        # Cálculo de la tasa interna de retorno (TIR)
        tir = (flujo_total / precio_compra) ** (1 / años_inversión) - 1

        # Cálculo del período de recuperación de la inversión
        recuperacion_inversion = precio_compra / flujo_anual

        # Impresión de resultados
        print("Cálculo ROI Bodega Industrial")
        print(f"Precio de compra: ${precio_compra:,.2f} MXN")
        print(f"Renta mensual: ${renta_mensual:,.2f} MXN")
        print(f"Gastos mensuales: ${gastos_mensuales:,.2f} MXN")
        print(f"Años de inversión: {años_inversión} años")
        print(f"Flujo anual estimado: ${flujo_anual:,.2f} MXN")
        print(f"Flujo total estimado: ${flujo_total:,.2f} MXN")
        print(f"ROI en {años_inversión} años: {roi:.2f}%")
        print(f"Valor futuro estimado: ${valor_futuro:,.2f} MXN")
        print(f"Ganancia total estimada: ${ganancia_total:,.2f} MXN")
        print(f"Tasa interna de retorno (TIR): {tir * 100:.2f}%")
        print(f"Período de recuperación de la inversión: {recuperacion_inversion:.2f} años")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"La inversión en la bodega industrial tiene un ROI de {roi:.2f}% en {años_inversión} años.")
        print(f"El valor futuro estimado es de ${valor_futuro:,.2f} MXN.")
        print(f"La ganancia total estimada es de ${ganancia_total:,.2f} MXN.")
        print(f"El período de recuperación de la inversión es de {recuperacion_inversion:.2f} años.")

    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")
        print("Uso: calculadora_roi_bodega_industrial.py [precio_compra] [renta_mensual] [gastos_mensuales] [años_inversión] [tasa_interes] [tasa_inflacion]")
        sys.exit(1)

if __name__ == "__main__":
    main()