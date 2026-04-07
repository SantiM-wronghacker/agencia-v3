"""
ÁREA: OPERACIONES
DESCRIPCIÓN: Agente que realiza calculadora capacidad instalada
TECNOLOGÍA: Python estándar
"""

import sys
import math
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto realistas para México
        if len(sys.argv) > 1:
            capacidad_instalada_mw = float(sys.argv[1])
            demanda_actual_mw = float(sys.argv[2])
            eficiencia = float(sys.argv[3])
            mantenimiento_porcentaje = float(sys.argv[4])
        else:
            capacidad_instalada_mw = 1500  # MW
            demanda_actual_mw = 1200  # MW
            eficiencia = 0.85  # 85%
            mantenimiento_porcentaje = 0.05  # 5%

        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        # Cálculos
        capacidad_util = capacidad_instalada_mw * eficiencia
        capacidad_disponible = capacidad_util * (1 - mantenimiento_porcentaje)
        margen = capacidad_disponible - demanda_actual_mw
        porcentaje_utilizacion = (demanda_actual_mw / capacidad_util) * 100
        porcentaje_mantenimiento = mantenimiento_porcentaje * 100
        factor_carga = demanda_actual_mw / capacidad_instalada_mw
        reserva_capacidad = capacidad_disponible - demanda_actual_mw
        punto_maximo_demanda = capacidad_instalada_mw * 0.8
        tiempo_maximo_demanda = 8  # horas
        energia_total_disponible = capacidad_disponible * 24  # MWh
        energia_total_consumida = demanda_actual_mw * 24  # MWh
        perdida_energia_mantenimiento = (capacidad_instalada_mw * mantenimiento_porcentaje) * 24  # MWh

        # Salida
        print(f"Fecha: {fecha_actual}")
        print(f"Capacidad instalada: {capacidad_instalada_mw:.2f} MW")
        print(f"Demanda actual: {demanda_actual_mw:.2f} MW")
        print(f"Capacidad disponible: {capacidad_disponible:.2f} MW")
        print(f"Margen de capacidad: {margen:.2f} MW")
        print(f"Porcentaje de utilización: {porcentaje_utilizacion:.2f}%")
        print(f"Porcentaje de mantenimiento: {porcentaje_mantenimiento:.2f}%")
        print(f"Factor de carga: {factor_carga:.2f}")
        print(f"Reserva de capacidad: {reserva_capacidad:.2f} MW")
        print(f"Eficiencia: {eficiencia*100:.2f}%")
        print(f"Punto máximo de demanda: {punto_maximo_demanda:.2f} MW")
        print(f"Tiempo máximo de demanda: {tiempo_maximo_demanda} horas")
        print(f"Energía total disponible: {energia_total_disponible:.2f} MWh")
        print(f"Energía total consumida: {energia_total_consumida:.2f} MWh")
        print(f"Pérdida de energía por mantenimiento: {perdida_energia_mantenimiento:.2f} MWh")
        print("Resumen ejecutivo:")
        print(f"La capacidad instalada es de {capacidad_instalada_mw:.2f} MW, con una demanda actual de {demanda_actual_mw:.2f} MW.")
        print(f"La capacidad disponible es de {capacidad_disponible:.2f} MW, con un margen de {margen:.2f} MW.")
        print(f"El porcentaje de utilización es del {porcentaje_utilizacion:.2f}%, con un porcentaje de mantenimiento del {porcentaje_mantenimiento:.2f}%.")        
    except ValueError:
        print("Error: Los parámetros deben ser números.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()