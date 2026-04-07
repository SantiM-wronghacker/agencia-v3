#!/usr/bin/env python3
"""
ÁREA: FINANZAS
DESCRIPCIÓN: calculadora isr mensual rapido
TECNOLOGÍA: Python estándar
"""

import sys
import re
import json
import math
from datetime import date
import os

def calculadora_isr_mensual_rapido(ingresos_brutos, tasa_isr=0.15, dias_trabajados=30):
    """Función pura, sin prints, sin side effects."""
    try:
        ingresos_brutos = float(ingresos_brutos)
        dias_trabajados = int(dias_trabajados)
        if dias_trabajados < 1:
            return "INVALIDO:dias_trabajados_invalido"
        if ingresos_brutos < 0:
            return "INVALIDO:ingresos_brutos_invalido"
        if tasa_isr < 0 or tasa_isr > 1:
            return "INVALIDO:tasa_isr_invalida"
        
        # ISR diario y mensual
        isr_diario = ingresos_brutos * tasa_isr / dias_trabajados
        isr_mensual = ingresos_brutos * tasa_isr
        
        # ISR anual
        isr_anual = ingresos_brutos * tasa_isr * 12
        
        # ISR diario y mensual promedio
        isr_diario_promedio = isr_diario * 30
        isr_mensual_promedio = isr_mensual * 12
        
        # Aguinaldo
        aguinaldo = ingresos_brutos * 0.025 * dias_trabajados
        
        # Prima vacacional
        prima_vacacional = ingresos_brutos * 0.025 * dias_trabajados
        
        # Salario base para ISR
        salario_base_isr = ingresos_brutos - (aguinaldo + prima_vacacional)
        
        # ISR diario y mensual con salario base
        isr_diario_salario_base = salario_base_isr * tasa_isr / dias_trabajados
        isr_mensual_salario_base = salario_base_isr * tasa_isr
        
        # ISR anual con salario base
        isr_anual_salario_base = salario_base_isr * tasa_isr * 12
        
        # ISR diario y mensual con salario base promedio
        isr_diario_promedio_salario_base = isr_diario_salario_base * 30
        isr_mensual_promedio_salario_base = isr_mensual_salario_base * 12
        
        # Resumen ejecutivo
        resumen_ejecutivo = f"""
ISR diario: ${isr_diario:,.2f} MXN
ISR mensual: ${isr_mensual:,.2f} MXN
ISR anual: ${isr_anual:,.2f} MXN
ISR diario promedio: ${isr_diario_promedio:,.2f} MXN
ISR mensual promedio: ${isr_mensual_promedio:,.2f} MXN
Aguinaldo: ${aguinaldo:,.2f} MXN
Prima vacacional: ${prima_vacacional:,.2f} MXN
Salario base para ISR: ${salario_base_isr:,.2f} MXN
ISR diario con salario base: ${isr_diario_salario_base:,.2f} MXN
ISR mensual con salario base: ${isr_mensual_salario_base:,.2f} MXN
ISR anual con salario base: ${isr_anual_salario_base:,.2f} MXN
ISR diario promedio con salario base: ${isr_diario_promedio_salario_base:,.2f} MXN
ISR mensual promedio con salario base: ${isr_mensual_promedio_salario_base:,.2f} MXN
"""
        
        return resumen_ejecutivo
    
    except ValueError:
        return "INVALIDO:ingresos_brutos_invalido o dias_trabajados_invalido"
    
    except Exception as e:
        return f"INVALIDO: {str(e)}"

def main():
    if len(sys.argv) > 1:
        ingresos_brutos = sys.argv[1]
        tasa_isr = sys.argv[2]
        dias_trabajados = sys.argv[3]
        print(calculadora_isr_mensual_rapido(ingresos_brutos, tasa_isr, dias_trabajados))
    else:
        ingresos_brutos = input("Ingrese los ingresos brutos: ")
        tasa_isr = input("Ingrese la tasa de ISR (porcentaje): ")
        dias_trabajados = input("Ingrese los días trabajados: ")