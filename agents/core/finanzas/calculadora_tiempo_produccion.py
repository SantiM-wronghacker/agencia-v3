"""
ÁREA: OPERACIONES
DESCRIPCIÓN: Agente que realiza calculadora tiempo producción con cálculos realistas para México
TECNOLOGÍA: Python estándar
"""

import sys
import datetime
import math

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcula_tiempo_produccion(cantidad, velocidad, horas_diarias=8, dias_semanales=5):
    if velocidad <= 0:
        raise ValueError("La velocidad debe ser mayor que cero")
    if cantidad < 0:
        raise ValueError("La cantidad no puede ser negativa")
    return cantidad / velocidad

def main():
    try:
        cantidad = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
        velocidad = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        horas_diarias = float(sys.argv[3]) if len(sys.argv) > 3 else 8
        dias_semanales = int(sys.argv[4]) if len(sys.argv) > 4 else 5

        tiempo_produccion = calcula_tiempo_produccion(cantidad, velocidad, horas_diarias, dias_semanales)

        print(f"Cálculo de tiempo de producción para {cantidad} unidades")
        print(f"Velocidad de producción: {velocidad} unidades/hora")
        print(f"Horas laborales diarias: {horas_diarias} horas")
        print(f"Días laborales semanales: {dias_semanales} días")
        print(f"Tiempo total: {tiempo_produccion:.2f} horas")
        print(f"Tiempo en minutos: {tiempo_produccion * 60:.2f} minutos")
        print(f"Tiempo en días: {tiempo_produccion / horas_diarias:.2f} días")
        print(f"Tiempo en semanas: {tiempo_produccion / (horas_diarias * dias_semanales):.2f} semanas")
        print(f"Tiempo en meses (22 días laborales/mes): {tiempo_produccion / (horas_diarias * 22):.2f} meses")
        print(f"Tiempo en años (260 días laborales/año): {tiempo_produccion / (horas_diarias * 260):.2f} años")

        # Cálculos de costos con valores realistas para México
        costo_hora = 250  # Salario mínimo diario en México (2023) / 8 horas
        costo_dia = 500  # Salario mínimo diario en México (2023)
        costo_mes = 7500  # Salario mínimo mensual en México (2023)

        print(f"\nCálculo de costos de producción:")
        print(f"Costo por hora (estimado): ${costo_hora:.2f}")
        print(f"Costo total (por hora): ${tiempo_produccion * costo_hora:.2f}")
        print(f"Costo total (por día): ${(tiempo_produccion / horas_diarias) * costo_dia:.2f}")
        print(f"Costo total (por mes): ${(tiempo_produccion / (horas_diarias * 22)) * costo_mes:.2f}")

        print("\nResumen ejecutivo:")
        print(f"Para producir {cantidad} unidades a {velocidad} unidades/hora:")
        print(f"- Tiempo total estimado: {tiempo_produccion:.2f} horas ({tiempo_produccion / 24:.2f} días completos)")
        print(f"- Costo estimado: ${tiempo_produccion * costo_hora:.2f} (basado en salario mínimo)")
        print(f"- Recomendación: Considerar ajustar la velocidad de producción a {velocidad * 1.2:.0f} unidades/hora para reducir tiempo en un 20%")

    except ValueError as e:
        print(f"Error de valor: {str(e)}")
    except ZeroDivisionError as e:
        print(f"Error de división por cero: {str(e)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()