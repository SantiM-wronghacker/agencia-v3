# ÁREA: MARKETING
# DESCRIPCIÓN: Agente que realiza generador buyer persona pro
# TECNOLOGÍA: Python estándar

import os
import sys
import json
import datetime
import math
import re
import random

def generador_buyer_persona_pro(nombre=None, apellido=None, edad=None, ingreso=None, interes=None, ubicacion=None, ocupacion=None, nivel_estudios=None, dispositivo=None):
    # Valores por defecto si no se especifican
    if nombre is None:
        nombres = ["Juan", "Pedro", "Luis", "Carlos", "Alberto"]
        nombre = random.choice(nombres)
    if apellido is None:
        apellidos = ["González", "Martínez", "Díaz", "García", "Rodríguez"]
        apellido = random.choice(apellidos)
    if edad is None:
        edades = [25, 30, 35, 40, 45]
        edad = random.choice(edades)
    if ingreso is None:
        ingresos = [50000, 60000, 70000, 80000, 90000]
        ingreso = random.choice(ingresos)
    if interes is None:
        intereses = ["viajes", "música", "lectura", "cine", "deporte"]
        interes = random.choice(intereses)
    if ubicacion is None:
        ubicaciones = ["Ciudad de México", "Guadalajara", "Monterrey", "Puebla", "León"]
        ubicacion = random.choice(ubicaciones)
    if ocupacion is None:
        ocupaciones = ["Estudiante", "Trabajador", "Emprendedor", "Retirado", "Independiente"]
        ocupacion = random.choice(ocupaciones)
    if nivel_estudios is None:
        niveles_estudios = ["Primaria", "Secundaria", "Preparatoria", "Universitario", "Posgrado"]
        nivel_estudios = random.choice(niveles_estudios)
    if dispositivo is None:
        dispositivos = ["Celular", "Tablet", "Computadora", "Smart TV", "Consola de videojuegos"]
        dispositivo = random.choice(dispositivos)

    # Busca datos reales con web_bridge si está disponible
    try:
        import web_bridge as web
        WEB = web.WEB  # True si hay conexión
        if WEB:
            nombres = web.buscar("nombres de personas comunes en México")
            apellidos = web.buscar("apellidos de personas comunes en México")
            edades = web.extraer_precios("edad promedio de la población mexicana")
            ingresos = web.extraer_precios("ingreso promedio de la población mexicana")
            intereses = web.extraer_precios("intereses comunes de la población mexicana")
            ubicaciones = web.extraer_precios("ubicaciones más comunes en México")
            ocupaciones = web.extraer_precios("ocupaciones más comunes en México")
            niveles_estudios = web.extraer_precios("niveles de estudios más comunes en México")
            dispositivos = web.extraer_precios("dispositivos más comunes en México")
    except ImportError:
        pass

    # Calculos precisos y realistas para México
    if ingreso < 20000:
        categoria_ingreso = "Baja"
    elif ingreso < 50000:
        categoria_ingreso = "Media"
    else:
        categoria_ingreso = "Alta"

    # Genera buyer persona pro aleatorio
    print(f"Nombre: {nombre} {apellido}")
    print(f"Edad: {edad} años")
    print(f"Ingreso: ${ingreso:.2f} pesos")
    print(f"Categoría de ingreso: {categoria_ingreso}")
    print(f"Ubicación: {ubicacion}")
    print(f"Ocupación: {ocupacion}")
    print(f"Nivel de estudios: {nivel_estudios}")
    print(f"Dispositivo: {dispositivo}")
    print(f"Intereses: {interes}")
    print(f"Resumen ejecutivo: La persona objetivo es un(a) {categoria_ingreso} ingreso, con {edad} años de edad, que reside en {ubicacion} y se dedica a {ocupacion}.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        nombre = sys.argv[1]
        apellido = sys.argv[2]
        edad = sys.argv[3]
        ingreso = sys.argv[4]