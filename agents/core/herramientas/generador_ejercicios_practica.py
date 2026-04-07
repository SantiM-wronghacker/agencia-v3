"""
ÁREA: EDUCACIÓN
DESCRIPCIÓN: Agente que realiza generador de ejercicios de práctica
TECNOLOGÍA: Python estándar
"""
import sys
import random
import datetime
import json
import math
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def generar_ejercicios(cantidad=5, temas=None, niveles=None, dificultad=None):
    if temas is None:
        temas = ["matemáticas", "español", "historia", "ciencias", "geografía"]
    if niveles is None:
        niveles = ["primaria", "secundaria", "preparatoria"]
    if dificultad is None:
        dificultad = ["baja", "media", "alta"]
    
    ejercicios = []
    for _ in range(cantidad):
        tema = random.choice(temas)
        nivel = random.choice(niveles)
        fecha = datetime.date.today().strftime("%d/%m/%Y")
        duracion = math.ceil(random.uniform(30, 90))  # Duración en minutos con precisión de 1 minuto
        problemas = math.ceil(random.uniform(5, 20))  # Problemas entre 5 y 20
        objetivos = [
            f"Comprender conceptos básicos de {tema}",
            f"Desarrollar habilidades de resolución de problemas en {tema}",
            f"Aplicar conocimientos de {tema} en situaciones reales"
        ]
        materiales = [
            f"Libro de texto de {tema}",
            f"Cuaderno y lápiz",
            f"Calculadora"
        ]
        ejercicio = {
            "tema": tema,
            "nivel": nivel,
            "fecha": fecha,
            "ejercicio": f"Ejercicio de {tema} para {nivel} - {problemas} problemas",
            "duracion": f"{duracion} minutos",
            "dificultad": random.choice(dificultad),
            "objetivos": objetivos,
            "materiales": materiales
        }
        ejercicios.append(ejercicio)
    
    return ejercicios

def main():
    try:
        if len(sys.argv) > 1:
            cantidad = int(sys.argv[1])
        else:
            cantidad = 5
        if len(sys.argv) > 2:
            temas = sys.argv[2].split(",")
        else:
            temas = ["matemáticas", "español", "historia", "ciencias", "geografía"]
        if len(sys.argv) > 3:
            niveles = sys.argv[3].split(",")
        else:
            niveles = ["primaria", "secundaria", "preparatoria"]
        if len(sys.argv) > 4:
            dificultad = sys.argv[4].split(",")
        else:
            dificultad = ["baja", "media", "alta"]
        
        ejercicios = generar_ejercicios(cantidad, temas, niveles, dificultad)
        
        for i, ejercicio in enumerate(ejercicios):
            print(f"Ejercicio {i+1}:")
            print(f"Tema: {ejercicio['tema']}")
            print(f"Nivel: {ejercicio['nivel']}")
            print(f"Fecha: {ejercicio['fecha']}")
            print(f"Ejercicio: {ejercicio['ejercicio']}")
            print(f"Duración: {ejercicio['duracion']}")
            print(f"Dificultad: {ejercicio['dificultad']}")
            print(f"Objetivos:")
            for objetivo in ejercicio['objetivos']:
                print(f"- {objetivo}")
            print(f"Materiales:")
            for material in ejercicio['materiales']:
                print(f"- {material}")
            print("\n")
        
        print("Resumen ejecutivo:")
        print(f"Se generaron {len(ejercicios)} ejercicios de práctica para {cantidad} temas.")
    
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()