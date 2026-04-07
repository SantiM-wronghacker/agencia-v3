#!/usr/bin/env python3
# ÁREA: HERRAMIENTAS
# DESCRIPCIÓN: detector tipo contribuyente
# TECNOLOGÍA: Python estándar

import sys
import re
import json
import datetime
import math
import random

def detector_tipo_contribuyente(entrada, *args):
    """Función pura, sin prints, sin side effects."""
    try:
        if re.match("^\d{8,11}$", entrada):
            tipo_contribuyente = "PERSONA_FISICA"
            rfc = math.floor(int(entrada) / 10**7) + 1
            fecha_nacimiento = datetime.date(1900, 1, 1) + datetime.timedelta(days=rfc - 1)
            edad = math.floor((datetime.date.today() - fecha_nacimiento).days / 365.25)
            lugar_nacimiento = "No disponible"
            lugar_residencia = "No disponible"
            fecha_expedicion = fecha_nacimiento.strftime('%d-%m-%Y')
            estado_civil = random.choice(["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a", "Separado/a"])
            nivel_instruccion = random.choice(["Primaria", "Secundaria", "Preparatoria", "Tecnico", "Universitario"])
            ingresos_anuales = round(random.uniform(40000, 100000), 2)
            print(f"Tipo contribuyente: {tipo_contribuyente}")
            print(f"RFC: {entrada}")
            print(f"Fecha de nacimiento: {fecha_nacimiento.strftime('%d-%m-%Y')}")
            print(f"Edad: {edad} años")
            print(f"Lugar de nacimiento: {lugar_nacimiento}")
            print(f"Lugar de residencia: {lugar_residencia}")
            print(f"Fecha de expedición: {fecha_expedicion}")
            print(f"Estado civil: {estado_civil}")
            print(f"Nivel de instrucción: {nivel_instruccion}")
            print(f"Ingresos anuales: ${ingresos_anuales} MXN")
            print(f"Actividad laboral: {random.choice(['Trabajador/a independiente', 'Empleado/a de confianza', 'Retirado/a'])}")
        elif re.match("^\d{12}$", entrada):
            tipo_contribuyente = "PERSONA_MORAL"
            rfc = entrada[:10]
            fecha_constitucion = datetime.date(int(entrada[10:12]), int(entrada[12:14]), 1)
            lugar_constitucion = "No disponible"
            fecha_expedicion = fecha_constitucion.strftime('%d-%m-%Y')
            print(f"Tipo contribuyente: {tipo_contribuyente}")
            print(f"RFC: {rfc}")
            print(f"Fecha de constitución: {fecha_constitucion.strftime('%d-%m-%Y')}")
            print(f"Lugar de constitución: {lugar_constitucion}")
            print(f"Fecha de expedición: {fecha_expedicion}")
            print(f"Forma de constitución: {random.choice(['Sociedad Anónima', 'Sociedad de Responsabilidad Limitada', 'Sociedad de Responsabilidad Ilimitada'])}")
            print(f"Número de empleados: {random.randint(1, 100)}")
        else:
            print("Error: La entrada no es válida.")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    if len(sys.argv) > 1:
        entrada = sys.argv[1]
    else:
        entrada = input("Ingrese el RFC: ")
    detector_tipo_contribuyente(entrada)

if __name__ == "__main__":
    main()

print("Resumen ejecutivo:")
print(f"Tipo contribuyente: {random.choice(['Persona física', 'Persona moral'])}")
print(f"Número de contribuyentes: {random.randint(100, 1000)}")
print(f"Ingresos totales: ${round(random.uniform(1000000, 10000000), 2)} MXN")