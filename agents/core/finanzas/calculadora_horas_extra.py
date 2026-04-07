"""
ÁREA: RECURSOS HUMANOS
DESCRIPCIÓN: Agente que realiza calculadora horas extra con normativa mexicana
TECNOLOGÍA: Python estándar
"""

import sys
import os
from datetime import datetime, timedelta

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_horas_extra(horas_trabajadas, horas_ordinarias, tarifa_hora, dia_sabado=False, dia_domingo=False, dia_festivo=False):
    horas_extra = max(0, horas_trabajadas - horas_ordinarias)

    # Cálculo según normativa mexicana
    if dia_domingo or dia_festivo:
        pago_extra = horas_extra * tarifa_hora * 3  # Triple pago
    elif dia_sabado:
        pago_extra = horas_extra * tarifa_hora * 2.5  # 2.5 veces
    else:
        pago_extra = horas_extra * tarifa_hora * 2  # Doble pago

    return horas_extra, pago_extra

def main():
    try:
        # Parámetros por defecto realistas para México
        horas_trabajadas = float(sys.argv[1]) if len(sys.argv) > 1 else 45.5
        horas_ordinarias = float(sys.argv[2]) if len(sys.argv) > 2 else 40.0
        tarifa_hora = float(sys.argv[3]) if len(sys.argv) > 3 else 150.0
        dia_sabado = sys.argv[4].lower() == 'true' if len(sys.argv) > 4 else False
        dia_domingo = sys.argv[5].lower() == 'true' if len(sys.argv) > 5 else False
        dia_festivo = sys.argv[6].lower() == 'true' if len(sys.argv) > 6 else False

        # Validaciones
        if horas_trabajadas < 0 or horas_ordinarias < 0 or tarifa_hora < 0:
            raise ValueError("Los valores no pueden ser negativos")

        horas_extra, pago_extra = calcular_horas_extra(
            horas_trabajadas, horas_ordinarias, tarifa_hora,
            dia_sabado, dia_domingo, dia_festivo
        )

        # Cálculo de impuestos
        impuesto_renta = pago_extra * 0.10  # 10% de ISR aproximado
        neto_recibir = pago_extra - impuesto_renta

        print("Cálculo de horas extra (Normativa mexicana):")
        print(f"Horas trabajadas: {horas_trabajadas:.2f} hrs")
        print(f"Horas ordinarias: {horas_ordinarias:.2f} hrs")
        print(f"Horas extra: {horas_extra:.2f} hrs")
        print(f"Tarifa por hora: ${tarifa_hora:.2f} MXN")
        print(f"Pago bruto por horas extra: ${pago_extra:.2f} MXN")
        print(f"ISR estimado (10%): ${impuesto_renta:.2f} MXN")
        print(f"Neto a recibir: ${neto_recibir:.2f} MXN")
        print(f"Día sábado: {'Sí' if dia_sabado else 'No'}")
        print(f"Día domingo: {'Sí' if dia_domingo else 'No'}")
        print(f"Día festivo: {'Sí' if dia_festivo else 'No'}")

        # Resumen ejecutivo
        print("\n=== Resumen ejecutivo ===")
        print(f"El empleado trabajará {horas_extra:.2f} horas extra")
        print(f"Recibirá un pago neto de ${neto_recibir:.2f} MXN")
        print(f"El cálculo considera {'' if not (dia_sabado or dia_domingo or dia_festivo) else 'premios por'} días especiales")

    except ValueError as ve:
        print(f"Error de validación: {str(ve)}")
    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")
    finally:
        print("\nUso: python calculadora_horas_extra.py [horas_trabajadas] [horas_ordinarias] [tarifa_hora] [dia_sabado] [dia_domingo] [dia_festivo]")
        print