"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora iva desglosado
TECNOLOGÍA: Python estándar
"""

import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def main():
    try:
        subtotal = float(sys.argv[1]) if len(sys.argv) > 1 else 1000.0
        iva = float(sys.argv[2]) if len(sys.argv) > 2 else 16.0
        descuento = float(sys.argv[3]) if len(sys.argv) > 3 else 10.0
        margen_utilidad = float(sys.argv[4]) if len(sys.argv) > 4 else 20.0
        costo_produccion_porcentaje = float(sys.argv[5]) if len(sys.argv) > 5 else 80.0
        costo_unitario = float(sys.argv[6]) if len(sys.argv) > 6 else 50.0
        cantidad_productos = int(sys.argv[7]) if len(sys.argv) > 7 else 100

        importe_iva = (subtotal * iva) / 100
        total = subtotal + importe_iva
        descuento_subtotal = (subtotal * descuento) / 100
        total_con_descuento = total - descuento_subtotal
        margen_utilidad_subtotal = (subtotal * margen_utilidad) / 100
        total_con_margen_utilidad = total + margen_utilidad_subtotal
        costo_produccion = (subtotal * costo_produccion_porcentaje) / 100
        utilidad_neta = total_con_descuento - costo_produccion
        costo_total_productos = costo_unitario * cantidad_productos
        beneficio_total = utilidad_neta + costo_total_productos

        print("Calculadora de IVA Desglosado")
        print("-----------------------------")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"IVA ({iva}%): ${importe_iva:.2f}")
        print(f"Total: ${total:.2f}")
        print(f"Descuento del {descuento}% sobre el subtotal: ${descuento_subtotal:.2f}")
        print(f"Total con descuento del {descuento}% sobre el subtotal: ${total_con_descuento:.2f}")
        print(f"Margen de utilidad ({margen_utilidad}% sobre el subtotal): ${margen_utilidad_subtotal:.2f}")
        print(f"Total con margen de utilidad ({margen_utilidad}% sobre el subtotal): ${total_con_margen_utilidad:.2f}")
        print(f"Costo de producción ({costo_produccion_porcentaje}% del subtotal): ${costo_produccion:.2f}")
        print(f"Utilidad neta (Total con descuento - Costo de producción): ${utilidad_neta:.2f}")
        print(f"Costo unitario por producto: ${costo_unitario:.2f}")
        print(f"Cantidad de productos: {cantidad_productos}")
        print(f"Costo total de productos: ${costo_total_productos:.2f}")
        print(f"Beneficio total (Utilidad neta + Costo total de productos): ${beneficio_total:.2f}")
        print("Resumen ejecutivo:")
        print(f"El total con descuento es ${total_con_descuento:.2f}, lo que representa un ahorro del {descuento}% sobre el subtotal.")
        print(f"El margen de utilidad es del {margen_utilidad}% sobre el subtotal, lo que significa que se obtiene un beneficio de ${margen_utilidad_subtotal:.2f} por cada ${subtotal:.2f} vendido.")
        print(f"El costo de producción es del {costo_produccion_porcentaje}% del subtotal, lo que significa que se invierten ${costo_produccion:.2f} para producir ${subtotal:.2f} en ventas.")
    except ValueError:
        print("Error: Los valores ingresados no son numéricos.")
    except IndexError:
        print("Error: Faltan argumentos.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()