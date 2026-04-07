import os
import sys
import math

def calcular_concreto(peso_concreto, precio_concreto):
    """
    Calcula el costo total del concreto.
    """
    try:
        peso_total = peso_concreto * 1000  # Convertir a gramos
        costo_total = peso_total * precio_concreto
        return costo_total
    except TypeError:
        print("Error: Los parámetros deben ser números.")
        return None
    except ValueError:
        print("Error: El precio del concreto debe ser un número positivo.")
        return None

def calcular_costo_pormetro_cuadrado(peso_concreto, precio_concreto):
    """
    Calcula el costo por metro cuadrado.
    """
    try:
        metros_cuadrados = 10  # Asumir 10 metros cuadrados por bulto
        costo_total = calcular_concreto(peso_concreto, precio_concreto)
        if costo_total is not None:
            return costo_total / metros_cuadrados
        else:
            return None
    except TypeError:
        return None

def calcular_costo_pormetro_lineal(peso_concreto, precio_concreto):
    """
    Calcula el costo por metro lineal.
    """
    try:
        metros_lineales = 20  # Asumir 20 metros lineales por bulto
        costo_total = calcular_concreto(peso_concreto, precio_concreto)
        if costo_total is not None:
            return costo_total / metros_lineales
        else:
            return None
    except TypeError:
        return None

def calcular_costo_pormetro_cúbico(peso_concreto, precio_concreto):
    """
    Calcula el costo por metro cúbico.
    """
    try:
        metros_cúbicos = 0.5  # Asumir 0.5 metros cúbicos por bulto
        costo_total = calcular_concreto(peso_concreto, precio_concreto)
        if costo_total is not None:
            return costo_total / metros_cúbicos
        else:
            return None
    except TypeError:
        return None

def main():
    if __name__ == "__main__":
        try:
            if len(sys.argv) != 4:
                print("Error: Faltan parámetros. Ejemplo: python calculadora_concreto.py 250 50 10")
                sys.exit(1)
            precio_concreto = float(sys.argv[1])
            peso_concreto = float(sys.argv[2])
            metros_cuadrados = float(sys.argv[3])

            # Realizar cálculos
            costo_total = calcular_concreto(peso_concreto, precio_concreto)
            costo_pormetro_cuadrado = calcular_costo_pormetro_cuadrado(peso_concreto, precio_concreto)
            costo_pormetro_lineal = calcular_costo_pormetro_lineal(peso_concreto, precio_concreto)
            costo_pormetro_cúbico = calcular_costo_pormetro_cúbico(peso_concreto, precio_concreto)

            # Mostrar resultados
            print("ÁREA: FINANZAS")
            print("DESCRIPCIÓN: Calculadora de concreto")
            print("TECNOLOGÍA: Python")
            print("Peso del concreto: {:.2f} kg".format(peso_concreto))
            print("Precio del concreto: ${:.2f}".format(precio_concreto))
            print("Metros cuadrados: {:.2f}".format(metros_cuadrados))
            print("Costo total: ${:.2f}".format(costo_total))
            print("Costo por metro cuadrado: ${:.2f}".format(costo_pormetro_cuadrado))
            print("Costo por metro lineal: ${:.2f}".format(costo_pormetro_lineal))
            print("Costo por metro cúbico: ${:.2f}".format(costo_pormetro_cúbico))
            print("Resumen ejecutivo: La calculadora de concreto proporciona información precisa sobre el costo del concreto.")
        except ValueError:
            print("Error: Los parámetros deben ser números.")

if __name__ == "__main__":
    main()