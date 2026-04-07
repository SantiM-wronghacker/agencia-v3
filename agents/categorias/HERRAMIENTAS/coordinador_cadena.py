"""
ÁREA: CEREBRO
DESCRIPCIÓN: Conector entre agentes: recibe el output de un agente y lo prepara como input estructurado para el siguiente. Elimina ruido, extrae datos clave y formatea para sys.argv.
TECNOLOGÍA: Python estándar
"""

import sys
import json
import re
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        if len(sys.argv) < 3:
            agente_origen = "simulador_hipoteca.py"
            agente_destino = "calculadora_roi.py"
            monto_prestamo = 100000
            plazo_anios = 10
            tasa_interes = 0.05
        else:
            agente_origen = sys.argv[1]
            agente_destino = sys.argv[2]
            monto_prestamo = float(sys.argv[3])
            plazo_anios = int(sys.argv[4])
            tasa_interes = float(sys.argv[5])

        # Simulación de output del agente origen
        output_agente_origen = {
            "monto_prestamo": monto_prestamo,
            "plazo_anios": plazo_anios,
            "tasa_interes": tasa_interes
        }

        # Elimina ruido y extrae datos clave
        datos_clave = {
            "monto": output_agente_origen["monto_prestamo"],
            "plazo": output_agente_origen["plazo_anios"],
            "tasa": output_agente_origen["tasa_interes"],
            "cuota_mensual": round(output_agente_origen["monto_prestamo"] * (output_agente_origen["tasa_interes"] / 12) / (1 - math.pow(1 + output_agente_origen["tasa_interes"] / 12, -output_agente_origen["plazo_anios"] * 12)), 2),
            "interes_total": round(output_agente_origen["monto_prestamo"] * output_agente_origen["tasa_interes"] * output_agente_origen["plazo_anios"], 2),
            "total_prestamo": round(output_agente_origen["monto_prestamo"] + output_agente_origen["monto_prestamo"] * output_agente_origen["tasa_interes"] * output_agente_origen["plazo_anios"], 2)
        }

        # Formatea para sys.argv
        input_agente_destino = f"{agente_destino} {datos_clave['monto']} {datos_clave['plazo']} {datos_clave['tasa']} {datos_clave['cuota_mensual']} {datos_clave['interes_total']} {datos_clave['total_prestamo']}"

        print(f"Input para {agente_destino}: {input_agente_destino}")
        print(f"Monto del préstamo: {datos_clave['monto']}")
        print(f"Plazo del préstamo: {datos_clave['plazo']} años")
        print(f"Tasa de interés: {datos_clave['tasa'] * 100}%")
        print(f"Cuota mensual: {datos_clave['cuota_mensual']}")
        print(f"Interés total: {datos_clave['interes_total']}")
        print(f"Total del préstamo: {datos_clave['total_prestamo']}")
        print("Resumen ejecutivo:")
        print(f"El préstamo de {datos_clave['monto']} con un plazo de {datos_clave['plazo']} años y una tasa de interés de {datos_clave['tasa'] * 100}% tiene una cuota mensual de {datos_clave['cuota_mensual']}. El interés total es de {datos_clave['interes_total']} y el total del préstamo es de {datos_clave['total_prestamo']}.")

    except Exception as e:
        print(f"Error: {str(e)}")
    except ValueError:
        print("Error: Los parámetros deben ser números.")
    except IndexError:
        print("Error: Faltan parámetros.")

if __name__ == "__main__":
    main()