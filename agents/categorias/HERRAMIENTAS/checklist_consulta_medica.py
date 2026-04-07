"""
ÁREA: SALUD
DESCRIPCIÓN: Agente que realiza checklist consulta medica
TECNOLOGÍA: Python estándar
"""

import sys
import os
import json
import datetime
import random
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_imc(peso, altura):
    return round(peso / (altura ** 2), 2)

def calcular_clasificacion_imc(imc):
    if imc < 18.5:
        return "Bajo peso"
    elif imc < 25:
        return "Normal"
    elif imc < 30:
        return "Sobrepeso"
    else:
        return "Obesidad"

def calcular_presion_arterial_sistolica(presion_arterial):
    return int(presion_arterial.split('/')[0])

def calcular_presion_arterial_diastolica(presion_arterial):
    return int(presion_arterial.split('/')[1])

def main():
    try:
        # Parámetros por defecto
        nombre_paciente = sys.argv[1] if len(sys.argv) > 1 else "Juan Pérez"
        edad = int(sys.argv[2]) if len(sys.argv) > 2 else 45
        peso = float(sys.argv[3]) if len(sys.argv) > 3 else 72.5
        altura = float(sys.argv[4]) if len(sys.argv) > 4 else 1.70
        fecha_consulta = sys.argv[5] if len(sys.argv) > 5 else datetime.date.today().isoformat()

        # Generar datos de ejemplo
        temperatura = round(random.uniform(36.0, 37.5), 1)
        presion_arterial = f"{random.randint(100, 140)}/{random.randint(60, 90)}"
        frecuencia_cardiaca = random.randint(60, 100)
        glucosa = random.randint(70, 120)
        imc = calcular_imc(peso, altura)
        clasificacion_imc = calcular_clasificacion_imc(imc)
        presion_arterial_sistolica = calcular_presion_arterial_sistolica(presion_arterial)
        presion_arterial_diastolica = calcular_presion_arterial_diastolica(presion_arterial)

        # Generar informe
        print(f"Paciente: {nombre_paciente} (Edad: {edad}, Peso: {peso} kg, Altura: {altura} m)")
        print(f"Fecha de consulta: {fecha_consulta}")
        print(f"Temperatura: {temperatura}°C | Presión arterial: {presion_arterial} mmHg")
        print(f"Presión arterial sistólica: {presion_arterial_sistolica} mmHg | Presión arterial diastólica: {presion_arterial_diastolica} mmHg")
        print(f"Frecuencia cardíaca: {frecuencia_cardiaca} lpm | Glucosa: {glucosa} mg/dL")
        print(f"IMC: {imc} (Clasificación: {clasificacion_imc})")
        print(f"Recomendaciones: {random.choice(['Controlar dieta', 'Ejercicio moderado', 'Revisión en 3 meses', 'Analíticas completas'])}")
        print(f"Observaciones: El paciente {nombre_paciente} debe realizar un seguimiento médico para controlar su {random.choice(['presión arterial', 'glucosa', 'frecuencia cardíaca'])}.")
        print(f"Plan de tratamiento: Se recomienda al paciente {nombre_paciente} {random.choice(['realizar ejercicio físico regularmente', 'reducir el consumo de sal', 'aumentar el consumo de frutas y verduras'])}.")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"Paciente: {nombre_paciente}")
        print(f"Edad: {edad} años")
        print(f"Peso: {peso} kg")
        print(f"Altura: {altura} m")
        print(f"IMC: {imc} ({clasificacion_imc})")
        print(f"Recomendaciones: {random.choice(['Controlar dieta', 'Ejercicio moderado', 'Revisión en 3 meses', 'Analíticas completas'])}")

    except Exception as e:
        print(f"Error en el proceso: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()