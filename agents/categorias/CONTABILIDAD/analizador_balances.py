"""
ÁREA: FINANZAS
DESCRIPCIÓN: Analiza un archivo de texto con activos y pasivos para calcular el capital contable y razones financieras básicas.
TECNOLOGÍA: Python
"""

import os
import sys
import time
import json
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

class AnalizadorBalances:
    def __init__(self, archivo):
        self.archivo = archivo
        self.activos = {}
        self.pasivos = {}
        self.capital_contable = 0
        self.liquidez = 0
        self.endeudamiento = 0
        self.rotacion_activos = 0
        self.rotacion_pasivos = 0

    def leer_archivo(self):
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    elementos = linea.split(',')
                    if elementos[0] == 'Activo':
                        self.activos[elementos[1]] = float(elementos[2])
                    elif elementos[0] == 'Pasivo':
                        self.pasivos[elementos[1]] = float(elementos[2])
        except FileNotFoundError:
            print("El archivo no existe")
            return None
        except Exception as e:
            print("Error al leer el archivo:", str(e))
            return None

    def calcular_capital_contable(self):
        total_activos = sum(self.activos.values())
        total_pasivos = sum(self.pasivos.values())
        self.capital_contable = total_activos - total_pasivos

    def calcular_razones_financieras(self):
        if self.capital_contable == 0:
            return None
        self.liquidez = self.activos.get('Caja y bancos', 0) / self.pasivos.get('Cuentas por pagar', 1)
        self.endeudamiento = sum(self.pasivos.values()) / self.capital_contable
        self.rotacion_activos = sum(self.activos.values()) / self.activos.get('Inventario', 1)
        self.rotacion_pasivos = sum(self.pasivos.values()) / self.pasivos.get('Cuentas por pagar', 1)

    def imprimir_resultados(self):
        print("Capital Contable:", self.capital_contable)
        print("Liquidez:", self.liquidez)
        print("Endeudamiento:", self.endeudamiento)
        print("Rotación de Activos:", self.rotacion_activos)
        print("Rotación de Pasivos:", self.rotacion_pasivos)
        print("Total Activos:", sum(self.activos.values()))
        print("Total Pasivos:", sum(self.pasivos.values()))
        print("Resumen Ejecutivo:")
        if self.liquidez > 1:
            print("La empresa tiene una buena liquidez")
        else:
            print("La empresa tiene una mala liquidez")
        if self.endeudamiento < 1:
            print("La empresa tiene un buen nivel de endeudamiento")
        else:
            print("La empresa tiene un mal nivel de endeudamiento")

def main():
    if len(sys.argv) > 1:
        archivo = sys.argv[1]
    else:
        archivo = 'balances.txt'
        print("Usando archivo por defecto:", archivo)
    analizador = AnalizadorBalances(archivo)
    analizador.leer_archivo()
    analizador.calcular_capital_contable()
    analizador.calcular_razones_financieras()
    analizador.imprimir_resultados()

if __name__ == "__main__":
    main()