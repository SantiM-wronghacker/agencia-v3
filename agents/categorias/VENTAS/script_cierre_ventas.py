"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza script cierre ventas
TECNOLOGÍA: Python estándar
"""

import sys
import os
import json
import datetime
import random
import math
import re

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Configuración por defecto
        fecha_cierre = datetime.date.today().strftime("%Y-%m-%d")
        if len(sys.argv) > 1:
            meta_ventas = int(sys.argv[1])
        else:
            meta_ventas = 500000  # Meta en MXN
        if len(sys.argv) > 2:
            ventas_realizadas = int(sys.argv[2])
        else:
            ventas_realizadas = random.randint(450000, 550000)  # Ventas en MXN
        if len(sys.argv) > 3:
            clientes_atendidos = int(sys.argv[3])
        else:
            clientes_atendidos = random.randint(100, 200)
        if len(sys.argv) > 4:
            tasa_conversion = float(sys.argv[4])
        else:
            tasa_conversion = random.uniform(0.15, 0.25)
        if len(sys.argv) > 5:
            productos_vendidos = int(sys.argv[5])
        else:
            productos_vendidos = random.randint(500, 1000)

        # Procesamiento
        diferencia_meta = ventas_realizadas - meta_ventas
        porcentaje_cumplimiento = (ventas_realizadas / meta_ventas) * 100
        ingresos_por_cliente = ventas_realizadas / clientes_atendidos
        tasa_cumplimiento = (diferencia_meta / meta_ventas) * 100
        productos_promedio_por_cliente = productos_vendidos / clientes_atendidos
        conversion_efectiva = tasa_conversion * clientes_atendidos

        # Salida
        print(f"Fecha de cierre: {fecha_cierre}")
        print(f"Meta de ventas: ${meta_ventas:,.2f} MXN")
        print(f"Ventas realizadas: ${ventas_realizadas:,.2f} MXN")
        print(f"Diferencia con meta: ${diferencia_meta:,.2f} MXN ({porcentaje_cumplimiento:.1f}%)")
        print(f"Clientes atendidos: {clientes_atendidos}")
        print(f"Productos vendidos: {productos_vendidos}")
        print(f"Tasa de conversión: {tasa_conversion:.1%}")
        print(f"Ingresos promedio por cliente: ${ingresos_por_cliente:,.2f} MXN")
        print(f"Tasa de cumplimiento: {tasa_cumplimiento:.1f}%")
        print(f"Productos promedio por cliente: {productos_promedio_por_cliente:.1f}")
        print(f"Conversión efectiva: {conversion_efectiva:.1f} clientes")
        print(f"Porcentaje de clientes que realizaron compras: {(tasa_conversion*100):.1f}%")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El día {fecha_cierre} se alcanzó un total de ${ventas_realizadas:,.2f} MXN en ventas, lo que representa un {porcentaje_cumplimiento:.1f}% del objetivo.")
        print(f"Se atendieron un total de {clientes_atendidos} clientes, con un promedio de ${ingresos_por_cliente:,.2f} MXN por cliente.")
        print(f"La tasa de conversión fue de {tasa_conversion:.1%}, lo que representa una conversión efectiva de {conversion_efectiva:.1f} clientes.")

    except ValueError as e:
        print(f"Error en el valor ingresado: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except ZeroDivisionError as e:
        print(f"Error al dividir por cero: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error en el script de cierre de ventas: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()