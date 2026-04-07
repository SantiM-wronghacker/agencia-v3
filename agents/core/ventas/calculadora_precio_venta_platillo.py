#!/usr/bin/env python3
# ÁREA: FINANZAS
# DESCRIPCIÓN: Agente que realiza calculadora precio venta platillo
# TECNOLOGÍA: Python estándar

import sys
import math

def calcular_precio_venta(costo_produccion, margen_ganancia, iva):
    return costo_produccion * (1 + margen_ganancia) * (1 + iva)

def calcular_utilidad(precio_venta, costo_produccion):
    return precio_venta - costo_produccion

def calcular_margen_utilidad(precio_venta, costo_produccion):
    if precio_venta == 0:
        return 0
    return (calcular_utilidad(precio_venta, costo_produccion) / precio_venta) * 100

def calcular_costo_produccion_con_iva(costo_produccion, margen_ganancia, iva):
    return costo_produccion * (1 + margen_ganancia) * iva

def calcular_impuesto_iva(precio_venta, iva):
    return precio_venta * iva

def calcular_utilidad_neta(precio_venta, costo_produccion, iva):
    return calcular_utilidad(precio_venta, costo_produccion) - calcular_impuesto_iva(precio_venta, iva)

def main():
    try:
        args = sys.argv
        if len(args) == 6:
            costo_produccion = float(args[1])
            margen_ganancia = float(args[2])
            iva = float(args[3])
            precio_venta = float(args[4])
            utilidad_neta = float(args[5])
        else:
            costo_produccion = 100.0  # default
            margen_ganancia = 0.3  # default
            iva = 0.16  # default
            precio_venta = 0.0
            utilidad_neta = 0.0

        if precio_venta == 0:
            precio_venta = calcular_precio_venta(costo_produccion, margen_ganancia, iva)

        if utilidad_neta == 0:
            utilidad_neta = calcular_utilidad_neta(precio_venta, costo_produccion, iva)

        costo_produccion_con_iva = calcular_costo_produccion_con_iva(costo_produccion, margen_ganancia, iva)
        margen_utilidad = calcular_margen_utilidad(precio_venta, costo_produccion)
        impuesto_iva = calcular_impuesto_iva(precio_venta, iva)

        print(f"Costo de producción: ${costo_produccion:.2f} MXN")
        print(f"Margen de ganancia: {margen_ganancia*100:.2f}%")
        print(f"IVA: {iva*100:.2f}%")
        print(f"Precio de venta: ${precio_venta:.2f} MXN")
        print(f"Utilidad neta: ${utilidad_neta:.2f} MXN")
        print(f"Margen de utilidad: {margen_utilidad:.2f}%")
        print(f"Costo de producción con IVA: ${costo_produccion_con_iva:.2f} MXN")
        print(f"Impuesto IVA: ${impuesto_iva:.2f} MXN")
        print(f"Porcentaje de costo de producción sobre el precio de venta: {(costo_produccion / precio_venta) * 100:.2f}%")
        print(f"Porcentaje de utilidad sobre el precio de venta: {(utilidad_neta / precio_venta) * 100:.2f}%")
        print(f"Resumen ejecutivo: El costo de producción es de ${costo_produccion:.2f} MXN, el margen de ganancia es de {margen_ganancia*100:.2f}%, el precio de venta es de ${precio_venta:.2f} MXN, la utilidad neta es de ${utilidad_neta:.2f} MXN, el margen de utilidad es de {margen_utilidad:.2f}%, el costo de producción con IVA es de ${costo_produccion_con_iva:.2f} MXN, el impuesto IVA es de ${impuesto_iva:.2f} MXN.")

    except ValueError:
        print("Error: Los valores ingresados no son válidos.")
    except IndexError:
        print("Error: Faltan argumentos.")

if __name__ == "__main__":
    main()