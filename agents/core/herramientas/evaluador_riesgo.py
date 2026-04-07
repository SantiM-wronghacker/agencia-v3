#!/usr/bin/env python3
# AREA: HERRAMIENTAS
# DESCRIPCIÓN: Agente que realiza evaluador de riesgo
# TECNOLOGÍA: Python estándar

import os
import sys
import json
import datetime
import math
import re
import random

def evaluador_riesgo(prima, tipo_cambio, riesgo, texto):
    try:
        # Procesar datos y calcular riesgo
        costo = prima * tipo_cambio
        seguro = costo * (1 + (riesgo * 0.10))  # agregar un 10% de riesgo
        beneficio = seguro * 0.05  # agregar un 5% de beneficio
        impuesto = seguro * 0.16  # agregar un 16% de impuesto
        total = seguro + impuesto

        # Imprimir resultados
        print("Riesgo:", riesgo)
        print("Prima:", prima)
        print("Tipo de cambio:", tipo_cambio)
        print("Costo:", costo)
        print("Seguro:", seguro)
        print("Beneficio:", beneficio)
        print("Impuesto:", impuesto)
        print("Total:", total)
        print("Texto:", texto)
        print("Fecha de cálculo:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print("El seguro tiene un costo de", seguro)
        print("y un beneficio de", beneficio)
        print("El riesgo asumido es del", riesgo*100, "%")
        print("El total incluye un impuesto del", impuesto)
        print("El plazo de pago es de", random.randint(1, 12), "meses")
        print("La tasa de interés anual es del", random.uniform(5, 15), "%")
        print("La prima es del", prima*100, "% del valor de la propiedad")
        print("El tipo de cambio es de", tipo_cambio, "MXN/USD")

        # Calculo de intereses moratorios
        plazo_pago = random.randint(1, 12)
        tasa_interes = random.uniform(5, 15)
        intereses_moratorios = seguro * (tasa_interes / 100) * (plazo_pago / 12)
        print("Intereses moratorios:", intereses_moratorios)

        # Calculo de penalidades por falta de pago
        penalidades_falta_pago = seguro * 0.01  # agregar un 1% de penalidades por falta de pago
        print("Penalidades por falta de pago:", penalidades_falta_pago)

        # Calculo de intereses por sobrepago
        intereses_sobrepago = seguro * (5 / 100)  # agregar un 5% de intereses por sobrepago
        print("Intereses por sobrepago:", intereses_sobrepago)

        # Resumen final
        print("\nResumen final:")
        print("El seguro tiene un costo total de", total)
        print("y una tasa de interés anual de", tasa_interes, "%")

        # Verificar si el riesgo es válido
        if riesgo < 0 or riesgo > 100:
            raise ValueError("El riesgo debe ser un número entre 0 y 100")

        # Verificar si la prima es válida
        if prima <= 0:
            raise ValueError("La prima debe ser un número positivo")

        # Verificar si el tipo de cambio es válido
        if tipo_cambio <= 0:
            raise ValueError("El tipo de cambio debe ser un número positivo")

    except ValueError as e:
        print("Error:", e)
    except Exception as e:
        print("Error:", e)

def main():
    if len(sys.argv) != 5:
        print("Uso: python evaluador_riesgo.py <prima> <tipo_cambio> <riesgo> <texto>")
        sys.exit(1)

    prima = float(sys.argv[1])
    tipo_cambio = float(sys.argv[2])
    riesgo = float(sys.argv[3])
    texto = sys.argv[4]

    evaluador_riesgo(prima, tipo_cambio, riesgo, texto)

if __name__ == "__main__":
    main()