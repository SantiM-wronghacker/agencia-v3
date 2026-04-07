"""
ÁREA: RESTAURANTES
DESCRIPCIÓN: Agente que realiza calculadora punto equilibrio restaurante
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcular_punto_equilibrio(ventas_diarias, costo_fijo, costo_variable):
    punto_equilibrio = (costo_fijo / (1 - (costo_variable / 100)))
    return punto_equilibrio

def calcular_dias_equilibrio(punto_equilibrio, ventas_diarias):
    return math.ceil(punto_equilibrio / ventas_diarias)

def calcular_margen_contribucion(ventas_diarias, costo_variable):
    return ventas_diarias * (1 - (costo_variable / 100))

def calcular_costo_total(costo_fijo, costo_variable, ventas_diarias):
    return costo_fijo + (costo_variable / 100) * ventas_diarias

def calcular_tasa_rentabilidad(margen_contribucion, costo_fijo):
    if costo_fijo == 0:
        return 0
    return (margen_contribucion / costo_fijo) * 100

def calcular_tiempo_recuperacion_inversion(costo_fijo, margen_contribucion):
    if margen_contribucion == 0:
        return float('inf')
    return costo_fijo / margen_contribucion

def main():
    try:
        ventas_diarias = float(sys.argv[1]) if len(sys.argv) > 1 else 5000.0  # Ventas diarias promedio en pesos mexicanos
        costo_fijo = float(sys.argv[2]) if len(sys.argv) > 2 else 20000.0  # Costo fijo mensual en pesos mexicanos
        costo_variable = float(sys.argv[3]) if len(sys.argv) > 3 else 50.0  # Costo variable como porcentaje de las ventas

        punto_equilibrio = calcular_punto_equilibrio(ventas_diarias, costo_fijo, costo_variable)
        dias_equilibrio = calcular_dias_equilibrio(punto_equilibrio, ventas_diarias)
        margen_contribucion = calcular_margen_contribucion(ventas_diarias, costo_variable)
        costo_total = calcular_costo_total(costo_fijo, costo_variable, ventas_diarias)
        tasa_rentabilidad = calcular_tasa_rentabilidad(margen_contribucion, costo_fijo)
        tiempo_recuperacion_inversion = calcular_tiempo_recuperacion_inversion(costo_fijo, margen_contribucion)

        print(f"Ventas diarias promedio: {ventas_diarias} pesos mexicanos")
        print(f"Costo fijo mensual: {costo_fijo} pesos mexicanos")
        print(f"Costo variable: {costo_variable}% de las ventas")
        print(f"Punto de equilibrio: {punto_equilibrio} pesos mexicanos")
        print(f"Días para alcanzar el punto de equilibrio: {dias_equilibrio} días")
        print(f"Margen de contribución: {margen_contribucion} pesos mexicanos")
        print(f"Costo total: {costo_total} pesos mexicanos")
        print(f"Tasa de rentabilidad: {tasa_rentabilidad}%")
        print(f"Tiempo de recuperación de la inversión: {tiempo_recuperacion_inversion} días")
        print("Resumen ejecutivo:")
        print(f"El punto de equilibrio se alcanzará en {dias_equilibrio} días, con un margen de contribución de {margen_contribucion} pesos mexicanos y una tasa de rentabilidad del {tasa_rentabilidad}%. El tiempo de recuperación de la inversión es de {tiempo_recuperacion_inversion} días.")
    except ValueError:
        print("Error: Los parámetros deben ser números.")
    except ZeroDivisionError:
        print("Error: No se puede dividir por cero.")

if __name__ == "__main__":
    main()