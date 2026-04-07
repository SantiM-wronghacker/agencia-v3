"""
AREA: FINANZAS
DESCRIPCION: Agente que realiza calculadora nomina
TECNOLOGIA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

def main():
    try:
        # Parámetros por defecto
        salario_diario = 500.0
        dias_trabajados = 30
        tasa_imss = 0.065
        tasa_isr = 0.10
        bono = 1000.0
        edad = 30
        estado_civil = "soltero"
        numero_dependientes = 0

        if len(sys.argv) > 1:
            salario_diario = float(sys.argv[1])
        if len(sys.argv) > 2:
            dias_trabajados = int(sys.argv[2])
        if len(sys.argv) > 3:
            tasa_imss = float(sys.argv[3])
        if len(sys.argv) > 4:
            tasa_isr = float(sys.argv[4])
        if len(sys.argv) > 5:
            bono = float(sys.argv[5])
        if len(sys.argv) > 6:
            edad = int(sys.argv[6])
        if len(sys.argv) > 7:
            estado_civil = sys.argv[7]
        if len(sys.argv) > 8:
            numero_dependientes = int(sys.argv[8])

        # Cálculos
        salario_mensual = salario_diario * dias_trabajados
        imss = salario_mensual * tasa_imss
        if salario_mensual < 5000:
            isr = 0
        elif salario_mensual < 10000:
            isr = (salario_mensual - 5000) * 0.10
        else:
            isr = (5000 * 0.10) + ((salario_mensual - 10000) * 0.20)
        neto = salario_mensual - imss - isr + bono
        aguinaldo = (salario_mensual / 12) * 15
        prima_vacacional = (salario_mensual / 12) * 25
        total_anual = neto * 12 + aguinaldo + prima_vacacional
        deduccion_por_edad = 0
        if edad > 60:
            deduccion_por_edad = 1000
        deduccion_por_estado_civil = 0
        if estado_civil == "casado":
            deduccion_por_estado_civil = 500
        deduccion_por_dependientes = numero_dependientes * 200
        total_deducciones = deduccion_por_edad + deduccion_por_estado_civil + deduccion_por_dependientes
        neto_con_deducciones = neto - total_deducciones

        # Imprimir resultados
        print("Salario diario: $", round(salario_diario, 2))
        print("Días trabajados: ", dias_trabajados)
        print("Salario mensual: $", round(salario_mensual, 2))
        print("IMSS: $", round(imss, 2))
        print("ISR: $", round(isr, 2))
        print("Neto: $", round(neto, 2))
        print("Aguinaldo: $", round(aguinaldo, 2))
        print("Prima vacacional: $", round(prima_vacacional, 2))
        print("Total anual: $", round(total_anual, 2))
        print("Deducción por edad: $", round(deduccion_por_edad, 2))
        print("Deducción por estado civil: $", round(deduccion_por_estado_civil, 2))
        print("Deducción por dependientes: $", round(deduccion_por_dependientes, 2))
        print("Total deducciones: $", round(total_deducciones, 2))
        print("Neto con deducciones: $", round(neto_con_deducciones, 2))
        print("Fecha de cálculo: ", datetime.date.today())
        print("Resumen ejecutivo: El salario neto es de $", round(neto, 2), "y el total anual es de $", round(total_anual, 2), "considerando deducciones el neto es de $", round(neto_con_deducciones, 2))

    except Exception as e:
        print("Error: ", str(e))

if __name__ == "__main__":
    main()