import os
import sys
import json
from datetime import datetime
import math

def cotizador_seguro_empresarial(empresa=None, seguro=None, premio=None, descuento=None, fecha_vigencia=None, tipo_cambio=None):
    try:
        # Verificar si se recibieron parametros por sys.argv
        if empresa is None:
            empresa = sys.argv[1] if len(sys.argv) > 1 else "ABC Seguros"
        if seguro is None:
            seguro = sys.argv[2] if len(sys.argv) > 2 else "Seguro de Responsabilidad Civil"
        if premio is None:
            premio = float(sys.argv[3]) if len(sys.argv) > 3 else 15000.00
        if descuento is None:
            descuento = float(sys.argv[4]) if len(sys.argv) > 4 else 0.10
        if fecha_vigencia is None:
            fecha_vigencia = datetime.now().strftime("%Y-%m-%d")
        if tipo_cambio is None:
            tipo_cambio = float(sys.argv[5]) if len(sys.argv) > 5 else 20.00

        # Verificar si los valores son válidos
        if premio < 0:
            raise ValueError("El premio no puede ser negativo")
        if descuento < 0 or descuento > 1:
            raise ValueError("El descuento debe ser entre 0 y 1")
        if tipo_cambio < 0:
            raise ValueError("El tipo de cambio no puede ser negativo")
        if premio * (1 - descuento) * tipo_cambio < 0:
            raise ValueError("El precio final no puede ser negativo")

        # Calculo del premio final con descuento
        premio_final = premio * (1 - descuento)
        iva = premio_final * 0.16
        total = premio_final + iva
        impuestos = premio_final * 0.16
        descuentos = premio_final * 0.10
        beneficios = premio_final * 0.05
        impuestos_nacionales = premio_final * 0.10
        impuestos_estatales = premio_final * 0.05
        impuestos_municipales = premio_final * 0.02

        # Impresion de resultados
        print("ÁREA: SEGUROS")
        print("DESCRIPCIÓN: Cotizador seguro empresarial")
        print("TECNOLOGÍA: Python estándar")
        print(f"Empresa: {empresa}")
        print(f"Seguro: {seguro}")
        print(f"Precio: ${premio:.2f}")
        print(f"Descuento: {descuento*100}%")
        print(f"Tipo de cambio: {tipo_cambio}")
        print(f"Fecha de vigencia: {fecha_vigencia}")
        print(f"Precio final: ${premio_final:.2f}")
        print(f"Impuestos: ${iva:.2f}")
        print(f"Total: ${total:.2f}")
        print(f"Descuentos: ${descuentos:.2f}")
        print(f"Beneficios: ${beneficios:.2f}")
        print(f"Impuestos nacionales: ${impuestos_nacionales:.2f}")
        print(f"Impuestos estatales: ${impuestos_estatales:.2f}")
        print(f"Impuestos municipales: ${impuestos_municipales:.2f}")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El seguro de {seguro} para la empresa {empresa} tiene un precio final de ${premio_final:.2f} después de aplicar un descuento del {descuento*100}%.")
        print(f"Los impuestos totales son de ${iva + impuestos_nacionales + impuestos_estatales + impuestos_municipales:.2f}.")
        print(f"Los beneficios totales son de ${beneficios:.2f}.")

    except IndexError:
        print("Falta de argumentos")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    cotizador_seguro_empresarial()