import sys
import math

def main():
    try:
        # Parámetros por defecto con valores realistas para México
        cac = float(sys.argv[1]) if len(sys.argv) > 1 else 50000.0  # CAC en MXN
        ltv = float(sys.argv[2]) if len(sys.argv) > 2 else 1500000.0  # LTV en MXN
        meses = int(sys.argv[3]) if len(sys.argv) > 3 else 12  # Periodo en meses
        tasa_descuento = float(sys.argv[4]) if len(sys.argv) > 4 else 10.0  # Tasa de descuento para el cálculo del valor presente

        # Cálculos
        ratio = ltv / cac
        payback_period = cac / (ltv / meses)
        roi = (ltv - cac) / cac * 100
        ltv_anual = ltv * 12 / meses
        margen = ltv - cac
        tasa_recuperacion = (ltv / cac) * 100
        punto_equilibrio = (cac / (ltv - cac)) * 100 if ltv > cac else 0
        crecimiento_anual = ((ltv_anual - cac) / cac) * 100
        valor_presente = ltv / (1 + tasa_descuento/100)**meses
        tasa_de_retorno = (ltv - cac) / cac * 100
        periodo_de_recuperacion = payback_period * (1 + tasa_descuento/100)**meses
        ingresos_netos = ltv - cac
        utilidad_neta = ingresos_netos / ltv * 100
        rentabilidad = ingresos_netos / cac * 100
        ratio_inversión = cac / ltv

        # Resultados
        print("ÁREA: FINANZAS")
        print("DESCRIPCIÓN: Agente que realiza calculadora cac ltv")
        print("TECNOLOGÍA: Python estándar")
        print(f"CAC: ${cac:.2f} MXN")
        print(f"LTV: ${ltv:.2f} MXN")
        print(f"Ratio LTV/CAC: {ratio:.2f}")
        print(f"Payback Period: {payback_period:.1f} meses")
        print(f"ROI: {roi:.1f}%")
        print(f"Margen por cliente: ${margen:.2f} MXN")
        print(f"Tasa de recuperación: {tasa_recuperacion:.1f}%")
        print(f"Punto de equilibrio: {punto_equilibrio:.1f}%")
        print(f"Crecimiento anual: {crecimiento_anual:.1f}%")
        print(f"LTV anual: ${ltv_anual:.2f} MXN")
        print(f"Meses para recuperar la inversión: {payback_period:.1f} meses")
        print(f"Valor presente: ${valor_presente:.2f} MXN")
        print(f"Tasa de retorno: {tasa_de_retorno:.1f}%")
        print(f"Periodo de recuperación: {periodo_de_recuperacion:.1f} meses")
        print(f"Ingresos netos: ${ingresos_netos:.2f} MXN")
        print(f"Utilidad neta: {utilidad_neta:.1f}%")
        print(f"Rentabilidad: {rentabilidad:.1f}%")
        print(f"Ratio inversión: {ratio_inversión:.2f}")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El proyecto tiene un LTV de ${ltv:.2f} MXN y un CAC de ${cac:.2f} MXN.")
        print(f"El ratio LTV/CAC es de {ratio:.2f} y el payback period es de {payback_period:.1f} meses.")
        print(f"La tasa de recuperación es de {tasa_recuperacion:.1f}% y el punto de equilibrio es de {punto_equilibrio:.1f}%.")

    except IndexError:
        print("Error: Faltan argumentos de entrada.")
    except ValueError:
        print("Error: Los argumentos de entrada deben ser números.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()