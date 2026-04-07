"""
ÁREA: LOGÍSTICA
DESCRIPCIÓN: Agente que realiza calculadora costo importacion
TECNOLOGÍA: Python estándar
"""

import sys
import math

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto realistas para México
        costo_producto = float(sys.argv[1]) if len(sys.argv) > 1 else 1000.0
        distancia = float(sys.argv[2]) if len(sys.argv) > 2 else 5000.0  # km
        peso = float(sys.argv[3]) if len(sys.argv) > 3 else 200.0  # kg
        arancel = float(sys.argv[4]) if len(sys.argv) > 4 else 0.15  # 15%
        seguro = float(sys.argv[5]) if len(sys.argv) > 5 else 0.02  # 2%
        tipo_cambio = float(sys.argv[6]) if len(sys.argv) > 6 else 20.0  # tipo de cambio

        # Cálculos
        flete = 0.5 * distancia * peso
        costo_total = costo_producto + flete
        costo_con_arancel = costo_total * (1 + arancel)
        costo_con_seguro = costo_con_arancel * (1 + seguro)
        iva = costo_con_seguro * 0.16
        costo_total_con_iva = costo_con_seguro + iva
        costo_total_dolares = costo_total_con_iva / tipo_cambio

        # Resultados
        print("Cálculo de costo de importación:")
        print(f"1. Costo producto: ${costo_producto:.2f} MXN")
        print(f"2. Flete (50% de distancia x peso): ${flete:.2f} MXN")
        print(f"3. Costo con arancel ({arancel*100:.0f}%): ${costo_con_arancel:.2f} MXN")
        print(f"4. Costo con seguro ({seguro*100:.0f}%): ${costo_con_seguro:.2f} MXN")
        print(f"5. Total con IVA (16%): ${costo_total_con_iva:.2f} MXN")
        print(f"6. Tipo de cambio: ${tipo_cambio:.2f} MXN/USD")
        print(f"7. Costo total en dólares: ${costo_total_dolares:.2f} USD")
        print(f"8. Peso total: {peso:.2f} kg")
        print(f"9. Distancia total: {distancia:.2f} km")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El costo total de importación es de ${costo_total_con_iva:.2f} MXN")
        print(f"El costo total en dólares es de ${costo_total_dolares:.2f} USD")
        print(f"El tipo de cambio utilizado es de ${tipo_cambio:.2f} MXN/USD")

    except IndexError:
        print("Error: No se proporcionaron suficientes parámetros")
        print("Uso: python calculadora_costo_importacion.py [costo_producto] [distancia_km] [peso_kg] [arancel] [seguro] [tipo_cambio]")
        print("Valores por defecto: costo=1000, distancia=5000, peso=200, arancel=15%, seguro=2%, tipo_cambio=20")

    except ValueError:
        print("Error: Los parámetros deben ser números")
        print("Uso: python calculadora_costo_importacion.py [costo_producto] [distancia_km] [peso_kg] [arancel] [seguro] [tipo_cambio]")
        print("Valores por defecto: costo=1000, distancia=5000, peso=200, arancel=15%, seguro=2%, tipo_cambio=20")

    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")
        print("Uso: python calculadora_costo_importacion.py [costo_producto] [distancia_km] [peso_kg] [arancel] [seguro] [tipo_cambio]")
        print("Valores por defecto: costo=1000, distancia=5000, peso=200, arancel=15%, seguro=2%, tipo_cambio=20")

if __name__ == "__main__":
    main()