"""
ÁREA: OPERACIONES
DESCRIPCIÓN: Agente que realiza calculadora eficiencia operativa con métricas financieras avanzadas para México
TECNOLOGÍA: Python estándar
"""

import sys
import math
from datetime import datetime

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calculadora_eficiencia_operativa(ventas, costos, personal, inflacion=0.04):
    try:
        if ventas <= 0 or costos < 0 or personal <= 0:
            raise ValueError("Valores inválidos")

        eficiencia = (ventas - costos) / ventas
        productividad = ventas / personal
        rentabilidad = (ventas - costos) / personal
        margen_de_utilidad = (ventas - costos) / ventas
        retorno_de_la_inversion = (ventas - costos) / costos

        # Métricas adicionales para contexto mexicano
        costo_por_empleado = costos / personal
        utilidad_neta = ventas - costos
        utilidad_por_empleado = utilidad_neta / personal
        indice_eficiencia = eficiencia * (1 + inflacion)

        return (
            eficiencia, productividad, rentabilidad, margen_de_utilidad,
            retorno_de_la_inversion, costo_por_empleado, utilidad_neta,
            utilidad_por_empleado, indice_eficiencia
        )
    except ZeroDivisionError:
        return None
    except ValueError as e:
        print(f"Error de validación: {e}")
        return None

def main():
    try:
        ventas = float(sys.argv[1]) if len(sys.argv) > 1 else 1000000.0
        costos = float(sys.argv[2]) if len(sys.argv) > 2 else 500000.0
        personal = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        inflacion = float(sys.argv[4]) if len(sys.argv) > 4 else 0.04

        resultados = calculadora_eficiencia_operativa(ventas, costos, personal, inflacion)

        if resultados is not None:
            eficiencia, productividad, rentabilidad, margen_de_utilidad, retorno_de_la_inversion, \
            costo_por_empleado, utilidad_neta, utilidad_por_empleado, indice_eficiencia = resultados

            print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Ventas: ${ventas:,.2f} MXN")
            print(f"Costos: ${costos:,.2f} MXN")
            print(f"Personal: {personal} personas")
            print(f"Costo por empleado: ${costo_por_empleado:,.2f} MXN")
            print(f"Utilidad neta: ${utilidad_neta:,.2f} MXN")
            print(f"Eficiencia operativa: {eficiencia*100:.2f}%")
            print(f"Productividad: ${productividad:,.2f} MXN por persona")
            print(f"Rentabilidad: ${rentabilidad:,.2f} MXN por persona")
            print(f"Margen de utilidad: {margen_de_utilidad*100:.2f}%")
            print(f"Retorno de la inversión: {retorno_de_la_inversion*100:.2f}%")
            print(f"Utilidad por empleado: ${utilidad_por_empleado:,.2f} MXN")
            print(f"Índice de eficiencia ajustado por inflación: {indice_eficiencia*100:.2f}%")
            print(f"Resumen ejecutivo: La eficiencia operativa es de {eficiencia*100:.2f}%, con una productividad de ${productividad:,.2f} MXN por persona y una rentabilidad de ${rentabilidad:,.2f} MXN por persona. La utilidad neta es de ${utilidad_neta:,.2f} MXN, lo que representa un margen del {margen_de_utilidad*100:.2f}%.")
        else:
            print("Error al calcular la eficiencia operativa")

    except ValueError:
        print("Error: Valores numéricos inválidos")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()