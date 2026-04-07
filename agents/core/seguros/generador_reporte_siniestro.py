"""
ÁREA: SEGUROS
DESCRIPCIÓN: Agente que realiza generador reporte siniestro
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime, timedelta

def generar_siniestro():
    fecha = datetime.now() - timedelta(days=random.randint(1, 365))
    return {
        "fecha": fecha.strftime("%Y-%m-%d"),
        "monto": round(random.uniform(1000, 100000), 2),
        "descripcion": random.choice(["Accidente de tránsito", "Incendio", "Robo", "Daño por agua"]),
        "ubicacion": random.choice(["Ciudad de México", "Guadalajara", "Monterrey", "Puebla"]),
        "estado": random.choice(["Pendiente", "En proceso", "Resuelto"]),
        "tipo_de_siniestro": random.choice(["Automotriz", "Vivienda", "Negocio"]),
        "numero_de_poliza": random.randint(1000, 9999),
        "nombre_de_asegurado": f"Asegurado {random.randint(1, 100)}",
        "monto_total_pagado": round(random.uniform(0, 100000), 2),
        "porcentaje_de_cobertura": round(random.uniform(0, 100), 2),
        "dias_para_resolucion": random.randint(1, 365),
        "costos_administrativos": round(random.uniform(100, 10000), 2),
        "impuestos": round(random.uniform(0, 10000), 2)
    }

def calcular_monto_total(siniestros):
    total_monto_pagado = 0
    total_monto_siniestros = 0
    for siniestro in siniestros:
        total_monto_pagado += siniestro["monto_total_pagado"]
        total_monto_siniestros += siniestro["monto"]
    return total_monto_pagado, total_monto_siniestros

def main():
    try:
        num_siniestros = int(sys.argv[1]) if len(sys.argv) > 1 else 5
        siniestros = [generar_siniestro() for _ in range(num_siniestros)]
        total_monto_pagado, total_monto_siniestros = calcular_monto_total(siniestros)
        for i, siniestro in enumerate(siniestros):
            print(f"Siniestro {i+1}:")
            print(f"Fecha: {siniestro['fecha']}")
            print(f"Monto: ${siniestro['monto']:.2f} MXN")
            print(f"Descripción: {siniestro['descripcion']}")
            print(f"Ubicación: {siniestro['ubicacion']}")
            print(f"Estado: {siniestro['estado']}")
            print(f"Tipo de siniestro: {siniestro['tipo_de_siniestro']}")
            print(f"Número de póliza: {siniestro['numero_de_poliza']}")
            print(f"Nombre de asegurado: {siniestro['nombre_de_asegurado']}")
            print(f"Monto total pagado: ${siniestro['monto_total_pagado']:.2f} MXN")
            print(f"Porcentaje de cobertura: {siniestro['porcentaje_de_cobertura']}%")
            print(f"Días para resolución: {siniestro['dias_para_resolucion']} días")
            print(f"Costos administrativos: ${siniestro['costos_administrativos']:.2f} MXN")
            print(f"Impuestos: ${siniestro['impuestos']:.2f} MXN")
            print("-" * 50)
        print("Resumen Ejecutivo:")
        print(f"Total de siniestros: {len(siniestros)}")
        print(f"Total monto pagado: ${total_monto_pagado:.2f} MXN")
        print(f"Total monto de siniestros: ${total_monto_siniestros:.2f} MXN")
        print(f"Promedio de monto pagado por siniestro: ${total_monto_pagado / len(siniestros):.2f} MXN")
    except ValueError:
        print("Error: El número de siniestros debe ser un entero.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()