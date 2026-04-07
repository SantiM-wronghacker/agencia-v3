#!/usr/bin/env python3
# AREA: TURISMO
# DESCRIPCION: Agente que realiza analizador temporadas
# TECNOLOGIA: Python estándar

import sys
import json
import random
from datetime import datetime
import math

def main():
    try:
        # Configuración por defecto
        año_actual = datetime.now().year
        temporada_alta = [6, 7, 8, 12]  # Junio, julio, agosto, diciembre
        temporada_baja = [1, 2, 3, 4, 5, 9, 10, 11]

        # Obtener parámetros desde la línea de comandos
        if len(sys.argv) > 1:
            try:
                año_actual = int(sys.argv[1])
                temporada_alta = list(map(int, sys.argv[2].split(',')))
                temporada_baja = list(map(int, sys.argv[3].split(',')))
            except ValueError:
                print("Error: Parámetros inválidos")
                return

        # Generar datos aleatorios de ocupación hotelera (0-100%)
        ocupacion_alta = [random.randint(70, 95) for _ in temporada_alta]
        ocupacion_baja = [random.randint(30, 60) for _ in temporada_baja]

        # Calcular promedios
        promedio_alta = sum(ocupacion_alta) / len(ocupacion_alta)
        promedio_baja = sum(ocupacion_baja) / len(ocupacion_baja)

        # Calcular desviación estándar
        desviacion_alta = math.sqrt(sum((x - promedio_alta) ** 2 for x in ocupacion_alta) / len(ocupacion_alta))
        desviacion_baja = math.sqrt(sum((x - promedio_baja) ** 2 for x in ocupacion_baja) / len(ocupacion_baja))

        # Calcular coeficiente de variación
        coeficiente_alta = desviacion_alta / promedio_alta
        coeficiente_baja = desviacion_baja / promedio_baja

        # Imprimir resultados
        print(f"Análisis de temporadas turísticas {año_actual}")
        print(f"Ocupación promedio temporada alta (meses {temporada_alta}): {promedio_alta:.1f}%")
        print(f"Ocupación promedio temporada baja (meses {temporada_baja}): {promedio_baja:.1f}%")
        print(f"Diferencia entre temporadas: {promedio_alta - promedio_baja:.1f} puntos porcentuales")
        print(f"Desviación estándar temporada alta: {desviacion_alta:.1f}%")
        print(f"Desviación estándar temporada baja: {desviacion_baja:.1f}%")
        print(f"Coeficiente de variación temporada alta: {coeficiente_alta:.2f}")
        print(f"Coeficiente de variación temporada baja: {coeficiente_baja:.2f}")
        print(f"Meses con mayor ocupación: {año_actual}-{max(temporada_alta)}")
        print(f"Meses con menor ocupación: {año_actual}-{min(temporada_alta)}")
        print(f"Promedio ocupación alta en verano: {(sum(ocupacion_alta[0::2]) / 2):.1f}%")
        print(f"Promedio ocupación baja en invierno: {(sum(ocupacion_baja[0::2]) / 2):.1f}%")
        print(f"Promedio ocupación alta en otoño: {(sum(ocupacion_alta[1::2]) / 2):.1f}%")
        print(f"Promedio ocupación baja en primavera: {(sum(ocupacion_baja[1::2]) / 2):.1f}%")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        if promedio_alta > promedio_baja:
            print(f"La temporada alta de {año_actual} presentó un promedio de ocupación de {promedio_alta:.1f}%.")
        else:
            print(f"La temporada baja de {año_actual} presentó un promedio de ocupación de {promedio_baja:.1f}%.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()