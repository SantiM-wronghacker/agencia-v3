"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora costo empleado mexico
TECNOLOGÍA: Python estándar
"""

import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_costo_empleado(salario_base, horas_trabajadas, dias_trabajados, bonificacion=0):
    if salario_base <= 0 or horas_trabajadas <= 0 or dias_trabajados <= 0:
        raise ValueError("Los valores de salario base, horas trabajadas y días trabajados deben ser mayores que cero.")

    if salario_base < 1000:
        salario_diario = salario_base / 30
    else:
        salario_diario = salario_base / 25

    if horas_trabajadas > 8:
        horas_extra = horas_trabajadas - 8
        costo_por_hora = (salario_diario * 1.5) / 8
    else:
        costo_por_hora = salario_diario / 8

    subtotal = costo_por_hora * horas_trabajadas * dias_trabajados
    impuesto = subtotal * 0.16  # 16% de impuesto
    seguro_social = subtotal * 0.11  # 11% de seguro social
    infonavit = subtotal * 0.05  # 5% de infonavit
    total = subtotal + impuesto + seguro_social + infonavit + bonificacion

    # Calculo de otros impuestos y beneficios
    isr = subtotal * 0.025  # 2.5% de ISR
    imss = subtotal * 0.11  # 11% de IMSS
    total_imss = imss + infonavit
    total_isr = subtotal + isr

    if dias_trabajados > 30:
        dias_adicionales = dias_trabajados - 30
        subtotal_adicionales = costo_por_hora * horas_trabajadas * dias_adicionales
        total += subtotal_adicionales

    return subtotal, impuesto, seguro_social, infonavit, total, isr, imss, total_imss, total_isr

def main():
    if len(sys.argv) < 5:
        print("Uso: python calculadora_costo_empleado_mexico.py <salario_base> <horas_trabajadas> <dias_trabajados> <bonificacion>")
        sys.exit(1)

    try:
        salario_base = float(sys.argv[1])
        horas_trabajadas = float(sys.argv[2])
        dias_trabajados = float(sys.argv[3])
        bonificacion = float(sys.argv[4])
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        subtotal, impuesto, seguro_social, infonavit, total, isr, imss, total_imss, total_isr = calcular_costo_empleado(salario_base, horas_trabajadas, dias_trabajados, bonificacion)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Resumen de costo del empleado:")
    print(f"Salario base: ${salario_base:.2f}")
    print(f"Horas trabajadas: {horas_trabajadas} horas")
    print(f"Días trabajados: {dias_trabajados} días")
    print(f"Bonificación: ${bonificacion:.2f}")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Impuesto: ${impuesto:.2f}")
    print(f"Seguro social: ${seguro_social:.2f}")
    print(f"Infonavit: ${infonavit:.2f}")
    print(f"Total: ${total:.2f}")
    print(f"ISR: ${isr:.2f}")
    print(f"IMSS: ${imss:.2f}")
    print(f"Total IMSS: ${total_imss:.2f}")
    print(f"Total ISR: ${total_isr:.2f}")
    print(f"Resumen ejecutivo: El costo total del empleado es de ${total:.2f}, lo que incluye un subtotal de ${subtotal:.2f}, un impuesto de ${impuesto:.2f} y un seguro social de ${seguro_social:.2f}.")

if __name__ == "__main__":
    main()