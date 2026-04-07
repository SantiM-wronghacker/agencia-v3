"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que monitorea la conexión a internet y busca información en Google con enfoque en México
TECNOLOGÍA: Python, requests, BeautifulSoup
"""
import os
import platform
import datetime
import time
import requests
from bs4 import BeautifulSoup
import sys
import json

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def ping_google():
    try:
        if platform.system().lower() == 'windows':
            ping_cmd = ['ping', '-n', '1', 'google.com']
        else:
            ping_cmd = ['ping', '-c', '1', 'google.com']

        response = os.system(' '.join(ping_cmd))
        if response == 0:
            return True
        return False
    except Exception as e:
        return False

def guardar_caida():
    try:
        with open('caidas.txt', 'a', encoding='utf-8') as archivo:
            archivo.write(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Caída de conexión\n')
    except Exception as e:
        print(f"Error al guardar caída: {str(e)}")

def buscar_informacion(busqueda):
    url = "https://www.google.com/search"
    params = {"q": busqueda}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        resumen = ""
        resultados = soup.find_all('h3')

        if not resultados:
            return "No se encontraron resultados relevantes"

        for i, resultado in enumerate(resultados[:5]):
            resumen += f"{i+1}. {resultado.text.strip()}\n"

        return resumen
    except requests.exceptions.RequestException as e:
        return f"Error de conexión: {str(e)}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"

def generar_resumen_ejecutivo(busqueda, resultados, conexion_exitosa):
    resumen = f"""
=== RESUMEN EJECUTIVO ===
Fecha: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Búsqueda realizada: {busqueda}
Estado de conexión: {'EXITOSA' if conexion_exitosa else 'FALLIDA'}
Resultados obtenidos: {len(resultados.split('\n')) - 1 if conexion_exitosa else 0}
Última caída registrada: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    return resumen

def main():
    busqueda = sys.argv[1] if len(sys.argv) > 1 else "inmobiliarias más grandes de México"
    intervalo = int(sys.argv[2]) if len(sys.argv) > 2 else 300

    while True:
        try:
            if ping_google():
                resumen = buscar_informacion(busqueda)
                conexion_exitosa = True
                print("=== INFORME DE MONITOREO ===")
                print(f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Búsqueda: {busqueda}")
                print("Resultados encontrados:")
                print(resumen)
                print(generar_resumen_ejecutivo(busqueda, resumen, True))
            else:
                guardar_caida()
                conexion_exitosa = False
                print("=== ALERTA DE CONEXIÓN ===")
                print(f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("Estado: Sin conexión a internet")
                print("Acción: Se ha registrado la caída en caidas.txt")
                print(generar_resumen_ejecutivo(busqueda, "", False))

            time.sleep(intervalo)
        except Exception as e:
            print(f"Error en el proceso principal: {str(e)}")
            time.sleep(intervalo)

if __name__ == '__main__':
    main()