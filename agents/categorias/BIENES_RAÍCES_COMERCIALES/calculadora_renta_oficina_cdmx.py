"""
ÁREA: BIENES RAÍCES COMERCIALES
DESCRIPCIÓN: Agente que realiza calculadora renta oficina cdmx
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcular_renta_oficina(metros_cuadrados=None, zona=None, mantenimiento=None, estacionamiento=None):
    # Parámetros por defecto realistas para CDMX
    metros_cuadrados = float(metros_cuadrados) if metros_cuadrados else 50.0
    zona = zona if zona else "Reforma"
    mantenimiento = float(mantenimiento) if mantenimiento else 0.15
    estacionamiento = estacionamiento if estacionamiento else "no"

    # Tarifas por zona (pesos por m2/mes)
    tarifas = {
        "Polanco": 1200,
        "Reforma": 950,
        "Santa Fe": 1050,
        "Condesa": 1100,
        "Roma": 900
    }

    # Cálculo base
    renta_base = metros_cuadrados * tarifas.get(zona, 800)  # 800 default si no está en el diccionario

    # Cálculo de mantenimiento
    mantenimiento_mensual = renta_base * mantenimiento

    # Costo estacionamiento (si aplica)
    estacionamiento_costo = 0
    if estacionamiento.lower() == "si":
        estacionamiento_costo = 3500

    # Cálculo total
    total_mensual = renta_base + mantenimiento_mensual + estacionamiento_costo
    anual = total_mensual * 12

    return {
        "metros_cuadrados": metros_cuadrados,
        "zona": zona,
        "renta_base_mensual": round(renta_base, 2),
        "mantenimiento_mensual": round(mantenimiento_mensual, 2),
        "estacionamiento": estacionamiento,
        "total_mensual": round(total_mensual, 2),
        "total_anual": round(anual, 2)
    }

def main():
    try:
        metros_cuadrados = sys.argv[1] if len(sys.argv) > 1 else None
        zona = sys.argv[2] if len(sys.argv) > 2 else None
        mantenimiento = sys.argv[3] if len(sys.argv) > 3 else None
        estacionamiento = sys.argv[4] if len(sys.argv) > 4 else None

        resultados = calcular_renta_oficina(metros_cuadrados, zona, mantenimiento, estacionamiento)

        print("Cálculo de renta para oficina en CDMX:")
        print(f"1. Área: {resultados['metros_cuadrados']} m² en zona {resultados['zona']}")
        print(f"2. Renta base mensual: ${resultados['renta_base_mensual']:,}")
        print(f"3. Mantenimiento mensual: ${resultados['mantenimiento_mensual']:,}")
        print(f"4. Estacionamiento: {resultados['estacionamiento']}")
        print(f"5. Costo estacionamiento mensual: ${3500 if resultados['estacionamiento'] == 'si' else 0:,}")
        print(f"6. Total mensual: ${resultados['total_mensual']:,}")
        print(f"7. Total anual: ${resultados['total_anual']:,}")
        print(f"8. Porcentaje de mantenimiento: {float(mantenimiento) * 100 if mantenimiento else 15}%")
        print("Resumen ejecutivo:")
        print(f"La renta total anual para una oficina de {resultados['metros_cuadrados']} m² en {resultados['zona']} es de ${resultados['total_anual']:,}.")
        print(f"El costo mensual de estacionamiento es de ${3500 if resultados['estacionamiento'] == 'si' else 0:,}.")
        print(f"El porcentaje de mantenimiento es de {float(mantenimiento) * 100 if mantenimiento else 15}%.")        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()