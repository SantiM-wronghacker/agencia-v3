"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza validador datos entrada
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_edad(anos, meses, dias):
    """Calcula la edad en años, meses y días"""
    return f"{anos} años, {meses} meses y {dias} días"

def calcular_edad_exacta(fecha_nacimiento):
    """Calcula la edad exacta en años, meses y días"""
    hoy = datetime.date.today()
    edad_anos = hoy.year - fecha_nacimiento.year
    edad_meses = (hoy.month - fecha_nacimiento.month) % 12
    edad_dias = (hoy.day - fecha_nacimiento.day) % 30
    return calcular_edad(edad_anos, edad_meses, edad_dias)

def generar_datos_aleatorios():
    """Genera datos aleatorios"""
    cp = random.randint(10000, 99999)
    telefono = random.randint(1000000000, 9999999999)
    fecha_nacimiento = datetime.date.today() - datetime.timedelta(days=random.randint(1, 365*80))
    return cp, telefono, fecha_nacimiento

def validar_direccion(direccion):
    """Valida la dirección"""
    patron = re.compile(r"^(Calle|Avenida|Privada) [a-zA-Z0-9 ]+, [0-9]+, [a-zA-Z ]+, [a-zA-Z ]+$")
    if not patron.match(direccion):
        raise ValueError("Dirección no cumple con el formato esperado")

def main():
    try:
        # Validación de argumentos
        if len(sys.argv) < 6:
            raise ValueError("Número de argumentos incorrecto. Se necesitan al menos 6 argumentos: nombre, edad, direccion, estado, pais y cp")
        
        # Asignación de argumentos
        nombre = sys.argv[1]
        edad = int(sys.argv[2])
        direccion = sys.argv[3]
        estado = sys.argv[4]
        pais = sys.argv[5]
        cp = sys.argv[6]
        
        # Validación de edad
        if edad < 0:
            raise ValueError("Edad no puede ser negativa")
        
        # Validación de dirección
        try:
            validar_direccion(direccion)
        except ValueError as e:
            print(f"Error: {e}")
            return
        
        # Generación de datos aleatorios
        telefono, fecha_nacimiento = generar_datos_aleatorios()
        
        # Cálculo de la edad exacta
        edad_exacta = calcular_edad_exacta(fecha_nacimiento)
        
        # Impresión de resultados
        print(f"Nombre: {nombre}")
        print(f"Edad: {edad_exacta}")
        print(f"Dirección: {direccion}, {estado}, {pais}")
        print(f"Código Postal: {cp}")
        print(f"Teléfono: {telefono}")
        print(f"Fecha de Nacimiento: {fecha_nacimiento.strftime('%d/%m/%Y')}")
        print(f"Estado: {estado}")
        print(f"País: {pais}")
        print(f"Código de Postal: {cp}")
        print(f"Teléfono: {telefono}")
        
        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"Nombre: {nombre}")
        print(f"Edad: {edad_exacta}")
        print(f"Dirección: {direccion}, {estado}, {pais}")
        print(f"Código Postal: {cp}")
        print(f"Teléfono: {telefono}")
        print(f"Fecha de Nacimiento: {fecha_nacimiento.strftime('%d/%m/%Y')}")
        print(f"Estado: {estado}")
        print(f"País: {pais}")
        print(f"Código de Postal: {cp}")
        print(f"Teléfono: {telefono}")
    
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()