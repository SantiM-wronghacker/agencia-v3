# FINANZAS / Calculadora de Enganche de Credito Infonavit / Python
# AREA: FINANZAS
# DESCRIPCION: Agente que realiza calculadora enganche credito infonavit
# TECNOLOGIA: Python

import sys
import math

def calcula_enganche(sueldo, antiguedad, precio_casa):
    try:
        if sueldo <= 10000:
            enganche = precio_casa * 0.1
        elif sueldo <= 20000:
            enganche = precio_casa * 0.12
        else:
            enganche = precio_casa * 0.15
        if antiguedad >= 5:
            enganche *= 0.9
        if antiguedad >= 10:
            enganche *= 0.85
        if antiguedad >= 15:
            enganche *= 0.8
        if antiguedad >= 20:
            enganche *= 0.75
        return enganche
    except ValueError:
        print("Error: Sueldo o antiguedad no es un número")
        return 0
    except Exception as e:
        print(f"Error al calcular el enganche: {e}")
        return 0

def calcula_credito_infonavit(precio_casa, enganche):
    return precio_casa - enganche

def calcula_cuota_mensual(credito_infonavit, tasa_interes, plazo_credito):
    return credito_infonavit * (tasa_interes / 12) * (1 + tasa_interes / 12) ** (plazo_credito * 12) / ((1 + tasa_interes / 12) ** (plazo_credito * 12) - 1)

def calcula_total_a_pagar(credito_infonavit, tasa_interes, plazo_credito):
    return credito_infonavit + (credito_infonavit * tasa_interes * plazo_credito)

def calcula_intereses_totales(credito_infonavit, tasa_interes, plazo_credito):
    return credito_infonavit * tasa_interes * plazo_credito

def main():
    try:
        sueldo = float(sys.argv[1]) if len(sys.argv) > 1 else 15000
        antiguedad = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        precio_casa = float(sys.argv[3]) if len(sys.argv) > 3 else 500000
        tasa_interes = float(sys.argv[4]) if len(sys.argv) > 4 else 0.07
        plazo_credito = int(sys.argv[5]) if len(sys.argv) > 5 else 20
        enganche = calcula_enganche(sueldo, antiguedad, precio_casa)
        credito_infonavit = calcula_credito_infonavit(precio_casa, enganche)
        cuota_mensual = calcula_cuota_mensual(credito_infonavit, tasa_interes, plazo_credito)
        total_a_pagar = calcula_total_a_pagar(credito_infonavit, tasa_interes, plazo_credito)
        intereses_totales = calcula_intereses_totales(credito_infonavit, tasa_interes, plazo_credito)
        print(f"Sueldo: {sueldo}")
        print(f"Antiguedad: {antiguedad} años")
        print(f"Precio de la casa: ${precio_casa}")
        print(f"Enganche: ${enganche}")
        print(f"Credito Infonavit: ${credito_infonavit}")
        print(f"Cuota mensual: ${cuota_mensual:.2f}")
        print(f"Total a pagar: ${total_a_pagar:.2f}")
        print(f"Intereses totales: ${intereses_totales:.2f}")
        print(f"Resumen ejecutivo: El cliente puede financiar una casa de ${precio_casa} con un enganche de ${enganche} y un credito de ${credito_infonavit}. La cuota mensual es de ${cuota_mensual:.2f} y el total a pagar es de ${total_a_pagar:.2f}. Los intereses totales ascienden a ${intereses_totales:.2f}.")
    except ValueError:
        print("Error: Los valores ingresados no son números")
    except Exception as e:
        print(f"Error al calcular los valores: {e}")

if __name__ == "__main__":
    main()