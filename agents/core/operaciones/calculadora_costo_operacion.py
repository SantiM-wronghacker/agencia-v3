"""
ÁREA: OPERACIONES
DESCRIPCIÓN: Agente que realiza calculadora costo operacion
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calculadora_costo_operacion(costo_producto, cantidad_venta, margen_ganancia, impuestos, tasa_inflacion=0.05):
    try:
        costo_total = costo_producto * cantidad_venta
        ganancia = (costo_total * margen_ganancia) / 100
        impuesto = (costo_total * impuestos) / 100
        ajuste_inflacion = (costo_total * tasa_inflacion) / 100
        precio_venta = costo_total + ganancia + impuesto + ajuste_inflacion
        utilidad_neta = precio_venta - costo_total - impuesto
        utilidad_bruta = precio_venta - costo_total
        margen_utilidad_neta = (utilidad_neta / precio_venta) * 100
        margen_utilidad_bruta = (utilidad_bruta / precio_venta) * 100
        return {
            "costo_total": round(costo_total, 2),
            "ganancia": round(ganancia, 2),
            "impuesto": round(impuesto, 2),
            "ajuste_inflacion": round(ajuste_inflacion, 2),
            "precio_venta": round(precio_venta, 2),
            "utilidad_neta": round(utilidad_neta, 2),
            "utilidad_bruta": round(utilidad_bruta, 2),
            "margen_utilidad_neta": round(margen_utilidad_neta, 2),
            "margen_utilidad_bruta": round(margen_utilidad_bruta, 2)
        }
    except ZeroDivisionError:
        return {"error": "No se puede dividir por cero"}
    except TypeError:
        return {"error": "Tipos de datos incorrectos"}
    except Exception as e:
        return {"error": str(e)}

def main():
    try:
        costo_producto = float(sys.argv[1]) if len(sys.argv) > 1 else 100.0
        cantidad_venta = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        margen_ganancia = float(sys.argv[3]) if len(sys.argv) > 3 else 20.0
        impuestos = float(sys.argv[4]) if len(sys.argv) > 4 else 16.0
        tasa_inflacion = float(sys.argv[5]) if len(sys.argv) > 5 else 0.05

        resultado = calculadora_costo_operacion(costo_producto, cantidad_venta, margen_ganancia, impuestos, tasa_inflacion)
        if "error" in resultado:
            print(f"Error: {resultado['error']}")
        else:
            print(f"Costo total: ${resultado['costo_total']}")
            print(f"Ganancia: ${resultado['ganancia']}")
            print(f"Impuesto: ${resultado['impuesto']}")
            print(f"Ajuste por inflación: ${resultado['ajuste_inflacion']}")
            print(f"Precio de venta: ${resultado['precio_venta']}")
            print(f"Utilidad neta: ${resultado['utilidad_neta']}")
            print(f"Utilidad bruta: ${resultado['utilidad_bruta']}")
            print(f"Margen de utilidad neta: {resultado['margen_utilidad_neta']}%")
            print(f"Margen de utilidad bruta: {resultado['margen_utilidad_bruta']}%")
            print("Resumen ejecutivo:")
            print(f"Con un costo de producción de ${costo_producto} y una cantidad de venta de {cantidad_venta},")
            print(f"el precio de venta es de ${resultado['precio_venta']} con una utilidad neta de ${resultado['utilidad_neta']}.")
            print(f"El margen de utilidad neta es de {resultado['margen_utilidad_neta']}%.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()