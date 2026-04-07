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

        print(f"Edad actual: {edad} años")
        print(f"Edad de retiro: {edad + años_retiro} años")
        print(f"Ahorro proyectado al retiro: ${math.floor(ahorro_proyectado)}")
        print(f"Aportación mensual: ${math.floor(aportacion_mensual)}")
        print(f"Tasa de interés anual: {tasa_interes*100}%")
        print(f"Salario mensual: ${math.floor(salario/12)}")
        print(f"Aportación anual: ${math.floor(aportacion_mensual * 12)}")
        print(f"Años hasta el retiro: {años_retiro} años")
        print(f"Total de aportaciones: ${math.floor(total_aportaciones)}")
        print(f"Total de intereses ganados: ${math.floor(total_intereses_ganados)}")
        print(f"Retiro mensual proyectado: ${math.floor(ahorro_proyectado / años_retiro)}")
        print(f"Resumen ejecutivo: El usuario tiene un ahorro proyectado de ${math.floor(ahorro_proyectado)} al retiro, con un total de aportaciones de ${math.floor(total_aportaciones)} y un total de intereses ganados de ${math.floor(total_intereses_ganados)}")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()