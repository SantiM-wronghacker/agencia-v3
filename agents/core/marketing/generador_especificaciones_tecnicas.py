"""
ÁREA: TECNOLOGÍA
DESCRIPCIÓN: Agente que realiza generador especificaciones tecnicas
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por línea de comandos con defaults
        proyecto = sys.argv[1] if len(sys.argv) > 1 else "Proyecto de Redes"
        ubicacion = sys.argv[2] if len(sys.argv) > 2 else "CDMX"
        presupuesto = float(sys.argv[3]) if len(sys.argv) > 3 else 500000.0

        # Generar especificaciones técnicas
        especificaciones = {
            "proyecto": proyecto,
            "ubicacion": ubicacion,
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "presupuesto": f"${presupuesto:,.2f} MXN",
            "requisitos": [
                f"Servidores: {random.randint(2, 5)} unidades",
                f"Switches: {random.randint(10, 20)} puertos",
                f"Cables: {random.randint(500, 1000)} metros",
                f"UPS: {random.randint(1, 3)} unidades",
                f"Backup: {random.randint(1, 5)} TB",
                f"Capacidad de almacenamiento: {random.randint(10, 50)} TB",
                f"Ancho de banda: {random.randint(100, 1000)} Mbps",
                f"Seguridad: Firewall, antivirus y sistema de detección de intrusos",
                f"Redundancia: {random.randint(1, 3)} sistemas de respaldo",
                f"Escalabilidad: Diseño para {random.randint(100, 1000)} usuarios"
            ],
            "notas": "Especificaciones generadas automáticamente"
        }

        # Imprimir resultados
        print(f"Proyecto: {especificaciones['proyecto']}")
        print(f"Ubicación: {especificaciones['ubicacion']}")
        print(f"Fecha: {especificaciones['fecha']}")
        print(f"Presupuesto: {especificaciones['presupuesto']}")
        print("Requisitos técnicos:")
        for req in especificaciones['requisitos']:
            print(f"- {req}")
        print("Resumen Ejecutivo:")
        print(f"El proyecto {especificaciones['proyecto']} requiere un presupuesto de {especificaciones['presupuesto']} para implementar una infraestructura de red en {especificaciones['ubicacion']}.")
        print(f"Los requisitos técnicos incluyen {len(especificaciones['requisitos'])} componentes, entre ellos servidores, switches, cables, UPS y sistemas de respaldo.")
        print(f"El proyecto está diseñado para ser escalable y seguro, con un sistema de detección de intrusos y firewall.")
        print(f"El presupuesto se distribuirá de la siguiente manera: 30% para servidores, 20% para switches y cables, 20% para UPS y sistemas de respaldo, y 30% para mano de obra y otros gastos.")

    except IndexError:
        print("Error: No se proporcionaron suficientes parámetros.", file=sys.stderr)
        print("Uso: python generador_especificaciones_tecnicas.py <proyecto> <ubicacion> <presupuesto>", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        print("Error: El presupuesto debe ser un número.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()