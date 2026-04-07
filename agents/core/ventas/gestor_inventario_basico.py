"""
ÁREA: OPERACIONES
DESCRIPCIÓN: Agente que realiza gestor inventario basico
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
        # Configuración por defecto
        archivo_inventario = "inventario.json"
        cantidad_articulos = 10
        precio_promedio = 150.50
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        impuesto = 0.16  # IVA en México
        costo_envio = 50.0  # Costo de envío promedio

        # Procesamiento de argumentos
        if len(sys.argv) > 1:
            archivo_inventario = sys.argv[1]
        if len(sys.argv) > 2:
            cantidad_articulos = int(sys.argv[2])
        if len(sys.argv) > 3:
            precio_promedio = float(sys.argv[3])
        if len(sys.argv) > 4:
            impuesto = float(sys.argv[4])
        if len(sys.argv) > 5:
            costo_envio = float(sys.argv[5])

        # Generar datos de inventario
        inventario = []
        total_ventas = 0.0
        total_costo = 0.0
        for i in range(1, cantidad_articulos + 1):
            articulo = {
                "id": f"ART-{random.randint(1000, 9999)}",
                "nombre": f"Producto {i}",
                "cantidad": random.randint(1, 100),
                "precio": round(precio_promedio * random.uniform(0.8, 1.2), 2),
                "fecha_registro": fecha_actual
            }
            inventario.append(articulo)
            total_ventas += articulo["precio"] * articulo["cantidad"]
            total_costo += (articulo["precio"] / (1 + impuesto)) * articulo["cantidad"]

        # Calcular estadísticas
        precio_promedio_real = sum(item["precio"] for item in inventario) / len(inventario)
        articulo_mas_caro = max(inventario, key=lambda x: x["precio"])
        articulo_mas_barato = min(inventario, key=lambda x: x["precio"])
        total_inventario = sum(item["precio"] * item["cantidad"] for item in inventario)
        utilidad_neta = total_ventas - total_costo - (total_inventario * impuesto) - costo_envio

        # Guardar en archivo
        with open(archivo_inventario, "w") as f:
            json.dump(inventario, f, indent=2)

        # Mostrar resultados
        print(f"Inventario generado con {len(inventario)} artículos")
        print(f"Fecha de generación: {fecha_actual}")
        print(f"Precio promedio: ${precio_promedio_real:.2f} MXN")
        print(f"Artículo más caro: ${articulo_mas_caro['precio']:.2f} MXN ({articulo_mas_caro['nombre']})")
        print(f"Artículo más barato: ${articulo_mas_barato['precio']:.2f} MXN ({articulo_mas_barato['nombre']})")
        print(f"Total en inventario: ${total_inventario:.2f} MXN")
        print(f"Total ventas: ${total_ventas:.2f} MXN")
        print(f"Total costo: ${total_costo:.2f} MXN")
        print(f"Utilidad neta: ${utilidad_neta:.2f} MXN")
        print(f"Costo de envío: ${costo_envio:.2f} MXN")
        print(f"Impuesto (IVA): {impuesto*100:.2f}%")
        print("Resumen ejecutivo:")
        print(f"El inventario generado tiene un total de {len(inventario)} artículos, con un precio promedio de ${precio_promedio_real:.2f} MXN.")
        print(f"El artículo más caro es {articulo_mas_caro['nombre']} con un precio de ${articulo_mas_caro['precio']:.2f} MXN.")
        print(f"La utilidad neta del inventario es de ${utilidad_neta:.2f} MXN, considerando un costo de envío de ${costo_envio:.2f} MXN y un impuesto del {impuesto*100:.2f}%.")

    except Exception as e:
        print(f"Error en el procesamiento: {str(e)}", file=sys.stderr)