"""
ÁREA: EDUCACIÓN
DESCRIPCIÓN: Agente que realiza generador plan estudio
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

def generar_plan_estudio(areas=None, niveles=None, horas_semanales=None, costo_mensual_min=1500, costo_mensual_max=5000):
    if areas is None:
        areas = ["Matemáticas", "Ciencias", "Historia", "Lengua", "Artes"]
    if niveles is None:
        niveles = ["Básico", "Intermedio", "Avanzado"]
    if horas_semanales is None:
        horas_semanales = [10, 15, 20, 25, 30]

    try:
        area_principal = random.choice(areas)
        nivel = random.choice(niveles)
        horas = random.choice(horas_semanales)
        duracion_meses = random.randint(3, 12)
        costo_mensual = round(random.uniform(costo_mensual_min, costo_mensual_max), 2)
        costo_total = round(costo_mensual * duracion_meses, 2)
        iva = round(costo_total * 0.16, 2)
        costo_total_con_iva = round(costo_total + iva, 2)
    except Exception as e:
        print(f"Error al generar el plan de estudio: {str(e)}", file=sys.stderr)
        sys.exit(1)

    plan = {
        "Área de estudio": area_principal,
        "Nivel": nivel,
        "Horas semanales": f"{horas} horas",
        "Duración": f"{duracion_meses} meses",
        "Costo mensual": f"${costo_mensual:.2f} MXN",
        "Costo total": f"${costo_total:.2f} MXN",
        "Costo total con IVA": f"${costo_total_con_iva:.2f} MXN",
        "IVA": f"{iva:.2f} MXN",
        "Fecha de generación": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Detalles": {
            "Descripción del área": f"El área de {area_principal} es fundamental para el desarrollo de habilidades",
            "Objetivos del nivel": f"El nivel {nivel} busca desarrollar habilidades avanzadas en {area_principal}",
            "Requisitos": "No se requieren conocimientos previos",
            "Beneficios": "Mejora la comprensión y el análisis de la materia"
        }
    }

    return plan

def main():
    try:
        if len(sys.argv) > 1:
            areas = sys.argv[1].split(',')
            niveles = sys.argv[2].split(',')
            horas_semanales = [int(x) for x in sys.argv[3].split(',')]
            costo_mensual_min = float(sys.argv[4])
            costo_mensual_max = float(sys.argv[5])
        else:
            areas = None
            niveles = None
            horas_semanales = None
            costo_mensual_min = 1500
            costo_mensual_max = 5000

        plan = generar_plan_estudio(areas, niveles, horas_semanales, costo_mensual_min, costo_mensual_max)
        print("Plan de Estudio:")
        for clave, valor in plan.items():
            if clave != "Detalles":
                print(f"{clave}: {valor}")
            else:
                print("Detalles:")
                for clave_detalle, valor_detalle in plan["Detalles"].items():
                    print(f"  {clave_detalle}: {valor_detalle}")

        print("\nResumen Ejecutivo:")
        print(f"El plan de estudio en {plan['Área de estudio']} tiene un costo total de {plan['Costo total']} MXN y un costo total con IVA de {plan['Costo total con IVA']} MXN.")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()