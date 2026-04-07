"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora calorias actividad
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcular_calorias(edad, peso, altura, actividad, tiempo):
    """Calcula calorias quemadas en actividad física."""
    try:
        if actividad not in ["caminar", "correr", "nadar", "ciclismo", "baile", "fútbol"]:
            raise ValueError("Actividad no válida")

        if tiempo <= 0:
            raise ValueError("Tiempo debe ser mayor que 0")

        if edad < 0 or peso < 0 or altura < 0 or tiempo < 0:
            raise ValueError("Valores no pueden ser negativos")

        if actividad == "caminar":
            met = 3.5
        elif actividad == "correr":
            met = 8.0
        elif actividad == "nadar":
            met = 6.0
        elif actividad == "ciclismo":
            met = 7.0
        elif actividad == "baile":
            met = 4.5
        elif actividad == "fútbol":
            met = 8.5
        else:
            raise ValueError("Actividad no válida")

        calorias = (met * peso * tiempo) / 200 * 0.85  # ajuste para México
        return round(calorias, 2)
    except ValueError as e:
        print(f"Error: {e}")
        return None

def calcular_calorias_basal(peso, altura, edad):
    """Calcula calorias basales."""
    try:
        if edad < 0 or peso < 0 or altura < 0:
            raise ValueError("Valores no pueden ser negativos")

        calorias_basal = 66 + (6.2 * peso) + (12.7 * altura) - (6.8 * edad)
        return round(calorias_basal, 2)
    except ValueError as e:
        print(f"Error: {e}")
        return None

def calcular_imc(peso, altura):
    """Calcula índice de masa corporal."""
    try:
        if peso < 0 or altura < 0:
            raise ValueError("Valores no pueden ser negativos")

        imc = peso / (altura / 100) ** 2
        if imc < 18.5:
            return "Peso bajo"
        elif imc < 25:
            return "Peso normal"
        elif imc < 30:
            return "Sobrepeso"
        elif imc < 35:
            return "Obesidad grado I"
        elif imc < 40:
            return "Obesidad grado II"
        else:
            return "Obesidad grado III"
    except ValueError as e:
        print(f"Error: {e}")
        return None

def main():
    if len(sys.argv) < 6:
        edad = 30
        peso = 70  # kg
        altura = 170  # cm
        actividad = "caminar"
        tiempo = 30  # minutos
    else:
        edad = int(sys.argv[1])
        peso = float(sys.argv[2])
        altura = float(sys.argv[3])
        actividad = sys.argv[4]
        tiempo = float(sys.argv[5])

    calorias = calcular_calorias(edad, peso, altura, actividad, tiempo)
    calorias_basal = calcular_calorias_basal(peso, altura, edad)
    imc = calcular_imc(peso, altura)

    print(f"Edad: {edad} años")
    print(f"Peso: {peso} kg")
    print(f"Altura: {altura} cm")
    print(f"Actividad: {actividad}")
    print(f"Tiempo: {tiempo} minutos")
    print(f"Calorias quemadas: {calorias} kcal")
    print(f"Calorias basales: {calorias_basal} kcal")
    print(f"Índice de masa corporal: {imc}")

    if calorias:
        print(f"Porcentaje de calorias quemadas en relación con calorias basales: {(calorias / calorias_basal) * 100}%")
    else:
        print("No se pudo calcular el porcentaje de calorias quemadas en relación con calorias basales")

if __name__ == "__main__":
    main()