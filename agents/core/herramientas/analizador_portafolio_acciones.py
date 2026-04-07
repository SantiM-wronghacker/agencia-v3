# FINANZAS/ANALIZADOR DE PORTAFOLIO DE ACCIONES/PYTHON
# AREA: FINANZAS
# DESCRIPCION: Agente que realiza analizador portafolio acciones
# TECNOLOGIA: PYTHON

import sys
import json
import datetime
import math
import random
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_rendimiento(inversion, plazo, tasa_interes):
    return inversion * math.pow(1 + tasa_interes, plazo)

def calcular_riesgo(inversion, plazo, tasa_riesgo):
    return random.uniform(0, 1) * inversion * math.pow(1 + tasa_riesgo, plazo)

def calcular_impuestos(rendimiento, tasa_impuesto):
    return rendimiento * tasa_impuesto

def calcular_inflacion(rendimiento, tasa_inflacion):
    return rendimiento / math.pow(1 + tasa_inflacion, plazo)

def calcular_impacto_inflacion(rendimiento, tasa_inflacion):
    return (rendimiento - calcular_inflacion(rendimiento, tasa_inflacion)) / rendimiento

def main():
    try:
        args = sys.argv
        if len(args) < 7:
            print("Error: Faltan argumentos de entrada.")
            sys.exit(1)

        if not os.path.exists('parametros.txt'):
            print("Error: Archivo de parametros no encontrado.")
            sys.exit(1)

        with open('parametros.txt', 'r') as f:
            parametros = json.load(f)

        inversion = float(parametros['inversion'])
        plazo = int(parametros['plazo'])
        tasa_interes = float(parametros['tasa_interes'])
        tasa_riesgo = float(parametros['tasa_riesgo'])
        tasa_impuesto = float(parametros['tasa_impuesto'])
        tasa_inflacion = float(parametros['tasa_inflacion'])

        rendimiento = calcular_rendimiento(inversion, plazo, tasa_interes)
        riesgo = calcular_riesgo(inversion, plazo, tasa_riesgo)
        impuestos = calcular_impuestos(rendimiento, tasa_impuesto)
        inflacion = calcular_inflacion(rendimiento, tasa_inflacion)
        impacto_inflacion = calcular_impacto_inflacion(rendimiento, tasa_inflacion)
        fecha_actual = datetime.datetime.now()
        fecha_vencimiento = fecha_actual + datetime.timedelta(days=plazo*365)

        print(f"Inversión inicial: ${inversion:.2f} MXN")
        print(f"Plazo de inversión: {plazo} años")
        print(f"Tasa de interés: {tasa_interes*100:.2f}%")
        print(f"Tasa de riesgo: {tasa_riesgo*100:.2f}%")
        print(f"Tasa de impuesto: {tasa_impuesto*100:.2f}%")
        print(f"Tasa de inflación: {tasa_inflacion*100:.2f}%")
        print(f"Rendimiento esperado: ${rendimiento:.2f} MXN")
        print(f"Riesgo asociado: ${riesgo:.2f} MXN")
        print(f"Impuestos a pagar: ${impuestos:.2f} MXN")
        print(f"Inflación esperada: ${inflacion:.2f} MXN")
        print(f"Impacto de la inflación en el rendimiento: {impacto_inflacion*100:.2f}%")
        print(f"Fecha de vencimiento: {fecha_vencimiento.strftime('%Y-%m-%d')}")

        print("\nResumen ejecutivo:")
        print(f"La inversión de ${inversion:.2f} MXN durante {plazo} años a una tasa de interés del {tasa_interes*100:.2f}% y una tasa de riesgo del {tasa_riesgo*100:.2f}% resulta en un rendimiento esperado de ${rendimiento:.2f} MXN, con un riesgo asociado de ${riesgo:.2f} MXN y un impacto de la inflación en el rendimiento de {impacto_inflacion*100:.2f}%.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()