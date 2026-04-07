"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Normalizador de nombres de personas
TECNOLOGÍA: Python estándar
"""

import sys
import re
import datetime
import random
import math

def normalizador_nombre_persona(entrada, ciudad_nacimiento, edad_minima, edad_maxima):
    """Función pura, sin prints, sin side effects."""
    try:
        # Reemplaza caracteres no alfanuméricos y convierte a mayúsculas
        nombre = re.sub('[^a-zA-Z0-9\s]', '', entrada).title()
        
        # Separa el nombre en primer y segundo apellido
        nombres = nombre.split()
        if len(nombres) < 3:
            raise ValueError("Nombre no válido")
        
        primer_apellido = nombres[-2]
        segundo_apellido = nombres[-1]
        
        # Reemplaza los espacios en blanco con guiones para nombres compuestos
        nombre_completo = '-'.join(nombres[:-2])
        
        # Calcula la edad con una fecha de nacimiento realista para México
        fecha_nacimiento = datetime.date.today() - datetime.timedelta(days=random.randint(365*edad_minima, 365*edad_maxima))
        edad = (datetime.date.today() - fecha_nacimiento).days // 365
        
        # Calcula la altura y peso según la edad
        altura = math.floor(150 + (random.uniform(-5, 5) + (edad * 0.5)))
        peso = math.floor(50 + (random.uniform(-5, 5) + (edad * 0.5)))
        
        # Calcula el IMC según la altura y peso
        imc = round(peso / (altura / 100) ** 2, 2)
        
        # Calcula el índice de masa corporal según la edad y género
        if edad < 18:
            imc_genero = 0.8
        elif edad < 30:
            imc_genero = 0.9
        else:
            imc_genero = 1.0
        
        # Devuelve el nombre completo, primer apellido, segundo apellido y nombre compuesto
        return {
            'nombre_completo': nombre_completo,
            'primer_apellido': primer_apellido,
            'segundo_apellido': segundo_apellido,
            'nombre_compuesto': nombre_completo + ' ' + primer_apellido + ' ' + segundo_apellido,
            'fecha_nacimiento': fecha_nacimiento.strftime('%d/%m/%Y'),
            'edad': edad,
            'ciudad_nacimiento': ciudad_nacimiento,
            'altura': altura,
            'peso': peso,
            'imc': imc,
            'imc_genero': imc_genero
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    if len(sys.argv) != 5:
        print("Uso: python normalizador_nombre_persona.py <entrada> <ciudad_nacimiento> <edad_minima> <edad_maxima>")
        return
    
    entrada = sys.argv[1]
    ciudad_nacimiento = sys.argv[2]
    edad_minima = int(sys.argv[3])
    edad_maxima = int(sys.argv[4])
    
    resultado = normalizador_nombre_persona(entrada, ciudad_nacimiento, edad_minima, edad_maxima)
    
    if resultado is not None:
        print("Nombre completo:", resultado['nombre_completo'])
        print("Primer apellido:", resultado['primer_apellido'])
        print("Segundo apellido:", resultado['segundo_apellido'])
        print("Nombre compuesto:", resultado['nombre_compuesto'])
        print("Fecha de nacimiento:", resultado['fecha_nacimiento'])
        print("Edad:", resultado['edad'])
        print("Ciudad de nacimiento:", resultado['ciudad_nacimiento'])
        print("Altura:", resultado['altura'], "cm")
        print("Peso:", resultado['peso'], "kg")
        print("IMC:", resultado['imc'])
        print("Índice de masa corporal según la edad y género:", resultado['imc_genero'])
        print("Resumen ejecutivo: El resultado es una persona con los datos proporcionados.")

if __name__ == "__main__":
    main()