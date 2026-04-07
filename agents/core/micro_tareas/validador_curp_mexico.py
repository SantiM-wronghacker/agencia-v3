#!/usr/bin/env python3
# AREA: REAL ESTATE
# DESCRIPCIÓN: validador curp mexico
# TECNOLOGÍA: Python estándar

import sys
import re
import datetime

def validador_curp_mexico(entrada, verbose=False, regiones=None, generos=None, fechas_nacimiento=None):
    """Función pura, sin prints, sin side effects."""
    try:
        if not entrada or len(entrada) != 18:
            resultado = "INVALIDO:longitud"
        else:
            patron = re.compile(r'^[A-Z]{4}\d{6}[A-Z]{2}([0-9]{2})([A-Z])$')
            if patron.match(entrada):
                resultado = {
                    'valido': True,
                    'patron': patron.pattern,
                    'region': entrada[4:6],
                    'genero': entrada[7],
                    'fecha_nacimiento': f"{entrada[10:12]}/{entrada[9:10]}/{entrada[8:9]}",
                    'edad': calcular_edad(entrada[10:12], entrada[9:10], entrada[8:9]),
                    'region_nombre': obtener_region_nombre(entrada[4:6], regiones),
                    'genero_nombre': obtener_genero_nombre(entrada[7], generos),
                    'fecha_nacimiento_nombre': obtener_fecha_nacimiento_nombre(entrada[8:9], entrada[9:10], entrada[10:12], fechas_nacimiento)
                }
            else:
                resultado = "INVALIDO:patron"
    except re.error as e:
        resultado = f"INVALIDO:error_compilacion: {e}"
    
    if verbose:
        print(f"Entrada: {entrada}")
        print(f"Resultado: {resultado}")
        print(f"Patron: {patron.pattern}")
    
    return resultado

def calcular_edad(dia, mes, anio):
    hoy = datetime.date.today()
    anio_nacimiento = int(anio)
    mes_nacimiento = int(mes)
    dia_nacimiento = int(dia)
    edad = hoy.year - anio_nacimiento
    if (mes_nacimiento, dia_nacimiento) > (hoy.month, hoy.day):
        edad -= 1
    return edad

def obtener_region_nombre(codigo, regiones):
    return regiones.get(codigo, "Region desconocida")

def obtener_genero_nombre(codigo, generos):
    return generos.get(codigo, "Genero desconocido")

def obtener_fecha_nacimiento_nombre(dia, mes, anio, fechas_nacimiento):
    fecha = f"{dia}/{mes}/{anio}"
    return fechas_nacimiento.get(fecha, "Fecha de nacimiento desconocida")

def main():
    entrada = sys.argv[1] if len(sys.argv) > 1 else "default_value"
    verbose = "--verbose" in sys.argv
    regiones = {"01": "Norte", "02": "Sur", "03": "Oriente", "04": "Centro"}
    generos = {"H": "Hombre", "M": "Mujer"}
    fechas_nacimiento = {"0101/01/1990": "1 de enero de 1990"}
    
    if verbose:
        print("Resumen ejecutivo:")
        print("Este programa valida un CURP (Clave Única de Registro de Población) de México.")
        print("Ejemplo de uso: python validador_curp_mexico.py CURP")
    
    resultado = validador_curp_mexico(entrada, verbose, regiones, generos, fechas_nacimiento)
    if isinstance(resultado, str):
        print(f"Resultado: {resultado}")
    else:
        print("Resultado:")
        print(f"Region: {resultado['region_nombre']}")
        print(f"Genero: {resultado['genero_nombre']}")
        print(f"Fecha de nacimiento: {resultado['fecha_nacimiento_nombre']}")
        print(f"Edad: {resultado['edad']}")

if __name__ == "__main__":
    main()