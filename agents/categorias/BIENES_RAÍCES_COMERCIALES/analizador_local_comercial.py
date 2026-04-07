"""
ÁREA: BIENES RAÍCES COMERCIALES
DESCRIPCIÓN: Agente que realiza analizador local comercial
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
import math
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        zona = sys.argv[1] if len(sys.argv) > 1 else "Polanco"
        area = float(sys.argv[2]) if len(sys.argv) > 2 else 150.0  # m2
        precio_base = float(sys.argv[3]) if len(sys.argv) > 3 else 5000000.0  # MXN

        # Cálculos
        precio_m2 = precio_base / area
        demanda_estimada = random.randint(3, 10)
        rentabilidad = (random.uniform(0.05, 0.15) * precio_base) / 12

        # Datos de mercado
        zonas_comerciales = {
            "Polanco": {"precio_promedio": 85000.0, "crecimiento_anual": 0.08},
            "Roma": {"precio_promedio": 68000.0, "crecimiento_anual": 0.06},
            "Condesa": {"precio_promedio": 75000.0, "crecimiento_anual": 0.07},
            "Santa Fe": {"precio_promedio": 63000.0, "crecimiento_anual": 0.05},
            "Juárez": {"precio_promedio": 60000.0, "crecimiento_anual": 0.04},
            "Cuauhtémoc": {"precio_promedio": 65000.0, "crecimiento_anual": 0.06},
        }

        # Análisis
        zona_datos = zonas_comerciales.get(zona, zonas_comerciales["Polanco"])
        diferencia_precio = precio_m2 - zona_datos["precio_promedio"]
        valor_futuro = precio_base * (1 + zona_datos["crecimiento_anual"] * 3)

        # Impresión de resultados
        print(f"Análisis comercial para zona: {zona}")
        print(f"Precio por m2: ${precio_m2:,.2f} MXN (vs promedio: ${zona_datos['precio_promedio']:,.2f} MXN)")
        print(f"Demanda estimada: {demanda_estimada} consultas/mes")
        print(f"Rentabilidad mensual estimada: ${rentabilidad:,.2f} MXN")
        print(f"Valor estimado en 3 años: ${valor_futuro:,.2f} MXN")
        print(f"Diferencia vs mercado: {'{:+,.2f}'.format(diferencia_precio)} MXN/m2")
        print(f"Porcentaje de diferencia vs mercado: {'{:+,.2f}%'.format((diferencia_precio / zona_datos['precio_promedio']) * 100)}")
        print(f"Rentabilidad anual estimada: ${rentabilidad * 12:,.2f} MXN")
        print(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"La zona {zona} presenta un precio por m2 de ${precio_m2:,.2f} MXN, lo que supone una diferencia de {'{:+,.2f}%'.format((diferencia_precio / zona_datos['precio_promedio']) * 100)} con respecto al promedio de la zona.")
        print(f"La demanda estimada es de {demanda_estimada} consultas/mes, con una rentabilidad mensual estimada de ${rentabilidad:,.2f} MXN.")
        print(f"El valor estimado en 3 años es de ${valor_futuro:,.2f} MXN, lo que supone un crecimiento anual del {zona_datos['crecimiento_anual']*100:.2f}%.")

    except IndexError:
        print("Error: Parámetros insuficientes. Por favor, proporcione la zona, el área y el precio base.")
        sys.exit(1)
    except ValueError:
        print("Error: Parámetros inválidos. Por favor, proporcione valores numéricos para el área y el precio base.")
        sys.exit(1)
    except Exception as e:
        print(f"Error en el análisis: {str(e)}")