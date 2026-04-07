"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Generador de fichas técnicas de propiedades
TECNOLOGÍA: Python
"""

import sys
import os
import json
from datetime import datetime
import math
import re

class Propiedad:
    def __init__(self, m2, recamaras, precio, ubicacion, antiguedad, estado, fecha_creacion=None, fecha_actualizacion=None, observaciones=None):
        self.m2 = m2
        self.recamaras = recamaras
        self.precio = precio
        self.ubicacion = ubicacion
        self.antiguedad = antiguedad
        self.estado = estado
        self.fecha_creacion = fecha_creacion
        self.fecha_actualizacion = fecha_actualizacion
        self.observaciones = observaciones

    def calcular_precio_por_m2(self):
        if self.m2 <= 0:
            return "Error: No se puede calcular el precio por m2 porque el tamaño es cero o negativo."
        return self.precio / self.m2

    def calcular_isr(self):
        return self.precio * 0.02

    def calcular_comision_agente(self):
        return self.precio * 0.05

    def calcular_iva(self):
        return self.precio * 0.16

    def calcular_total_con_iva(self):
        return self.precio + self.calcular_iva()

    def calcular_total_con_isr(self):
        return self.precio + self.calcular_isr()

    def calcular_total_con_comision(self):
        return self.precio + self.calcular_comision_agente()

    def generador_ficha_tecnica(self):
        try:
            isr = self.calcular_isr()
            comision_agente = self.calcular_comision_agente()
            iva = self.calcular_iva()
            total_con_iva = self.calcular_total_con_iva()
            total_con_isr = self.calcular_total_con_isr()
            total_con_comision = self.calcular_total_con_comision()
            precio_por_m2 = self.calcular_precio_por_m2()

            return f"Ficha Técnica de Propiedad en {self.ubicacion}\n\n" \
                   f"* Tamaño: {self.m2} m2\n" \
                   f"* Recámaras: {self.recamaras}\n" \
                   f"* Precio: ${self.precio:,.2f}\n" \
                   f"* Antigüedad: {self.antiguedad} años\n" \
                   f"* Estado: {self.estado}\n" \
                   f"* Precio por m2: ${precio_por_m2:,.2f}\n" \
                   f"* Impuesto sobre la renta (ISR): ${isr:,.2f}\n" \
                   f"* Comisión del agente: ${comision_agente:,.2f}\n" \
                   f"* IVA: ${iva:,.2f}\n" \
                   f"* Total con IVA: ${total_con_iva:,.2f}\n" \
                   f"* Total con ISR: ${total_con_isr:,.2f}\n" \
                   f"* Total con comisión: ${total_con_comision:,.2f}\n" \
                   f"* Fecha de creación: {self.fecha_creacion or 'No especificada'}\n" \
                   f"* Fecha de actualización: {self.fecha_actualizacion or 'No especificada'}\n" \
                   f"* Observaciones: {self.observaciones or 'No especificadas'}\n" \
                   f"* Resumen ejecutivo: Esta propiedad es una excelente opción para aquellos que buscan un lugar cómodo y seguro en {self.ubicacion}.\n"
        except Exception as e:
            return f"Error: {str(e)}"

def main():
    if len(sys.argv) != 2:
        print("Uso: python generador_fichas_tecnicas.py <propiedad>")
        sys.exit(1)

    propiedad = json.loads(sys.argv[1])
    print(Propiedad(**propiedad).generador_ficha_tecnica())

if __name__ == "__main__":
    main()