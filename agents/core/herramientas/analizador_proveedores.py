import os
import sys
import json
import math
import re
import datetime
import random

def analizador_proveedores(proveedores, precios):
    try:
        # Analizar precios y resultados
        mejor_proveedor = max(precios, key=precios.get)
        peor_proveedor = min(precios, key=precios.get)
        promedio_precio = sum(precios.values()) / len(precios)
        desviacion_estandar = math.sqrt(sum((p - promedio_precio) ** 2 for p in precios.values()) / len(precios))
        varianza = sum((p - promedio_precio) ** 2 for p in precios.values()) / (len(precios) - 1)
        maximo_precio = max(precios.values())
        minimo_precio = min(precios.values())
        rango_precio = maximo_precio - minimo_precio
        mediana_precio = sorted(precios.values())[len(precios) // 2]
        cuartil_1_precio = sorted(precios.values())[len(precios) // 4]
        cuartil_3_precio = sorted(precios.values())[3 * len(precios) // 4]

        # Imprimir resultados
        print(f"AREA: HERRAMIENTAS")
        print(f"DESCRIPCION: Analizador Proveedores")
        print(f"TECNOLOGIA: Python")
        print(f"Mejor proveedor: {mejor_proveedor} - Precio: {precios[mejor_proveedor]:.2f} MXN")
        print(f"Peor proveedor: {peor_proveedor} - Precio: {precios[peor_proveedor]:.2f} MXN")
        print(f"Promedio de precios: {promedio_precio:.2f} MXN")
        print(f"Desviación estándar: {desviacion_estandar:.2f} MXN")
        print(f"Varianza: {varianza:.2f} MXN")
        print(f"Maximo precio: {maximo_precio:.2f} MXN")
        print(f"Minimo precio: {minimo_precio:.2f} MXN")
        print(f"Rango de precios: {rango_precio:.2f} MXN")
        print(f"Mediana de precios: {mediana_precio:.2f} MXN")
        print(f"Cuartil 1 de precios: {cuartil_1_precio:.2f} MXN")
        print(f"Cuartil 3 de precios: {cuartil_3_precio:.2f} MXN")
        print(f"Resumen ejecutivo: El análisis de precios ha revelado una variabilidad significativa entre los diferentes proveedores.")
        print(f"Resumen ejecutivo: El promedio de precios es {promedio_precio:.2f} MXN, mientras que la desviación estándar es de {desviacion_estandar:.2f} MXN.")
        print(f"Resumen ejecutivo: El rango de precios es de {minimo_precio:.2f} MXN a {maximo_precio:.2f} MXN.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--analizar":
        if len(sys.argv) > 2 and sys.argv[2] == "--proveedores":
            if len(sys.argv) > 3:
                proveedores = sys.argv[3:]
                precios = {}
                for proveedor in proveedores:
                    try:
                        precio = float(sys.argv[sys.argv.index(proveedor) + 1])
                        precios[proveedor] = precio
                    except ValueError:
                        print(f"Error: El precio de {proveedor} no es un número.")
                if len(precios) > 0:
                    analizador_proveedores(proveedores, precios)
                else:
                    print("Error: No se han proporcionado precios.")
    else:
        print("Error: No se ha proporcionado la opción --analizar --proveedores.")

if __name__ == "__main__":
    main()