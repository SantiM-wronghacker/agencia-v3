import os
import sys
import json
import datetime
import math
import re
import random
import argparse

def cotizador_poliza_auto():
    try:
        parser = argparse.ArgumentParser(description='Cotizador Poliza Auto')
        parser.add_argument('--tipo-seguro', type=str, help='Tipo de seguro')
        parser.add_argument('--precio-seguro', type=float, help='Precio seguro')
        parser.add_argument('--cargo-servicio', type=float, default=500.0, help='Cargo por servicio')
        parser.add_argument('--impuesto', type=float, default=0.10, help='Impuesto sobre el precio seguro')
        parser.add_argument('--edad-conductor', type=int, default=30, help='Edad del conductor')
        parser.add_argument('--antiguedad-vehiculo', type=int, default=5, help='Antigüedad del vehículo')
        args = parser.parse_args()

        if args.tipo_seguro and args.precio_seguro:
            tipo_seguro = args.tipo_seguro
            precio_seguro = args.precio_seguro
        else:
            tipo_seguro = 'seguro de responsabilidad civil'
            precio_seguro = 1500.0
        
        if tipo_seguro == 'seguro de responsabilidad civil':
            precio_seguro = 1500.0
        elif tipo_seguro == 'seguro de daños a terceros':
            precio_seguro = 2000.0
        elif tipo_seguro == 'seguro de accidentes personales':
            precio_seguro = 3000.0
        elif tipo_seguro == 'seguro de robo y hurto':
            precio_seguro = 1000.0
        else:
            print(f'Error: Tipo de seguro no válido')
            return
        
        # Calcular el factor de riesgo según la edad del conductor
        if args.edad_conductor < 25:
            factor_riesgo = 1.2
        elif args.edad_conductor < 40:
            factor_riesgo = 1.0
        else:
            factor_riesgo = 0.8
        
        # Calcular el factor de riesgo según la antigüedad del vehículo
        if args.antiguedad_vehiculo < 3:
            factor_riesgo_vehiculo = 1.1
        elif args.antiguedad_vehiculo < 10:
            factor_riesgo_vehiculo = 1.0
        else:
            factor_riesgo_vehiculo = 0.9
        
        # Calcular el precio seguro con los factores de riesgo
        precio_seguro *= factor_riesgo * factor_riesgo_vehiculo
        
        # Agregar un impuesto sobre el precio seguro
        precio_seguro *= (1 + args.impuesto)
        
        # Calcular la cotización total
        cotizacion_total = precio_seguro + args.cargo_servicio
        
        # Mostrar los datos
        print(f'AREA: SEGUROS')
        print(f'DESCRIPCIÓN: Agente que realiza cotizador poliza auto')
        print(f'TECNOLOGÍA: Python estándar')
        print(f'Cotización total: {cotizacion_total:.2f} MXN')
        print(f'Datos de ejemplo:')
        print(f'  - Tipo de seguro: {tipo_seguro}')
        print(f'  - Precio seguro: {precio_seguro:.2f} MXN')
        print(f'  - Cargo por servicio: {args.cargo_servicio:.2f} MXN')
        print(f'  - Impuesto sobre el precio seguro: {args.impuesto*100:.2f}%')
        print(f'  - Edad del conductor: {args.edad_conductor} años')
        print(f'  - Antigüedad del vehículo: {args.antiguedad_vehiculo} años')
        print(f'  - Factor de riesgo según la edad del conductor: {factor_riesgo:.2f}')
        print(f'  - Factor de riesgo según la antigüedad del vehículo: {factor_riesgo_vehiculo:.2f}')
        print(f'Resumen ejecutivo:')
        print(f'  - La cotización total es de {cotizacion_total:.2f} MXN')
        print(f'  - El precio seguro es de {precio_seguro:.2f} MXN')
        print(f'  - El cargo por servicio es de {args.cargo_servicio:.2f} MXN')
    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == "__main__":
    cotizador