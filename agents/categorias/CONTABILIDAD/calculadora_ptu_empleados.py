"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora ptu empleados
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcula_ptu(salario_diario, dias_trabajados, dias_incapacidad=0):
    if dias_trabajados <= 0:
        return 0
    dias_efectivos = max(0, dias_trabajados - dias_incapacidad)
    ptu = salario_diario * dias_efectivos * 0.0925
    return ptu

def calcula_isr(salario_diario, dias_trabajados, dias_incapacidad=0):
    dias_efectivos = max(0, dias_trabajados - dias_incapacidad)
    subtotal = salario_diario * dias_efectivos
    if subtotal <= 4160:
        return 0
    elif subtotal <= 6240:
        return subtotal * 0.10
    elif subtotal <= 8640:
        return subtotal * 0.15
    elif subtotal <= 12000:
        return subtotal * 0.20
    elif subtotal <= 15000:
        return subtotal * 0.25
    else:
        return subtotal * 0.30

def calcula_imss(salario_diario, dias_trabajados, dias_incapacidad=0):
    dias_efectivos = max(0, dias_trabajados - dias_incapacidad)
    subtotal = salario_diario * dias_efectivos
    if subtotal <= 4160:
        return 0
    elif subtotal <= 6240:
        return subtotal * 0.04
    elif subtotal <= 8640:
        return subtotal * 0.05
    elif subtotal <= 12000:
        return subtotal * 0.06
    elif subtotal <= 15000:
        return subtotal * 0.07
    else:
        return subtotal * 0.08

def calcula_descuento(salario_diario, dias_trabajados, dias_incapacidad=0):
    dias_efectivos = max(0, dias_trabajados - dias_incapacidad)
    subtotal = salario_diario * dias_efectivos
    return subtotal * 0.10

def main():
    try:
        salario_diario = float(sys.argv[1]) if len(sys.argv) > 1 else 500.0
        dias_trabajados = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        dias_incapacidad = int(sys.argv[3]) if len(sys.argv) > 3 else 0

        if salario_diario <= 0 or dias_trabajados < 0 or dias_incapacidad < 0:
            raise ValueError("Valores no válidos")

        ptu = calcula_ptu(salario_diario, dias_trabajados, dias_incapacidad)
        isr = calcula_isr(salario_diario, dias_trabajados, dias_incapacidad)
        imss = calcula_imss(salario_diario, dias_trabajados, dias_incapacidad)
        descuento = calcula_descuento(salario_diario, dias_trabajados, dias_incapacidad)
        subtotal = salario_diario * dias_trabajados
        total = subtotal - isr - imss - descuento

        print(f"ÁREA: FINANZAS")
        print(f"DESCRIPCIÓN: Agente que realiza calculadora ptu empleados")
        print(f"TECNOLOGÍA: Python estándar")
        print(f"Salario diario: ${salario_diario:.2f}")
        print(f"Días trabajados: {dias_trabajados}")
        print(f"Días incapacidades: {dias_incapacidad}")
        print(f"PTU: ${ptu:.2f}")
        print(f"ISR: ${isr:.2f}")
        print(f"IMSS: ${imss:.2f}")
        print(f"Descuento: ${descuento:.2f}")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Total: ${total:.2f}")
        print(f"Resumen ejecutivo: El total es la suma de la cantidad total de dinero que se gana menos los impuestos y descuentos.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()