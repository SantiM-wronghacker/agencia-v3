"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza analizador AB test
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def analizador_ab_test(precio=100.00, conversion=20.00, unidades_vendidas=100, impuestos=0.16, depreciacion=0.05, amortizacion=0.03, costos_fijos=5000, costos_variables=0.10):
    try:
        # Calcular resultados
        ingresos = precio * unidades_vendidas
        beneficio = ingresos - (precio * conversion)
        impuestos_calculados = ingresos * impuestos  # Impuestos en México (16%)
        utilidad_neta = beneficio - impuestos_calculados
        ganancia_por_unidad = beneficio / unidades_vendidas
        margen_ganancia = (beneficio / ingresos) * 100
        rentabilidad = utilidad_neta / ingresos * 100
        depreciacion_calculada = ingresos * depreciacion  # Depreciación en México (5%)
        amortizacion_calculada = ingresos * amortizacion  # Amortización en México (3%)
        costos_variables_calculados = ingresos * costos_variables  # Costos variables en México (10%)
        utilidad_operativa = beneficio - costos_fijos - costos_variables_calculados

        # Mostrar resultados
        print(f"Precio: ${precio:.2f}")
        print(f"Tipo de cambio: ${conversion:.2f}")
        print(f"Unidades vendidas: {unidades_vendidas}")
        print(f"Ingresos: ${ingresos:.2f}")
        print(f"Beneficio: ${beneficio:.2f}")
        print(f"Impuestos: ${impuestos_calculados:.2f}")
        print(f"Utilidad neta: ${utilidad_neta:.2f}")
        print(f"Ganancia por unidad: ${ganancia_por_unidad:.2f}")
        print(f"Margen de ganancia: {margen_ganancia:.2f}%")
        print(f"Rentabilidad: {rentabilidad:.2f}%")
        print(f"Depreciación: ${depreciacion_calculada:.2f}")
        print(f"Amortización: ${amortizacion_calculada:.2f}")
        print(f"Costos fijos: ${costos_fijos:.2f}")
        print(f"Costos variables: ${costos_variables_calculados:.2f}")
        print(f"Utilidad operativa: ${utilidad_operativa:.2f}")
        print(f"Margen de ganancia por unidad: {(beneficio / unidades_vendidas) * 100:.2f}%")
        print(f"Costo de producción por unidad: {(costos_fijos + costos_variables_calculados) / unidades_vendidas:.2f}")

        # Resumen ejecutivo
        if utilidad_neta > 0:
            print("El negocio tiene una utilidad neta positiva.")
        else:
            print("El negocio tiene una utilidad neta negativa.")
        print("Recomendaciones:")
        if rentabilidad < 10:
            print("Aumentar el precio o reducir los costos.")
        elif margen_ganancia < 20:
            print("Aumentar el precio o reducir los costos.")
        elif costos_fijos > 0.1 * ingresos:
            print("Reducir los costos fijos.")
        else:
            print("El negocio está funcionando correctamente.")

    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    if len(sys.argv) > 1:
        precio = float(sys.argv[1])
        conversion = float(sys.argv[2])
        unidades_vendidas = int(sys.argv[3])
        impuestos = float(sys.argv[4])
        depreciacion = float(sys.argv[5])
        amortizacion = float(sys.argv[6])
        costos_fijos = int(sys.argv[7])
        costos_variables = float(sys.argv[8])
        analizador_ab_test(precio, conversion, unidades_vendidas, impuestos, depreciacion, amortizacion, costos_fijos, costos_variables)
    else:
        analizador_ab_test()

if __name__ == "__main__":
    main()