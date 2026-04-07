import sys
import math

# Encabezado
AREA = "HERRAMIENTAS"
DESCRIPCION = "Comparador de Créditos"
TECNOLOGIA = "Python"

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def calcular_pago_mensual(monto, tasa, plazo):
    return monto * (tasa / 100 / 12) / (1 - math.pow(1 + tasa / 100 / 12, -plazo * 12))

def calcular_costo_total(monto, tasa, plazo):
    return calcular_pago_mensual(monto, tasa, plazo) * plazo * 12

def calcular_cat(monto, costo_total):
    return (costo_total - monto) / monto * 100

def main():
    try:
        if len(sys.argv) == 6:
            monto = float(sys.argv[1])
            tasa1 = float(sys.argv[2])
            tasa2 = float(sys.argv[3])
            tasa3 = float(sys.argv[4])
            plazo = int(sys.argv[5])
        else:
            monto = 2000000  # monto promedio de un crédito hipotecario en México
            tasa1 = 9.5  # tasa de interés promedio de un crédito hipotecario en México
            tasa2 = 10.2  # tasa de interés promedio de un crédito hipotecario con garantía en México
            tasa3 = 11.0  # tasa de interés promedio de un crédito hipotecario sin garantía en México
            plazo = 20  # plazo promedio de un crédito hipotecario en México

        pago_mensual1 = calcular_pago_mensual(monto, tasa1, plazo)
        pago_mensual2 = calcular_pago_mensual(monto, tasa2, plazo)
        pago_mensual3 = calcular_pago_mensual(monto, tasa3, plazo)

        costo_total1 = calcular_costo_total(monto, tasa1, plazo)
        costo_total2 = calcular_costo_total(monto, tasa2, plazo)
        costo_total3 = calcular_costo_total(monto, tasa3, plazo)

        cat1 = calcular_cat(monto, costo_total1)
        cat2 = calcular_cat(monto, costo_total2)
        cat3 = calcular_cat(monto, costo_total3)

        print(f"Resumen de opciones de crédito:")
        print(f"Opción 1: Tasa de interés {tasa1}%, plazo {plazo} años, monto {monto}")
        print(f"  - Pago mensual: {pago_mensual1:.2f}")
        print(f"  - Costo total: {costo_total1:.2f}")
        print(f"  - CAT: {cat1:.2f}%")
        print(f"Opción 2: Tasa de interés {tasa2}%, plazo {plazo} años, monto {monto}")
        print(f"  - Pago mensual: {pago_mensual2:.2f}")
        print(f"  - Costo total: {costo_total2:.2f}")
        print(f"  - CAT: {cat2:.2f}%")
        print(f"Opción 3: Tasa de interés {tasa3}%, plazo {plazo} años, monto {monto}")
        print(f"  - Pago mensual: {pago_mensual3:.2f}")
        print(f"  - Costo total: {costo_total3:.2f}")
        print(f"  - CAT: {cat3:.2f}%")

        print(f"\nResumen ejecutivo:")
        print(f"El crédito con la tasa de interés más baja ({tasa1}%) resulta ser la opción más asequible, con un pago mensual de {pago_mensual1:.2f} y un costo total de {costo_total1:.2f}. El CAT de esta opción es de {cat1:.2f}%.")

    except ValueError:
        print("Error: Los valores de entrada deben ser números.")
    except IndexError:
        print("Error: Faltan argumentos de entrada.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()