"""
ÁREA: RESTAURANTES
DESCRIPCIÓN: Agente que realiza generador menu precios
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime
import math

def main():
    try:
        # Configuración por defecto
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        platos = ["Tacos al pastor", "Enchiladas verdes", "Pozole rojo", "Mole de pollo", "Chilaquiles"]
        precios_base = [55, 70, 85, 95, 60]
        impuestos = 0.16  # IVA

        # Parámetros configurables
        dia = sys.argv[1] if len(sys.argv) > 1 else random.choice(dias_semana)
        descuento = float(sys.argv[2]) if len(sys.argv) > 2 else random.uniform(0, 0.2)
        propina = float(sys.argv[3]) if len(sys.argv) > 3 else 0.1

        # Generar menú con precios
        menu = []
        total_ventas = 0
        total_descuentos = 0
        total_propina = 0
        for plato, precio in zip(platos, precios_base):
            precio_descuento = precio * (1 - descuento)
            precio_final = precio_descuento * (1 + impuestos)
            menu.append({
                "plato": plato,
                "precio_original": precio,
                "precio_descuento": round(precio_descuento, 2),
                "precio_final": round(precio_final, 2),
                "descuento": f"{descuento*100:.1f}%"
            })
            total_ventas += precio_final
            total_descuentos += precio * descuento
            total_propina += precio_final * propina

        # Generar salida
        print(f"MENÚ DEL DÍA: {dia.upper()}")
        print(f"FECHA: {datetime.now().strftime('%d/%m/%Y')}")
        print("PLATO\t\tPRECIO ORIGINAL\tPRECIO DESCUENTO\tPRECIO FINAL\tDESCUENTO")
        for item in menu:
            print(f"{item['plato']}\t${item['precio_original']:.2f}\t${item['precio_descuento']:.2f}\t${item['precio_final']:.2f}\t{item['descuento']}")
        print(f"TOTAL VENTAS: ${total_ventas:.2f}")
        print(f"TOTAL DESCUENTOS: ${total_descuentos:.2f}")
        print(f"TOTAL PROPINA ({propina*100:.0f}%): ${total_propina:.2f}")
        print(f"IMPUESTOS (IVA {impuestos*100:.0f}%): ${total_ventas - sum(item['precio_descuento'] for item in menu):.2f}")
        print(f"TOTAL A PAGAR: ${total_ventas + total_propina:.2f}")

        # Resumen ejecutivo
        print("\nRESUMEN EJECUTIVO:")
        print(f"Total de ventas: ${total_ventas:.2f}")
        print(f"Total de descuentos: ${total_descuentos:.2f}")
        print(f"Total de propina: ${total_propina:.2f}")
        print(f"Total a pagar: ${total_ventas + total_propina:.2f}")
        print(f"Margen de ganancia (antes de impuestos): {(total_ventas - sum(item['precio_original'] for item in menu)) / sum(item['precio_original'] for item in menu) * 100:.2f}%")
        print(f"Margen de ganancia (después de impuestos): {(total_ventas - sum(item['precio_descuento'] for item in menu)) / sum(item['precio_descuento'] for item in menu) * 100:.2f}%")

    except ValueError as e:
        print(f"Error: {e}")
    except IndexError:
        print("Error: No se proporcionaron los parámetros necesarios")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()