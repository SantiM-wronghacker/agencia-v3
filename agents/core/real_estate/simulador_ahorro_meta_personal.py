import sys
import json
import datetime
import math

# ARCHIVO: simulador_ahorro_meta_personal.py
# AREA: REAL ESTATE
# DESCRIPCION: Agente que realiza simulador ahorro meta personal
# TECNOLOGIA: Python

def main():
    try:
        meta = float(sys.argv[1]) if len(sys.argv) > 1 else 100000.0
        ahorro_mensual = float(sys.argv[2]) if len(sys.argv) > 2 else 5000.0
        tasa_interes = float(sys.argv[3]) if len(sys.argv) > 3 else 0.04
        tiempo_ahorro = float(sys.argv[4]) if len(sys.argv) > 4 else 12.0

        if meta <= 0 or ahorro_mensual <= 0 or tasa_interes <= 0 or tiempo_ahorro <= 0:
            raise ValueError("Los valores de meta, ahorro mensual, tasa de interés y tiempo de ahorro deben ser mayores que cero.")

        if tasa_interes < 0 or tasa_interes > 1:
            raise ValueError("La tasa de interés debe estar entre 0 y 1.")

        if tiempo_ahorro < 1:
            raise ValueError("El tiempo de ahorro debe ser al menos 1 mes.")

        monto_total = 0.0
        meses = 0
        intereses_ganados = 0.0
        while monto_total < meta:
            monto_total += ahorro_mensual
            interes_mensual = (monto_total * tasa_interes) / 12.0
            monto_total += interes_mensual
            intereses_ganados += interes_mensual
            meses += 1

        print(f"Meta de ahorro: ${meta:.2f}")
        print(f"Ahorro mensual: ${ahorro_mensual:.2f}")
        print(f"Tasa de interés: {tasa_interes*100:.2f}%")
        print(f"Tiempo de ahorro estimado: {math.ceil(meses)} meses")
        print(f"Monto total ahorrado: ${monto_total:.2f}")
        print(f"Intereses ganados: ${intereses_ganados:.2f}")
        print(f"Fecha estimada de logro de meta: {(datetime.date.today() + datetime.timedelta(days=math.ceil(meses)*30)).strftime('%d/%m/%Y')}")
        print(f"Total de ahorro mensual realizado: ${ahorro_mensual * math.ceil(meses):.2f}")
        print(f"Porcentaje de intereses ganados sobre el monto total: {(intereses_ganados / monto_total) * 100:.2f}%")
        print(f"Cuota mensual de intereses: ${interes_mensual:.2f}")
        print(f"Monto total de intereses pagados: ${intereses_ganados:.2f}")
        print(f"Fecha de inicio del ahorro: {(datetime.date.today() - datetime.timedelta(days=math.ceil(meses)*30)).strftime('%d/%m/%Y')}")
        print(f"Fecha de logro de meta: {(datetime.date.today() + datetime.timedelta(days=math.ceil(meses)*30)).strftime('%d/%m/%Y')}")

        print("\nResumen Ejecutivo:")
        print(f"El objetivo de ahorro es de ${meta:.2f} y se espera alcanzarlo en {math.ceil(meses)} meses.")
        print(f"El monto total ahorrado será de ${monto_total:.2f} y se ganarán ${intereses_ganados:.2f} en intereses.")
        print(f"La fecha estimada de logro de meta es {(datetime.date.today() + datetime.timedelta(days=math.ceil(meses)*30)).strftime('%d/%m/%Y')}.")

    except IndexError:
        print("Falta de argumentos. Por favor, ingrese la meta, el ahorro mensual, la tasa de interés y el tiempo de ahorro como argumentos.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()