"""
ÁREA: EDUCACIÓN
DESCRIPCIÓN: Agente que realiza calculadora roi educativo
TECNOLOGÍA: Python estándar
"""

import sys
import math

def main():
    try:
        # Parámetros por defecto
        inversion = float(sys.argv[1]) if len(sys.argv) > 1 else 100000.0
        porcentaje_interes = float(sys.argv[2]) if len(sys.argv) > 2 else 6.0  # Tasa de interés promedio en México
        años = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        tasa_inflacion = float(sys.argv[4]) if len(sys.argv) > 4 else 3.5  # Tasa de inflación promedio en México
        impuesto_renta = float(sys.argv[5]) if len(sys.argv) > 5 else 10.0  # Impuesto a la renta promedio en México

        # Cálculo del ROI
        roi = (inversion * (1 + porcentaje_interes / 100) ** años) - inversion

        # Cálculo del ROI anual
        roi_anual = (inversion * (1 + porcentaje_interes / 100)) - inversion

        # Cálculo del valor presente neto
        vpn = inversion * ((1 + porcentaje_interes / 100) ** años) / (1 + tasa_inflacion / 100) ** años - inversion

        # Cálculo de la tasa interna de retorno
        tir = ((inversion * (1 + porcentaje_interes / 100) ** años) / inversion) ** (1 / años) - 1

        # Cálculo del impuesto a la renta
        impuesto = roi * impuesto_renta / 100

        # Cálculo del ROI después de impuestos
        roi_despues_impuestos = roi - impuesto

        # Impresión de resultados
        print(f"Inversión inicial: ${inversion:,.2f} MXN")
        print(f"Interés anual: {porcentaje_interes}%")
        print(f"Años: {años}")
        print(f"Tasa de inflación: {tasa_inflacion}%")
        print(f"Impuesto a la renta: {impuesto_renta}%")
        print(f"ROI total: ${roi:,.2f} MXN")
        print(f"ROI anual: ${roi_anual:,.2f} MXN")
        print(f"Valor presente neto: ${vpn:,.2f} MXN")
        print(f"Tasa interna de retorno: {tir * 100:.2f}%")
        print(f"Impuesto a la renta sobre el ROI: ${impuesto:,.2f} MXN")
        print(f"ROI después de impuestos: ${roi_despues_impuestos:,.2f} MXN")
        print(f"Rentabilidad anual después de impuestos: {(roi_despues_impuestos / años):,.2f} MXN")
        print(f"Rentabilidad total después de impuestos durante {años} años: ${roi_despues_impuestos:,.2f} MXN")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"La inversión de ${inversion:,.2f} MXN durante {años} años con un interés anual de {porcentaje_interes}% y una tasa de inflación de {tasa_inflacion}% generará un ROI total de ${roi:,.2f} MXN y un ROI anual de ${roi_anual:,.2f} MXN.")
        print(f"Después de impuestos, el ROI total será de ${roi_despues_impuestos:,.2f} MXN y la rentabilidad anual será de {(roi_despues_impuestos / años):,.2f} MXN.")
        print(f"Se recomienda considerar los impuestos y la inflación al momento de tomar decisiones de inversión.")

    except ValueError:
        print("Error: Los parámetros deben ser numéricos.")
    except IndexError:
        print("Error: Faltan parámetros. Por favor, proporcione la inversión inicial, el interés anual, los años, la tasa de inflación y el impuesto a la renta.")

if __name__ == "__main__":
    main()