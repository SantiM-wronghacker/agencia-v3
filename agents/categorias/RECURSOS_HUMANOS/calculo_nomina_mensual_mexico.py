"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculo nomina mensual mexico
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calculo_nomina(salario_diario, dias_trabajados, impuesto_porcentaje=0.16, seguro_social_porcentaje=0.11, infonavit_porcentaje=0.05):
    try:
        salario_mensual = salario_diario * dias_trabajados
        impuesto = salario_mensual * impuesto_porcentaje
        seguro_social = salario_mensual * seguro_social_porcentaje
        infonavit = salario_mensual * infonavit_porcentaje
        total_deducciones = impuesto + seguro_social + infonavit
        neto = salario_mensual - total_deducciones
        return {
            "salario_mensual": salario_mensual,
            "impuesto": impuesto,
            "seguro_social": seguro_social,
            "infonavit": infonavit,
            "total_deducciones": total_deducciones,
            "neto": neto
        }
    except Exception as e:
        return str(e)

def main():
    try:
        if len(sys.argv) < 3:
            print("Uso: python calculo_nomina_mensual_mexico.py <salario_diario> <dias_trabajados> <impuesto_porcentaje> <seguro_social_porcentaje> <infonavit_porcentaje>")
            print("Ejemplo: python calculo_nomina_mensual_mexico.py 500.0 30 0.16 0.11 0.05")
            return
        salario_diario = float(sys.argv[1])
        dias_trabajados = int(sys.argv[2])
        if len(sys.argv) > 3:
            impuesto_porcentaje = float(sys.argv[3])
        else:
            impuesto_porcentaje = 0.16
        if len(sys.argv) > 4:
            seguro_social_porcentaje = float(sys.argv[4])
        else:
            seguro_social_porcentaje = 0.11
        if len(sys.argv) > 5:
            infonavit_porcentaje = float(sys.argv[5])
        else:
            infonavit_porcentaje = 0.05
        resultado = calculo_nomina(salario_diario, dias_trabajados, impuesto_porcentaje, seguro_social_porcentaje, infonavit_porcentaje)
        if isinstance(resultado, dict):
            print("Resumen de Nómina:")
            print("--------------------")
            print("Salario Diario: $", round(salario_diario, 2))
            print("Días Trabajados: ", dias_trabajados)
            print("Salario Mensual: $", round(resultado["salario_mensual"], 2))
            print("Impuesto ({}%): $".format(int(impuesto_porcentaje*100)), round(resultado["impuesto"], 2))
            print("Seguro Social ({}%): $".format(int(seguro_social_porcentaje*100)), round(resultado["seguro_social"], 2))
            print("Infonavit ({}%): $".format(int(infonavit_porcentaje*100)), round(resultado["infonavit"], 2))
            print("Total Deducciones: $", round(resultado["total_deducciones"], 2))
            print("Neto: $", round(resultado["neto"], 2))
            print("Margen de Utilidad: {}%".format(round((resultado["neto"] / resultado["salario_mensual"]) * 100, 2)))
            print("Resumen Ejecutivo:")
            print("--------------------")
            print("El salario mensual es de ${} con un impuesto de ${}, un seguro social de ${} y un infonavit de ${}.".format(round(resultado["salario_mensual"], 2), round(resultado["impuesto"], 2), round(resultado["seguro_social"], 2), round(resultado["infonavit"], 2)))
            print("El total de deducciones es de ${} y el neto es de ${}.".format(round(resultado["total_deducciones"], 2), round(resultado["neto"], 2)))
        else:
            print(resultado)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()