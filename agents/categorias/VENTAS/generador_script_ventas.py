"""ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza generador script ventas
TECNOLOGÍA: Python estándar, sin web_bridge
"""

import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios(archivo_config="precios.json"):
    try:
        # Obtener precios de venta desde archivo de configuración
        with open(archivo_config, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: El archivo de configuración '{archivo_config}' no existe.")
        return None
    except json.JSONDecodeError:
        print(f"Error: El archivo de configuración '{archivo_config}' no es válido.")
        return None
    except Exception as e:
        print(f"Error al obtener precios: {e}")
        return None

def generar_script_ventas(precios):
    try:
        # Generar script de ventas
        script = ""
        for producto, precio in precios.items():
            script += f"Venta de {producto} por {precio:.2f} pesos\n"
        return script
    except Exception as e:
        print(f"Error al generar script de ventas: {e}")
        return None

def calcular_total(precios):
    try:
        # Calcular total de ventas
        total = sum(precios.values())
        return total
    except TypeError:
        print("Error: La lista de precios no es válida.")
        return None
    except Exception as e:
        print(f"Error al calcular total: {e}")
        return None

def generar_resumen_ejecutivo(total):
    try:
        # Generar resumen ejecutivo
        fecha_hoy = datetime.date.today().strftime("%d/%m/%Y")
        iva = 0.16  # IVA en México
        total_iva = total * iva
        total_final = total + total_iva
        return f"Resumen Ejecutivo - {fecha_hoy}\nTotal de Ventas: {total:.2f} pesos\nIVA (16%): {total_iva:.2f} pesos\nTotal Final: {total_final:.2f} pesos\n"
    except Exception as e:
        print(f"Error al generar resumen ejecutivo: {e}")
        return None

def generar_resumen_factura(total, iva, total_final):
    try:
        # Generar resumen de factura
        fecha_hoy = datetime.date.today().strftime("%d/%m/%Y")
        return f"Resumen de Factura - {fecha_hoy}\nTotal de Ventas: {total:.2f} pesos\nIVA (16%): {iva:.2f} pesos\nTotal Final: {total_final:.2f} pesos\n"
    except Exception as e:
        print(f"Error al generar resumen de factura: {e}")
        return None

def main():
    try:
        # Obtener argumentos de línea de comandos
        if len(sys.argv) < 2:
            print("Faltan argumentos de línea de comandos")
            sys.exit(1)
        
        archivo_salida = sys.argv[1]
        archivo_config = sys.argv[2] if len(sys.argv) > 2 else "precios.json"
        
        # Extraer precios de venta
        precios = extraer_precios(archivo_config)
        if precios:
            # Generar script de ventas
            script = generar_script_ventas(precios)
            # Calcular total de ventas
            total = calcular_total(precios)
            if total:
                # Generar resumen ejecutivo
                resumen_ejecutivo = generar_resumen_ejecutivo(total)
                # Generar resumen de factura
                iva = total * 0.16
                total_final = total + iva
                resumen_factura = generar_resumen_factura(total, iva, total_final)
                # Escribir en archivo de salida
                with open(archivo_salida, "w") as f:
                    f.write(script)
                    f.write("\n")
                    f.write(resumen_ejecutivo)
                    f.write("\n")
                    f.write(resumen_factura)
                    print(f"Archivo '{archivo_salida}' creado con éxito.")
    except Exception as e:
        print(f"Error principal: {e}")

if __name__ == "__main__":
    main()