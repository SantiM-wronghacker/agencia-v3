# REAL ESTATE
# Analizador de plusvalia de colonia
# Python
# AREA: REAL ESTATE
# DESCRIPCION: Agente que realiza analizador plusvalia colonia
# TECNOLOGIA: Python

import sys
import os
import math

def main():
    try:
        # Parametros default
        colonia = sys.argv[1] if len(sys.argv) > 1 else 'Polanco'
        precio_m2 = float(sys.argv[2]) if len(sys.argv) > 2 else 80000.0
        area = float(sys.argv[3]) if len(sys.argv) > 3 else 200.0
        incremento_anual = float(sys.argv[4]) if len(sys.argv) > 4 else 5.0
        anos = int(sys.argv[5]) if len(sys.argv) > 5 else 5
        tasa_inflacion = float(sys.argv[6]) if len(sys.argv) > 6 else 3.5

        # Verificar valores validos
        if precio_m2 <= 0:
            raise ValueError('Precio por m2 debe ser mayor que 0')
        if area <= 0:
            raise ValueError('Area debe ser mayor que 0')
        if incremento_anual < 0:
            raise ValueError('Incremento anual debe ser mayor o igual a 0')
        if anos < 0:
            raise ValueError('Años debe ser mayor o igual a 0')
        if tasa_inflacion < 0:
            raise ValueError('Tasa de inflacion debe ser mayor o igual a 0')

        # Calculo de plusvalia
        precio_inicial = precio_m2 * area
        plusvalia_anual = (precio_inicial * incremento_anual) / 100
        plusvalia_total = 0
        valor_actual = precio_inicial
        resultados_anuales = []
        for i in range(anos):
            plusvalia_anual = (valor_actual * incremento_anual) / 100
            valor_actual += plusvalia_anual
            valor_actual *= (1 + tasa_inflacion / 100)
            plusvalia_total += plusvalia_anual
            resultados_anuales.append({
                'año': i + 1,
                'plusvalia_anual': plusvalia_anual,
                'valor_actual': valor_actual,
                'incremento_porcentaje': (plusvalia_anual / valor_actual) * 100 if valor_actual!= 0 else 0,
                'tasa_inflacion_acumulada': (1 + tasa_inflacion / 100) ** (i + 1)
            })

        # Impresion de resultados
        print(f'Colonia: {colonia}')
        print(f'Precio inicial: ${precio_m2:.2f} por m2')
        print(f'Area: {area:.2f} m2')
        print(f'Plusvalia anual: {incremento_anual:.2f}%')
        print(f'Tasa de inflacion: {tasa_inflacion:.2f}%')
        print(f'Plusvalia total en {anos} años: ${plusvalia_total:.2f}')
        print(f'Valor actual en {anos} años: ${valor_actual:.2f}')
        print(f'Incremento total en {anos} años: {(plusvalia_total / precio_inicial) * 100:.2f}%')
        print('Resultados anuales:')
        for resultado in resultados_anuales:
            print(f'Año {resultado["año"]}: Plusvalia anual ${resultado["plusvalia_anual"]:.2f}, Valor actual ${resultado["valor_actual"]:.2f}, Incremento porcentaje {(resultado["incremento_porcentaje"]):.2f}%')
        print('Resumen ejecutivo:')
        print(f'El valor de la propiedad en {colonia} aumentó un {((plusvalia_total / precio_inicial) * 100):.2f}% en {anos} años, con una plusvalia anual promedio de ${((plusvalia_total / anos)): .2f} y una tasa de inflacion acumulada de {(1 + tasa_inflacion / 100) ** anos * 100:.2f}%')

    except IndexError:
        print('Faltan argumentos de línea de comandos')
    except ValueError as e:
        print(str(e))
    except Exception as e:
        print('Ocurrió un error: ' + str(e))

if __name__ == "__main__":
    main()