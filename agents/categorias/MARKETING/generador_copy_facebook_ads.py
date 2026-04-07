#!/usr/bin/env python3
"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza generador copy facebook ads
TECNOLOGÍA: Python estándar
"""

import sys
import random
from datetime import datetime, timedelta

def generate_copy(city=None, product=None, discount=None, date=None):
    try:
        products = ["Ropa deportiva", "Zapatos casuales", "Accesorios de moda", "Bolsas de diseño", "Relojes elegantes"]
        discounts = ["20%", "30%", "40%", "50%", "60%"]
        cities = ["CDMX", "Guadalajara", "Monterrey", "Puebla", "Querétaro"]
        dates = ["hoy", "mañana", "este fin de semana", "esta semana", "este mes"]

        if product is None:
            product = random.choice(products)
        if discount is None:
            discount = random.choice(discounts)
        if city is None:
            city = random.choice(cities)
        if date is None:
            date = random.choice(dates)

        precio_original = 2500
        descuento_porcentaje = int(discount.strip('%'))
        precio_descuento = precio_original - (precio_original * descuento_porcentaje / 100)
        ahorro = precio_original - precio_descuento

        copy = [
            f"¡OFERTA EXCLUSIVA EN {product.upper()}!",
            f"Solo {discount} de descuento en {product} en {city}.",
            f"¡Solo {date}! No te lo pierdas.",
            f"Envíos gratis a toda la República Mexicana.",
            f"¡Compra ahora y ahorra hasta ${ahorro:.2f} MXN!",
            f"Fecha de inicio: {datetime.now().strftime('%Y-%m-%d')}",
            f"Fecha de fin: {(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}",
            f"Precio original: ${precio_original:.2f} MXN",
            f"Precio con descuento: ${precio_descuento:.2f} MXN",
            f"Ahorrando: ${ahorro:.2f} MXN",
            f"Descuento porcentaje: {descuento_porcentaje}%",
            f"Producto: {product}",
            f"Ciudad: {city}",
            f"Fecha de la oferta: {date}",
            f"Calificación del producto: {random.randint(1, 5)} estrellas",
            f"Comentarios del producto: {random.randint(1, 10)} comentarios",
            f"Ventas del producto: {random.randint(1, 100)} ventas"
        ]

        return copy

    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--help":
            print("Uso: python generador_copy_facebook_ads.py [ciudad] [producto] [descuento] [fecha]")
        else:
            city = sys.argv[1] if len(sys.argv) > 1 else None
            product = sys.argv[2] if len(sys.argv) > 2 else None
            discount = sys.argv[3] if len(sys.argv) > 3 else None
            date = sys.argv[4] if len(sys.argv) > 4 else None

            copy = generate_copy(city, product, discount, date)
            for line in copy:
                print(line)
            print("\nResumen ejecutivo:")
            print(f"La oferta es válida para la ciudad de {copy[12]} y el producto {copy[6]}.")
            print(f"El descuento es del {copy[1]} y el precio con descuento es de ${copy[7]} MXN.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()