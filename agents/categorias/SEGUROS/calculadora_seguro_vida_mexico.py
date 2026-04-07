"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora seguro vida mexico
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcula_seguro_vida(edad, sexo, estado_civil, ingresos_mensuales, dependientes):
    try:
        if edad < 0 or edad > 120:
            raise ValueError("Edad inválida")
        if sexo not in ['M', 'F']:
            raise ValueError("Sexo inválido")
        if estado_civil not in ['S', 'C', 'D']:
            raise ValueError("Estado civil inválido")
        if ingresos_mensuales < 0:
            raise ValueError("Ingresos mensuales no pueden ser negativos")
        if dependientes < 0:
            raise ValueError("Número de dependientes no puede ser negativo")
    except ValueError as e:
        print(f"Error: {e}")
        return None

    prima_base = 800.0  
    ajuste_edad = 0.05 * (edad - 25)
    ajuste_sexo = 0.1 if sexo == 'M' else -0.05
    ajuste_estado_civil = 0.05 if estado_civil == 'C' else 0.0
    ajuste_ingresos = 0.01 * (ingresos_mensuales / 15000.0)  
    ajuste_dependientes = 0.05 * dependientes
    prima = prima_base + ajuste_edad + ajuste_sexo + ajuste_estado_civil + ajuste_ingresos + ajuste_dependientes
    return prima

def calcula_prima_anual(prima):
    return prima * 12

def calcula_prima_mensual(prima):
    return prima / 12

def calcula_prima_trimestral(prima):
    return prima * 3

def calcula_prima_semestral(prima):
    return prima * 6

def calcula_prima_con_iva(prima):
    return prima * 1.16

def calcula_prima_con_descuento(prima):
    return prima * 12 * 0.95

def main():
    try:
        edad = int(sys.argv[1]) if len(sys.argv) > 1 else 30
        sexo = sys.argv[2] if len(sys.argv) > 2 else 'M'
        estado_civil = sys.argv[3] if len(sys.argv) > 3 else 'S'
        ingresos_mensuales = int(sys.argv[4]) if len(sys.argv) > 4 else 25000
        dependientes = int(sys.argv[5]) if len(sys.argv) > 5 else 2
        prima = calcula_seguro_vida(edad, sexo, estado_civil, ingresos_mensuales, dependientes)
        
        if prima is None:
            return

        print(f'Datos del asegurado:')
        print(f'Edad: {edad} años')
        print(f'Sexo: {sexo}')
        print(f'Estado civil: {estado_civil}')
        print(f'Ingresos mensuales: ${ingresos_mensuales:,.2f} MXN')
        print(f'Dependientes: {dependientes} personas')
        print(f'Prima del seguro de vida: ${prima:,.2f} MXN')
        print(f'Prima anual del seguro de vida: ${calcula_prima_anual(prima):,.2f} MXN')
        print(f'Prima mensual del seguro de vida: ${calcula_prima_mensual(prima):,.2f} MXN')
        print(f'Prima trimestral del seguro de vida: ${calcula_prima_trimestral(prima):,.2f} MXN')
        print(f'Prima semestral del seguro de vida: ${calcula_prima_semestral(prima):,.2f} MXN')
        print(f'Prima con IVA del seguro de vida: ${calcula_prima_con_iva(prima):,.2f} MXN')
        print(f'Prima con descuento del seguro de vida: ${calcula_prima_con_descuento(prima):,.2f} MXN')
        print(f'Resumen ejecutivo: El seguro de vida cuesta ${prima:,.2f} MXN al año, lo que equivale a ${calcula_prima_mensual(prima):,.2f} MXN al mes.')
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()