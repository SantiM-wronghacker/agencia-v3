#!/usr/bin/env python3
# ÁREA: FINANZAS
# DESCRIPCIÓN: Calculadora de descuento de precio
# TECNOLOGÍA: Python estándar

import sys
import os
import math

def calcular_descuento_precio(precio, descuento, iva=0.16):
    try:
        precio = float(precio)
        descuento = float(descuento)
        if precio < 0 or descuento < 0:
            raise ValueError
        if descuento > 100:
            raise ValueError
        if precio == 0:
            raise ValueError
        if descuento == 0:
            raise ValueError
        if precio < 1:
            raise ValueError
        if descuento < 1:
            raise ValueError
        if precio > 1000000:
            raise ValueError
        if iva < 0 or iva > 1:
            raise ValueError
        if iva != 0.16:
            print("Nota: El IVA utilizado es el estándar de México (16%). Puede cambiarlo si lo desea.")
        resultado = precio - (precio * descuento / 100)
        resultado = round(resultado, 2)
        precio_con_iva = resultado + (resultado * iva)
        precio_con_iva_redondeado = round(precio_con_iva, 2)
        precio_con_iva_sin_redondeo = round(precio_con_iva, 4)
        return (
            f"Precio original: ${precio:.2f}\n"
            f"Descuento: {descuento}%\n"
            f"Precio con descuento: ${resultado:.2f}\n"
            f"Precio con descuento sin redondeo: ${precio - (precio * descuento / 100):.4f}\n"
            f"Precio con IVA: ${precio_con_iva:.2f}\n"
            f"Precio con IVA redondeado: ${precio_con_iva_redondeado:.2f}\n"
            f"Precio con IVA sin redondeo: ${precio_con_iva_sin_redondeo:.4f}\n"
            f"IVA aplicado: {iva * 100}%\n"
            f"Precio con descuento y IVA: ${resultado + (resultado * iva):.2f}\n"
            f"Resumen ejecutivo: La calculadora de descuento de precio ha calculado el precio con descuento y IVA para el producto con precio original de ${precio:.2f} aplicando un descuento de {descuento}%.\n"
            f"Resumen ejecutivo: El precio con descuento y IVA sin redondeo es ${precio - (precio * descuento / 100) + (precio - (precio * descuento / 100)) * iva:.4f}.\n"
            f"Resumen ejecutivo: El precio con descuento y IVA es ${resultado + (resultado * iva):.2f}.\n"
            f"Resumen ejecutivo: El IVA aplicado es {iva * 100}%.\n"
            f"Resumen ejecutivo: El precio con descuento es ${resultado:.2f}.\n"
            f"Resumen ejecutivo: El precio con IVA es ${precio_con_iva:.2f}.\n"
            f"Resumen ejecutivo: El precio con descuento sin redondeo es ${precio - (precio * descuento / 100):.4f}.\n"
            f"Resumen ejecutivo: El precio con IVA sin redondeo es ${precio_con_iva_sin_redondeo:.4f}.\n"
        )
    except ValueError:
        return "Error: Los valores de precio y descuento deben ser números positivos y no superar el 100%."

def main():
    if len(sys.argv) != 4:
        print("Uso: python calculadora_descuento_precio.py <precio> <descuento> <iva>")
    else:
        try:
            precio = float(sys.argv[1])
            descuento = float(sys.argv[2])
            iva = float(sys.argv[3])
            if iva < 0 or iva > 1:
                raise ValueError
            resultado = calcular_descuento_precio(precio, descuento, iva)
            print(resultado)
        except ValueError:
            print("Error: Los valores de precio, descuento y iva deben ser números y el iva debe estar entre 0 y 1.")

if __name__ == "__main__":
    main()