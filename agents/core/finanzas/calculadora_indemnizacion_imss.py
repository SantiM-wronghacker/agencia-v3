"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora de indemnización IMSS
TECNOLOGÍA: Python estándar
"""

import sys
import math
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_indemnizacion(salario_diario, anos_trabajados):
    """Calcula la indemnización IMSS según la ley mexicana con ajustes por antigüedad."""
    if anos_trabajados < 0:
        raise ValueError("Años trabajados no pueden ser negativos")
    if anos_trabajados < 1:
        return 0

    # Ajuste por antigüedad (20% adicional por cada año después del primero)
    factor_antiguedad = 1 + min(0.2, 0.02 * (anos_trabajados - 1))

    if anos_trabajados <= 15:
        indemnizacion_base = salario_diario * 90 * anos_trabajados * factor_antiguedad
    else:
        indemnizacion_base = salario_diario * 90 * 15 * factor_antiguedad + salario_diario * 20 * (anos_trabajados - 15) * factor_antiguedad

    # Impuestos y deducciones
    try:
        impuestos = indemnizacion_base * 0.15
    except ZeroDivisionError:
        impuestos = 0
    try:
        deducciones = indemnizacion_base * 0.05
    except ZeroDivisionError:
        deducciones = 0

    indemnizacion_final = indemnizacion_base - impuestos + deducciones

    # Convertir a meses y años
    meses = (indemnizacion_final / 30)
    anos = math.floor(meses / 12)
    meses = meses % 12

    # Calcula el monto diario
    monto_diario = indemnizacion_final / anos_trabajados

    # Calcula el porcentaje de aumento por antigüedad
    porcentaje_aumento = (factor_antiguedad - 1) * 100

    return indemnizacion_base, impuestos, deducciones, indemnizacion_final, anos, meses, monto_diario, porcentaje_aumento

def main():
    try:
        if len(sys.argv) < 3:
            print("Falta de argumentos. Uso: calculadora_indemnizacion_imss.py [salario_diario] [anos_trabajados]")
            sys.exit(1)
        salario_diario = float(sys.argv[1])
        anos_trabajados = float(sys.argv[2])
    except ValueError:
        print("Error de formato en los argumentos. Uso: calculadora_indemnizacion_imss.py [salario_diario] [anos_trabajados]")
        sys.exit(1)

    if salario_diario <= 0:
        print("El salario diario no puede ser 0 o negativo.")
        sys.exit(1)

    try:
        indemnizacion_base, impuestos, deducciones, indemnizacion_final, anos, meses, monto_diario, porcentaje_aumento = calcular_indemnizacion(salario_diario, anos_trabajados)
    except ValueError as e:
        print(str(e))
        sys.exit(1)

    print("Indemnización base: $", round(indemnizacion_base, 2))
    print("Impuestos: $", round(impuestos, 2))
    print("Deducciones: $", round(deducciones, 2))
    print("Indemnización final: $", round(indemnizacion_final, 2))
    print("Años: ", anos)
    print("Meses: ", meses)
    print("Monto diario: $", round(monto_diario, 2))
    print("Porcentaje de aumento por antigüedad: ", round(porcentaje_aumento, 2), "%")

    print("\nResumen ejecutivo:")
    print("La indemnización final es de $", round(indemnizacion_final, 2), "y se calcula con un aumento del", round(porcentaje_aumento, 2), "% debido a la antigüedad.")

if __name__ == "__main__":
    main()