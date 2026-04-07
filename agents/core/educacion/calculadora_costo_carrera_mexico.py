#!/usr/bin/env python3

"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza cálculo de costo de carrera en México
TECNOLOGÍA: Python estándar
"""

import sys
import math
import os

def main():
    try:
        # Parámetros por defecto realistas para México
        carrera = sys.argv[1] if len(sys.argv) > 1 else "Ingeniería"
        semestres = int(sys.argv[2]) if len(sys.argv) > 2 else 8
        costo_semestre = float(sys.argv[3]) if len(sys.argv) > 3 else 25000.0  # MXN
        costo_libros = float(sys.argv[4]) if len(sys.argv) > 4 else 2000.0  # MXN
        costo_transporte = float(sys.argv[5]) if len(sys.argv) > 5 else 1500.0  # MXN
        costo_alojamiento = float(sys.argv[6]) if len(sys.argv) > 6 else 8000.0  # MXN
        costo_comida = float(sys.argv[7]) if len(sys.argv) > 7 else 5000.0  # MXN
        tasa_inflacion = float(sys.argv[8]) if len(sys.argv) > 8 else 0.03  # Tasa de inflación anual en México

        # Cálculos
        costo_total = costo_semestre * semestres
        costo_mensual = ((costo_semestre / 5) + (costo_libros / 10) + (costo_transporte / 5) + (costo_alojamiento / 12) + (costo_comida / 30)) * 12  # 12 meses por año
        costo_anual = ((costo_semestre * 2) + (costo_libros * 2) + (costo_transporte * 10) + (costo_alojamiento * 2) + (costo_comida * 2)) * 2  # 2 semestres por año
        costo_total_estimado = costo_total + (costo_libros * semestres) + (costo_transporte * semestres) + (costo_alojamiento * semestres) + (costo_comida * semestres)
        costo_total_estimado_inflacion = costo_total_estimado * (1 + tasa_inflacion) ** semestres

        # Output
        print("Cálculo de costo de carrera en México")
        print(f"Área: Finanzas")
        print(f"Carrera: {carrera}")
        print(f"Número de semestres: {semestres}")
        print(f"Costo por semestre: ${costo_semestre:,.2f} MXN")
        print(f"Costo total estimado: ${costo_total:,.2f} MXN")
        print(f"Costo mensual estimado: ${costo_mensual:,.2f} MXN")
        print(f"Costo anual estimado: ${costo_anual:,.2f} MXN")
        print(f"Costo total estimado con inflación: ${costo_total_estimado_inflacion:,.2f} MXN")
        print(f"Costo de libros por semestre: ${costo_libros:,.2f} MXN")
        print(f"Costo de transporte por semestre: ${costo_transporte:,.2f} MXN")
        print(f"Costo de alojamiento por semestre: ${costo_alojamiento:,.2f} MXN")
        print(f"Costo de comida por semestre: ${costo_comida:,.2f} MXN")
        print("Resumen Ejecutivo:")
        print(f"El costo total estimado para la carrera de {carrera} es de ${costo_total_estimado_inflacion:,.2f} MXN, considerando {semestres} semestres y una tasa de inflación anual del {tasa_inflacion*100}%.")

    except ValueError:
        print("Error: Los parámetros deben ser numéricos.")
    except IndexError:
        print("Error: Faltan parámetros. Por favor, ingrese los parámetros necesarios.")

if __name__ == "__main__":
    main()