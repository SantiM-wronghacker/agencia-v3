"""
ÁREA: RRHH
DESCRIPCIÓN: Agente que realiza generador preguntas entrevista
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def generar_preguntas(cantidad_preguntas=5, nombres=None, categorias=None, dificultades=None):
    try:
        if cantidad_preguntas < 1:
            raise ValueError("La cantidad de preguntas debe ser mayor o igual a 1")
        
        if nombres is None:
            nombres = ["¿Cuál es su nombre completo?", "¿Qué es su cargo actual?", "¿Cuál es su experiencia laboral?", "¿Cuáles son sus habilidades?", "¿Cuál es su objetivo laboral?"]
        if categorias is None:
            categorias = ["Personal", "Laboral", "Educativa", "Habilidades", "Objetivos"]
        if dificultades is None:
            dificultades = ["Fácil", "Moderada", "Difícil"]
        
        if len(nombres) != len(categorias) or len(nombres) != len(dificultades):
            raise ValueError("Los vectores de nombres, categorías y dificultades deben tener la misma longitud")
        
        preguntas = []
        for i in range(cantidad_preguntas):
            pregunta = {
                "id": i+1,
                "nombre": nombres[i % len(nombres)],
                "categoria": categorias[i % len(categorias)],
                "dificultad": dificultades[i % len(dificultades)]
            }
            preguntas.append(json.dumps(pregunta))
        
        return preguntas
    
    except Exception as e:
        print(f"Error: {e}")
        return []

def calcular_edad(nacimiento):
    try:
        fecha_actual = datetime.datetime.now()
        edad = fecha_actual.year - nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (nacimiento.month, nacimiento.day))
        return edad
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def calcular_edad_mexico(nacimiento):
    try:
        fecha_actual = datetime.datetime.now()
        edad = fecha_actual.year - nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (nacimiento.month, nacimiento.day))
        # Ajuste para el caso de que el día de nacimiento sea después del día actual
        if (fecha_actual.month, fecha_actual.day) < (nacimiento.month, nacimiento.day):
            edad -= 1
        return edad
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    try:
        if len(sys.argv) > 1:
            cantidad_preguntas = int(sys.argv[1])
        else:
            cantidad_preguntas = 5
        
        if len(sys.argv) > 2:
            try:
                nacimiento = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
                edad = calcular_edad_mexico(nacimiento)
                print(f"Edad: {edad} años")
            except ValueError:
                print("Error: La fecha de nacimiento debe ser en formato YYYY-MM-DD")
        else:
            print("No se proporcionó la fecha de nacimiento")
        
        if len(sys.argv) > 3:
            nombres = sys.argv[3].split(',')
            categorias = sys.argv[4].split(',')
            dificultades = sys.argv[5].split(',')
            preguntas = generar_preguntas(cantidad_preguntas, nombres, categorias, dificultades)
            print("Preguntas:")
            for pregunta in preguntas:
                print(pregunta)
        else:
            preguntas = generar_preguntas(cantidad_preguntas)
            print("Preguntas:")
            for pregunta in preguntas:
                print(pregunta)
        
        print("\nResumen ejecutivo:")
        print(f"Se generaron {cantidad_preguntas} preguntas de entrevista.")
        print(f"La edad calculada para la fecha de nacimiento {sys.argv[2]} es de {edad} años.")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()