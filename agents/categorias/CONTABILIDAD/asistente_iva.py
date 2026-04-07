"""
ÁREA: FINANZAS
DESCRIPCIÓN: Asistente para calcular el IVA de una lista de montos con enfoque en normativa mexicana
TECNOLOGÍA: Python
"""

import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

class AsistenteIVA:
    def __init__(self, montos, iva=0.16, retencion=0.0, exento=False):
        self.montos = montos
        self.iva = iva
        self.retencion = retencion
        self.exento = exento
        self.validar_montos()

    def validar_montos(self):
        if not all(isinstance(monto, (int, float)) for monto in self.montos):
            raise ValueError("Todos los montos deben ser números")
        if any(monto < 0 for monto in self.montos):
            raise ValueError("Los montos no pueden ser negativos")

    def calcular_subtotal(self):
        return sum(self.montos)

    def calcular_iva(self):
        if self.exento:
            return 0
        return self.calcular_subtotal() * self.iva

    def calcular_retencion(self):
        if self.retencion <= 0:
            return 0
        return self.calcular_subtotal() * self.retencion

    def calcular_total(self):
        subtotal = self.calcular_subtotal()
        iva = self.calcular_iva()
        retencion = self.calcular_retencion()
        return subtotal + iva - retencion

    def generar_resumen(self):
        subtotal = self.calcular_subtotal()
        iva = self.calcular_iva()
        retencion = self.calcular_retencion()
        total = self.calcular_total()

        resumen = f"Resumen de declaración contable:\n"
        resumen += f"Subtotal: ${subtotal:.2f}\n"
        resumen += f"IVA ({self.iva*100}%): ${iva:.2f}\n"
        resumen += f"Retención ({self.retencion*100}%): ${retencion:.2f}\n"
        resumen += f"Total a pagar: ${total:.2f}\n"
        resumen += f"Total de montos: {len(self.montos)}\n"
        resumen += f"Monto promedio: ${subtotal/len(self.montos):.2f}\n"
        resumen += f"Monto máximo: ${max(self.montos):.2f}\n"
        resumen += f"Monto mínimo: ${min(self.montos):.2f}\n"
        resumen += f"Porcentaje de IVA sobre total: {iva/total*100:.2f}%\n"
        resumen += f"Porcentaje de retención sobre total: {retencion/total*100:.2f}%\n"
        resumen += f"Monto redondeado: ${math.ceil(total):.2f}\n"
        resumen += f"Monto redondeado (centavos): ${math.floor(total):.2f}\n"
        resumen += f"Monto redondeado (banco): ${round(total, -1):.2f}\n"

        return resumen

    def generar_resumen_ejecutivo(self):
        subtotal = self.calcular_subtotal()
        iva = self.calcular_iva()
        retencion = self.calcular_retencion()
        total = self.calcular_total()

        ejecutivo = f"\nResumen ejecutivo:\n"
        ejecutivo += f"El total a pagar es de ${total:.2f}\n"
        ejecutivo += f"De este monto, ${iva:.2f} corresponden a IVA ({self.iva*100}%)\n"
        ejecutivo += f"Y ${retencion:.2f} son retenciones ({self.retencion*100}%)\n"
        ejecutivo += f"El subtotal antes de impuestos es ${subtotal:.2f}\n"
        ejecutivo += f"El monto promedio por transacción es ${subtotal/len(self.montos):.2f}\n"
        ejecutivo += f"El monto máximo registrado es ${max(self.montos):.2f}\n"
        ejecutivo += f"El monto mínimo registrado es ${min(self.montos):.2f}\n"

        return ejecutivo