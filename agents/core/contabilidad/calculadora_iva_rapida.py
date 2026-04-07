#!/usr/bin/env python3

"""
ÁREA: FINANZAS
DESCRIPCIÓN: Calculadora de IVA rápida
TECNOLOGÍA: Python estándar
"""

import sys
import argparse

def calculadora_iva_rapida(iva, precio, *args):
    """Función pura, sin prints, sin side effects."""
    try:
        iva = float(iva)
        precio = float(precio)
        if iva < 0:
            return "INVALIDO:iva_negativo"
        elif iva > 1000000000:
            return "INVALIDO:iva_muy_alto"
        elif iva < 0.01:
            return "INVALIDO:iva_muy_bajo"

        # Calculos precisos y realistas para México
        iva_calculado = iva * precio * 0.16
        iva_total = precio + iva_calculado
        iva_sobre_precio = iva_calculado / precio * 100
        iva_sobre_total = (iva_calculado / iva_total) * 100
        iva_sobre_precio_venta = (iva_calculado / (precio + iva_calculado)) * 100
        iva_sobre_precio_base = (iva / (iva + iva_calculado)) * 100
        iva_sobre_precio_base_total = (iva_total / (precio + iva_calculado)) * 100
        iva_sobre_precio_base_iva = (iva_calculado / (precio + iva_calculado)) * 100

        # Agregar más datos útiles
        iva_sobre_precio_base_iva_total = (iva_calculado / iva_total) * 100
        iva_sobre_precio_base_iva_precio = (iva_calculado / precio) * 100
        iva_sobre_precio_base_iva_precio_venta = (iva_calculado / (precio + iva_calculado)) * 100

        # Agregar resumen ejecutivo
        resumen_ejecutivo = f"El IVA calculado es de {iva_calculado:.2f} y el IVA total es de {iva_total:.2f}."

        # Agregar encabezado AREA/DESCRIPCION/TECNOLOGIA
        encabezado = f"""
Área: Finanzas
Descripción: Calculadora de IVA rápida
Tecnología: Python estándar

"""

        return f"""
{encabezado}
IVA: {iva_calculado:.2f}
IVA total: {iva_total:.2f}
IVA porcentaje: 16%
IVA base: {precio:.2f}
IVA calculado: {iva_calculado:.2f}
IVA total: {iva_total:.2f}
IVA porcentaje sobre precio: {iva_sobre_precio:.2f}%
IVA porcentaje sobre total: {iva_sobre_total:.2f}%
IVA porcentaje sobre precio de venta: {iva_sobre_precio_venta:.2f}%
IVA sobre precio de venta (%): {iva_sobre_precio_venta:.2f}%
IVA sobre precio (%): {iva_sobre_precio:.2f}%
IVA sobre total (%): {iva_sobre_total:.2f}%
IVA sobre precio de venta base: {iva_sobre_precio_base:.2f}%
IVA sobre precio de venta base total: {iva_sobre_precio_base_total:.2f}%
IVA sobre precio base: {iva_sobre_precio_base:.2f}%
IVA sobre precio base iva: {iva_sobre_precio_base_iva:.2f}%
IVA sobre precio base iva total: {iva_sobre_precio_base_iva_total:.2f}%
IVA sobre precio base iva precio: {iva_sobre_precio_base_iva_precio:.2f}%
IVA sobre precio base iva precio venta: {iva_sobre_precio_base_iva_precio_venta:.2f}%
{resumen_ejecutivo}
"""

    except ValueError:
        return "INVALIDO:iva_o_precio_no_es_float"

def main():
    parser = argparse.ArgumentParser(description='Calculadora de IVA rápida')
    parser.add_argument('--iva', type=float, required=True, help='IVA a calcular')
    parser.add_argument('--precio', type=float, required=True, help='Precio a calcular')
    args = parser.parse_args()

    resultado = calculadora_iva_rapida(args.iva, args.precio)

    if resultado.startswith("INVALIDO:"):
        print(f"Error: {resultado}")