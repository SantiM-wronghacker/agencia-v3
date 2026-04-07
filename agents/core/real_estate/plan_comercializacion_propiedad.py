import sys
import json
import datetime
import math
import re
import random
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        precio_venta = float(sys.argv[1]) if len(sys.argv) > 1 else 5000000.0
        comision_agente = float(sys.argv[2]) if len(sys.argv) > 2 else 0.05
        gastos_cierre = float(sys.argv[3]) if len(sys.argv) > 3 else 0.10
        impuesto_traslado = float(sys.argv[4]) if len(sys.argv) > 4 else 0.02
        impuesto_over = float(sys.argv[5]) if len(sys.argv) > 5 else 0.08
        tasa_interes_anual = float(sys.argv[6]) if len(sys.argv) > 6 else 0.12
        plazo_pago = int(sys.argv[7]) if len(sys.argv) > 7 else 30

        # Verificar si los parámetros son válidos
        if precio_venta <= 0 or comision_agente < 0 or gastos_cierre < 0 or impuesto_traslado < 0 or impuesto_over < 0 or tasa_interes_anual < 0 or plazo_pago <= 0:
            raise ValueError("Los parámetros deben ser números positivos")

        # Cálculo de comisiones y gastos
        comision_agente_total = precio_venta * comision_agente
        gastos_cierre_total = precio_venta * gastos_cierre
        impuesto_traslado_total = precio_venta * impuesto_traslado
        impuesto_over_total = precio_venta * impuesto_over
        tasa_interes_mensual = (tasa_interes_anual / 100 / 12) * precio_venta
        total_intereses = tasa_interes_mensual * plazo_pago
        total_pagar = precio_venta + comision_agente_total + gastos_cierre_total + impuesto_traslado_total + impuesto_over_total + total_intereses

        # Resumen de resultados
        print("ÁREA: REAL ESTATE")
        print("DESCRIPCION: Agente que realiza plan comercializacion propiedad")
        print("TECNOLOGÍA: Python estándar")
        print(f"Precio de venta: ${precio_venta:,.2f} MXN")
        print(f"Comisión del agente: ${comision_agente_total:,.2f} MXN ({comision_agente*100:.2f}%)")
        print(f"Gastos de cierre: ${gastos_cierre_total:,.2f} MXN ({gastos_cierre*100:.2f}%)")
        print(f"Impuesto de traslado: ${impuesto_traslado_total:,.2f} MXN ({impuesto_traslado*100:.2f}%)")
        print(f"Impuesto de sobre: ${impuesto_over_total:,.2f} MXN ({impuesto_over*100:.2f}%)")
        print(f"Tasa de interés anual: {tasa_interes_anual*100:.2f}%")
        print(f"Plazo de pago: {plazo_pago} meses")
        print(f"Total a pagar: ${total_pagar:,.2f} MXN")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El precio de venta de la propiedad es de ${precio_venta:,.2f} MXN.")
        print(f"La comisión del agente será de ${comision_agente_total:,.2f} MXN.")
        print(f"Los gastos de cierre serán de ${gastos_cierre_total:,.2f} MXN.")
        print(f"El impuesto de traslado será de ${impuesto_traslado_total:,.2f} MXN.")
        print(f"El impuesto de sobre será de ${impuesto_over_total:,.2f} MXN.")
        print(f"El total a pagar será de ${total_pagar:,.2f} MXN.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()