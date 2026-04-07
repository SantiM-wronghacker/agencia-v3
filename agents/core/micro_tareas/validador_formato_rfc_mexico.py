# AREA: REAL ESTATE
# DESCRIPCION: Agente que realiza validador formato rfc mexico
# TECNOLOGIA: Python

import sys
import re
import datetime
import math

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        rfc = sys.argv[1] if len(sys.argv) > 1 else "PEM180101HTCSDN09"
        patron = re.compile(r'^[A-Z]{4}\d{6}[A-Z0-9]{3}$')
        if patron.match(rfc):
            print("RFC:", rfc)
            fecha_nacimiento = datetime.datetime(int("19" + rfc[8:10]) if int(rfc[8:10]) > 50 else "20" + rfc[8:10], int(rfc[4:6]), int(rfc[6:8]))
            print("Fecha de nacimiento:", fecha_nacimiento.strftime("%d/%m/%Y"))
            lugar_nacimiento = obtener_lugar_nacimiento(rfc[11])
            print("Lugar de nacimiento:", lugar_nacimiento)
            tipo_persona = "Fisica" if rfc[10] in "0123456789" else "Moral"
            print("Tipo de persona:", tipo_persona)
            homoclave = rfc[9]
            print("Homoclave:", homoclave)
            genero = "Masculino" if rfc[10] in "012345678" else "Femenino"
            print("Genero:", genero)
            edad = calcular_edad(fecha_nacimiento)
            print("Edad:", edad)
            estado_civil = "Soltero" if rfc[10] in "0123" else "Casado" if rfc[10] in "4567" else "Divorciado" if rfc[10] in "89" else "Viudo"
            print("Estado civil:", estado_civil)
            nacionalidad = "Mexicana" if rfc[11] != "32" else "Extranjera"
            print("Nacionalidad:", nacionalidad)
            print("Resumen:")
            print("El RFC proporcionado es valido y pertenece a una persona", tipo_persona)
            print("con fecha de nacimiento", fecha_nacimiento.strftime("%d/%m/%Y"))
            print("y lugar de nacimiento en", lugar_nacimiento)
            print("La persona tiene", edad, "años de edad.")
            print("Su estado civil es", estado_civil)
            print("Y su nacionalidad es", nacionalidad)
        else:
            print("RFC no valido")
    except Exception as e:
        print("Error:", str(e))

def obtener_lugar_nacimiento(clave):
    lugares = {
        "0": "Ciudad de Mexico",
        "1": "Aguascalientes",
        "2": "Baja California",
        "3": "Baja California Sur",
        "4": "Campeche",
        "5": "Chiapas",
        "6": "Chihuahua",
        "7": "Coahuila",
        "8": "Colima",
        "9": "Durango",
        "10": "Guanajuato",
        "11": "Guerrero",
        "12": "Hidalgo",
        "13": "Jalisco",
        "14": "Estado de Mexico",
        "15": "Michoacan",
        "16": "Morelos",
        "17": "Nayarit",
        "18": "Nuevo Leon",
        "19": "Oaxaca",
        "20": "Puebla",
        "21": "Queretaro",
        "22": "Quintana Roo",
        "23": "San Luis Potosi",
        "24": "Sinaloa",
        "25": "Sonora",
        "26": "Tabasco",
        "27": "Tamaulipas",
        "28": "Tlaxcala",
        "29": "Veracruz",
        "30": "Yucatan",
        "31": "Zacatecas",
        "32": "Extranjero"
    }
    return lugares.get(clave, "Clave no encontrada")

def calcular_edad(fecha_nacimiento):
    hoy = datetime.datetime.now()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

if __name__ == "__main__":
    main()