"""
ÁREA: RESTAURANTES
DESCRIPCIÓN: Agente que realiza generador receta estandarizada
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
        nombre_receta = sys.argv[1] if len(sys.argv) > 1 else "Ensalada César"
        porciones = int(sys.argv[2]) if len(sys.argv) > 2 else 4
        costo_porcion = float(sys.argv[3]) if len(sys.argv) > 3 else 59.90

        # Generar datos de la receta
        ingredientes = [
            {"nombre": "Lechuga romana", "cantidad": f"{random.randint(100, 200)}g", "costo": round(random.uniform(10.0, 20.0), 2)},
            {"nombre": "Pollo a la parrilla", "cantidad": f"{random.randint(150, 250)}g", "costo": round(random.uniform(20.0, 30.0), 2)},
            {"nombre": "Croutons", "cantidad": f"{random.randint(30, 50)}g", "costo": round(random.uniform(5.0, 10.0), 2)},
            {"nombre": "Queso parmesano", "cantidad": f"{random.randint(10, 20)}g", "costo": round(random.uniform(10.0, 20.0), 2)},
            {"nombre": "Aderezo César", "cantidad": f"{random.randint(30, 50)}ml", "costo": round(random.uniform(5.0, 10.0), 2)}
        ]

        # Cálculos
        costo_total = costo_porcion * porciones
        tiempo_preparacion = random.randint(10, 20)
        fecha_creacion = datetime.now().strftime("%Y-%m-%d")
        iva = round(costo_total * 0.16, 2)
        total_con_iva = round(costo_total + iva, 2)

        # Generar receta estandarizada
        receta = {
            "nombre": nombre_receta,
            "porciones": porciones,
            "costo_por_porcion": f"${costo_porcion:.2f}",
            "costo_total": f"${costo_total:.2f}",
            "costo_total_con_iva": f"${total_con_iva:.2f}",
            "tiempo_preparacion": f"{tiempo_preparacion} minutos",
            "fecha_creacion": fecha_creacion,
            "ingredientes": ingredientes
        }

        # Imprimir resultados
        print("RECETA ESTANDARIZADA")
        print(f"Nombre: {receta['nombre']}")
        print(f"Porciones: {receta['porciones']} | Costo total: {receta['costo_total']}")
        print(f"Costo total con IVA: {receta['costo_total_con_iva']}")
        print(f"Tiempo de preparación: {receta['tiempo_preparacion']}")
        print("Ingredientes principales:")
        for ingrediente in receta['ingredientes']:
            print(f"- {ingrediente['nombre']}: {ingrediente['cantidad']} | Costo: ${ingrediente['costo']:.2f}")
        print(f"Impuesto al valor agregado (IVA): ${iva:.2f}")
        print("RESUMEN EJECUTIVO")
        print(f"La receta {receta['nombre']} tiene un costo total de {receta['costo_total']} y un costo total con IVA de {receta['costo_total_con_iva']}.")
        print(f"El tiempo de preparación es de {receta['tiempo_preparacion']} minutos y la fecha de creación es {receta['fecha_creacion']}.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()