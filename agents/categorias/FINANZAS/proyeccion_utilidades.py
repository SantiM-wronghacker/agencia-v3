#!/usr/bin/env python3
"""
ÁREA: FINANZAS
DESCRIPCIÓN: Simulador de utilidades para calcular utilidades anuales y mensuales con consideraciones fiscales mexicanas
TECNOLOGÍA: Python
"""

import sys
import time
import math
from datetime import datetime
import json

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

class SimuladorUtilidades:
    def __init__(self, metas_ventas_mensuales, gastos_fijos_mensuales, tasa_impuesto=0.30):
        if len(metas_ventas_mensuales) != 12 or len(gastos_fijos_mensuales) != 12:
            raise ValueError("Se requieren exactamente 12 valores para metas de ventas y gastos fijos")
        self.metas_ventas_mensuales = metas_ventas_mensuales
        self.gastos_fijos_mensuales = gastos_fijos_mensuales
        self.tasa_impuesto = tasa_impuesto

    def calcular_utilidades_anuales(self):
        utilidades_anuales = 0
        for i in range(12):
            utilidad_mensual = self.metas_ventas_mensuales[i] - self.gastos_fijos_mensuales[i]
            utilidades_anuales += utilidad_mensual
        utilidad_neta = utilidades_anuales * (1 - self.tasa_impuesto)
        return {
            "utilidades_brutas": utilidades_anuales,
            "utilidad_neta": utilidad_neta,
            "tasa_impuesto": self.tasa_impuesto
        }

    def calcular_utilidad_mensual(self, mes):
        if mes < 1 or mes > 12:
            raise ValueError("Mes debe ser entre 1 y 12")
        utilidad_mensual = self.metas_ventas_mensuales[mes - 1] - self.gastos_fijos_mensuales[mes - 1]
        utilidad_neta = utilidad_mensual * (1 - self.tasa_impuesto)
        return {
            "mes": mes,
            "utilidad_mensual": utilidad_mensual,
            "utilidad_neta": utilidad_neta
        }

    def generar_resumen_ejecutivo(self):
        utilidades_brutas, utilidad_neta = self.calcular_utilidades_anuales()
        mes_mas_rentable = max(range(12), key=lambda i: self.metas_ventas_mensuales[i] - self.gastos_fijos_mensuales[i]) + 1
        mes_menos_rentable = min(range(12), key=lambda i: self.metas_ventas_mensuales[i] - self.gastos_fijos_mensuales[i]) + 1

        resumen_ejecutivo = {
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "utilidades_brutas": utilidades_brutas,
            "utilidad_neta": utilidad_neta,
            "tasa_impuesto": self.tasa_impuesto,
            "mes_mas_rentable": mes_mas_rentable,
            "mes_menos_rentable": mes_menos_rentable,
            "utilidad_mensual_mas_rentable": self.calcular_utilidad_mensual(mes_mas_rentable),
            "utilidad_mensual_menos_rentable": self.calcular_utilidad_mensual(mes_menos_rentable)
        }
        return resumen_ejecutivo

def main():
    if len(sys.argv) != 5:
        print("Uso: python proyeccion_utilidades.py <metas_ventas_mensual_1> <metas_ventas_mensual_2> ... <metas_ventas_mensual_12>")
        sys.exit(1)

    metas_ventas_mensuales = [float(arg) for arg in sys.argv[1:13]]
    gastos_fijos_mensuales = [float(arg) for arg in sys.argv[13:]]

    simulador = SimuladorUtilidades(metas_ventas_mensuales, gastos_fijos_mensuales)
    print(json.dumps(simulator.generar_resumen_ejecutivo(), indent=4))

if __name__ == "__main__":
    main()