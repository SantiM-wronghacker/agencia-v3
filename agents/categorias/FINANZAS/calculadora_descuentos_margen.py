"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora descuentos margen
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcula_descuento(precio, porcentaje):
    """
    Calcula el descuento aplicado a un precio.
    
    Args:
        precio (float): Precio original.
        porcentaje (float): Porcentaje de descuento.
    
    Returns:
        float: Descuento aplicado.
    """
    return precio * (porcentaje / 100)

def calcula_margen(precio, costo):
    """
    Calcula el margen de ganancia.
    
    Args:
        precio (float): Precio de venta.
        costo (float): Costo de producción.
    
    Returns:
        float: Margen de ganancia.
    """
    return (precio - costo) / precio * 100

def calcula_iva(precio, porcentaje_iva):
    """
    Calcula el IVA aplicado a un precio.
    
    Args:
        precio (float): Precio original.
        porcentaje_iva (float): Porcentaje de IVA.
    
    Returns:
        float: IVA aplicado.
    """
    return precio * (porcentaje_iva / 100)

def main():
    try:
        precio = float(sys.argv[1]) if len(sys.argv) > 1 else 100.0
        porcentaje_descuento = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
        costo = float(sys.argv[3]) if len(sys.argv) > 3 else 80.0
        porcentaje_iva = float(sys.argv[4]) if len(sys.argv) > 4 else 16.0

        descuento = calcula_descuento(precio, porcentaje_descuento)
        precio_con_descuento = precio - descuento
        iva = calcula_iva(precio_con_descuento, porcentaje_iva)
        precio_con_iva = precio_con_descuento + iva
        margen = calcula_margen(precio_con_iva, costo + iva)
        utilidad = precio_con_iva - (costo + iva)
        rentabilidad = (utilidad / (costo + iva)) * 100 if (costo + iva) != 0 else 0
        punto_de_equilibrio = (costo + iva) / (1 - (porcentaje_descuento / 100))

        print(f"Precio original: ${precio:.2f} MXN")
        print(f"Descuento aplicado: {porcentaje_descuento}%")
        print(f"Descuento calculado: ${descuento:.2f} MXN")
        print(f"Precio con descuento: ${precio_con_descuento:.2f} MXN")
        print(f"IVA aplicado: {porcentaje_iva}%")
        print(f"IVA calculado: ${iva:.2f} MXN")
        print(f"Precio con IVA: ${precio_con_iva:.2f} MXN")
        print(f"Margen calculado: {margen:.2f}%")
        print(f"Costo total (incluyendo IVA): ${costo + iva:.2f} MXN")
        print(f"Utilidad: ${utilidad:.2f} MXN")
        print(f"Rentabilidad: {rentabilidad:.2f}%")
        print(f"Punto de equilibrio: {punto_de_equilibrio:.2f} MXN")
        print(f"Resumen ejecutivo: El precio original de ${precio:.2f} MXN con un descuento de {porcentaje_descuento}% y un IVA de {porcentaje_iva}%, resulta en un precio final de ${precio_con_iva:.2f} MXN.")
        print(f"Resumen ejecutivo: La utilidad obtenida es de ${utilidad:.2f} MXN y la rentabilidad es de {rentabilidad:.2f}%.")
        print(f"Resumen ejecutivo: El punto de equilibrio es de {punto_de_equilibrio:.2f} MXN.")

    except ValueError:
        print("Error: Los valores ingresados no son números.")
    except IndexError:
        print("Error: Faltan valores en la lista de argumentos.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()