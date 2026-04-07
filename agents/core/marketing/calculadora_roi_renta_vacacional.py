"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora ROI renta vacacional
TECNOLOGÍA: Python estándar
"""

import sys
import math

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calculadora_roi(precio_compra, gastos_iniciales, renta_mensual, gastos_mensuales, tasa_interes):
    try:
        roi = (renta_mensual - gastos_mensuales) * 12 / (precio_compra + gastos_iniciales)
        roi_anualizado = roi * (1 + tasa_interes/100)
        return roi_anualizado
    except ZeroDivisionError:
        print("Error: No se puede realizar el cálculo debido a un denominador cero.")
        return None

def calculadora_roi_mensual(precio_compra, gastos_iniciales, renta_mensual, gastos_mensuales, tasa_interes):
    try:
        roi_mensual = (renta_mensual - gastos_mensuales) / (precio_compra + gastos_iniciales)
        return roi_mensual
    except ZeroDivisionError:
        print("Error: No se puede realizar el cálculo debido a un denominador cero.")
        return None

def calculadora_pago_anual(precio_compra, gastos_iniciales, renta_mensual, gastos_mensuales, tasa_interes):
    try:
        pago_anual = (renta_mensual - gastos_mensuales) * 12
        return pago_anual
    except TypeError:
        print("Error: Uno o más argumentos no son números.")
        return None

def main():
    try:
        precio_compra = float(sys.argv[1]) if len(sys.argv) > 1 else 2000000.0
        gastos_iniciales = float(sys.argv[2]) if len(sys.argv) > 2 else 50000.0
        renta_mensual = float(sys.argv[3]) if len(sys.argv) > 3 else 15000.0
        gastos_mensuales = float(sys.argv[4]) if len(sys.argv) > 4 else 3000.0
        tasa_interes = float(sys.argv[5]) if len(sys.argv) > 5 else 8.0

        roi_anualizado = calculadora_roi(precio_compra, gastos_iniciales, renta_mensual, gastos_mensuales, tasa_interes)
        roi_mensual = calculadora_roi_mensual(precio_compra, gastos_iniciales, renta_mensual, gastos_mensuales, tasa_interes)
        pago_anual = calculadora_pago_anual(precio_compra, gastos_iniciales, renta_mensual, gastos_mensuales, tasa_interes)

        print("ÁREA: FINANZAS")
        print("DESCRIPCIÓN: Agente que realiza calculadora ROI renta vacacional")
        print("TECNOLOGÍA: Python estándar")

        print("\nPrecio de compra: $", precio_compra)
        print("Gastos iniciales: $", gastos_iniciales)
        print("Renta mensual: $", renta_mensual)
        print("Gastos mensuales: $", gastos_mensuales)
        print("Tasa de interés: {:.2f}%".format(tasa_interes))

        if roi_anualizado is not None:
            print("\nROI anualizado: {:.2f}%".format(roi_anualizado * 100))
        if roi_mensual is not None:
            print("ROI mensual: {:.2f}%".format(roi_mensual * 100))
        if pago_anual is not None:
            print("Pago anual: $", pago_anual)

        print("\nResumen ejecutivo:")
        print("El ROI anualizado es de {:.2f}% y el ROI mensual es de {:.2f}%.".format(roi_anualizado * 100, roi_mensual * 100))
        print("El pago anual es de $", pago_anual)

    except ValueError:
        print("Error: Uno o más argumentos no son números.")
    except IndexError:
        print("Error: Faltan argumentos.")

if __name__ == "__main__":
    main()