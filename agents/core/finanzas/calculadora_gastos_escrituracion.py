"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza calculadora gastos escrituracion
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
        # Parámetros por defecto realistas
        precio_propiedad = float(sys.argv[1]) if len(sys.argv) > 1 else 1500000.0
        estado = sys.argv[2] if len(sys.argv) > 2 else "CDMX"

        # Cálculo de gastos
        if estado == "CDMX":
            impuesto_transmision = 0.03 * precio_propiedad
            honorarios_notario = 0.015 * precio_propiedad
            avaluo = 0.005 * precio_propiedad
            registro_publico = 0.002 * precio_propiedad
            isr = 0.008 * precio_propiedad
            otros_gastos = 0.001 * precio_propiedad
        elif estado == "EDOMEX":
            impuesto_transmision = 0.025 * precio_propiedad
            honorarios_notario = 0.012 * precio_propiedad
            avaluo = 0.004 * precio_propiedad
            registro_publico = 0.0015 * precio_propiedad
            isr = 0.007 * precio_propiedad
            otros_gastos = 0.0012 * precio_propiedad
        else:
            impuesto_transmision = 0.02 * precio_propiedad
            honorarios_notario = 0.01 * precio_propiedad
            avaluo = 0.003 * precio_propiedad
            registro_publico = 0.001 * precio_propiedad
            isr = 0.005 * precio_propiedad
            otros_gastos = 0.001 * precio_propiedad

        total_gastos = (impuesto_transmision + honorarios_notario +
                        avaluo + registro_publico + isr + otros_gastos)

        # Salida
        print(f"Cálculo de gastos de escrituración para propiedad de ${precio_propiedad:,.2f} en {estado}")
        print(f"Impuesto de transmisión: ${impuesto_transmision:,.2f}")
        print(f"Honorarios notario: ${honorarios_notario:,.2f}")
        print(f"Avalúo: ${avaluo:,.2f}")
        print(f"Registro público: ${registro_publico:,.2f}")
        print(f"ISR: ${isr:,.2f}")
        print(f"Otros gastos: ${otros_gastos:,.2f}")
        print(f"Total de gastos: ${total_gastos:,.2f}")
        print(f"Total a pagar (incluyendo precio de propiedad): ${precio_propiedad + total_gastos:,.2f}")
        print(f"Porcentaje de gastos con respecto al precio de propiedad: {(total_gastos / precio_propiedad) * 100:.2f}%")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El total de gastos para la escrituración de la propiedad es de ${total_gastos:,.2f}.")
        print(f"El monto total a pagar, incluyendo el precio de la propiedad, es de ${precio_propiedad + total_gastos:,.2f}.")
        print(f"Los gastos representan {(total_gastos / precio_propiedad) * 100:.2f}% del precio de la propiedad.")

    except ValueError:
        print("Error: El precio de la propiedad debe ser un número.")
        print("Uso: python calculadora_gastos_escrituracion.py <precio_propiedad> <estado>")
        print("Ejemplo: python calculadora_gastos_escrituracion.py 1500000 CDMX")
    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")
        print("Uso: python calculadora_gastos_escrituracion.py <precio_propiedad> <estado>")
        print("Ejemplo: python calculadora_gastos_escrituracion.py 1500000 CDMX")

if __name__ == "__main__":
    main()