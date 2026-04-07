"""
ÁREA: TECNOLOGÍA
DESCRIPCIÓN: Agente que realiza calculadora roi automatizacion
TECNOLOGÍA: Python estándar
"""

import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_roi(inversion, ahorro_anual, anos, tasa_descuento=0.05):
    try:
        inversion = float(inversion)
        ahorro_anual = float(ahorro_anual)
        anos = int(anos)
    except ValueError:
        return None

    if inversion <= 0 or ahorro_anual <= 0 or anos <= 0:
        return None

    flujo_caja = ahorro_anual * anos
    valor_futuro = 0
    for i in range(anos):
        valor_futuro += ahorro_anual / (1 + tasa_descuento) ** (i + 1)
    roi = (valor_futuro - inversion) / inversion * 100
    return round(roi, 2)

def calcular_tiempo_recuperacion(inversion, ahorro_anual):
    try:
        inversion = float(inversion)
        ahorro_anual = float(ahorro_anual)
    except ValueError:
        return None

    if inversion <= 0 or ahorro_anual <= 0:
        return None

    return math.ceil(inversion / ahorro_anual)

def calcular_valor_futuro(inversion, ahorro_anual, anos, tasa_descuento=0.05):
    try:
        inversion = float(inversion)
        ahorro_anual = float(ahorro_anual)
        anos = int(anos)
    except ValueError:
        return None

    if inversion <= 0 or ahorro_anual <= 0 or anos <= 0:
        return None

    valor_futuro = 0
    for i in range(anos):
        valor_futuro += ahorro_anual / (1 + tasa_descuento) ** (i + 1)
    return round(valor_futuro + inversion, 2)

def main():
    try:
        args = sys.argv[1:]
        inversion = args[0] if len(args) > 0 else "50000"
        ahorro_anual = args[1] if len(args) > 1 else "10000"
        anos = args[2] if len(args) > 2 else "3"

        roi = calcular_roi(inversion, ahorro_anual, anos)
        tiempo_recuperacion = calcular_tiempo_recuperacion(inversion, ahorro_anual)
        valor_futuro = calcular_valor_futuro(inversion, ahorro_anual, anos)

        if roi is None or tiempo_recuperacion is None or valor_futuro is None:
            print("Error: Parámetros inválidos. Uso: python calculadora_roi_automatizacion.py [inversión] [ahorro_anual] [años]")
            print("Ejemplo: python calculadora_roi_automatizacion.py 50000 10000 3")
            return

        print(f"Inversión inicial: ${inversion}")
        print(f"Ahorro anual: ${ahorro_anual}")
        print(f"Años de retorno: {anos}")
        print(f"Valor futuro (con 5% de descuento): ${valor_futuro}")
        print(f"ROI: {roi}%")
        print(f"Tiempo de recuperación: {tiempo_recuperacion} años")
        print(f"Flujo de caja anual: ${ahorro_anual}")
        print(f"Flujo de caja total: ${int(ahorro_anual) * int(anos)}")
        print(f"Tasa de descuento: 5%")
        print("Resumen ejecutivo:")
        print(f"La inversión de ${inversion} durante {anos} años, con un ahorro anual de ${ahorro_anual}, generará un ROI de {roi}% y un valor futuro de ${valor_futuro}. El tiempo de recuperación de la inversión es de {tiempo_recuperacion} años.")

    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()