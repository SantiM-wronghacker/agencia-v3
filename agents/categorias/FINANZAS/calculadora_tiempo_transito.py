"""
ÁREA: LOGÍSTICA
DESCRIPCIÓN: Agente que realiza calculadora tiempo transito
TECNOLOGÍA: Python estándar
"""

import sys
import json
from datetime import datetime, timedelta

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_tiempo_transito(distancia_km=500, velocidad_promedio=80, tiempo_espera=2):
    """
    Calcula el tiempo de transito basado en la distancia, velocidad promedio y tiempo de espera.
    
    Args:
        distancia_km (float): Distancia en kilómetros. Por defecto es 500 km.
        velocidad_promedio (float): Velocidad promedio en km/h. Por defecto es 80 km/h.
        tiempo_espera (float): Tiempo de espera en horas. Por defecto es 2 horas.
    
    Returns:
        dict: Diccionario con los resultados del cálculo.
    """
    tiempo_conduccion = distancia_km / velocidad_promedio
    tiempo_total = tiempo_conduccion + tiempo_espera
    fecha_hora_actual = datetime.now()
    fecha_hora_llegada = fecha_hora_actual + timedelta(hours=tiempo_total)

    return {
        "distancia_km": distancia_km,
        "velocidad_promedio": velocidad_promedio,
        "tiempo_conduccion_horas": round(tiempo_conduccion, 2),
        "tiempo_espera_horas": tiempo_espera,
        "tiempo_total_horas": round(tiempo_total, 2),
        "fecha_hora_actual": fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S"),
        "fecha_hora_llegada": fecha_hora_llegada.strftime("%Y-%m-%d %H:%M:%S")
    }

def main():
    try:
        if len(sys.argv) > 1:
            try:
                distancia_km = float(sys.argv[1])
            except ValueError:
                distancia_km = 500
                print(f"Advertencia: El valor '{sys.argv[1]}' no es un número. Se utilizará el valor por defecto de 500 km.")
        else:
            distancia_km = 500

        if len(sys.argv) > 2:
            try:
                velocidad_promedio = float(sys.argv[2])
            except ValueError:
                velocidad_promedio = 80
                print(f"Advertencia: El valor '{sys.argv[2]}' no es un número. Se utilizará el valor por defecto de 80 km/h.")
        else:
            velocidad_promedio = 80

        if len(sys.argv) > 3:
            try:
                tiempo_espera = float(sys.argv[3])
            except ValueError:
                tiempo_espera = 2
                print(f"Advertencia: El valor '{sys.argv[3]}' no es un número. Se utilizará el valor por defecto de 2 horas.")
        else:
            tiempo_espera = 2

        resultado = calcular_tiempo_transito(distancia_km, velocidad_promedio, tiempo_espera)
        print("=== CÁLCULO DE TIEMPO DE TRÁNSITO ===")
        print(f"Distancia: {resultado['distancia_km']} km")
        print(f"Velocidad promedio: {resultado['velocidad_promedio']} km/h")
        print(f"Tiempo de conducción: {resultado['tiempo_conduccion_horas']} horas")
        print(f"Tiempo de espera: {resultado['tiempo_espera_horas']} horas")
        print(f"Tiempo total estimado: {resultado['tiempo_total_horas']} horas")
        print(f"Fecha y hora actual: {resultado['fecha_hora_actual']}")
        print(f"Fecha y hora estimada de llegada: {resultado['fecha_hora_llegada']}")
        print("\n=== RESUMEN EJECUTIVO ===")
        print(f"El tiempo total estimado de transito es de {resultado['tiempo_total_horas']} horas, considerando una distancia de {resultado['distancia_km']} km, una velocidad promedio de {resultado['velocidad_promedio']} km/h y un tiempo de espera de {resultado['tiempo_espera_horas']} horas.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()