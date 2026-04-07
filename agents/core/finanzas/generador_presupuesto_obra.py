"""
ÁREA: CONSTRUCCIÓN
DESCRIPCIÓN: Agente que realiza generador presupuesto obra
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generador_presupuesto_obra(precios, tipo_cambio, cantidad_madera, cantidad_acero, cantidad_cemento):
    try:
        # Calcular presupuesto
        presupuesto = 0.0
        presupuesto += cantidad_madera * precios["madera"]  # Madera para la estructura
        presupuesto += cantidad_acero * precios["acero"]  # Acero para la estructura
        presupuesto += cantidad_cemento * precios["cemento"]  # Cemento para la estructura
        presupuesto *= tipo_cambio  # Convertir a dólares

        # Calcular impuestos y costos adicionales
        impuesto_madera = cantidad_madera * precios["madera"] * 0.16  # 16% de impuesto sobre la madera
        impuesto_acero = cantidad_acero * precios["acero"] * 0.16  # 16% de impuesto sobre el acero
        impuesto_cemento = cantidad_cemento * precios["cemento"] * 0.16  # 16% de impuesto sobre el cemento
        costo_transporte = (cantidad_madera + cantidad_acero + cantidad_cemento) * 0.05  # 5% de costo de transporte

        # Mostrar resultados
        print("Presupuesto total: {:.2f} USD".format(presupuesto))
        print("Materiales:")
        print("  Madera: {:.2f} m3 x {:.2f} USD/m3 = {:.2f} USD".format(cantidad_madera, precios["madera"], cantidad_madera * precios["madera"]))
        print("  Acero: {:.2f} toneladas x {:.2f} USD/tonelada = {:.2f} USD".format(cantidad_acero, precios["acero"], cantidad_acero * precios["acero"]))
        print("  Cemento: {:.2f} toneladas x {:.2f} USD/tonelada = {:.2f} USD".format(cantidad_cemento, precios["cemento"], cantidad_cemento * precios["cemento"]))
        print("Impuestos:")
        print("  Impuesto sobre la madera: {:.2f} USD".format(impuesto_madera))
        print("  Impuesto sobre el acero: {:.2f} USD".format(impuesto_acero))
        print("  Impuesto sobre el cemento: {:.2f} USD".format(impuesto_cemento))
        print("Costos adicionales:")
        print("  Costo de transporte: {:.2f} USD".format(costo_transporte))
        print("Tipo de cambio: {:.2f}".format(tipo_cambio))
        print("Fecha de cálculo: {}".format(datetime.date.today()))
        print("Resumen ejecutivo:")
        print("  El presupuesto total para la obra es de {:.2f} USD, incluyendo {:.2f} USD en materiales, {:.2f} USD en impuestos y {:.2f} USD en costos adicionales.".format(presupuesto, cantidad_madera * precios["madera"] + cantidad_acero * precios["acero"] + cantidad_cemento * precios["cemento"], impuesto_madera + impuesto_acero + impuesto_cemento, costo_transporte))
    except Exception as e:
        print("Error: {}".format(e))

def main():
    if len(sys.argv)!= 7:
        print("Uso: python generador_presupuesto_obra.py <precio_madera> <precio_acero> <precio_cemento> <tipo_cambio> <cantidad_madera> <cantidad_acero> <cantidad_cemento>")
        return

    try:
        precios = {
            "madera": float(sys.argv[1]),
            "acero": float(sys.argv[2]),
            "cemento": float(sys.argv[3])
        }
        tipo_cambio = float(sys.argv[4])
        cantidad_madera = float(sys.argv[5])
        cantidad_acero = float(sys.argv[6])
        cantidad_cemento = float(sys.argv[7])

        generador_presupuesto_obra(precios, tipo_cambio, cantidad_madera, cantidad_acero, cantidad_cemento)
    except Exception as e:
        print("Error: {}".format(e))

if __name__ == "__main__":
    main()