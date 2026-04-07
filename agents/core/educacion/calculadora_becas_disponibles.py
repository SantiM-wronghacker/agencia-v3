"""
ÁREA: EDUCACIÓN
DESCRIPCIÓN: Agente que realiza calculadora becas disponibles
TECNOLOGÍA: Python estándar
"""
import sys
import random
from datetime import datetime
import math

def main():
    try:
        # Parámetros por defecto
        if len(sys.argv) > 1:
            presupuesto = int(sys.argv[1])
            becas_por_estudiante = int(sys.argv[2])
            estudiantes_registrados = int(sys.argv[3])
            tasa_inflacion = float(sys.argv[4]) if len(sys.argv) > 4 else 0.03
            impuestos = float(sys.argv[5]) if len(sys.argv) > 5 else 0.10
        else:
            presupuesto = 15000000  # MXN
            becas_por_estudiante = 5000  # MXN
            estudiantes_registrados = 2000
            tasa_inflacion = 0.03
            impuestos = 0.10

        # Procesamiento
        if presupuesto <= 0 or becas_por_estudiante <= 0 or estudiantes_registrados <= 0:
            raise ValueError("Parámetros deben ser números positivos")

        becas_disponibles = math.floor(presupuesto / becas_por_estudiante)
        becas_otorgadas = min(estudiantes_registrados, becas_disponibles)
        presupuesto_restante = presupuesto - (becas_otorgadas * becas_por_estudiante)
        porcentaje_asignado = (becas_otorgadas / estudiantes_registrados) * 100
        porcentaje_presupuesto_asignado = (becas_otorgadas * becas_por_estudiante / presupuesto) * 100
        ajuste_por_inflacion = presupuesto * tasa_inflacion
        impuestos_pagados = presupuesto * impuestos
        presupuesto_real = presupuesto - impuestos_pagados - ajuste_por_inflacion

        # Salida
        print("=== REPORTE DE BECAS DISPONIBLES ===")
        print(f"Presupuesto total: ${presupuesto:,.2f} MXN")
        print(f"Becas disponibles: {becas_disponibles:,} (${becas_por_estudiante:,.2f} c/u)")
        print(f"Estudiantes beneficiados: {becas_otorgadas:,} ({porcentaje_asignado:.1f}%)")
        print(f"Presupuesto restante: ${presupuesto_restante:,.2f} MXN")
        print(f"Porcentaje de presupuesto asignado: {porcentaje_presupuesto_asignado:.1f}%")
        print(f"Fecha de cálculo: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Estudiantes no beneficiados: {estudiantes_registrados - becas_otorgadas:,} ({100 - porcentaje_asignado:.1f}%)")
        print(f"Monto total de becas: ${becas_otorgadas * becas_por_estudiante:,.2f} MXN")
        print(f"Ajuste por inflación: ${ajuste_por_inflacion:,.2f} MXN ({tasa_inflacion*100:.2f}%)")
        print(f"Impuestos pagados: ${impuestos_pagados:,.2f} MXN ({impuestos*100:.2f}%)")
        print(f"Presupuesto real: ${presupuesto_real:,.2f} MXN")
        print("=== RESUMEN EJECUTIVO ===")
        print(f"El presupuesto total es de ${presupuesto:,.2f} MXN, con un ajuste por inflación de ${ajuste_por_inflacion:,.2f} MXN y un pago de impuestos de ${impuestos_pagados:,.2f} MXN.")
        print(f"Se otorgarán becas a {becas_otorgadas:,} estudiantes, lo que representa el {porcentaje_asignado:.1f}% del total de estudiantes registrados.")
        print(f"El presupuesto restante es de ${presupuesto_restante:,.2f} MXN.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()