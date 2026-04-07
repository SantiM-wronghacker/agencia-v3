# AREA: FINANZAS
# DESCRIPCION: Agente que realiza calculadora afore retiro
# TECNOLOGIA: Python estándar

import sys
import math
import datetime

def calcular_aportacion_mensual(salario, aportacion):
    return salario * aportacion / 12

def calcular_ahorro_proyectado(aportacion_mensual, tasa_interes, años):
    ahorro_actual = 0.0
    for año in range(años):
        ahorro_actual = (ahorro_actual + aportacion_mensual * 12) * (1 + tasa_interes)
    return ahorro_actual

def calcular_total_aportaciones(aportacion_mensual, años):
    return aportacion_mensual * 12 * años

def calcular_total_intereses_ganados(ahorro_proyectado, total_aportaciones):
    return ahorro_proyectado - total_aportaciones

def calcular_cantidad_retiro(ahorro_proyectado, años_retiro):
    return ahorro_proyectado / años_retiro

def calcular_cantidad_mensual_retiro(cantidad_retiro, años_retiro):
    return cantidad_retiro / años_retiro

def main():
    try:
        edad = int(sys.argv[1]) if len(sys.argv) > 1 else 30
        salario = float(sys.argv[2]) if len(sys.argv) > 2 else 15000.0
        aportacion = float(sys.argv[3]) if len(sys.argv) > 3 else 0.065
        tasa_interes = float(sys.argv[4]) if len(sys.argv) > 4 else 0.04
        años_retiro = int(sys.argv[5]) if len(sys.argv) > 5 else 25

        if edad < 0 or salario < 0 or aportacion < 0 or tasa_interes < 0 or años_retiro < 0:
            raise ValueError("Los valores no pueden ser negativos")

        if aportacion > 1:
            raise ValueError("La aportación no puede ser mayor a 1")

        if tasa_interes > 0.1:
            raise ValueError("La tasa de interés no puede ser mayor a 10%")

        if años_retiro > 50:
            raise ValueError("El número de años hasta el retiro no puede ser mayor a 50")

        aportacion_mensual = calcular_aportacion_mensual(salario, aportacion)
        ahorro_proyectado = calcular_ahorro_proyectado(aportacion_mensual, tasa_interes, años_retiro)
        total_aportaciones = calcular_total_aportaciones(aportacion_mensual, años_retiro)
        total_intereses_ganados = calcular_total_intereses_ganados(ahorro_proyectado, total_aportaciones)
        cantidad_retiro = calcular_cantidad_retiro(ahorro_proyectado, años_retiro)
        cantidad_mensual_retiro = calcular_cantidad_mensual_retiro(cantidad_retiro, años_retiro)

        print(f"Área: FINANZAS")
        print(f"Descripción: Agente que realiza calculadora afore retiro")
        print(f"Tecnología: Python estándar")
        print(f"Edad actual: {edad} años")
        print(f"Edad de retiro: {edad + años_retiro} años")
        print(f"Salario: ${salario:.2f}")
        print(f"Aplicación de aportación: {aportacion * 100}%")
        print(f"Tasa de interés: {tasa_interes * 100}%")
        print(f"Años hasta el retiro: {años_retiro}")
        print(f"Aportación mensual: ${aportacion_mensual:.2f}")
        print(f"Ahorro proyectado: ${ahorro_proyectado:.2f}")
        print(f"Total de aportaciones: ${total_aportaciones:.2f}")
        print(f"Total de intereses ganados: ${total_intereses_ganados:.2f}")
        print(f"Cantidad de retiro: ${cantidad_retiro:.2f}")
        print(f"Cantidad mensual de retiro: ${cantidad_mensual_retiro:.2f}")
        print(f"Resumen ejecutivo: El cálculo anterior muestra la cantidad de dinero que se aportará mensualmente y la cantidad total de dinero que se habrá aportado hasta el retiro.")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()