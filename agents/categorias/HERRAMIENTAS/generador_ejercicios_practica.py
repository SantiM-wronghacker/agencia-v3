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

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def generar_ejercicios(cantidad=5, temas=None, niveles=None):
    if temas is None:
        temas = ["matemáticas", "español", "historia", "ciencias", "geografía"]
    if niveles is None:
        niveles = ["primaria", "secundaria", "preparatoria"]
    
    ejercicios = []
    for _ in range(cantidad):
        tema = random.choice(temas)
        nivel = random.choice(niveles)
        fecha = datetime.date.today().strftime("%d/%m/%Y")
        dificultad = random.choice(["baja", "media", "alta"])
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
            "dificultad": dificultad,
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
            temas = None
        if len(sys.argv) > 3:
            niveles = sys.argv[3].split(",")
        else:
            niveles = None
        try:
            ejercicios = generar_ejercicios(cantidad, temas, niveles)
        except Exception as e:
            print(f"Error: {e}")
            return
        
        print(f"ÁREA: EDUCACIÓN")
        print(f"DESCRIPCIÓN: Agente que realiza generador de ejercicios de práctica")
        print(f"TECNOLOGÍA: Python estándar")
        print(f"Cantidad de ejercicios generados: {len(ejercicios)}")
        print("Ejercicios generados:")
        for idx, ejercicio in enumerate(ejercicios, 1):
            print(f"{idx}. {ejercicio['tema']} - {ejercicio['nivel']} - {ejercicio['dificultad']}")
        
        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"Se han generado {len(ejercicios)} ejercicios de práctica para {cantidad} temas y niveles.")
        print(f"Los ejercicios incluyen objetivos y materiales para cada tema y nivel.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()