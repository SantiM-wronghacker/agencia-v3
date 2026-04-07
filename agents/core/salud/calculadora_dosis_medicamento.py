"""
ÁREA: SALUD
DESCRIPCIÓN: Agente que realiza calculadora dosis medicamento
TECNOLOGÍA: Python estándar
"""

import sys
import math

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_dosis(peso, edad, medicamento):
    dosis = 0
    if medicamento == "paracetamol":
        dosis = (peso * 10) / 100
    elif medicamento == "ibuprofeno":
        dosis = (peso * 5) / 100
    elif medicamento == "aspirina":
        dosis = (peso * 3) / 100
    return dosis

def calcular_dosis_realista(peso, edad, medicamento):
    dosis = 0
    if medicamento == "paracetamol":
        if edad < 12:
            dosis = (peso * 10) / 100
        elif edad < 18:
            dosis = (peso * 12) / 100
        else:
            dosis = (peso * 15) / 100
    elif medicamento == "ibuprofeno":
        if edad < 12:
            dosis = (peso * 5) / 100
        elif edad < 18:
            dosis = (peso * 7) / 100
        else:
            dosis = (peso * 10) / 100
    elif medicamento == "aspirina":
        if edad < 12:
            dosis = (peso * 3) / 100
        elif edad < 18:
            dosis = (peso * 5) / 100
        else:
            dosis = (peso * 7) / 100
    return dosis

def main():
    try:
        peso = float(sys.argv[1]) if len(sys.argv) > 1 else 70
        edad = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        medicamento = sys.argv[3] if len(sys.argv) > 3 else "paracetamol"
        
        dosis_paracetamol = calcular_dosis(peso, edad, "paracetamol")
        dosis_ibuprofeno = calcular_dosis(peso, edad, "ibuprofeno")
        dosis_aspirina = calcular_dosis(peso, edad, "aspirina")
        
        dosis_paracetamol_realista = calcular_dosis_realista(peso, edad, "paracetamol")
        dosis_ibuprofeno_realista = calcular_dosis_realista(peso, edad, "ibuprofeno")
        dosis_aspirina_realista = calcular_dosis_realista(peso, edad, "aspirina")
        
        print(f"Peso: {peso} kg")
        print(f"Edad: {edad} años")
        print(f"Medicamento: {medicamento}")
        print(f"Dosis de paracetamol (simple): {dosis_paracetamol} mg")
        print(f"Dosis de ibuprofeno (simple): {dosis_ibuprofeno} mg")
        print(f"Dosis de aspirina (simple): {dosis_aspirina} mg")
        print(f"Dosis de paracetamol (realista): {dosis_paracetamol_realista} mg")
        print(f"Dosis de ibuprofeno (realista): {dosis_ibuprofeno_realista} mg")
        print(f"Dosis de aspirina (realista): {dosis_aspirina_realista} mg")
        print(f"Precauciones: No exceder la dosis recomendada. Consultar con un médico antes de tomar cualquier medicamento.")
        print(f"Observaciones: La dosis realista se basa en la edad y el peso del paciente. Es importante consultar con un médico para obtener una dosis personalizada.")
        print("Resumen ejecutivo:")
        print(f"El paciente de {edad} años y {peso} kg puede tomar {dosis_paracetamol_realista} mg de paracetamol, {dosis_ibuprofeno_realista} mg de ibuprofeno o {dosis_aspirina_realista} mg de aspirina.")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Usage: python calculadora_dosis_medicamento.py <peso> <edad> <medicamento>")

if __name__ == "__main__":
    main()