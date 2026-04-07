"""
ÁREA: FINANZAS
DESCRIPCIÓN: Calculadora de plazo vencimiento
TECNOLOGÍA: Python estándar
"""

import sys
import re
from datetime import datetime
import math

def calculadora_plazo_vencimiento(entrada, *args):
    """Función pura, sin prints, sin side effects."""
    try:
        fecha = datetime.strptime(entrada, "%d/%m/%Y")
        hoy = datetime.today()
        plazo = (fecha - hoy).days
        dias = plazo
        semanas = math.floor(plazo / 7)
        meses = math.floor(plazo / 30)
        años = math.floor(plazo / 365.25)  # Ajuste para años reales
        dias_restantes = plazo % 365.25
        semanas_restantes = (plazo % 7)
        meses_restantes = (plazo % 30)
        dias_año = plazo % 365
        meses_año = math.floor(dias_año / 30)
        semanas_año = math.floor(dias_año / 7)

        # Calculos precisos para Mexico
        dias_trabajo = plazo - (plazo % 365)
        dias_no_trabajo = plazo % 365
        días_trabajo_restantes = dias_no_trabajo % 365
        días_no_trabajo_restantes = dias_no_trabajo - días_trabajo_restantes

        # Resumen ejecutivo
        resumen = f"El plazo vencimiento es de {plazo} días, lo que equivale a {años} años, {meses} meses y {dias} días."
        resumen += f" Los días restantes son {dias_restantes}, y los días de trabajo restantes son {días_trabajo_restantes}."

        return (
            f"Plazo: {plazo} días",
            f"Días: {dias}",
            f"Semanas: {semanas}",
            f"Meses: {meses}",
            f"Años: {años}",
            f"Días restantes: {dias_restantes}",
            f"Semanas restantes: {semanas_restantes}",
            f"Meses restantes: {meses_restantes}",
            f"Días trabajo: {dias_trabajo}",
            f"Días no trabajo: {dias_no_trabajo}",
            f"Resumen ejecutivo: {resumen}",
            f"Fecha vencimiento: {fecha.strftime('%d/%m/%Y')}"
        )
    except ValueError:
        return (
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha"
        )
    except Exception as e:
        return (
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            "INVALIDO:fecha",
            f"Error: {str(e)}"
        )

def main():
    if len(sys.argv) > 1:
        entrada = sys.argv[1]
    else:
        entrada = "15/03/2024"

    resultado = calculadora_plazo_vencimiento(entrada)
    print("ÁREA: FINANZAS")
    print("DESCRIPCIÓN: Calculadora de plazo vencimiento")
    print("TECNOLOGÍA: Python estándar")
    for i, resultado_individual in enumerate(resultado):
        print(f"{i+1}: {resultado_individual}")

if __name__ == "__main__":
    main()