import sys
import math
import os
import datetime
import json

def main():
    try:
        # Obtener valores de la linea de comandos
        num_mesas = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        num_clientes = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        tiempo_rotacion = int(sys.argv[3]) if len(sys.argv) > 3 else 60
        gasto_promedio = float(sys.argv[4]) if len(sys.argv) > 4 else 200.0
        horas_operacion = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        dias_operacion = int(sys.argv[6]) if len(sys.argv) > 6 else 7
        anio_operacion = int(sys.argv[7]) if len(sys.argv) > 7 else 2023

        # Imprimir encabezado
        print("# AREA: FINANZAS")
        print("# DESCRIPCION: RESTAURANTES/CALCULADORA ROTACION MESA/PYTHON")
        print("# TECNOLOGIA: PYTHON")
        print("---------------------------")

        # Imprimir datos de entrada
        print(f"Número de mesas: {num_mesas}")
        print(f"Número de clientes: {num_clientes}")
        print(f"Tiempo de rotación (minutos): {tiempo_rotacion}")
        print(f"Gasto promedio por cliente: ${gasto_promedio:.2f}")
        print(f"Horas de operación: {horas_operacion}")
        print(f"Días de operación: {dias_operacion}")
        print(f"Año de operación: {anio_operacion}")

        # Calcular datos importantes
        mesas_ocupadas = math.ceil(num_clientes / num_mesas)
        rotaciones_por_hora = math.floor(60 / tiempo_rotacion)
        ingresos_por_rotacion = math.floor(gasto_promedio * num_clientes)
        ingresos_por_hora = math.floor((gasto_promedio * num_clientes) * (60 / tiempo_rotacion))
        ingresos_por_dia = math.floor(ingresos_por_hora * horas_operacion)
        ingresos_por_semana = math.floor(ingresos_por_dia * dias_operacion)
        ingresos_por_mes = math.floor(ingresos_por_semana * 4)
        ingresos_por_año = math.floor(ingresos_por_mes * 12)

        # Imprimir datos importantes
        print(f"Mesas ocupadas: {mesas_ocupadas}")
        print(f"Rotaciones por hora: {rotaciones_por_hora}")
        print(f"Ingresos por rotación: ${ingresos_por_rotacion:,}")
        print(f"Ingresos por hora: ${ingresos_por_hora:,}")
        print(f"Ingresos por día: ${ingresos_por_dia:,}")
        print(f"Ingresos por semana: ${ingresos_por_semana:,}")
        print(f"Ingresos por mes: ${ingresos_por_mes:,}")
        print(f"Ingresos por año: ${ingresos_por_año:,}")

        # Imprimir resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El restaurante tiene {num_mesas} mesas y puede atender a {mesas_ocupadas} clientes por mesa.")
        print(f"La rotación de clientes es de {rotaciones_por_hora} veces por hora.")
        print(f"Los ingresos por rotación son de ${ingresos_por_rotacion:,} y por hora son de ${ingresos_por_hora:,}.")
        print(f"Los ingresos diarios son de ${ingresos_por_dia:,} y semanales son de ${ingresos_por_semana:,}.")
        print(f"Los ingresos mensuales son de ${ingresos_por_mes:,} y anuales son de ${ingresos_por_año:,}.")

    except IndexError:
        print("Falta de argumentos en la linea de comandos.")
    except ValueError:
        print("Valor no válido en la linea de comandos.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()