#!/usr/bin/env python3
# AREA: HERRAMIENTAS
# DESCRIPCION: Parseador Fecha Espanol
# TECNOLOGIA: Python 3

import sys
import re
from datetime import datetime
import argparse

def parseador_fecha_espanol(entrada, formato_fecha="%d/%m/%Y", *args):
    """Función pura, sin prints, sin side effects."""
    if not isinstance(entrada, str):
        raise TypeError("La entrada debe ser una cadena de texto")
    
    try:
        patron = re.compile(r"(\d{1,2}) de (enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre) de (\d{4})")
        match = patron.match(entrada)
        if match:
            try:
                dia, mes, anio = match.groups()
                mes_map = {
                    "enero": 1,
                    "febrero": 2,
                    "marzo": 3,
                    "abril": 4,
                    "mayo": 5,
                    "junio": 6,
                    "julio": 7,
                    "agosto": 8,
                    "septiembre": 9,
                    "octubre": 10,
                    "noviembre": 11,
                    "diciembre": 12
                }
                fecha = datetime(int(anio), int(mes_map[mes]), int(dia))
                if fecha.year < 1900 or fecha.year > 2100:
                    raise ValueError("Fecha invalida: año fuera de rango")
                if fecha.month < 1 or fecha.month > 12:
                    raise ValueError("Fecha invalida: mes fuera de rango")
                if fecha.day < 1 or fecha.day > 31:
                    raise ValueError("Fecha invalida: día fuera de rango")
                if fecha.month in [4, 6, 9, 11] and fecha.day > 30:
                    raise ValueError("Fecha invalida: día fuera de rango")
                if fecha.month == 2 and fecha.day > 29:
                    raise ValueError("Fecha invalida: día fuera de rango")
                if fecha.month == 2 and fecha.day == 29 and fecha.year % 4 == 0 and (fecha.year % 100 != 0 or fecha.year % 400 == 0):
                    raise ValueError("Fecha invalida: día fuera de rango")
                if fecha.month == 2 and fecha.day == 29 and fecha.year % 4 != 0:
                    raise ValueError("Fecha invalida: día fuera de rango")
                if fecha.weekday() == 6:
                    raise ValueError("Fecha invalida: día de fin de semana")
                return {
                    "dia": dia,
                    "mes": mes,
                    "anio": anio,
                    "fecha": fecha.strftime(formato_fecha),
                    "dia_semana": fecha.weekday(),
                    "dias_faltantes": (datetime.now() - fecha).days
                }
            except ValueError as e:
                raise ValueError("Error al parsear fecha: " + str(e))
        else:
            raise ValueError("Fecha no encontrada en la entrada")
    except TypeError as e:
        raise TypeError("Error al parsear entrada: " + str(e))

def main():
    parser = argparse.ArgumentParser(description="Parseador de fecha español")
    parser.add_argument("-f", "--entrada", help="Fecha en formato español", required=True)
    parser.add_argument("-o", "--output", help="Formato de salida de la fecha", default="%d/%m/%Y")
    args = parser.parse_args()
    try:
        resultado = parseador_fecha_espanol(args.entrada, args.output)
        print("Resultado:")
        print("Dia:", resultado["dia"])
        print("Mes:", resultado["mes"])
        print("Año:", resultado["anio"])
        print("Fecha:", resultado["fecha"])
        print("Dia de la semana:", resultado["dia_semana"])
        print("Días faltantes:", resultado["dias_faltantes"])
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()