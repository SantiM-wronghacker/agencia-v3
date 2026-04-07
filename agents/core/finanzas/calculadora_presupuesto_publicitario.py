"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora presupuesto publicitario
TECNOLOGÍA: Python estándar
"""

import sys
import math
import random
import datetime

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcula_presupuesto(inversión_total, porcentaje_publicidad):
    """
    Calcula el presupuesto publicitario
    """
    presupuesto_publicitario = inversión_total * (porcentaje_publicidad / 100)
    return presupuesto_publicitario

def calcula_costo_por_plataforma(presupuesto_publicitario, porcentaje_facebook, porcentaje_instagram, porcentaje_twitter):
    """
    Calcula el costo por plataforma
    """
    try:
        costo_facebook = presupuesto_publicitario * (porcentaje_facebook / 100)
        costo_instagram = presupuesto_publicitario * (porcentaje_instagram / 100)
        costo_twitter = presupuesto_publicitario * (porcentaje_twitter / 100)
        return costo_facebook, costo_instagram, costo_twitter
    except ZeroDivisionError:
        print("Error: El porcentaje no puede ser 0")
        return 0, 0, 0

def calcula_impuesto(presupuesto_publicitario):
    """
    Calcula el impuesto
    """
    try:
        impuesto = presupuesto_publicitario * 0.16  # Impuesto al 16%
        return impuesto
    except TypeError:
        print("Error: El presupuesto publicitario debe ser un número")
        return 0

def calcula_total_con_impuesto(presupuesto_publicitario, impuesto):
    """
    Calcula el total con impuesto
    """
    try:
        total_con_impuesto = presupuesto_publicitario + impuesto
        return total_con_impuesto
    except TypeError:
        print("Error: El presupuesto publicitario y el impuesto deben ser números")
        return 0

def main():
    try:
        inversión_total = float(sys.argv[1]) if len(sys.argv) > 1 else 100000
        porcentaje_publicidad = float(sys.argv[2]) if len(sys.argv) > 2 else 20
        porcentaje_facebook = float(sys.argv[3]) if len(sys.argv) > 3 else 40
        porcentaje_instagram = float(sys.argv[4]) if len(sys.argv) > 4 else 30
        porcentaje_twitter = float(sys.argv[5]) if len(sys.argv) > 5 else 30

        presupuesto_publicitario = calcula_presupuesto(inversión_total, porcentaje_publicidad)
        costo_facebook, costo_instagram, costo_twitter = calcula_costo_por_plataforma(presupuesto_publicitario, porcentaje_facebook, porcentaje_instagram, porcentaje_twitter)
        impuesto = calcula_impuesto(presupuesto_publicitario)
        total_con_impuesto = calcula_total_con_impuesto(presupuesto_publicitario, impuesto)

        print(f"Inversión total: ${inversión_total:.2f}")
        print(f"Presupuesto publicitario: ${presupuesto_publicitario:.2f}")
        print(f"Costo Facebook: ${costo_facebook:.2f}")
        print(f"Costo Instagram: ${costo_instagram:.2f}")
        print(f"Costo Twitter: ${costo_twitter:.2f}")
        print(f"Impuesto: ${impuesto:.2f}")
        print(f"Total con impuesto: ${total_con_impuesto:.2f}")

        print("\nResumen ejecutivo:")
        print(f"El presupuesto publicitario de ${presupuesto_publicitario:.2f} se utiliza en un 40% para Facebook, un 30% para Instagram y un 30% para Twitter.")
        print(f"El impuesto al 16% es de ${impuesto:.2f}.")
        print(f"El total con impuesto es de ${total_con_impuesto:.2f}.")

    except IndexError:
        print("Error: Faltan argumentos")

if __name__ == "__main__":
    main()