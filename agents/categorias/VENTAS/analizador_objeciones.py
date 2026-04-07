"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza analizador objeciones
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Configuración por defecto
        archivo = sys.argv[1] if len(sys.argv) > 1 else "objeciones.json"
        dias = int(sys.argv[2]) if len(sys.argv) > 2 else 30

        # Cargar datos de objeciones
        with open(archivo, 'r') as f:
            datos = json.load(f)

        # Análisis de objeciones
        total_objeciones = len(datos)
        objeciones_resueltas = sum(1 for o in datos if o.get('resuelta', False))
        porcentaje_resueltas = (objeciones_resueltas / total_objeciones) * 100 if total_objeciones > 0 else 0
        objeciones_repetidas = sum(1 for o in datos if datos.count(o) > 1)
        promedio_dias_resolucion = sum(
            o.get('dias_resolucion', 0) for o in datos if o.get('resuelta', False)
        ) / objeciones_resueltas if objeciones_resueltas > 0 else 0
        max_dias_resolucion = max(o.get('dias_resolucion', 0) for o in datos)
        min_dias_resolucion = min(o.get('dias_resolucion', 0) for o in datos if o.get('resuelta', False))
        objeciones_pendientes = total_objeciones - objeciones_resueltas
        tasa_resolucion = (objeciones_resueltas / total_objeciones) * 100 if total_objeciones > 0 else 0
        tasa_repetidas = (objeciones_repetidas / total_objeciones) * 100 if total_objeciones > 0 else 0

        # Generar reporte
        print("=== REPORTE DE OBJECIONES ===")
        print(f"Total de objeciones analizadas: {total_objeciones}")
        print(f"Objeciones resueltas: {objeciones_resueltas} ({porcentaje_resueltas:.2f}%)")
        print(f"Objeciones pendientes: {objeciones_pendientes} ({100 - porcentaje_resueltas:.2f}%)")
        print(f"Objeciones repetidas: {objeciones_repetidas} ({tasa_repetidas:.2f}%)")
        print(f"Promedio días de resolución: {promedio_dias_resolucion:.1f} días")
        print(f"Máximo días de resolución: {max_dias_resolucion} días")
        print(f"Mínimo días de resolución: {min_dias_resolucion} días")
        print(f"Tasa de resolución: {tasa_resolucion:.2f}%")
        print(f"Objetivo: Reducir objeciones en {dias} días")
        print(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Resumen ejecutivo
        print("\n=== RESUMEN EJECUTIVO ===")
        print(f"En resumen, se analizaron {total_objeciones} objeciones, de las cuales {objeciones_resueltas} fueron resueltas.")
        print(f"La tasa de resolución es del {tasa_resolucion:.2f}% y la tasa de objeciones repetidas es del {tasa_repetidas:.2f}%.")
        print(f"El objetivo es reducir objeciones en {dias} días.")

    except FileNotFoundError:
        print("Error: El archivo de objeciones no existe.")
    except json.JSONDecodeError:
        print("Error: El archivo de objeciones no es un JSON válido.")
    except Exception as e:
        print(f"Error al procesar objeciones: {str(e)}")

if __name__ == "__main__":
    main()