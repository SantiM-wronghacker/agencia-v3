import os
import sys
import json
from datetime import datetime
import math
import re
import random

def cotizador_seguro_empresarial(empresa=None, seguro=None, premio=None, descuento=None, fecha_vigencia=None, tipo_cambio=None):
    try:
        # Verificar si se recibieron parametros por sys.argv
        if empresa is None:
            empresa = sys.argv[1] if len(sys.argv) > 1 else "ABC Seguros"
        if seguro is None:
            seguro = sys.argv[2] if len(sys.argv) > 2 else "Seguro de Responsabilidad Civil"
        if premio is None:
            premio = float(sys.argv[3]) if len(sys.argv) > 3 else 15000.00
        if descuento is None:
            descuento = float(sys.argv[4]) if len(sys.argv) > 4 else 0.10
        if fecha_vigencia is None:
            fecha_vigencia = datetime.now().strftime("%Y-%m-%d")
        if tipo_cambio is None:
            tipo_cambio = 20.00

        # Verificar si los valores son válidos
        if premio < 0:
            raise ValueError("El premio no puede ser negativo")
        if descuento < 0 or descuento > 1:
            raise ValueError("El descuento debe ser entre 0 y 1")
        if tipo_cambio < 0:
            raise ValueError("El tipo de cambio no puede ser negativo")
        if premio * (1 - descuento) * tipo_cambio < 0:
            raise ValueError("El precio final no puede ser negativo")

        # Calculo del premio final con descuento
        premio_final = premio * (1 - descuento)

        # Impresion de resultados
        print("ÁREA: SEGUROS")
        print("DESCRIPCIÓN: Cotizador seguro empresarial")
        print("TECNOLOGÍA: Python estándar")
        print(f"Empresa: {empresa}")
        print(f"Seguro: {seguro}")
        print(f"Precio: ${premio:.2f}")
        print(f"Descuento: {descuento*100}%")
        print(f"Precio final: ${premio_final:.2f}")
        print(f"Fecha de vigencia: {fecha_vigencia}")
        print(f"Tipo de cambio: ${tipo_cambio:.2f}")
        print(f"Valor de cambio (MXN): ${premio_final * tipo_cambio:.2f}")
        print(f"Comisión de agente: ${premio_final * 0.05:.2f}")
        print(f"Total a pagar: ${premio_final + (premio_final * 0.05):.2f}")
        print(f"Valor de seguro por día: ${premio_final / 365:.2f}")
        print(f"Valor de seguro por mes: ${premio_final / 30:.2f}")
        print(f"Valor de seguro por año: ${premio_final:.2f}")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"La empresa {empresa} ha contratado el seguro de responsabilidad civil por un precio de ${premio:.2f}.")
        print(f"Después de aplicar un descuento del {descuento*100}% se obtiene un precio final de ${premio_final:.2f}.")
        print(f"El tipo de cambio utilizado fue de ${tipo_cambio:.2f} y el valor de cambio en pesos mexicanos fue de ${premio_final * tipo_cambio:.2f}.")

    except ValueError as e:
        print(f"Error: {e}")
    except IndexError:
        print("Error: Faltan argumentos")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cotizador_seguro_empresarial(*sys.argv[1:])
    else:
        print("Error: Faltan argumentos")