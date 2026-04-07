#!/usr/bin/env python3

"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza analizador costos indirectos
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def analizar_costos_indirectos(materiales, mano_de_obra, transporte):
    try:
        # Buscar datos reales con web si disponible
        try:
            import web_bridge as web
            WEB = web.WEB  # True si hay conexión
            if WEB:
                precios = web.extraer_precios()
                if precios:
                    materiales = precios
                else:
                    print("No se encontraron precios en la web.")
        except ImportError:
            print("No se puede acceder a la web.")

        # Calcular costos indirectos
        costo_total = sum(materiales.values()) + mano_de_obra + transporte
        costo_materiales = sum(materiales.values())
        costo_manufactura = mano_de_obra + transporte
        margen_beneficio = costo_total - costo_materiales
        porcentaje_margen_beneficio = (100 * margen_beneficio) / costo_total
        tiempo_entrega_estimado = math.ceil((costo_total / 1000) * 5)
        costo_unitario_por_metro_cuadrado = (costo_total / 100) * 10
        costo_por_metro_cuadrado = (costo_total / 100) * 10
        costo_por_metro_cuadrado_con_margen = (costo_total / 100) * 10 + margen_beneficio
        costo_unitario_mano_obra = mano_de_obra / 100
        costo_unitario_transporte = transporte / 100
        costo_unitario_materiales = sum(materiales.values()) / 100

        # Mostrar resultados
        print(f"Costo total: {costo_total:.2f} MXN")
        print(f"Materiales: {costo_materiales:.2f} MXN")
        print(f"Mano de obra y transporte: {costo_manufactura:.2f} MXN")
        print(f"Margen de beneficio: {margen_beneficio:.2f} MXN")
        print(f"Porcentaje de margen de beneficio: {porcentaje_margen_beneficio:.2f}%")
        print(f"Tiempo de entrega estimado: {tiempo_entrega_estimado} días")
        print(f"Costo unitario por metro cuadrado: {costo_unitario_por_metro_cuadrado:.2f} MXN/m²")
        print(f"Costo por metro cuadrado: {costo_por_metro_cuadrado:.2f} MXN/m²")
        print(f"Costo por metro cuadrado con margen de beneficio: {costo_por_metro_cuadrado_con_margen:.2f} MXN/m²")
        print(f"Costo unitario mano de obra: {costo_unitario_mano_obra:.2f} MXN/hora")
        print(f"Costo unitario transporte: {costo_unitario_transporte:.2f} MXN/km")
        print(f"Costo unitario materiales: {costo_unitario_materiales:.2f} MXN/kg")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El costo total del proyecto es de {costo_total:.2f} MXN.")
        print(f"El margen de beneficio es de {porcentaje_margen_beneficio:.2f}%.")
        print(f"El tiempo de entrega estimado es de {tiempo_entrega_estimado} días.")
        print(f"El costo unitario por metro cuadrado es de {costo_unitario_por_metro_cuadrado:.2f} MXN/m².")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: analizador_costos_indirectos.py <materiales> <mano_de_obra> <transporte>")
        sys.exit(1)

    materiales = json.loads(sys.argv[1])
    mano_de_obra = float(sys.argv[2])
    transporte = float(sys.argv[3])

    analizar_costos_indirectos(materiales, mano_de_obra, transporte)