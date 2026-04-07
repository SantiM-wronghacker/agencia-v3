"""
ÁREA: TURISMO
DESCRIPCIÓN: Agente que realiza generador paquete turistico
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime, timedelta
from math import ceil

def generar_paquete(destinos=None, actividades=None, precios=None):
    try:
        if destinos is None:
            destinos = sys.argv[1].split(",") if len(sys.argv) > 1 else ["Cancún", "Los Cabos", "Puerto Vallarta", "Riviera Maya", "Guadalajara"]
        if actividades is None:
            actividades = sys.argv[2].split(",") if len(sys.argv) > 2 else ["Excursión a ruinas mayas", "Tour gastronómico", "Buceo en arrecifes", "Visita a parques naturales", "Experiencia cultural"]
        if precios is None:
            precios = sys.argv[3].split(",") if len(sys.argv) > 3 else [1500, 2200, 2800, 3500, 4200]

        destino = random.choice(destinos)
        actividad = random.choice(actividades)
        precio = random.choice(precios)
        dias = random.randint(3, 7)
        fecha_salida = datetime.now() + timedelta(days=random.randint(7, 30))

        regalo = random.choice(["Kit de bienvenida", "Paquete de cuidado personal", "Voucher de spa"])
        transporte = random.choice(["Avión", "Coche alquilado", "Taxi"])

        return {
            "destino": destino,
            "actividad": actividad,
            "precio": precio,
            "dias": dias,
            "fecha_salida": fecha_salida.strftime("%Y-%m-%d"),
            "regalo": regalo,
            "transporte": transporte
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def calcular_impuestos(precio):
    try:
        iva = 0.16
        isr = 0.10
        return precio * iva + precio * isr
    except Exception as e:
        print(f"Error: {e}")
        return 0

def calcular_total(precio, impuestos, descuento):
    try:
        return precio + impuestos - descuento
    except Exception as e:
        print(f"Error: {e}")
        return 0

def calcular_descuento(precio, dias):
    try:
        if dias >= 7:
            return precio * 0.10
        elif dias >= 5:
            return precio * 0.05
        else:
            return 0
    except Exception as e:
        print(f"Error: {e}")
        return 0

def calcular_gastos_adicionales(precio, dias, destino):
    try:
        if destino == "Cancún":
            return precio * 0.05
        elif destino == "Los Cabos":
            return precio * 0.03
        else:
            return 0
    except Exception as e:
        print(f"Error: {e}")
        return 0

def main():
    try:
        paquete = generar_paquete(sys.argv[1], sys.argv[2], sys.argv[3])
        if paquete:
            impuestos = calcular_impuestos(paquete["precio"])
            descuento = calcular_descuento(paquete["precio"], paquete["dias"])
            gastos_adicionales = calcular_gastos_adicionales(paquete["precio"], paquete["dias"], paquete["destino"])
            total = calcular_total(paquete["precio"], impuestos, descuento)
            print("Resumen Ejecutivo:")
            print(f"Destino: {paquete['destino']}")
            print(f"Actividad: {paquete['actividad']}")
            print(f"Precio: {paquete['precio']}")
            print(f"Días: {paquete['dias']}")
            print(f"Fecha de Salida: {paquete['fecha_salida']}")
            print(f"Regalo: {paquete['regalo']}")
            print(f"Transporte: {paquete['transporte']}")
            print(f"Impuestos: {impuestos}")
            print(f"Descuento: {descuento}")
            print(f"Gastos Adicionales: {gastos_adicionales}")
            print(f"Total: {total}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()