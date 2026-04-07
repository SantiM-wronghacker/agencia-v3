import sys
import json
import math
import os
import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        if len(sys.argv) < 2:
            raise ValueError("Falta el parámetro de capital")
        capital = float(sys.argv[1])
        if len(sys.argv) < 3:
            raise ValueError("Falta el parámetro de plazo")
        plazo = int(sys.argv[2])
        if len(sys.argv) < 4:
            raise ValueError("Falta el parámetro de tasa CETES")
        tasa_cetes = float(sys.argv[3])
        if len(sys.argv) < 5:
            raise ValueError("Falta el parámetro de tasa UDIBONOS")
        tasa_udibonos = float(sys.argv[4])
        if len(sys.argv) < 6:
            raise ValueError("Falta el parámetro de tasa CESD")
        tasa_cesd = float(sys.argv[5])

        # Cálculos
        rendimiento_cetes = capital * math.pow(1 + tasa_cetes/12, plazo*12) - capital
        rendimiento_udibonos = capital * math.pow(1 + tasa_udibonos/12, plazo*12) - capital
        rendimiento_cesd = capital * math.pow(1 + tasa_cesd/12, plazo*12) - capital
        tasa_inflacion = 0.04  # 4% anual
        rendimiento_real_cetes = rendimiento_cetes - (capital * math.pow(1 + tasa_inflacion/12, plazo*12) - capital)
        rendimiento_real_udibonos = rendimiento_udibonos - (capital * math.pow(1 + tasa_inflacion/12, plazo*12) - capital)
        rendimiento_real_cesd = rendimiento_cesd - (capital * math.pow(1 + tasa_inflacion/12, plazo*12) - capital)

        # Resultados
        print(f"Comparador de instrumentos de inversión (MXN)")
        print(f"Área: Finanzas")
        print(f"Descripción: Comparador de instrumentos de inversión")
        print(f"Tecnología: Python estándar")
        print(f"Capital inicial: ${capital:,.2f}")
        print(f"Plazo: {plazo} años")
        print(f"Tasa CETES: {tasa_cetes}% anual")
        print(f"Tasa UDIBONOS: {tasa_udibonos}% anual")
        print(f"Tasa CESD: {tasa_cesd}% anual")
        print(f"Rendimiento CETES: ${rendimiento_cetes:,.2f}")
        print(f"Rendimiento UDIBONOS: ${rendimiento_udibonos:,.2f}")
        print(f"Rendimiento CESD: ${rendimiento_cesd:,.2f}")
        print(f"Rendimiento real CETES: ${rendimiento_real_cetes:,.2f}")
        print(f"Rendimiento real UDIBONOS: ${rendimiento_real_udibonos:,.2f}")
        print(f"Rendimiento real CESD: ${rendimiento_real_cesd:,.2f}")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        if rendimiento_real_cetes > rendimiento_real_udibonos and rendimiento_real_cetes > rendimiento_real_cesd:
            print("El instrumento de inversión más rentable es el CETES.")
        elif rendimiento_real_udibonos > rendimiento_real_cetes and rendimiento_real_udibonos > rendimiento_real_cesd:
            print("El instrumento de inversión más rentable es el UDIBONOS.")
        else:
            print("El instrumento de inversión más rentable es el CESD.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()