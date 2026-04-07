"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza análisis punto de equilibrio
TECNOLOGÍA: Python estándar
"""

import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_punto_equilibrio(costo_fijo, precio_venta, costo_variable):
    """
    Calcula el punto de equilibrio en unidades y en pesos mexicanos
    """
    try:
        punto_equilibrio_unidades = costo_fijo / (precio_venta - costo_variable)
        punto_equilibrio_pesos = punto_equilibrio_unidades * precio_venta
        return punto_equilibrio_unidades, punto_equilibrio_pesos
    except ZeroDivisionError:
        return None, None
    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")
        return None, None

def calcular_margen_contribucion(precio_venta, costo_variable):
    """
    Calcula el margen de contribución
    """
    try:
        margen_contribucion = (precio_venta - costo_variable) / precio_venta
        return margen_contribucion
    except ZeroDivisionError:
        return None
    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")
        return None

def calcular_tasa_recuperacion_inversion(costo_fijo, punto_equilibrio_pesos):
    """
    Calcula la tasa de recuperación de la inversión
    """
    try:
        tasa_recuperacion = (punto_equilibrio_pesos / costo_fijo) * 100
        return tasa_recuperacion
    except ZeroDivisionError:
        return None
    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")
        return None

def main():
    try:
        # Parámetros por defecto realistas para México
        costo_fijo = float(sys.argv[1]) if len(sys.argv) > 1 else 50000.0
        precio_venta = float(sys.argv[2]) if len(sys.argv) > 2 else 250.0
        costo_variable = float(sys.argv[3]) if len(sys.argv) > 3 else 150.0

        unidades, pesos = calcular_punto_equilibrio(costo_fijo, precio_venta, costo_variable)
        margen_contribucion = calcular_margen_contribucion(precio_venta, costo_variable)
        tasa_recuperacion = calcular_tasa_recuperacion_inversion(costo_fijo, pesos)

        if unidades is not None:
            print("Análisis de Punto de Equilibrio")
            print(f"Costo Fijo: ${costo_fijo:,.2f} MXN")
            print(f"Precio de Venta Unitario: ${precio_venta:,.2f} MXN")
            print(f"Costo Variable Unitario: ${costo_variable:,.2f} MXN")
            print(f"Punto de Equilibrio: {unidades:,.2f} unidades")
            print(f"Monto en Pesos: ${pesos:,.2f} MXN")
            print(f"Margen de Contribución: {margen_contribucion*100 if margen_contribucion is not None else None:.2f}%")
            print(f"Tasa de Recuperación de la Inversión: {tasa_recuperacion:.2f}%")
            print("Resumen Ejecutivo:")
            print(f"El punto de equilibrio se alcanza cuando se venden {unidades:,.2f} unidades, lo que genera un monto de ${pesos:,.2f} MXN.")
            print(f"El margen de contribución es de {margen_contribucion*100 if margen_contribucion is not None else None:.2f}%, lo que indica que cada unidad vendida aporta {margen_contribucion*precio_venta if margen_contribucion is not None else None:.2f} MXN a la empresa.")
            print(f"La tasa de recuperación de la inversión es de {tasa_recuperacion:.2f}%, lo que significa que la inversión se recupera en {1/tasa_recuperacion*100 if tasa_recuperacion is not None else None:.2f} años.")
        else:
            print("Error: El precio de venta debe ser mayor al costo variable")

    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")

if __name__ == "__main__":
    main()