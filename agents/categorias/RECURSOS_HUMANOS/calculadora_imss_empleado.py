"""
ÁREA: FINANZAS
DESCRIPCIÓN: Calculadora IMSS empleado
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calculadora_imss_empleado(salario_base, prima_base=0.05, fondo_pension_base=0.07, fondo_cesantias_base=0.01):
    try:
        salario_base = float(salario_base)
        if salario_base < 0:
            return "INVALIDO: salario_base negativo"
        if salario_base > 25000:
            return "INVALIDO: salario_base excede el límite"
        if salario_base <= 1000:
            prima = salario_base * prima_base
            fondo_pension = salario_base * fondo_pension_base
            fondo_cesantias = salario_base * fondo_cesantias_base
            descuento_prima = 0
            descuento_fondo_pension = 0
            descuento_fondo_cesantias = 0
        elif salario_base <= 1500:
            prima = salario_base * prima_base
            fondo_pension = salario_base * (fondo_pension_base + 0.01)
            fondo_cesantias = salario_base * (fondo_cesantias_base + 0.005)
            descuento_prima = 0
            descuento_fondo_pension = salario_base * 0.01
            descuento_fondo_cesantias = salario_base * 0.005
        elif salario_base <= 2500:
            prima = salario_base * prima_base
            fondo_pension = salario_base * (fondo_pension_base + 0.03)
            fondo_cesantias = salario_base * (fondo_cesantias_base + 0.01)
            descuento_prima = 0
            descuento_fondo_pension = salario_base * 0.03
            descuento_fondo_cesantias = salario_base * 0.01
        else:
            prima = salario_base * prima_base
            fondo_pension = salario_base * (fondo_pension_base + 0.04)
            fondo_cesantias = salario_base * (fondo_cesantias_base + 0.015)
            descuento_prima = 0
            descuento_fondo_pension = salario_base * 0.04
            descuento_fondo_cesantias = salario_base * 0.015
        total_descuentos = descuento_prima + descuento_fondo_pension + descuento_fondo_cesantias
        total_pagar = salario_base - total_descuentos
        return f"""
salario_base: {salario_base}
prima: {prima}
fondo_pension: {fondo_pension}
fondo_cesantias: {fondo_cesantias}
descuento_prima: {descuento_prima}
descuento_fondo_pension: {descuento_fondo_pension}
descuento_fondo_cesantias: {descuento_fondo_cesantias}
total_descuentos: {total_descuentos}
total_pagar: {total_pagar}
"""
    except ValueError:
        return "INVALIDO: no numerico"
    except Exception as e:
        return f"INVALIDO: {str(e)}"

def main():
    salario_base = sys.argv[1] if len(sys.argv) > 1 else "1000"
    prima_base = sys.argv[2] if len(sys.argv) > 2 else "0.05"
    fondo_pension_base = sys.argv[3] if len(sys.argv) > 3 else "0.07"
    fondo_cesantias_base = sys.argv[4] if len(sys.argv) > 4 else "0.01"
    resultado = calculadora_imss_empleado(salario_base, prima_base, fondo_pension_base, fondo_cesantias_base)
    print(resultado)
    print("Resumen ejecutivo:")
    print("El salario base de ${} con prima de {}%, fondo pension de {}% y fondo cesantias de {}%".format(salario_base, prima_base*100, fondo_pension_base*100, fondo_cesantias_base*100))
    print("Genera un total de descuentos de ${} y un total a pagar de ${}".format(resultado.split("\n")[-2].split(":")[1].strip(), resultado.split("\n")[-1].split(":")[1].strip()))

if __name__ == "__main__":
    main()