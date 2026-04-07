"""
ÁREA: LOGÍSTICA
DESCRIPCIÓN: Agente que realiza tracker pedidos basico
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime, timedelta
import math

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def main():
    try:
        # Configuración por parámetros
        clientes = sys.argv[2] if len(sys.argv) > 2 else ["Agencia Santi", "Distribuidora del Norte", "Supermercados del Sur"]
        productos = sys.argv[3] if len(sys.argv) > 3 else ["Refrescos", "Botanas", "Carnes", "Lácteos", "Frutas"]
        estados = sys.argv[4] if len(sys.argv) > 4 else ["En preparación", "En tránsito", "Entregado", "Retrasado", "Cancelado"]
        num_pedidos = int(sys.argv[1]) if len(sys.argv) > 1 else 10

        # Generar datos de ejemplo
        pedidos = []
        for i in range(1, num_pedidos + 1):
            cliente = random.choice(clientes)
            producto = random.choice(productos)
            cantidad = random.randint(10, 100)
            fecha_entrega = datetime.now() + timedelta(days=random.randint(1, 7))
            estado = random.choice(estados)
            pedidos.append({
                "id": f"PED-{i:04d}",
                "cliente": cliente,
                "producto": producto,
                "cantidad": cantidad,
                "fecha_entrega": fecha_entrega.strftime("%Y-%m-%d"),
                "estado": estado
            })

        # Mostrar resultados
        print("=== TRACKER DE PEDIDOS BÁSICO ===")
        print(f"ÁREA: LOGÍSTICA")
        print(f"DESCRIPCIÓN: Agente que realiza tracker pedidos básico")
        print(f"TECNOLOGÍA: Python estándar")
        print(f"Fecha de reporte: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total de pedidos: {len(pedidos)}")
        print(f"Productos más comunes: {', '.join(set(p['producto'] for p in pedidos))}")
        print(f"Clientes atendidos: {', '.join(set(p['cliente'] for p in pedidos))}")
        print(f"Estados de pedidos: {', '.join(set(p['estado'] for p in pedidos))}")
        print(f"Fecha de entrega más temprana: {min(p['fecha_entrega'] for p in pedidos)}")
        print(f"Fecha de entrega más tardía: {max(p['fecha_entrega'] for p in pedidos)}")
        print(f"Total de productos: {sum(p['cantidad'] for p in pedidos)}")
        print(f"Promedio de productos por pedido: {math.ceil(sum(p['cantidad'] for p in pedidos) / len(pedidos))}")
        print(f"Pedidos retrasados: {len([p for p in pedidos if p['estado'] in ['Retrasado', 'Cancelado']])}")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El tracker de pedidos básico ha generado {len(pedidos)} pedidos para {len(set(p['cliente'] for p in pedidos))} clientes.")
        print(f"Los productos más comunes han sido {', '.join(set(p['producto'] for p in pedidos))}.")
        print(f"La fecha de entrega más temprana es {min(p['fecha_entrega'] for p in pedidos)} y la más tardía es {max(p['fecha_entrega'] for p in pedidos)}.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()