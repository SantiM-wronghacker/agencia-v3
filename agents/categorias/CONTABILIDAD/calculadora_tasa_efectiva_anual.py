import sys
import math
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcula_tasa_efectiva_anual(tasa_nominal, frecuencia):
    return (1 + (tasa_nominal / 100) / frecuencia) ** frecuencia - 1

def calcula_interes_compuesto(capital, tasa_efectiva_anual, años):
    return capital * (1 + tasa_efectiva_anual) ** años - capital

def calcula_cuota_anual(capital, tasa_efectiva_anual, años):
    return capital * tasa_efectiva_anual / (1 - (1 + tasa_efectiva_anual) ** (-años))

def calcula_precio_presente(anualidad, tasa_efectiva_anual, años):
    return anualidad / (tasa_efectiva_anual * (1 + tasa_efectiva_anual) ** años)

def main():
    try:
        tasa_nominal = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0
        frecuencia = int(sys.argv[2]) if len(sys.argv) > 2 else 12
        capital = float(sys.argv[3]) if len(sys.argv) > 3 else 10000.0
        años = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        anualidad = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0

        if frecuencia < 1 or frecuencia > 365:
            raise ValueError("Frecuencia debe ser entre 1 y 365")

        if capital < 0 or tasa_nominal < 0 or años < 1 or anualidad < 0:
            raise ValueError("Valores no pueden ser negativos")

        try:
            tasa_efectiva_anual = calcula_tasa_efectiva_anual(tasa_nominal, frecuencia)
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)

        print("AREA: FINANZAS")
        print("DESCRIPCION: Calculadora de tasa efectiva anual")
        print("TECNOLOGIA: Python")
        print(f"Tasa nominal: {tasa_nominal}%")
        print(f"Frecuencia de pago: {frecuencia} veces al año")
        print(f"Tasa efectiva anual: {tasa_efectiva_anual * 100:.4f}%")
        print(f"Interés anual: {(tasa_efectiva_anual * 100):.4f}%")
        print(f"Ejemplo con ${capital:.2f}: ${capital * (1 + tasa_efectiva_anual):.2f}")
        print(f"Interés compuesto durante {años} años: ${calcula_interes_compuesto(capital, tasa_efectiva_anual, años):.2f}")
        print(f"Cuota anual para pagar ${capital} en {años} años: ${calcula_cuota_anual(capital, tasa_efectiva_anual, años):.2f}")
        print(f"Precio presente de ${anualidad} durante {años} años a una tasa de {tasa_efectiva_anual * 100:.4f}%: ${calcula_precio_presente(anualidad, tasa_efectiva_anual, años):.2f}")

        print("\nRESUMEN EJECUTIVO:")
        print(f"La tasa efectiva anual para una tasa nominal de {tasa_nominal}% y una frecuencia de pago de {frecuencia} veces al año es de {tasa_efectiva_anual * 100:.4f}%.")

        if tasa_efectiva_anual > 0.1:
            print("Nota: La tasa efectiva anual es alta, lo que puede indicar un alto riesgo de pérdida de capital.")
        elif tasa_efectiva_anual < 0.01:
            print("Nota: La tasa efectiva anual es baja, lo que puede indicar un bajo rendimiento del inversión.")

    except IndexError:
        print("Error: Faltan argumentos de línea de comandos.")
    except ValueError as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()