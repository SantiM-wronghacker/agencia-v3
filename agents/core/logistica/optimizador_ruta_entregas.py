"""
ÁREA: LOGÍSTICA
DESCRIPCIÓN: Agente que realiza optimizador ruta entregas
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_distancia(lat1, lon1, lat2, lon2):
    radio_tierra = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    distancia = radio_tierra * c
    return distancia

def calcular_distancia_mexico(lat1, lon1, lat2, lon2):
    radio_tierra = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    distancia = radio_tierra * c
    # Corregir para México
    distancia *= 0.995
    return distancia

def optimizar_ruta_entregas(ubicaciones):
    if len(ubicaciones) < 2:
        return []
    ruta_optima = [ubicaciones[0]]
    ubicaciones_restantes = ubicaciones[1:]
    while ubicaciones_restantes:
        distancia_minima = float('inf')
        siguiente_ubicacion = None
        for ubicacion in ubicaciones_restantes:
            try:
                distancia = calcular_distancia_mexico(ruta_optima[-1]['lat'], ruta_optima[-1]['lon'], ubicacion['lat'], ubicacion['lon'])
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    siguiente_ubicacion = ubicacion
            except KeyError:
                print("Error: ubicación faltante")
        if siguiente_ubicacion is None:
            print("Error: no se pudo encontrar la ubicación mas cercana")
        else:
            ruta_optima.append(siguiente_ubicacion)
            ubicaciones_restantes.remove(siguiente_ubicacion)
    return ruta_optima

def main():
    try:
        if len(sys.argv) < 2:
            ubicaciones = [
                {'lat': 19.4326, 'lon': -99.1332},
                {'lat': 19.4426, 'lon': -99.1432},
                {'lat': 19.4526, 'lon': -99.1532},
                {'lat': 19.4626, 'lon': -99.1632},
                {'lat': 19.4726, 'lon': -99.1732}
            ]
        else:
            ubicaciones = json.loads(sys.argv[1])
        ruta_optima = optimizar_ruta_entregas(ubicaciones)
        distancia_total = 0
        for i in range(len(ruta_optima) - 1):
            distancia = calcular_distancia_mexico(ruta_optima[i]['lat'], ruta_optima[i]['lon'], ruta_optima[i+1]['lat'], ruta_optima[i+1]['lon'])
            distancia_total += distancia
            print(f"Distancia desde {ruta_optima[i]['lat']}, {ruta_optima[i]['lon']} a {ruta_optima[i+1]['lat']}, {ruta_optima[i+1]['lon']}: {distancia:.2f} km")
        print(f"Distancia total: {distancia_total:.2f} km")
        print(f"Ruta óptima: {', '.join([f'{ubicacion['lat']}, {ubicacion['lon']}' for ubicacion in ruta_optima])}")
        print(f"Tiempo de ejecución: {datetime.datetime.now().strftime('%H:%M:%S')}")
    except json.JSONDecodeError:
        print("Error: formato de JSON inválido")
    except KeyError:
        print("Error: falta información en las ubicaciones")

if __name__ == "__main__":
    main()