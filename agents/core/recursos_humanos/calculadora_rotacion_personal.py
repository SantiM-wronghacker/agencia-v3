"""
ÁREA: RECURSOS HUMANOS
DESCRIPCIÓN: Agente que realiza calculadora rotacion personal
TECNOLOGÍA: Python estándar
"""

import sys
import json
from datetime import datetime

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_rotacion_personal(meses_trabajadores=12, trabajadores_inicial=100, trabajadores_final=95, bajas=5):
    """
    Calcula la rotación de personal en un periodo dado.
    """
    try:
        rotacion = (bajas / ((trabajadores_inicial + trabajadores_final) / 2)) * 100
        return round(rotacion, 2)
    except ZeroDivisionError:
        return 0

def calcular_costo_rotacion(rotacion, trabajadores_inicial, trabajadores_final, bajas):
    """
    Calcula el costo de la rotación de personal.
    """
    try:
        costo_rotacion = (bajas / ((trabajadores_inicial + trabajadores_final) / 2)) * 100 * 5000  # costo promedio de reemplazo de un trabajador en México
        return round(costo_rotacion, 2)
    except ZeroDivisionError:
        return 0

def calcular_tiempo_promedio_rotacion(trabajadores_inicial, trabajadores_final, bajas):
    """
    Calcula el tiempo promedio de rotación de personal.
    """
    try:
        tiempo_promedio = (trabajadores_inicial - trabajadores_final) / bajas
        return round(tiempo_promedio, 2)
    except ZeroDivisionError:
        return 0

def main():
    try:
        # Configuración por defecto
        meses_trabajadores = 12
        trabajadores_inicial = 100
        trabajadores_final = 95
        bajas = 5

        # Procesar argumentos
        if len(sys.argv) > 1:
            try:
                trabajadores_inicial = int(sys.argv[1])
                trabajadores_final = int(sys.argv[2])
                bajas = int(sys.argv[3])
            except (ValueError, IndexError):
                pass

        # Cálculo
        rotacion = calcular_rotacion_personal(meses_trabajadores, trabajadores_inicial, trabajadores_final, bajas)
        costo_rotacion = calcular_costo_rotacion(rotacion, trabajadores_inicial, trabajadores_final, bajas)
        tiempo_promedio_rotacion = calcular_tiempo_promedio_rotacion(trabajadores_inicial, trabajadores_final, bajas)

        # Resultados
        print("=== REPORTE DE ROTACIÓN DE PERSONAL ===")
        print(f"Trabajadores iniciales: {trabajadores_inicial}")
        print(f"Trabajadores finales: {trabajadores_final}")
        print(f"Bajas en el periodo: {bajas}")
        print(f"Rotación mensual: {rotacion}%")
        print(f"Costo de la rotación: ${costo_rotacion}")
        print(f"Tiempo promedio de rotación: {tiempo_promedio_rotacion} meses")
        print(f"Fecha de cálculo: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Meses de trabajo: {meses_trabajadores}")
        print("=== RESUMEN EJECUTIVO ===")
        print(f"La rotación de personal es de {rotacion}%, lo que implica un costo de ${costo_rotacion} y un tiempo promedio de rotación de {tiempo_promedio_rotacion} meses.")

    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")

if __name__ == "__main__":
    main()