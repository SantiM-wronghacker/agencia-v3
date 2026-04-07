"""
ÁREA: OPERACIONES
DESCRIPCIÓN: Agente que realiza generador checklist procesos
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime, timedelta

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def generar_checklist(procesos=None):
    if procesos is None:
        procesos = [
            {"id": 1, "nombre": "Revisión de documentos", "frecuencia": "diario", "ultima_revision": "2023-11-15"},
            {"id": 2, "nombre": "Verificación de inventario", "frecuencia": "semanal", "ultima_revision": "2023-11-10"},
            {"id": 3, "nombre": "Actualización de precios", "frecuencia": "mensual", "ultima_revision": "2023-10-15"},
            {"id": 4, "nombre": "Auditoría de procesos", "frecuencia": "trimestral", "ultima_revision": "2023-07-20"},
            {"id": 5, "nombre": "Mantenimiento preventivo", "frecuencia": "anual", "ultima_revision": "2023-01-10"}
        ]

    resumen = {"total": 0, "al_dia": 0, "vencidos": 0}

    for proceso in procesos:
        print(f"Proceso {proceso['id']}: {proceso['nombre']}")
        print(f"  - Frecuencia: {proceso['frecuencia']}")
        print(f"  - Última revisión: {proceso['ultima_revision']}")
        
        try:
            ultima_revision = datetime.strptime(proceso['ultima_revision'], '%Y-%m-%d').date()
            hoy = datetime.now().date()
            
            if proceso['frecuencia'] == "diario":
                vencido = ultima_revision < (hoy - timedelta(days=1))
            elif proceso['frecuencia'] == "semanal":
                vencido = ultima_revision < (hoy - timedelta(days=7))
            elif proceso['frecuencia'] == "mensual":
                vencido = ultima_revision < (hoy - timedelta(days=30))
            elif proceso['frecuencia'] == "trimestral":
                vencido = ultima_revision < (hoy - timedelta(days=90))
            elif proceso['frecuencia'] == "anual":
                vencido = ultima_revision < (hoy - timedelta(days=365))
            else:
                vencido = True
            
            estado = "Al día" if not vencido else "Vencido"
            print(f"  - Estado: {estado}")
            resumen["total"] += 1
            if estado == "Al día":
                resumen["al_dia"] += 1
            else:
                resumen["vencidos"] += 1
            
            print(f"  - Prioridad: {random.choice(['Alta', 'Media', 'Baja'])}")
            print(f"  - Responsable: {random.choice(['Juan', 'María', 'Pedro'])}")
            print(f"  - Observaciones: {random.choice(['Sin observaciones', 'Revisar documentos', 'Verificar inventario'])}")
            print()
        except Exception as e:
            print(f"Error al procesar proceso {proceso['id']}: {e}", file=sys.stderr)

    print("Resumen Ejecutivo:")
    print(f"  - Total de procesos: {resumen['total']}")
    print(f"  - Procesos al día: {resumen['al_dia']}")
    print(f"  - Procesos vencidos: {resumen['vencidos']}")

def main():
    try:
        if len(sys.argv) > 1:
            procesos = json.loads(sys.argv[1])
            generar_checklist(procesos)
        else:
            generar_checklist()
    except Exception as e:
        print(f"Error al generar checklist: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()