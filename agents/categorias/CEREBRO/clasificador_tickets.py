"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza clasificador tickets
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def clasificar_tickets(tickets=None):
    if tickets is None:
        tickets = [
            {"id": 1, "asunto": "Problema con conexión a internet", "descripcion": "No puedo acceder a la red"},
            {"id": 2, "asunto": "Problema con software", "descripcion": "El software no se abre correctamente"},
            {"id": 3, "asunto": "Problema con hardware", "descripcion": "Mi equipo se ha congelado"},
            {"id": 4, "asunto": "Problema con seguridad", "descripcion": "Mi cuenta ha sido hackeada"},
            {"id": 5, "asunto": "Problema con configuración", "descripcion": "No puedo configurar mi cuenta"}
        ]

    if WEB:
        # Buscar tickets en la base de datos
        try:
            tickets = web.buscar("tickets")
        except Exception as e:
            print(f"Error al buscar tickets: {e}")

        # Extraer precios de la web
        try:
            precios = web.extraer_precios()
            print(f"Precios actuales: {precios}")
        except Exception as e:
            print(f"Error al extraer precios: {e}")

        # Obtener noticias de la web
        try:
            noticias = web.fetch_texto("noticias")
            print(f"Noticias actuales: {noticias}")
        except Exception as e:
            print(f"Error al obtener noticias: {e}")

    # Clasificar tickets
    clasificados = {}
    for ticket in tickets:
        categoria = None
        try:
            if "internet" in ticket["descripcion"].lower():
                categoria = "Conexión a internet"
            elif "software" in ticket["descripcion"].lower():
                categoria = "Software"
            elif "hardware" in ticket["descripcion"].lower():
                categoria = "Hardware"
            elif "seguridad" in ticket["descripcion"].lower():
                categoria = "Seguridad"
            elif "configuracion" in ticket["descripcion"].lower():
                categoria = "Configuración"
            else:
                categoria = "Otro"
        except KeyError:
            print(f"Error al procesar ticket {ticket['id']}: falta información")

        if categoria not in clasificados:
            clasificados[categoria] = []

        clasificados[categoria].append(ticket)

    # Mostrar resultados
    for categoria, tickets in clasificados.items():
        print(f"Categoría: {categoria}")
        for ticket in tickets:
            print(f"  - Ticket {ticket['id']}: {ticket['asunto']}")

    # Resumen ejecutivo
    print(f"Total de tickets: {len(tickets)}")
    print(f"Total de categorías: {len(clasificados)}")

def main():
    try:
        if len(sys.argv) > 1:
            tickets = json.loads(sys.argv[1])
        else:
            tickets = None
        clasificar_tickets(tickets)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()