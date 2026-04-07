"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Genera scripts de llamada de ventas personalizados para diferentes tipos de prospectos. Incluye apertura, manejo de objeciones y cierre según el perfil del cliente.
TECNOLOGÍA: Python estándar
"""

import sys
import json
import os

def obtener_caracteristicas(producto):
    try:
        caracteristicas = {
            "departamento_polanco": "amplios espacios, excelente ubicación y acabados de lujo",
            "casa_hacienda": "jardines amplios, piscina y áreas de recreación",
            "oficina_centro": "excelente ubicación, fácil acceso y seguridad las 24 horas"
        }
        return caracteristicas.get(producto, "no disponible")
    except Exception as e:
        return f"Error: {str(e)}"

def obtener_beneficios(producto):
    try:
        beneficios = {
            "departamento_polanco": "seguridad, comodidad y acceso a servicios de alta calidad",
            "casa_hacienda": "espacio para familia y amigos, tranquilidad y conexión con la naturaleza",
            "oficina_centro": "acceso a servicios de alta calidad, fácil acceso y seguridad las 24 horas"
        }
        return beneficios.get(producto, "no disponible")
    except Exception as e:
        return f"Error: {str(e)}"

def obtener_precios(producto):
    try:
        precios = {
            "departamento_polanco": {
                "precio_base": 5000000,
                "precio_promedio": 7000000
            },
            "casa_hacienda": {
                "precio_base": 10000000,
                "precio_promedio": 15000000
            },
            "oficina_centro": {
                "precio_base": 2000000,
                "precio_promedio": 3000000
            }
        }
        return precios.get(producto, "no disponible")
    except Exception as e:
        return f"Error: {str(e)}"

def generar_script(tipo_prospecto, producto, nombre_asesor, caracteristicas_producto, beneficios_producto, precio_base, precio_promedio):
    try:
        script = f"Script de llamada para {tipo_prospecto} interesado en {producto}:\n"
        script += f"Apertura: Hola, ¿cómo estás? Me llamo {nombre_asesor} y soy asesor de ventas.\n"
        script += f"Manejo de objeciones: ¿Cuál es tu principal preocupación al considerar la compra de un {producto}?\n"
        script += f"Cierre: ¿Qué te parece si agendamos una cita para discutir más a fondo tus necesidades y cómo podemos ayudarte a encontrar el {producto} perfecto?\n"
        script += f"Detalles del producto: El {producto} es un producto de alta calidad que ofrece {caracteristicas_producto} características y beneficios.\n"
        script += f"Beneficios del producto: Al adquirir nuestro {producto}, podrás disfrutar de {beneficios_producto} beneficios y ventajas.\n"
        script += f"Precio del producto: El precio base del {producto} es de ${precio_base} y el precio promedio es de ${precio_promedio}.\n"
        script += f"Resumen ejecutivo: El {producto} es una excelente opción para aquellos que buscan un producto de alta calidad y precio competitivo.\n"
        return script
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    if len(sys.argv) != 6:
        print("Error: Faltan argumentos")
        return

    tipo_prospecto = sys.argv[1]
    producto = sys.argv[2]
    nombre_asesor = sys.argv[3]
    caracteristicas_producto = obtener_caracteristicas(producto)
    beneficios_producto = obtener_beneficios(producto)
    precio_base = obtener_precios(producto)["precio_base"]
    precio_promedio = obtener_precios(producto)["precio_promedio"]

    script = generar_script(tipo_prospecto, producto, nombre_asesor, caracteristicas_producto, beneficios_producto, precio_base, precio_promedio)
    print(script)

if __name__ == "__main__":
    main()