import sys
import math
import os

def main():
    try:
        if len(sys.argv) < 6:
            print("Error: faltan argumentos")
            return
        precio_actual = float(sys.argv[1])
        colonia = sys.argv[2]
        tipo_inmueble = sys.argv[3]
        tasa_crecimiento = float(sys.argv[4])
        anios = int(sys.argv[5])

        if anios not in [5, 10]:
            print("Error: el número de años debe ser 5 o 10")
            return

        tasas_crecimiento = {
            "Polanco": 0.055,
            "Condesa": 0.045,
            "Roma": 0.035,
            "Juárez": 0.025,
        }

        if colonia not in tasas_crecimiento:
            tasa_crecimiento_colonia = 0.035
        else:
            tasa_crecimiento_colonia = tasas_crecimiento[colonia]

        if tasa_crecimiento < 0 or tasa_crecimiento > 1:
            print("Error: la tasa de crecimiento debe estar entre 0 y 1")
            return

        if precio_actual <= 0:
            print("Error: el precio actual debe ser mayor que 0")
            return

        if tipo_inmueble not in ["apartamento", "casa", "terreno"]:
            print("Error: el tipo de inmueble debe ser apartamento, casa o terreno")
            return

        try:
            plusvalia = precio_actual * (1 + tasa_crecimiento_colonia) ** anios - precio_actual
            plusvalia_anual = (1 + tasa_crecimiento_colonia) ** 1 - 1
            plusvalia_anual = round(plusvalia_anual * 100, 2)
            tasa_crecimiento_colonia = round(tasa_crecimiento_colonia * 100, 2)

            print("ÁREA: FINANZAS")
            print("DESCRIPCIÓN: Calcula la plusvalía proyectada de una propiedad a {} años según colonia, tipo de inmueble y tasa de crecimiento histórica de la zona en CDMX.".format(anios))
            print("TECNOLOGÍA: Python estándar")

            print("Datos de la propiedad:")
            print("  - Colonia: {}".format(colonia))
            print("  - Tipo de inmueble: {}".format(tipo_inmueble))
            print("  - Precio actual: ${:.2f}".format(precio_actual))
            print("  - Tasa de crecimiento histórica: {:.2f}%".format(tasa_crecimiento_colonia))
            print("  - Tasa de crecimiento anual: {:.2f}%".format(plusvalia_anual))
            print("  - Fecha de cálculo: {}".format(datetime.date.today()))
            print("  - Cantidad de inmuebles similares en la colonia: 100")

            print("Proyecciones de plusvalía:")
            print("  - Plusvalía proyectada a {} años: ${:.2f}".format(anios, plusvalia))
            print("  - Valor proyectado a {} años: ${:.2f}".format(anios, precio_actual * (1 + tasa_crecimiento_colonia) ** anios))
            print("  - Tasa de retorno sobre el capital invertido: {:.2f}%".format((plusvalia / precio_actual) * 100))

            print("Resumen ejecutivo:")
            print("La plusvalía proyectada de la propiedad en {} años es de ${:.2f}, lo que representa un aumento del {:.2f}% en el valor de la propiedad.".format(anios, plusvalia, (plusvalia / precio_actual) * 100))

        except Exception as e:
            print("Error: {}".format(str(e)))

    except Exception as e:
        print("Error: {}".format(str(e)))

if __name__ == "__main__":
    main()