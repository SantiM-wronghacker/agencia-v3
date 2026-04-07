"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora costo platillo
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcula_costo_platillo(costo_ingrediente, cantidad_ingrediente, precio_venta):
    try:
        # Verificar que los parámetros sean válidos
        if cantidad_ingrediente <= 0:
            raise ValueError("La cantidad de ingredientes debe ser mayor que cero.")
        if precio_venta <= 0:
            raise ValueError("El precio de venta del platillo debe ser mayor que cero.")
        if costo_ingrediente < 0:
            raise ValueError("El costo por ingrediente no puede ser negativo.")

        # Calcular el costo total
        costo_total = costo_ingrediente * cantidad_ingrediente

        # Calcular la ganancia
        ganancia = precio_venta - costo_total

        # Calcular el porcentaje de ganancia
        porcentaje_ganancia = (ganancia / costo_total) * 100 if costo_total > 0 else 0

        # Calcular el impuesto total
        impuesto_total = (precio_venta * 16) / 100  # Impuesto en porcentaje

        # Calcular el precio de venta con impuesto
        precio_venta_con_impuesto = precio_venta + impuesto_total

        # Calcular el margen de ganancia
        margen_de_ganancia = (ganancia / precio_venta) * 100 if precio_venta > 0 else 0

        # Calcular la cantidad de platos que se pueden vender con el costo total
        cantidad_platos = math.ceil(costo_total / 100)

        # Calcular el valor total de las ventas
        valor_total_ventas = precio_venta_con_impuesto * cantidad_platos

        return (
            costo_total,
            ganancia,
            porcentaje_ganancia,
            impuesto_total,
            precio_venta_con_impuesto,
            margen_de_ganancia,
            cantidad_platos,
            valor_total_ventas,
        )
    except ValueError as e:
        print(f"Error: {e}")
        return None, None, None, None, None, None, None, None
    except ZeroDivisionError:
        print("Error: No se pudo calcular el costo total, la ganancia, el porcentaje de ganancia, el impuesto total, el precio de venta con impuesto o el margen de ganancia.")
        return None, None, None, None, None, None, None, None

def main():
    try:
        # Parámetros por defecto
        costo_ingrediente = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0  # Costo por ingrediente en pesos mexicanos
        cantidad_ingrediente = int(sys.argv[2]) if len(sys.argv) > 2 else 5  # Cantidad de ingredientes
        precio_venta = float(sys.argv[3]) if len(sys.argv) > 3 else 50.0  # Precio de venta del platillo en pesos mexicanos

        costo_total, ganancia, porcentaje_ganancia, impuesto_total, precio_venta_con_impuesto, margen_de_ganancia, cantidad_platos, valor_total_ventas = calcula_costo_platillo(costo_ingrediente, cantidad_ingrediente, precio_venta)

        if costo_total is not None:
            print("Resumen ejecutivo:")
            print(f"Cantidad de ingredientes: {cantidad_ingrediente}")
            print(f"Costo por ingrediente: ${costo_ingrediente:.2f}")
            print(f"Precio de venta: ${precio_venta:.2f}")
            print(f"Cantidad de platos que se pueden vender: {cantidad_platos}")
            print(f"Valor total de las ventas: ${valor_total_ventas:.2f}")
            print(f"Costo total: ${costo_total:.2f}")
            print(f"Ganancia: ${ganancia:.2f}")
            print(f"Porcentaje de ganancia: {porcentaje_ganancia:.2f}%")
            print(f"Impuesto total: ${impuesto_total:.2f}")
            print(f"Precio de venta con impuesto: ${precio_venta_con_impuesto:.2f}")
            print(f"Márgen de ganancia: {margen_de_ganancia:.2f}%")
    except IndexError:
        print("Error: Faltan parámetros. Por favor, ingrese el costo por ingrediente, la cantidad de ingredientes y el precio de venta.")

if __name__ == "__main__":
    main()