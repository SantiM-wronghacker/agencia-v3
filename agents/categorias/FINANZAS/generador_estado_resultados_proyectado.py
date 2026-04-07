# FINANZAS/Generador Estado Resultados Proyectado/Python
# AREA: FINANZAS
# DESCRIPCION: Agente que realiza generador estado resultados proyectado
# TECNOLOGIA: Python

import sys
import json
import datetime
import math
import random

def main():
    try:
        fecha_actual = datetime.date.today()
        año_proyectado = int(sys.argv[1]) if len(sys.argv) > 1 else fecha_actual.year + 1
        ventas_proyectadas = float(sys.argv[2]) if len(sys.argv) > 2 else 1000000.0
        costos_proyectados = float(sys.argv[3]) if len(sys.argv) > 3 else 500000.0
        gastos_proyectados = float(sys.argv[4]) if len(sys.argv) > 4 else 200000.0
        impuestos_proyectados = float(sys.argv[5]) if len(sys.argv) > 5 else 0.1 * ventas_proyectadas
        depreciacion_proyectada = float(sys.argv[6]) if len(sys.argv) > 6 else 0.05 * costos_proyectados
        utilidad_proyectada = ventas_proyectadas - costos_proyectados - gastos_proyectados - impuestos_proyectados - depreciacion_proyectada
        margen_utilidad_proyectada = (utilidad_proyectada / ventas_proyectadas) * 100 if ventas_proyectadas > 0 else 0
        roa_proyectado = (utilidad_proyectada / (costos_proyectados + gastos_proyectados)) * 100 if (costos_proyectados + gastos_proyectados) > 0 else 0
        roe_proyectado = (utilidad_proyectada / (costos_proyectados + gastos_proyectados + impuestos_proyectados)) * 100 if (costos_proyectados + gastos_proyectados + impuestos_proyectados) > 0 else 0
        deuda_proyectada = float(sys.argv[7]) if len(sys.argv) > 7 else 0
        intereses_proyectados = deuda_proyectada * 0.05
        flujo_efectivo_proyectado = utilidad_proyectada + depreciacion_proyectada - intereses_proyectados

        print(f"Estado de Resultados Proyectado para el año {año_proyectado}:")
        print(f"Ventas Proyectadas: ${ventas_proyectadas:,.2f} MXN")
        print(f"Costos Proyectados: ${costos_proyectados:,.2f} MXN")
        print(f"Gastos Proyectados: ${gastos_proyectados:,.2f} MXN")
        print(f"Impuestos Proyectados: ${impuestos_proyectados:,.2f} MXN")
        print(f"Depreciación Proyectada: ${depreciacion_proyectada:,.2f} MXN")
        print(f"Utilidad Proyectada: ${utilidad_proyectada:,.2f} MXN")
        print(f"Margen de Utilidad Proyectado: {margen_utilidad_proyectada:.2f}%")
        print(f"ROA Proyectado: {roa_proyectado:.2f}%")
        print(f"ROE Proyectado: {roe_proyectado:.2f}%")
        print(f"Deuda Proyectada: ${deuda_proyectada:,.2f} MXN")
        print(f"Intereses Proyectados: ${intereses_proyectados:,.2f} MXN")
        print(f"Flujo Efectivo Proyectado: ${flujo_efectivo_proyectado:,.2f} MXN")

        print("\nResumen Ejecutivo:")
        print(f"El estado de resultados proyectado para el año {año_proyectado} muestra una utilidad de ${utilidad_proyectada:,.2f} MXN, con un margen de utilidad de {margen_utilidad_proyectada:.2f}% y un ROA de {roa_proyectado:.2f}%.")

    except IndexError:
        print("Error: Faltan argumentos de línea de comandos.")
    except ValueError:
        print("Error: Los argumentos de línea de comandos deben ser números.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()