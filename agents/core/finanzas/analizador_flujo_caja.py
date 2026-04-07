import sys
import math
import os

# AREA: FINANZAS
# DESCRIPCION: Analiza flujo de caja mensual de un negocio. Recibe ingresos y egresos por categoría, calcula saldo neto, identifica meses críticos y proyecta 12 meses hacia adelante.
# TECNOLOGIA: Python

def main():
    try:
        if len(sys.argv) == 7:
            ingresos_mensuales = int(sys.argv[1])
            egresos_fijos = int(sys.argv[2])
            egresos_variables = int(sys.argv[3])
            tasa_interes_anual = float(sys.argv[4])
            tasa_inflacion_anual = float(sys.argv[5])
            meses_proyeccion = int(sys.argv[6])
        else:
            ingresos_mensuales = 200000  # Ingresos mensuales promedio en México
            egresos_fijos = 120000  # Egresos fijos promedio en México
            egresos_variables = 40000  # Egresos variables promedio en México
            tasa_interes_anual = 0.08  # Tasa de interés anual promedio en México
            tasa_inflacion_anual = 0.04  # Tasa de inflación anual promedio en México
            meses_proyeccion = 12

        try:
            if ingresos_mensuales <= 0:
                raise ValueError("Ingresos mensuales deben ser positivos")
            if egresos_fijos < 0:
                raise ValueError("Egresos fijos no pueden ser negativos")
            if egresos_variables < 0:
                raise ValueError("Egresos variables no pueden ser negativos")
            if tasa_interes_anual < 0 or tasa_inflacion_anual < 0:
                raise ValueError("Tasas de interés e inflación no pueden ser negativas")
            if meses_proyeccion < 1:
                raise ValueError("Meses de proyección deben ser al menos 1")

            saldo_neto = ingresos_mensuales - egresos_fijos - egresos_variables
            meses_criticos = 0
            proyeccion = []
            intereses_mensuales = (ingresos_mensuales * tasa_interes_anual) / 12
            ajuste_precios_mensuales = (ingresos_mensuales * tasa_inflacion_anual) / 12

            for i in range(meses_proyeccion):
                saldo_proyectado = saldo_neto * (i + 1) + intereses_mensuales * (i + 1) - ajuste_precios_mensuales * (i + 1)
                if saldo_proyectado < 0:
                    meses_criticos += 1
                proyeccion.append(saldo_proyectado)

            print(f"{'Descripción':^20}{'Valor':^15}")
            print(f"{'-' * 20}{'-' * 15}")
            print(f"Ingresos mensuales: ${ingresos_mensuales:,.2f} MXN")
            print(f"Egresos fijos: ${egresos_fijos:,.2f} MXN")
            print(f"Egresos variables: ${egresos_variables:,.2f} MXN")
            print(f"Saldo neto: ${saldo_neto:,.2f} MXN")
            print(f"Meses críticos: {meses_criticos} meses")
            print(f"Tasa de interés anual: {tasa_interes_anual * 100:.2f}%")
            print(f"Tasa de inflación anual: {tasa_inflacion_anual * 100:.2f}%")
            print(f"Meses de proyección: {meses_proyeccion} meses")
            print(f"{'-' * 20}{'-' * 15}")
            print(f"{'Resumen ejecutivo':^40}")
            print(f"El flujo de caja del negocio es estable, pero se espera un déficit en {meses_criticos} meses.")
            print(f"Se recomienda ajustar los egresos variables y considerar la posibilidad de aumentar los ingresos.")
        except ValueError as e:
            print(f"Error: {e}")
    except IndexError:
        print("Error: Faltan argumentos de línea de comandos")

if __name__ == "__main__":
    main()