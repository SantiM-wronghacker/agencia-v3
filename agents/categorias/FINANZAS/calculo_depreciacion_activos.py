"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza cálculo de depreciación de activos con metodología mexicana
TECNOLOGÍA: Python estándar
"""

import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calculo_depreciacion(valor_inicial, vida_util, anios_transcurridos, metodo="lineal"):
    if metodo == "lineal":
        depreciacion_acumulada = valor_inicial * (anios_transcurridos / vida_util)
    elif metodo == "diminucion_saldo":
        depreciacion_acumulada = 0
        for anio in range(1, anios_transcurridos + 1):
            valor_anterior = valor_inicial - depreciacion_acumulada
            depreciacion_anual = valor_anterior * (2 / vida_util)
            depreciacion_acumulada += depreciacion_anual
    else:
        raise ValueError("Método de depreciación no válido")

    return depreciacion_acumulada

def main():
    try:
        if len(sys.argv) < 4:
            raise ValueError("Faltan parámetros. Uso: python calculo_depreciacion_activos.py <valor_inicial> <vida_util> <anios_transcurridos> [metodo]")

        valor_inicial = float(sys.argv[1])
        vida_util = int(sys.argv[2])
        anios_transcurridos = int(sys.argv[3])
        metodo = sys.argv[4] if len(sys.argv) > 4 else "lineal"

        if vida_util <= 0:
            raise ValueError("La vida útil debe ser mayor que cero")

        if anios_transcurridos < 0:
            raise ValueError("Los años transcurridos no pueden ser negativos")

        if anios_transcurridos > vida_util:
            raise ValueError("Los años transcurridos no pueden superar la vida útil")

        depreciacion_acumulada = calculo_depreciacion(valor_inicial, vida_util, anios_transcurridos, metodo)
        valor_actual = valor_inicial - depreciacion_acumulada
        tasa_depreciacion_anual = (depreciacion_acumulada / anios_transcurridos) if anios_transcurridos > 0 else 0
        porcentaje_depreciacion = (depreciacion_acumulada / valor_inicial) * 100 if valor_inicial > 0 else 0
        valor_residual = valor_actual if anios_transcurridos < vida_util else 0
        depreciacion_anual_promedio = depreciacion_acumulada / anios_transcurridos if anios_transcurridos > 0 else 0

        print("=== INFORME DE DEPRECIACIÓN DE ACTIVOS ===")
        print(f"Valor Inicial: ${valor_inicial:,.2f} MXN")
        print(f"Vida Útil: {vida_util} años")
        print(f"Años Transcurridos: {anios_transcurridos} años")
        print(f"Método de Depreciación: {metodo}")
        print(f"Depreciación Acumulada: ${depreciacion_acumulada:,.2f} MXN")
        print(f"Valor Actual: ${valor_actual:,.2f} MXN")
        print(f"Valor Residual: ${valor_residual:,.2f} MXN")
        print(f"Tasa Depreciación Anual: ${tasa_depreciacion_anual:,.2f} MXN")
        print(f"Porcentaje Depreciación: {porcentaje_depreciacion:.2f}%")
        print(f"Depreciación Anual Promedio: ${depreciacion_anual_promedio:,.2f} MXN")
        print(f"Resumen Ejecutivo: El activo ha depreciado un {porcentaje_depreciacion:.2f}% de su valor inicial en {anios_transcurridos} años, con una tasa de depreciación anual de ${tasa_depreciacion_anual:,.2f} MXN. El valor actual del activo es de ${valor_actual:,.2f} MXN.")
        print("=== FIN DEL INFORME ===")

    except ValueError as ve:
        print(f"Error de validación: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()