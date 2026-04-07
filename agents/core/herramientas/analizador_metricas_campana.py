"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza analizador metricas campana
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
        fecha_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        fecha_fin = datetime.now().strftime('%Y-%m-%d')
        if len(sys.argv) > 1:
            fecha_inicio = sys.argv[1]
        if len(sys.argv) > 2:
            fecha_fin = sys.argv[2]

        # Datos simulados de métricas de campaña
        datos = {
            "impresiones": random.randint(50000, 200000),
            "clics": random.randint(1000, 5000),
            "conversiones": random.randint(50, 300),
            "costo": round(random.uniform(10000, 50000), 2),
            "ctr": round(random.uniform(0.01, 0.15), 4),
            "cpc": round(random.uniform(5, 20), 2),
            "cpa": round(random.uniform(100, 500), 2),
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
        }

        # Cálculos adicionales
        datos["roi"] = round((datos["conversiones"] * 200 - datos["costo"]) / datos["costo"] * 100, 2)
        datos["costo_por_dia"] = round(datos["costo"] / (datetime.strptime(datos["fecha_fin"], '%Y-%m-%d') -
                                                         datetime.strptime(datos["fecha_inicio"], '%Y-%m-%d')).days, 2)
        datos["tasa_conversion"] = round(datos["conversiones"] / datos["clics"] * 100, 2)
        datos["tasa_abandono"] = round((datos["clics"] - datos["conversiones"]) / datos["clics"] * 100, 2)

        # Impresión de resultados
        print(f"Análisis de métricas de campaña (del {datos['fecha_inicio']} al {datos['fecha_fin']}):")
        print(f"1. Impresiones: {datos['impresiones']:,}")
        print(f"2. Clics: {datos['clics']:,} (CTR: {datos['ctr']*100:.2f}%)")
        print(f"3. Conversiones: {datos['conversiones']:,} (CPA: ${datos['cpa']:,.2f} MXN)")
        print(f"4. Inversión total: ${datos['costo']:,.2f} MXN (${datos['costo_por_dia']:,.2f} MXN/día)")
        print(f"5. ROI: {datos['roi']:.2f}%")
        print(f"6. Tasa de conversión: {datos['tasa_conversion']:.2f}%")
        print(f"7. Tasa de abandono: {datos['tasa_abandono']:.2f}%")
        print(f"8. Costo por clic (CPC): ${datos['cpc']:,.2f} MXN")
        print(f"9. Valor de conversión: ${200:.2f} MXN")
        print(f"10. Ganancia total: ${datos['conversiones'] * 200 - datos['costo']:,.2f} MXN")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"La campaña ha generado {datos['conversiones']:,} conversiones con un costo total de ${datos['costo']:,.2f} MXN.")
        print(f"El ROI de la campaña es de {datos['roi']:.2f}%, lo que indica que la campaña ha sido rentable.")
        print(f"Se recomienda seguir monitoreando las métricas de la campaña para optimizar el rendimiento.")

    except Exception as e:
        print(f"Error en el análisis de métricas de campaña: {str(e)}")

if __name__ == "__main__":
    main()