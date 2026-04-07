#!/usr/bin/env python3
"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Evalúa una zona o colonia de CDMX para inversión inmobiliaria. Analiza plusvalía, seguridad, servicios, demanda de renta y emite un score de 1 a 10 con recomendación.
TECNOLOGÍA: Python estándar
"""
import sys
import json
import math
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def evaluar_zona(colonia, presupuesto):
    try:
        # Plusvalía
        if colonia not in ["Polanco", "Condesa", "Roma", "Juárez", "Cuauhtémoc"]:
            raise ValueError("Colonia no válida")
        
        plusvalia = {
            "Polanco": 0.07,
            "Condesa": 0.05,
            "Roma": 0.04,
            "Juárez": 0.03,
            "Cuauhtémoc": 0.02
        }.get(colonia)
        
        # Seguridad
        seguridad = {
            "Polanco": 9,
            "Condesa": 8,
            "Roma": 7,
            "Juárez": 6,
            "Cuauhtémoc": 5
        }.get(colonia, 4)
        
        # Servicios
        servicios = {
            "Polanco": 9,
            "Condesa": 8,
            "Roma": 7,
            "Juárez": 6,
            "Cuauhtémoc": 5
        }.get(colonia, 4)
        
        # Demanda de renta
        demanda_renta = {
            "Polanco": 8,
            "Condesa": 7,
            "Roma": 6,
            "Juárez": 5,
            "Cuauhtémoc": 4
        }.get(colonia, 3)
        
        # Score
        score = (plusvalia * 25 + seguridad * 25 + servicios * 20 + demanda_renta * 30) / 100
        score = math.ceil(score * 10)
        
        # Recomendación
        if score >= 8:
            recomendacion = "Invierta"
        elif score >= 5:
            recomendacion = "Considere"
        else:
            recomendacion = "No invierta"
        
        return score, recomendacion, plusvalia, seguridad, servicios, demanda_renta
    
    except Exception as e:
        return None, str(e), None, None, None, None

def main():
    if len(sys.argv) < 3:
        print("Uso: python evaluador_zona.py <colonia> <presupuesto>")
        sys.exit(1)
    
    colonia = sys.argv[1]
    try:
        presupuesto = int(sys.argv[2])
    except ValueError:
        print("Error: Presupuesto debe ser un número")
        sys.exit(1)
    
    if presupuesto < 100000:
        print("Error: Presupuesto mínimo es $100,000")
        sys.exit(1)
    
    score, recomendacion, plusvalia, seguridad, servicios, demanda_renta = evaluar_zona(colonia, presupuesto)
    
    if score is None:
        print("Error:", recomendacion)
    else:
        print(f"Colonia: {colonia}")
        print(f"Presupuesto: ${presupuesto}")
        print(f"Plusvalía: {plusvalia * 100}%")
        print(f"Seguridad: {seguridad}/10")
        print(f"Servicios: {servicios}/10")
        print(f"Demanda de renta: {demanda_renta}/10")
        print(f"Score: {score}/10")
        print(f"Recomendación: {recomendacion}")
        print(f"Resumen ejecutivo: La colonia {colonia} es adecuada para la inversión inmobiliaria con un presupuesto de ${presupuesto}.")
    
if __name__ == "__main__":
    main()