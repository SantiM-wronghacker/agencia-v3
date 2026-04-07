import sys
import json
import datetime
import math
import re
import random
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        area = 'CEREBRO'
        descripcion = 'Generador de briefing diario'
        tecnologia = 'Python'
        print(f'{area}/{descripcion}/{tecnologia}')

        fecha_actual = datetime.datetime.now()
        print(f'Fecha actual: {fecha_actual.strftime("%Y-%m-%d %H:%M:%S")}')

        temperatura_mexico = round(random.uniform(15, 30), 2)
        humedad_mexico = round(random.uniform(40, 80), 2)
        print(f'Temperatura en México: {temperatura_mexico}°C')
        print(f'Humedad en México: {humedad_mexico}%')

        poblacion_mexico = 127575529
        print(f'Población de México: {poblacion_mexico} habitantes')

        tipo_cambio = round(random.uniform(18, 22), 2)
        print(f'Tipo de cambio (MXN/USD): {tipo_cambio}')

        temperatura_ciudades = {
            'Ciudad de México': round(random.uniform(15, 25), 2),
            'Guadalajara': round(random.uniform(18, 28), 2),
            'Monterrey': round(random.uniform(20, 30), 2)
        }
        for ciudad, temperatura in temperatura_ciudades.items():
            print(f'Temperatura en {ciudad}: {temperatura}°C')

        indice_inflacion = round(random.uniform(2, 5), 2)
        print(f'Índice de inflación: {indice_inflacion}%')

        tasa_desempleo = round(random.uniform(2, 5), 2)
        print(f'Tasa de desempleo: {tasa_desempleo}%')

        reservas_petroleras = round(random.uniform(5000, 10000), 2)
        print(f'Reservas petroleras: {reservas_petroleras} millones de barriles')

        produccion_agricola = round(random.uniform(100, 200), 2)
        print(f'Producción agrícola: {produccion_agricola} millones de toneladas')

        produccion_industrial = round(random.uniform(500, 1000), 2)
        print(f'Producción industrial: {produccion_industrial} millones de unidades')

        consumo_energetico = round(random.uniform(100, 200), 2)
        print(f'Consumo energético: {consumo_energetico} millones de kilovatios')

        tasa_crecimiento_pib = round(random.uniform(2, 5), 2)
        print(f'Tasa de crecimiento del PIB: {tasa_crecimiento_pib}%')

        deuda_publica = round(random.uniform(1000, 2000), 2)
        print(f'Deuda pública: {deuda_publica} miles de millones de pesos')

        print('\nResumen Ejecutivo:')
        print(f'La fecha actual es {fecha_actual.strftime("%Y-%m-%d %H:%M:%S")}.')
        print(f'La temperatura en México es de {temperatura_mexico}°C y la humedad es del {humedad_mexico}%.')
        print(f'La población de México es de {poblacion_mexico} habitantes.')
        print(f'El tipo de cambio es de {tipo_cambio} MXN/USD.')
        print(f'El índice de inflación es del {indice_inflacion}% y la tasa de desempleo es del {tasa_desempleo}%.')
        print(f'Las reservas petroleras son de {reservas_petroleras} millones de barriles y la producción agrícola es de {produccion_agricola} millones de toneladas.')

    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == "__main__":
    main()