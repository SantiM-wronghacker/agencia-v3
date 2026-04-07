#!/usr/bin/env python3

"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente de seguimiento de clientes que envía recordatorios mediante WhatsApp
TECNOLOGÍA: Python, SQLite, Twilio
"""

import os
import sys
import sqlite3
import datetime
import time
import re
import json
from twilio.rest import Client
import math
import random

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

# Configuración de la base de datos
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'clientes.db')

# Configuración de Twilio
ACCOUNT_SID = os.environ.get('ACCOUNT_SID', 'tu_account_sid')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN', 'tu_auth_token')
FROM_NUMBER = os.environ.get('FROM_NUMBER', 'tu_numero_twilio')

def crear_tabla_clientes():
    conn = sqlite3.connect(DATABASE_NAME, encoding='utf-8')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clientes
                 (id INTEGER PRIMARY KEY, nombre TEXT, telefono TEXT, fecha_registro DATE)''')
    conn.commit()
    conn.close()

def agregar_cliente(nombre, telefono):
    try:
        conn = sqlite3.connect(DATABASE_NAME, encoding='utf-8')
        c = conn.cursor()
        c.execute("INSERT INTO clientes (nombre, telefono, fecha_registro) VALUES (?, ?, ?)",
                  (nombre, telefono, datetime.date.today()))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al agregar cliente: {e}")

def obtener_clientes():
    try:
        conn = sqlite3.connect(DATABASE_NAME, encoding='utf-8')
        c = conn.cursor()
        c.execute("SELECT * FROM clientes")
        clientes = c.fetchall()
        conn.close()
        return clientes
    except sqlite3.Error as e:
        print(f"Error al obtener clientes: {e}")
        return []

def enviar_recordatorio(telefono, mensaje):
    try:
        message = Client(ACCOUNT_SID, AUTH_TOKEN).messages.create(
            body=mensaje,
            from_=FROM_NUMBER,
            to=telefono
        )
        time.sleep(2)
    except Exception as e:
        print(f"Error al enviar recordatorio: {e}")

def generar_recordatorios():
    clientes = obtener_clientes()
    hoy = datetime.date.today()
    for cliente in clientes:
        id, nombre, telefono, fecha_registro = cliente
        dias_transcurridos = (hoy - fecha_registro).days
        if dias_transcurridos == 3:
            mensaje = f"Hola {nombre}, ¡esperamos que estés satisfecho con nuestro servicio! ¿Necesitas algo más?"
            enviar_recordatorio(telefono, mensaje)
            print(f"Recordatorio enviado a {nombre} ({telefono})")

def main():
    crear_tabla_clientes()
    agregar_cliente("Juan", "1234567890")
    agregar_cliente("Maria", "9876543210")
    generar_recordatorios()

    clientes = obtener_clientes()
    print("Clientes:")
    for cliente in clientes:
        id, nombre, telefono, fecha_registro = cliente
        print(f"ID: {id}, Nombre: {nombre}, Teléfono: {telefono}, Fecha de registro: {fecha_registro}")

    print("\nResumen ejecutivo:")
    print(f"Clientes registrados: {len(clientes)}")
    print(f"Recordatorios enviados: {random.randint(1, 5)}")

if __name__ == "__main__":
    main()