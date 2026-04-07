import sys
import json
import random
import math
import re
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_costo_remodelacion(area_m2, tipo_remodelacion, calidad):
    """
    Calcula el costo estimado de remodelación en pesos mexicanos.
    """
    # Costos base por m2 (MXN)
    costos_base = {
        'baja': 1800,
        'media': 3000,
        'alta': 5000
    }

    # Ajuste por tipo de remodelación
    ajustes = {
        'cocina': 1.3,
        'baño': 1.2,
        'sala': 1.1,
        'recámara': 1.0,
        'integral': 1.4
    }

    # Ajuste por calidad
    calidad_factor = {
        'económica': 0.8,
        'estándar': 1.0,
        'premium': 1.3
    }

    # Costos adicionales por tipo de remodelación
    costos_adicionales = {
        'cocina': 50000,
        'baño': 30000,
        'sala': 20000,
        'recámara': 10000,
        'integral': 100000
    }

    costo_base = costos_base.get(calidad.lower(), 3000) * area_m2
    costo_ajustado = costo_base * ajustes.get(tipo_remodelacion.lower(), 1.0)
    costo_final = costo_ajustado * calidad_factor.get(calidad.lower(), 1.0)

    # Añadir costos adicionales
    costo_final += costos_adicionales.get(tipo_remodelacion.lower(), 0)

    # Añadir variabilidad (+/- 10%)
    costo_final *= random.uniform(0.9, 1.1)

    # Añadir impuestos (16% de IVA)
    costo_final *= 1.16

    return round(costo_final, 2)

def main():
    try:
        # Parámetros por defecto
        area_m2 = float(sys.argv[1]) if len(sys.argv) > 1 else 50.0
        tipo_remodelacion = sys.argv[2].lower() if len(sys.argv) > 2 else 'media'
        calidad = sys.argv[3].lower() if len(sys.argv) > 3 else 'estándar'

        if tipo_remodelacion not in ['cocina', 'baño', 'sala', 'recámara', 'integral']:
            raise ValueError("Tipo de remodelación no válido")

        if calidad not in ['económica', 'estándar', 'premium']:
            raise ValueError("Calidad no válida")

        costo = calcular_costo_remodelacion(area_m2, tipo_remodelacion, calidad)

        print("===== ESTIMADOR DE COSTOS DE REMODELACIÓN =====")
        print("ÁREA/DESCRIPCION:")
        print("Remodelación de una habitación de {} m²".format(area_m2))
        print("TECNOLOGIA:")
        print("Python 3.x")
        print("===== DATOS DE ENTRADA =====")
        print("Área: {} m²".format(area_m2))
        print("Tipo de remodelación: {}".format(tipo_remodelacion.capitalize()))
        print("Calidad: {}".format(calidad.capitalize()))
        print("===== RESULTADOS =====")
        print("Costo estimado: ${}".format(costo))
        print("Impuestos (16% de IVA): ${}".format(round(costo * 0.16, 2)))
        print("Total: ${}".format(round(costo * 1.16, 2)))
        print("===== RESUMEN EJECUTIVO =====")
        print("El costo estimado de la remodelación es de ${} con un total de ${} incluyendo impuestos.".format(costo, round(costo * 1.16, 2)))
    except ValueError as e:
        print("Error: {}".format(e))
    except Exception as e:
        print("Error: {}".format(e))

if __name__ == "__main__":
    main()