"""
ÁREA: BIENES RAÍCES COMERCIALES
DESCRIPCIÓN: Agente que realiza calculadora contrato arrendamiento comercial
TECNOLOGÍA: Python estándar
"""

import sys
import math
from datetime import datetime, timedelta

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        precio_mensual = 15000  # MXN
        iva = 0.16
        mantenimiento = 0.05
        dias_mora = 3
        penalizacion_mora = 0.02
        tasa_inflacion = 0.03
        tasa_interes = 0.06

        # Procesar argumentos
        if len(sys.argv) > 1:
            precio_mensual = float(sys.argv[1])
        if len(sys.argv) > 2:
            iva = float(sys.argv[2])
        if len(sys.argv) > 3:
            mantenimiento = float(sys.argv[3])
        if len(sys.argv) > 4:
            dias_mora = int(sys.argv[4])
        if len(sys.argv) > 5:
            penalizacion_mora = float(sys.argv[5])

        # Cálculos
        iva_mensual = precio_mensual * iva
        total_mensual = precio_mensual + iva_mensual
        mantenimiento_mensual = total_mensual * mantenimiento
        total_con_mantenimiento = total_mensual + mantenimiento_mensual

        # Penalización por mora
        penalizacion_diaria = precio_mensual * penalizacion_mora
        penalizacion_total = penalizacion_diaria * dias_mora

        # Ajuste por inflación
        ajuste_inflacion = precio_mensual * tasa_inflacion

        # Intereses por pago anticipado
        intereses_pago_anticipado = precio_mensual * tasa_interes

        # Fecha de cálculo
        fecha_actual = datetime.now().strftime("%d/%m/%Y")

        # Salida
        print(f"Cálculo de contrato de arrendamiento comercial - {fecha_actual}")
        print(f"Renta mensual: ${precio_mensual:,.2f} MXN")
        print(f"IVA (16%): ${iva_mensual:,.2f} MXN")
        print(f"Total mensual (incl. IVA): ${total_mensual:,.2f} MXN")
        print(f"Mantenimiento (5%): ${mantenimiento_mensual:,.2f} MXN")
        print(f"Total con mantenimiento: ${total_con_mantenimiento:,.2f} MXN")
        print(f"Penalización por {dias_mora} días de mora: ${penalizacion_total:,.2f} MXN")
        print(f"Ajuste por inflación (3%): ${ajuste_inflacion:,.2f} MXN")
        print(f"Intereses por pago anticipado (6%): ${intereses_pago_anticipado:,.2f} MXN")
        print(f"Total anual: ${total_con_mantenimiento * 12:,.2f} MXN")
        print(f"Total con ajuste por inflación: ${total_con_mantenimiento + ajuste_inflacion:,.2f} MXN")
        print(f"Total con intereses por pago anticipado: ${total_con_mantenimiento + intereses_pago_anticipado:,.2f} MXN")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El contrato de arrendamiento comercial tiene un total mensual de ${total_con_mantenimiento:,.2f} MXN.")
        print(f"El ajuste por inflación es de ${ajuste_inflacion:,.2f} MXN.")
        print(f"Los intereses por pago anticipado son de ${intereses_pago_anticipado:,.2f} MXN.")
        print(f"El total anual es de ${total_con_mantenimiento * 12:,.2f} MXN.")

    except ValueError as e:
        print(f"Error en el valor: {str(e)}")
    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")

if __name__ == "__main__":
    main()