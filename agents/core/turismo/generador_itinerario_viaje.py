"""
ÁREA: TURISMO
DESCRIPCIÓN: Agente que realiza generador itinerario viaje
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime, timedelta

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        destino = sys.argv[1] if len(sys.argv) > 1 else "Cancún"
        dias = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        presupuesto = float(sys.argv[3]) if len(sys.argv) > 3 else 15000.0

        # Datos de ejemplo para destinos en México
        destinos = {
            "Cancún": {"hoteles": ["Riu Palace", "Hyatt Ziva", "Grand Fiesta Americana"],
                      "actividades": ["Playa Delfines", "Xcaret", "Isla Mujeres"],
                      "gastos_diarios": 1200.0,
                      "impuestos": 0.16,
                      "propinas": 0.10},
            "CDMX": {"hoteles": ["W Mexico City", "Four Seasons", "Grand Fiesta Americana"],
                     "actividades": ["Zócalo", "Teotihuacán", "Museo Frida Kahlo"],
                     "gastos_diarios": 900.0,
                     "impuestos": 0.16,
                     "propinas": 0.10},
            "Guadalajara": {"hoteles": ["Grand Fiesta Americana", "Hyatt Regency", "Sheraton"],
                           "actividades": ["Centro Histórico", "Hospicio Cabañas", "Laguna de Chapala"],
                           "gastos_diarios": 700.0,
                           "impuestos": 0.16,
                           "propinas": 0.10}
        }

        if destino not in destinos:
            print(f"Destino no disponible. Usando Cancún por defecto.")
            destino = "Cancún"

        datos_destino = destinos[destino]

        # Generar itinerario
        print(f"Itinerario para {dias} días en {destino} con presupuesto de ${presupuesto:.2f} MXN")
        print(f"Gasto diario estimado: ${datos_destino['gastos_diarios']:.2f} MXN")
        print(f"Presupuesto total estimado: ${dias * datos_destino['gastos_diarios']:.2f} MXN")
        print(f"Impuestos estimados (16%): ${dias * datos_destino['gastos_diarios'] * datos_destino['impuestos']:.2f} MXN")
        print(f"Propinas estimadas (10%): ${dias * datos_destino['gastos_diarios'] * datos_destino['propinas']:.2f} MXN")

        print("\nItinerario sugerido:")
        for dia in range(1, dias + 1):
            hotel = random.choice(datos_destino["hoteles"])
            actividad = random.choice(datos_destino["actividades"])
            print(f"Día {dia}: Alojamiento en {hotel} - Actividad: {actividad}")

        print("\nResumen ejecutivo:")
        print(f"Destino: {destino}")
        print(f"Días: {dias}")
        print(f"Presupuesto: ${presupuesto:.2f} MXN")
        print(f"Presupuesto total estimado: ${dias * datos_destino['gastos_diarios'] + dias * datos_destino['gastos_diarios'] * datos_destino['impuestos'] + dias * datos_destino['gastos_diarios'] * datos_destino['propinas']:.2f} MXN")

    except ValueError:
        print("Error: Los parámetros deben ser numéricos.")
    except IndexError:
        print("Error: Faltan parámetros. Utilice el formato: python generador_itinerario_viaje.py <destino> <días> <presupuesto>")

if __name__ == "__main__":
    main()