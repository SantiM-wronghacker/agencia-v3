import os
import sys
import json
import datetime
import math
import re
import random
import statistics

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def extraer_precios():
    if WEB:
        return web.extraer_precios()
    else:
        return {
            "materia_prima": float(sys.argv[1]) if len(sys.argv) > 1 else 150.0,
            "energia": float(sys.argv[2]) if len(sys.argv) > 2 else 75.0,
            "mano_de_obra": float(sys.argv[3]) if len(sys.argv) > 3 else 250.0
        }

def calcular_costo(precios):
    return round(precios["materia_prima"] + precios["energia"] + precios["mano_de_obra"], 2)

def calcular_eficiencia(produccion, costo):
    if costo == 0:
        return 0
    return round((produccion / costo) * 100, 2)

def calcular_utilidad(produccion, costo):
    try:
        return round(produccion * 10 - costo, 2)
    except Exception as e:
        return str(e)

def calcular_media(produccion):
    return round(statistics.mean(produccion), 2)

def calcular_desviacion_estandar(produccion):
    return round(statistics.stdev(produccion), 2)

def calcular_dias_productivos(produccion, dias):
    return round(produccion / dias, 2)

def calcular_tasa_productiva(produccion, dias, costo):
    return round((produccion / dias) / (costo / (dias * 8)), 2)

def main():
    try:
        # Datos de ejemplo
        produccion = [int(sys.argv[4]) if len(sys.argv) > 4 else 1000 for _ in range(5)]  # Unidades producidas
        dias = int(sys.argv[5]) if len(sys.argv) > 5 else 30  # Dias de producción
        costo = calcular_costo(extraer_precios())
        eficiencia = calcular_eficiencia(sum(produccion), costo)
        utilidad = calcular_utilidad(sum(produccion), costo)
        media = calcular_media(produccion)
        desviacion_estandar = calcular_desviacion_estandar(produccion)
        dias_productivos = calcular_dias_productivos(sum(produccion), dias)
        tasa_productiva = calcular_tasa_productiva(sum(produccion), dias, costo)

        # Mostrar resultados
        print("ÁREA: MANUFACTURA")
        print("DESCRIPCIÓN: Analizador 5s")
        print("TECNOLOGÍA: Python estándar")
        print("Producción: {0} unidades".format(", ".join(map(str, produccion))))
        print("Costo: {0} MXN".format(costo))
        print("Eficiencia: {0}%".format(eficiencia))
        print("Utilidad: {0} MXN".format(utilidad))
        print("Media de producción: {0} unidades".format(media))
        print("Desviación estándar: {0} unidades".format(desviacion_estandar))
        print("Días productivos: {0} días".format(dias_productivos))
        print("Tasa productiva: {0} unidades/día".format(tasa_productiva))
        print("Resumen ejecutivo: La empresa ha producido {0} unidades en {1} días a un costo de {2} MXN, lo que representa una eficiencia del {3}% y una utilidad de {4} MXN.".format(sum(produccion), dias, costo, eficiencia, utilidad))
    except IndexError:
        print("Error: Faltan argumentos de línea de comandos.")
    except Exception as e:
        print("Error: {0}".format(str(e)))
    finally:
        print("Fin del análisis.")

if __name__ == "__main__":
    main()