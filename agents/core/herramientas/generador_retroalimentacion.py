"""
AREA: HERRAMIENTAS
DESCRIPCION: Agente que realiza generador retroalimentacion
TECNOLOGIA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random
from datetime import date

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def generador_retroalimentacion(libro_precio=100, pizarron_precio=50, computadora_precio=200, tipo_de_cambio="20 MXN/USD", noticias=None):
    hoy = date.today()
    if WEB:
        try:
            precios = web.extraer_precios()
            tipo_de_cambio = web.fetch_texto("https://www.banxico.org.mx/tipcubos.html")
            noticias = web.buscar("noticias educación")
        except Exception as e:
            print(f"Error al buscar datos: {e}")
            precios = {"libro": libro_precio, "pizarrón": pizarron_precio, "computadora": computadora_precio}
            noticias = ["Noticia 1", "Noticia 2", "Noticia 3"]
    else:
        precios = {"libro": libro_precio, "pizarrón": pizarron_precio, "computadora": computadora_precio}
        if noticias is None:
            noticias = ["Noticia 1", "Noticia 2", "Noticia 3"]

    print(f"Fecha: {hoy}")
    print(f"Precio del libro: {precios['libro']} MXN")
    print(f"Precio del pizarrón: {precios['pizarrón']} MXN")
    print(f"Precio de la computadora: {precios['computadora']} MXN")
    print(f"Tipo de cambio: {tipo_de_cambio}")
    print(f"Noticias:")
    for noticia in noticias:
        print(f"- {noticia}")
    ipc = math.ceil(precios['libro'] * 0.1 + precios['pizarrón'] * 0.2 + precios['computadora'] * 0.7)
    print(f"Índice de precios al consumidor (IPC): {ipc}")
    ipc_computadora = math.ceil(precios['computadora'] * 1.05)
    print(f"Índice de precios de la computadora: {ipc_computadora}")
    ipc_pizarron = math.ceil(precios['pizarrón'] * 1.1)
    print(f"Índice de precios del pizarrón: {ipc_pizarron}")
    ipc_libro = math.ceil(precios['libro'] * 1.2)
    print(f"Índice de precios del libro: {ipc_libro}")
    print(f"Variación porcentual del IPC: {(ipc - (precios['libro'] + precios['pizarrón'] + precios['computadora'])) / (precios['libro'] + precios['pizarrón'] + precios['computadora']) * 100:.2f}%")
    print(f"Variación porcentual del IPC de la computadora: {(ipc_computadora - precios['computadora']) / precios['computadora'] * 100:.2f}%")
    print(f"Variación porcentual del IPC del pizarrón: {(ipc_pizarron - precios['pizarrón']) / precios['pizarrón'] * 100:.2f}%")
    print(f"Variación porcentual del IPC del libro: {(ipc_libro - precios['libro']) / precios['libro'] * 100:.2f}%")
    print("Resumen ejecutivo:")
    print(f"El IPC actual es de {ipc} y ha variado {(ipc - (precios['libro'] + precios['pizarrón'] + precios['computadora'])) / (precios['libro'] + precios['pizarrón'] + precios['computadora']) * 100:.2f}% con respecto al precio actual de los productos.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        libro_precio = float(sys.argv[1])
        pizarron_precio = float(sys.argv[2])
        computadora_precio = float(sys.argv[3])
        tipo_de_cambio = sys.argv[4]
        noticias = sys.argv[5:]
    else:
        libro_precio = 100
        pizarron_precio = 50