"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora costo envio mexico con tarifas realistas
TECNOLOGÍA: Python estándar
"""

import sys
import math
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_costo_envio(origen, destino, peso, distancia):
    # Tarifas realistas para México (2023)
    COSTO_FIJO = 50.00
    COSTO_KM = 15.50
    COSTO_KG = 22.75
    COSTO_MINIMO = 100.00

    # Ajuste por zona (ejemplo: 10% más caro a zonas remotas)
    zonas_remotas = ['Chihuahua', 'Durango', 'Baja California Sur']
    factor_zona = 1.10 if destino in zonas_remotas else 1.00

    # Validaciones
    if peso <= 0:
        raise ValueError("El peso debe ser mayor a 0 kg")
    if distancia <= 0:
        raise ValueError("La distancia debe ser mayor a 0 km")

    # Cálculo del costo total
    costo_distancia = distancia * COSTO_KM * factor_zona
    costo_peso = peso * COSTO_KG
    costo_total = max(COSTO_FIJO + costo_distancia + costo_peso, COSTO_MINIMO)

    # Cálculo del tiempo de entrega
    tiempo_entrega = distancia / 100  # km/h

    # Cálculo del costo de seguro
    costo_seguro = peso * 0.05  # 5% del peso

    return {
        "origen": origen,
        "destino": destino,
        "peso_kg": peso,
        "distancia_km": distancia,
        "costo_distancia": round(costo_distancia, 2),
        "costo_peso": round(costo_peso, 2),
        "costo_fijo": COSTO_FIJO,
        "costo_total": round(costo_total, 2),
        "factor_zona": factor_zona,
        "es_zona_remota": destino in zonas_remotas,
        "tiempo_entrega": round(tiempo_entrega, 2),
        "costo_seguro": round(costo_seguro, 2)
    }

def main():
    try:
        # Parámetros por defecto realistas
        origen = sys.argv[1] if len(sys.argv) > 1 else "CDMX"
        destino = sys.argv[2] if len(sys.argv) > 2 else "Guadalajara"
        peso = float(sys.argv[3]) if len(sys.argv) > 3 else 5.2
        distancia = float(sys.argv[4]) if len(sys.argv) > 4 else 550.0

        resultado = calcular_costo_envio(origen, destino, peso, distancia)

        print("=== DETALLES DEL ENVÍO ===")
        print(f"Ruta: {resultado['origen']} → {resultado['destino']}")
        print(f"Peso: {resultado['peso_kg']} kg")
        print(f"Distancia: {resultado['distancia_km']} km")
        print(f"Costo distancia: ${resultado['costo_distancia']}")
        print(f"Costo peso: ${resultado['costo_peso']}")
        print(f"Costo fijo: ${resultado['costo_fijo']}")
        print(f"Costo total: ${resultado['costo_total']}")
        print(f"Factor zona: {resultado['factor_zona']}")
        print(f"Es zona remota: {resultado['es_zona_remota']}")
        print(f"Tiempo entrega: {resultado['tiempo_entrega']} horas")
        print(f"Costo seguro: ${resultado['costo_seguro']}")

        print("\n=== RESUMEN EJECUTIVO ===")
        print(f"El costo total del envío es ${resultado['costo_total']}")
        print(f"El tiempo de entrega es de {resultado['tiempo_entrega']} horas")
        print(f"El costo de seguro es de ${resultado['costo_seguro']}")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()