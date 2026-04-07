"""
ÁREA: SALUD
DESCRIPCIÓN: Agente que realiza calculadora imc riesgo
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcular_imc(peso, altura):
    return peso / (altura ** 2)

def determinar_riesgo(imc):
    if imc < 18.5:
        return "Bajo peso (Riesgo: Bajo)"
    elif 18.5 <= imc < 25:
        return "Peso normal (Riesgo: Mínimo)"
    elif 25 <= imc < 30:
        return "Sobrepeso (Riesgo: Moderado)"
    elif 30 <= imc < 35:
        return "Obesidad grado I (Riesgo: Alto)"
    elif 35 <= imc < 40:
        return "Obesidad grado II (Riesgo: Muy alto)"
    else:
        return "Obesidad grado III (Riesgo: Extremadamente alto)"

def calcular_porcentaje_grasa(peso, altura):
    return (1.20 * peso / (altura ** 2)) - 10

def calcular_calorias_en_reposo(peso, altura, edad, sexo):
    if sexo.lower() == "hombre":
        return 66 + (6.2 * peso) + (12.7 * altura) - (6.8 * edad)
    elif sexo.lower() == "mujer":
        return 655 + (4.35 * peso) + (4.7 * altura) - (4.7 * edad)

def calcular_necesidad_calorica(diario, actividad):
    if actividad == "sedentario":
        return diario * 1.2
    elif actividad == "ligero":
        return diario * 1.375
    elif actividad == "moderado":
        return diario * 1.55
    elif actividad == "alto":
        return diario * 1.725
    elif actividad == "muy_alto":
        return diario * 1.9

def main():
    try:
        if len(sys.argv) < 6:
            peso = 70  # Default en kg
            altura = 1.75  # Default en metros
            edad = 30  # Default en años
            sexo = "hombre"  # Default
            actividad = "moderado"  # Default
        else:
            peso = float(sys.argv[1])
            altura = float(sys.argv[2])
            edad = int(sys.argv[3])
            sexo = sys.argv[4]
            actividad = sys.argv[5]

        imc = calcular_imc(peso, altura)
        riesgo = determinar_riesgo(imc)
        porcentaje_grasa = calcular_porcentaje_grasa(peso, altura)
        calorias_en_reposo = calcular_calorias_en_reposo(peso, altura, edad, sexo)
        necesidad_calorica = calcular_necesidad_calorica(calorias_en_reposo, actividad)

        print("Cálculo de IMC y riesgo para salud")
        print(f"Peso: {peso} kg")
        print(f"Altura: {altura} m")
        print(f"Edad: {edad} años")
        print(f"Sexo: {sexo}")
        print(f"Actividad física: {actividad}")
        print(f"IMC: {imc:.2f}")
        print(f"Riesgo para la salud: {riesgo}")
        print(f"Porcentaje de grasa corporal: {porcentaje_grasa:.2f}%")
        print(f"Calorías en reposo: {calorias_en_reposo:.2f} kcal")
        print(f"Necesidad calorica diaria: {necesidad_calorica:.2f} kcal")
        print("Resumen ejecutivo:")
        print(f"Para una persona de {edad} años, {sexo}, con un peso de {peso} kg y una altura de {altura} m,")
        print(f"con una actividad física {actividad}, su IMC es {imc:.2f}, lo que indica {riesgo}.")
        print(f"Su porcentaje de grasa corporal es {porcentaje_grasa:.2f}%, y su necesidad calorica diaria es {necesidad_calorica:.2f} kcal.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()