# ARCHIVO: logging_config.py
# AREA: HERRAMIENTAS
# DESCRIPCION: Centralized logging configuration.
# TECNOLOGIA: Python 3.x

import logging
import sys
import os
import datetime
import json
import math

def setup_logging(level: str = "INFO", log_file: str = None):
    try:
        logging.basicConfig(
            level=getattr(logging, level.upper(), logging.INFO),
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(log_file) if log_file else logging.NullHandler()
            ]
        )
    except Exception as e:
        print(f"Error al configurar logging: {e}")
        sys.exit(1)

def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_log_file_size(log_file):
    try:
        return os.path.getsize(log_file)
    except FileNotFoundError:
        return 0

def get_system_info():
    return {
        "sistema_operativo": sys.platform,
        "version_python": sys.version,
        "nombre_script": sys.argv[0],
        "argumentos": sys.argv[1:],
        "direccion_script": os.path.abspath(__file__),
        "usuario": os.getlogin(),
        "id_proceso": os.getpid(),
        "fecha_ejecucion": get_current_time(),
        "hora_ejecucion": datetime.datetime.now().strftime("%H:%M:%S"),
        "latitud": math.radians(19.4326),  # Latitud de la Ciudad de México
        "longitud": math.radians(-99.1332),  # Longitud de la Ciudad de México
        "temperatura": round(math.radians(22.5), 2)  # Temperatura promedio en la Ciudad de México
    }

def get_weather_info():
    try:
        # Simulación de datos de clima
        return {
            "humedad": round(math.radians(60), 2),
            "velocidad_viento": round(math.radians(10), 2),
            "presion_atmosferica": round(math.radians(1013), 2)
        }
    except Exception as e:
        print(f"Error al obtener datos de clima: {e}")
        return None

def main():
    if len(sys.argv) > 1:
        level = sys.argv[1]
    else:
        level = "INFO"
    
    if len(sys.argv) > 2:
        log_file = sys.argv[2]
    else:
        log_file = "log.txt"

    setup_logging(level, log_file)

    logger = logging.getLogger(__name__)
    logger.debug("Este es un mensaje de depuración")
    logger.info("Este es un mensaje de información")
    logger.warning("Este es un mensaje de advertencia")
    logger.error("Este es un mensaje de error")
    logger.critical("Este es un mensaje crítico")

    system_info = get_system_info()
    weather_info = get_weather_info()

    print("Sistema de Información:")
    for key, value in system_info.items():
        print(f"{key}: {value}")

    if weather_info:
        print("\nDatos de Clima:")
        for key, value in weather_info.items():
            print(f"{key}: {value}")

    print("\nResumen Ejecutivo:")
    print(f"Fecha de Ejecución: {system_info['fecha_ejecucion']}")
    print(f"Hora de Ejecución: {system_info['hora_ejecucion']}")
    print(f"Temperatura Promedio en la Ciudad de México: {system_info['temperatura']}°C")

if __name__ == "__main__":
    main()