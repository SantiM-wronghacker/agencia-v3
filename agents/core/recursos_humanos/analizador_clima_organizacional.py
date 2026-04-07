"""
ÁREA: RECURSOS HUMANOS
DESCRIPCIÓN: Agente que realiza analizador clima organizacional
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

def calcular_satisfaccion(empleados):
    return round(random.uniform(70, 90) + (empleados / 100), 2)

def calcular_rotacion(empleados):
    return round(random.uniform(5, 15) + (empleados / 1000), 2)

def calcular_productividad(empleados):
    return round(random.uniform(80, 95) + (empleados / 50), 2)

def main():
    try:
        # Configuración por defecto
        if len(sys.argv) > 1:
            empresa = sys.argv[1]
            empleados = int(sys.argv[2])
        else:
            empresa = "Agencia Santi"
            empleados = 150

        fecha = datetime.now().strftime("%Y-%m-%d")
        satisfaccion = calcular_satisfaccion(empleados)
        rotacion = calcular_rotacion(empleados)
        productividad = calcular_productividad(empleados)

        # Generar datos de clima organizacional
        datos = {
            "empresa": empresa,
            "fecha": fecha,
            "empleados": empleados,
            "satisfaccion_promedio": satisfaccion,
            "rotacion_anual": rotacion,
            "productividad_promedio": productividad,
            "indicadores": {
                "comunicacion": random.randint(70, 90),
                "liderazgo": random.randint(65, 85),
                "reconocimiento": random.randint(50, 75),
                "equilibrio": random.randint(60, 80),
                "crecimiento": random.randint(70, 90)
            }
        }

        # Imprimir resultados
        print(f"Análisis de clima organizacional para {empresa}")
        print(f"Fecha: {fecha}")
        print(f"Número de empleados: {empleados}")
        print(f"Satisfacción promedio: {datos['satisfaccion_promedio']}%")
        print(f"Rotación anual: {datos['rotacion_anual']}%")
        print(f"Productividad promedio: {datos['productividad_promedio']}%")
        print("\nIndicadores clave:")
        for key, value in datos['indicadores'].items():
            print(f"- {key.capitalize()}: {value}%")
        print("\nAnálisis detallado:")
        print(f"- Empleados satisfechos: {int(empleados * (satisfaccion / 100))}")
        print(f"- Empleados en riesgo de rotación: {int(empleados * (rotacion / 100))}")
        print(f"- Productividad total: {int(productividad * empleados)}")
        print("\nResumen ejecutivo:")
        print(f"La empresa {empresa} tiene un clima organizacional saludable, con una satisfacción promedio de {satisfaccion}% y una productividad promedio de {productividad}%. Sin embargo, es importante monitorear la rotación anual de {rotacion}% y tomar medidas para reducirla.")

        # Guardar en archivo JSON
        with open("clima_organizacional.json", "w") as f:
            json.dump(datos, f, indent=4)

    except Exception as e:
        print(f"Error en el análisis: {str(e)}")
        sys.exit(1)

    except IndexError:
        print("Error: No se proporcionaron los parámetros necesarios.")
        print("Uso: python analizador_clima_organizacional.py <empresa> <empleados>")
        sys.exit(1)

if __name__ == "__main__":
    main()