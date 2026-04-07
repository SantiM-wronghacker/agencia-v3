"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Validador de RFC México
TECNOLOGÍA: Python estándar
"""

import sys
import re
import datetime
import math

def validador_rfc_mexico(entrada, patron=None):
    """Función pura, sin prints, sin side effects."""
    if patron is None:
        patron = re.compile(r'^[A-Z]{3}\d{6}[A-Z][ADG]|[A-Z]{4}\d{6}[A-Z][LMNOP][0-9]$')
    try:
        if patron.match(entrada):
            return "VALIDO"
        else:
            return "INVALIDO"
    except Exception as e:
        return f"ERROR: {str(e)}"

def calcular_edadRFC(entrada):
    """Calcula la edad del RFC según la fecha de nacimiento."""
    try:
        fecha_nacimiento = datetime.datetime.strptime(entrada[-10:], '%Y%m%d')
        fecha_actual = datetime.datetime.now()
        edad = (fecha_actual - fecha_nacimiento).days // 365
        return edad
    except ValueError:
        return "Fecha de nacimiento inválida"

def calcular_digitoVerificador(entrada):
    """Calcula el dígito verificador del RFC."""
    try:
        suma = 0
        for i in range(0, 12):
            if i % 2 == 0:
                suma += int(entrada[i]) * 2
            else:
                suma += int(entrada[i])
        digito = (11 - suma % 11) % 10
        return digito
    except Exception as e:
        return f"Error al calcular el dígito verificador: {str(e)}"

def calcular_fecha_nacimiento(entrada):
    """Calcula la fecha de nacimiento según el RFC."""
    try:
        fecha_nacimiento = datetime.datetime.strptime(entrada[-10:], '%Y%m%d')
        return fecha_nacimiento.strftime('%d-%m-%Y')
    except ValueError:
        return "Fecha de nacimiento inválida"

def calcular_dias_vivos(entrada):
    """Calcula los días vivos según la fecha de nacimiento."""
    try:
        fecha_nacimiento = datetime.datetime.strptime(entrada[-10:], '%Y%m%d')
        fecha_actual = datetime.datetime.now()
        dias_vivos = (fecha_actual - fecha_nacimiento).days
        return dias_vivos
    except ValueError:
        return "Fecha de nacimiento inválida"

def main():
    patron = sys.argv[2] if len(sys.argv) > 2 else None
    entrada = sys.argv[1] if len(sys.argv) > 1 else "default_value"
    resultado = validador_rfc_mexico(entrada, patron)
    print(f"RFC: {entrada}")
    print(f"Resultado: {resultado}")
    print(f"Patrón utilizado: {patron if patron else 'Patrón predeterminado'}")
    print(f"Fecha de ejecución: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Edad del RFC: {calcular_edadRFC(entrada)} años")
    print(f"Día de nacimiento: {calcular_fecha_nacimiento(entrada)}")
    print(f"Días vivos: {calcular_dias_vivos(entrada)}")
    print(f"Dígito verificador del RFC: {calcular_digitoVerificador(entrada)}")
    print("Resumen ejecutivo:")
    print("El programa validó el RFC proporcionado según el patrón especificado.")
    print("Si no se proporcionó un patrón, se utilizó el patrón predeterminado.")
    print("Se calcularon la edad del RFC, la fecha de nacimiento, los días vivos y el dígito verificador.")
    print("Si el RFC no es válido, se indicó el error correspondiente.")

if __name__ == "__main__":
    main()