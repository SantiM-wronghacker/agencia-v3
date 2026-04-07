"""
ÁREA: FINANZAS
DESCRIPCIÓN: Calculadora de ROI para propiedades inmobiliarias
TECNOLOGÍA: Python
"""

import sys
import math

class CalculadoraROI:
    def __init__(self, precio_compra, gastos_iniciales, alquiler_mensual, gastos_mensuales, tasa_interes_anual):
        self.precio_compra = precio_compra
        self.gastos_iniciales = gastos_iniciales
        self.alquiler_mensual = alquiler_mensual
        self.gastos_mensuales = gastos_mensuales
        self.tasa_interes_anual = tasa_interes_anual

    def calcular_roi(self):
        inversion_total = self.precio_compra + self.gastos_iniciales
        flujo_caja_anual = (self.alquiler_mensual - self.gastos_mensuales) * 12
        roi_anual = (flujo_caja_anual / inversion_total) * 100
        return roi_anual

    def calcular_flujo_caja_mensual(self):
        flujo_caja_mensual = self.alquiler_mensual - self.gastos_mensuales
        return flujo_caja_mensual

    def calcular_tiempo_recuperacion(self):
        inversion_total = self.precio_compra + self.gastos_iniciales
        flujo_caja_mensual = self.alquiler_mensual - self.gastos_mensuales
        if flujo_caja_mensual <= 0:
            return "No es posible calcular el tiempo de recuperación"
        tiempo_recuperacion = inversion_total / flujo_caja_mensual
        return tiempo_recuperacion

    def calcular_valor_actual(self):
        tasa_interes_mensual = self.tasa_interes_anual / 12
        flujo_caja_mensual = self.alquiler_mensual - self.gastos_mensuales
        valor_actual = flujo_caja_mensual / tasa_interes_mensual
        return valor_actual

def main():
    if len(sys.argv) > 1:
        try:
            precio_compra = float(sys.argv[1])
            gastos_iniciales = float(sys.argv[2])
            alquiler_mensual = float(sys.argv[3])
            gastos_mensuales = float(sys.argv[4])
            tasa_interes_anual = float(sys.argv[5]) / 100
        except ValueError:
            print("Parámetros inválidos. Utilice números reales.")
            return
    else:
        precio_compra = 2000000
        gastos_iniciales = 100000
        alquiler_mensual = 15000
        gastos_mensuales = 5000
        tasa_interes_anual = 0.095

    calculadora = CalculadoraROI(precio_compra, gastos_iniciales, alquiler_mensual, gastos_mensuales, tasa_interes_anual)

    print(f"Parámetros utilizados:")
    print(f"Precio de compra: ${precio_compra:.2f}")
    print(f"Gastos iniciales: ${gastos_iniciales:.2f}")
    print(f"Alquiler mensual: ${alquiler_mensual:.2f}")
    print(f"Gastos mensuales: ${gastos_mensuales:.2f}")
    print(f"Tasa de interés anual: {tasa_interes_anual*100:.2f}%")

    print("\nResultados:")
    print(f"ROI anual: {calculadora.calcular_roi():.2f}%")
    print(f"Flujo de caja mensual: ${calculadora.calcular_flujo_caja_mensual():.2f}")
    print(f"Tiempo de recuperación: {calculadora.calcular_tiempo_recuperacion():.2f} meses")
    print(f"Valor actual: ${calculadora.calcular_valor_actual():.2f}")

    print("\nResumen ejecutivo:")
    print(f"La inversión en la propiedad inmobiliaria tiene un ROI anual de {calculadora.calcular_roi():.2f}% y un flujo de caja mensual de ${calculadora.calcular_flujo_caja_mensual():.2f}.")
    print(f"El tiempo de recuperación de la inversión es de aproximadamente {calculadora.calcular_tiempo_recuperacion():.2f} meses.")
    print(f"El valor actual de la propiedad es de aproximadamente ${calculadora.calcular_valor_actual():.2f}.")

if __name__ == "__main__":
    main()