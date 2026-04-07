"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza análisis detallado de cartera de propiedades
TECNOLOGÍA: Python estándar
"""

import sys
import json
import os
from datetime import datetime
from math import floor

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_iva(valor):
    return valor * 0.16

def calcular_terreno(valor, metros):
    return valor / metros if metros > 0 else 0

def main():
    try:
        # Configuración por defecto
        archivo = "cartera_propiedades.json"
        if len(sys.argv) > 1:
            archivo = sys.argv[1]

        # Verificar existencia del archivo
        if not os.path.exists(archivo):
            print("Error: Archivo de cartera no encontrado.")
            return

        # Cargar datos de propiedades
        with open(archivo, 'r') as f:
            propiedades = json.load(f)

        if not propiedades:
            print("Error: Archivo vacío o con formato incorrecto.")
            return

        # Análisis de cartera
        total_propiedades = len(propiedades)
        total_valor = sum(p['valor'] for p in propiedades)
        promedio_valor = total_valor / total_propiedades
        propiedades_vendidas = sum(1 for p in propiedades if p.get('vendida', False))
        porcentaje_vendido = (propiedades_vendidas / total_propiedades * 100)

        # Cálculos adicionales
        total_terreno = sum(p.get('metros', 0) for p in propiedades)
        promedio_terreno = total_terreno / total_propiedades if total_propiedades > 0 else 0
        valor_por_m2 = total_valor / total_terreno if total_terreno > 0 else 0
        total_iva = sum(calcular_iva(p['valor']) for p in propiedades)
        propiedades_altas = sum(1 for p in propiedades if p['valor'] > 5000000)
        propiedades_bajas = sum(1 for p in propiedades if p['valor'] < 1000000)

        # Generar fecha de reporte
        fecha_reporte = datetime.now().strftime("%d/%m/%Y %H:%M")

        # Imprimir resultados
        print(f"REPORTE DE CARTERA DE PROPIEDADES - {fecha_reporte}")
        print("=" * 50)
        print(f"Total de propiedades: {total_propiedades}")
        print(f"Valor total de la cartera: ${total_valor:,.2f} MXN")
        print(f"Valor promedio por propiedad: ${promedio_valor:,.2f} MXN")
        print(f"Propiedades vendidas: {propiedades_vendidas} ({porcentaje_vendido:.1f}%)")
        print(f"Propiedades disponibles: {total_propiedades - propiedades_vendidas}")
        print(f"Metros cuadrados totales: {total_terreno:,.0f} m²")
        print(f"Valor promedio por m²: ${valor_por_m2:,.2f} MXN")
        print(f"Propiedades de alto valor (>5M MXN): {propiedades_altas}")
        print(f"Propiedades de bajo valor (<1M MXN): {propiedades_bajas}")
        print(f"IVA estimado (16%): ${total_iva:,.2f} MXN")
        print("=" * 50)
        print("RESUMEN EJECUTIVO:")
        print(f"La cartera contiene {total_propiedades} propiedades con un valor total de ${total_valor:,.2f} MXN.")
        print(f"El {porcentaje_vendido:.1f}% de las propiedades ya están vendidas.")
        print(f"El valor promedio por propiedad es de ${promedio_valor:,.2f} MXN.")
        print(f"El valor promedio por m² es de ${valor_por_m2:,.2f} MXN.")
        print(f"Se recomienda enfocar estrategias en propiedades de alto valor ({propiedades_altas} disponibles).")

    except json.JSONDecodeError:
        print("Error: Formato JSON inválido en el archivo de propiedades.")
    except KeyError as e:
        print(f"Error: Falta campo obligatorio en el archivo: {str(e)}")
    except Exception as e:
        print(f"Error en el análisis: {str(e)}")

if __name__ == "__main__":
    main()