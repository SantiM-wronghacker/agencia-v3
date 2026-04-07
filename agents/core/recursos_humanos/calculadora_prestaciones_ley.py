"""
ÁREA: RECURSOS HUMANOS
DESCRIPCIÓN: Agente que realiza calculadora prestaciones ley
TECNOLOGÍA: Python estándar
"""

import sys
import math
from datetime import datetime

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_prestaciones(salario_diario, antiguedad_anios):
    try:
        # Cálculo de prima vacacional (20% del salario diario * días de vacaciones)
        dias_vacaciones = min(antiguedad_anios, 6) * 2  # Máximo 12 días
        prima_vacacional = salario_diario * dias_vacaciones * 0.20

        # Cálculo de aguinaldo (15 días de salario)
        aguinaldo = salario_diario * 15

        # Cálculo de vacaciones (días de vacaciones * salario diario)
        vacaciones = salario_diario * dias_vacaciones

        # Cálculo de indemnización (3 meses de salario)
        indemnizacion = salario_diario * 30 * 3

        # Cálculo de salario pendiente (3 meses de salario)
        salario_pendiente = salario_diario * 30 * 3

        # Cálculo de total de prestaciones
        total_prestaciones = prima_vacacional + aguinaldo + vacaciones + indemnizacion + salario_pendiente

        return {
            "prima_vacacional": round(prima_vacacional, 2),
            "aguinaldo": round(aguinaldo, 2),
            "vacaciones": round(vacaciones, 2),
            "indemnizacion": round(indemnizacion, 2),
            "salario_pendiente": round(salario_pendiente, 2),
            "total_prestaciones": round(total_prestaciones, 2)
        }
    except Exception as e:
        print(f"Error en el cálculo de prestaciones: {str(e)}")
        return None

def main():
    try:
        if len(sys.argv) < 3:
            print("Usando valores por defecto: salario diario 300 MXN, 5 años de antigüedad")
            salario_diario = 300
            antiguedad_anios = 5
        else:
            salario_diario = float(sys.argv[1])
            antiguedad_anios = float(sys.argv[2])

        resultados = calcular_prestaciones(salario_diario, antiguedad_anios)

        if resultados is not None:
            print(f"Cálculo de prestaciones para salario diario: ${salario_diario:.2f} MXN")
            print(f"Antigüedad: {antiguedad_anios} años")
            print(f"Prima vacacional: ${resultados['prima_vacacional']:.2f} MXN")
            print(f"Aguinaldo: ${resultados['aguinaldo']:.2f} MXN")
            print(f"Vacaciones: ${resultados['vacaciones']:.2f} MXN")
            print(f"Indemnización: ${resultados['indemnizacion']:.2f} MXN")
            print(f"Salario pendiente: ${resultados['salario_pendiente']:.2f} MXN")
            print(f"Total de prestaciones: ${resultados['total_prestaciones']:.2f} MXN")
            print(f"Fecha de cálculo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("Resumen ejecutivo:")
            print(f"El total de prestaciones para un empleado con {antiguedad_anios} años de antigüedad y un salario diario de ${salario_diario:.2f} MXN es de ${resultados['total_prestaciones']:.2f} MXN.")
    except Exception as e:
        print(f"Error en la ejecución del programa: {str(e)}")

if __name__ == "__main__":
    main()