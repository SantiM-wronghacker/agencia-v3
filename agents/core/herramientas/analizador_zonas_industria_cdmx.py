import sys
import json
import datetime
import math
import re
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_precio_total(precio_por_metro_cuadrado, area):
    return precio_por_metro_cuadrado * area

def calcular_numero_de_locales(area):
    return math.floor(area / 100)

def obtener_datos_de_zona(zona):
    try:
        with open('zonas_industriales.json') as f:
            datos = json.load(f)
            return datos[zona]
    except FileNotFoundError:
        print(f"Archivo de datos de zonas industriales no encontrado")
        return None
    except KeyError:
        print(f"Zona industrial no encontrada: {zona}")
        return None
    except Exception as e:
        print(f"Error al obtener datos de zona: {e}")
        return None

def obtener_tecnologia(zona):
    try:
        with open('tecnologias.json') as f:
            datos = json.load(f)
            return datos[zona]
    except FileNotFoundError:
        print(f"Archivo de datos de tecnologias no encontrado")
        return None
    except KeyError:
        print(f"Tecnologia no encontrada para zona: {zona}")
        return None
    except Exception as e:
        print(f"Error al obtener tecnologia para zona: {e}")
        return None

def obtener_resumen_ejecutivo(zona, precio_total, numero_de_locales):
    return f"Resumen ejecutivo para zona {zona}: Precio total ${precio_total:.2f}, Número de locales {numero_de_locales}"

def main():
    zona_default = 'Cuauhtemoc'
    precio_default = 5000000
    area_default = 1000
    tecnologia_default = 'Avanzada'

    if len(sys.argv) > 1:
        zona = sys.argv[1]
    else:
        zona = zona_default

    if len(sys.argv) > 2:
        precio = int(sys.argv[2])
    else:
        precio = precio_default

    if len(sys.argv) > 3:
        area = int(sys.argv[3])
    else:
        area = area_default

    if len(sys.argv) > 4:
        tecnologia = sys.argv[4]
    else:
        tecnologia = tecnologia_default

    zonas_industriales = {
        'Cuauhtemoc': {'precio': 5000000, 'area': 1000},
        'Miguel Hidalgo': {'precio': 6000000, 'area': 1200},
        'Alvaro Obregon': {'precio': 5500000, 'area': 1100},
        'Benito Juarez': {'precio': 5800000, 'area': 1150},
        'Coyoacan': {'precio': 5200000, 'area': 1050},
    }

    zona_industrial = obtener_datos_de_zona(zona)
    tecnologia_zona = obtener_tecnologia(zona)

    if zona_industrial and tecnologia_zona:
        print("AREA")
        print(f"Zona industrial: {zona}")
        print(f"Precio por metro cuadrado: ${zona_industrial['precio'] / zona_industrial['area']:.2f}")
        print(f"Area total: {zona_industrial['area']} m2")
        print(f"Precio total: ${zona_industrial['precio']:.2f}")
        print(f"Numero de locales: {calcular_numero_de_locales(zona_industrial['area'])}")
        print(f"Tecnologia: {tecnologia_zona}")
        print("DESCRIPCION")
        print(f"Ubicacion: {zona_industrial['ubicacion']}")
        print(f"Descripcion: {zona_industrial['descripcion']}")
        print("TECNOLOGIA")
        print(f"Tecnologia: {tecnologia_zona}")
        print("RESUMEN EJECUTIVO")
        print(obtener_resumen_ejecutivo(zona, zona_industrial['precio'], calcular_numero_de_locales(zona_industrial['area'])))
    else:
        print("No se pudieron obtener los datos de la zona industrial")

if __name__ == "__main__":
    main()