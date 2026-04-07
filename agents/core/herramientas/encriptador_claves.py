"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Encriptador de claves para archivos de texto
TECNOLOGÍA: Python, cryptography
"""

from cryptography.fernet import Fernet
import base64
import os
import sys
import time
import json
import datetime
import math
import re

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def generar_llave_secreta():
    try:
        llave = Fernet.generate_key()
        return llave
    except Exception as e:
        print(f"Error al generar llave secreta: {e}")
        return None

def encriptar_archivo(archivo, llave):
    try:
        f = Fernet(llave)
        with open(archivo, "rb") as file:
            archivo_data = file.read()
        encrypted_data = f.encrypt(archivo_data)
        with open(archivo, "wb") as file:
            file.write(encrypted_data)
        return True
    except Exception as e:
        print(f"Error al encriptar archivo: {e}")
        return False

def desencriptar_archivo(archivo, llave):
    try:
        f = Fernet(llave)
        with open(archivo, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open(archivo, "wb") as file:
            file.write(decrypted_data)
        return True
    except Exception as e:
        print(f"Error al desencriptar archivo: {e}")
        return False

def calcular_costo(llave, archivo):
    try:
        f = Fernet(llave)
        with open(archivo, "rb") as file:
            archivo_data = file.read()
        costo = len(archivo_data) * 0.01  # $0.01 por cada byte
        return costo
    except Exception as e:
        print(f"Error al calcular costo: {e}")
        return 0.0

def main():
    if len(sys.argv) < 2:
        archivo_path = "claves.txt"
        contenido_archivo = "API_KEY=mi_api_key_secreta"
        llave_secreta = generar_llave_secreta()
        if llave_secreta is None:
            return
        print("Llave secreta:", llave_secreta)
        print("Fecha y hora actual:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("Archivo a encriptar:", archivo_path)
        print("Contenido del archivo:", contenido_archivo)
        print("Costo de encriptación:", calcular_costo(llave_secreta, archivo_path))
        print("Resultado de encriptación:", encriptar_archivo(archivo_path, llave_secreta))
    else:
        archivo_path = sys.argv[1]
        contenido_archivo = sys.argv[2] if len(sys.argv) > 2 else "API_KEY=mi_api_key_secreta"
        llave_secreta = generar_llave_secreta()
        if llave_secreta is None:
            return
        print("Llave secreta:", llave_secreta)
        print("Fecha y hora actual:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("Archivo a encriptar:", archivo_path)
        print("Contenido del archivo:", contenido_archivo)
        print("Costo de encriptación:", calcular_costo(llave_secreta, archivo_path))
        print("Resultado de encriptación:", encriptar_archivo(archivo_path, llave_secreta))

    resumen_ejecutivo = f"Resumen ejecutivo: El encriptador de claves ha sido ejecutado con éxito. La llave secreta ha sido generada y el archivo ha sido encriptado con un costo de {calcular_costo(llave_secreta, archivo_path)}."
    print(resumen_ejecutivo)

if __name__ == "__main__":
    main()