"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza análisis de cuellos botella
TECNOLOGÍA: Python estándar
"""
import sys
import json
import random
from datetime import datetime
import math

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        dias = int(sys.argv[1]) if len(sys.argv) > 1 else 30
        umbral = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8
        max_produccion = float(sys.argv[3]) if len(sys.argv) > 3 else 500  # Máximo de producción diaria
        intervalo_observacion = float(sys.argv[4]) if len(sys.argv) > 4 else 7  # Intervalo de observación para cálculo de promedios móviles

        if intervalo_observacion < 1:
            raise ValueError("Intervalo de observación debe ser mayor o igual a 1")

        if dias < 1:
            raise ValueError("Número de días debe ser mayor o igual a 1")

        if umbral < 0 or umbral > 1:
            raise ValueError("Umbral debe estar entre 0 y 1")

        if max_produccion < 1:
            raise ValueError("Máximo de producción diaria debe ser mayor o igual a 1")

        # Simulación de datos de producción diaria (en unidades)
        datos_produccion = [random.randint(100, max_produccion) for _ in range(dias)]

        # Análisis de cuellos de botella
        promedios_moviles = []
        for i in range(dias - intervalo_observacion):
            ventana = datos_produccion[i:i+intervalo_observacion]
            promedios_moviles.append(sum(ventana) / intervalo_observacion)

        # Identificación de cuellos de botella
        cuellos_botella = []
        for i, promedio in enumerate(promedios_moviles):
            if promedio < umbral * max(datos_produccion):
                cuellos_botella.append({
                    'dia': i + 1,
                    'promedio': round(promedio, 2),
                    'produccion': datos_produccion[i]
                })

        # Reporte
        print(f"Análisis de cuellos de botella (últimos {dias} días)")
        print(f"Fecha de análisis: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print(f"Total días analizados: {dias}")
        print(f"Días con cuellos de botella: {len(cuellos_botella)}")
        print(f"Producción promedio en cuellos de botella: {sum(c['promedio'] for c in cuellos_botella)/len(cuellos_botella) if cuellos_botella else 0:.2f} unidades")
        print(f"Producción total: {sum(datos_produccion)} unidades")
        print(f"Producción promedio diaria: {sum(datos_produccion)/len(datos_produccion):.2f} unidades")
        print(f"Umbral de cuello de botella: {umbral * 100} %")
        print(f"Intervalo de observación: {intervalo_observacion} días")
        print(f"Maximo de producción diaria: {max_produccion} unidades")

        # Resumen ejecutivo
        if len(cuellos_botella) > 0:
            print(f"Se identificaron {len(cuellos_botella)} días con cuellos de botella, lo que representa un {round(len(cuellos_botella)/dias*100, 2)}% de los días analizados.")
            print(f"La producción promedio en estos días fue de {sum(c['promedio'] for c in cuellos_botella)/len(cuellos_botella):.2f} unidades.")
        else:
            print("No se identificaron cuellos de botella en los días analizados.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()