# TURISMO
# Agencia de viajes Way2TheUnknown, cotiza viajes completos con fee del 8%
# Python 3.x

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

def calcular_precio_base(destino, duracion, tipo_de_viaje):
    try:
        precios_base = {
            "nacional": 500,
            "internacional": 1500
        }
        tipo_de_viaje = tipo_de_viaje.lower()
        if tipo_de_viaje not in precios_base:
            raise ValueError("Tipo de viaje no valido")
        
        precio = precios_base[tipo_de_viaje] * duracion
        if destino == "Europa":
            precio *= 1.2
        elif destino == "Asia":
            precio *= 1.5
        elif destino == "America":
            precio *= 1.1
        return precio
    
    except Exception as e:
        print(f"Error en calcular_precio_base: {str(e)}")
        return None

def calcular_precio_total(precio_base, moneda):
    try:
        if precio_base is None:
            raise ValueError("Precio base no valido")
        
        fee = precio_base * 0.08
        if moneda.upper() == "MXN":
            tipo_cambio = 20
            precio_total = (precio_base + fee) * tipo_cambio
        else:
            precio_total = precio_base + fee
        
        return precio_total
    
    except Exception as e:
        print(f"Error en calcular_precio_total: {str(e)}")
        return None

def calcular_impuestos(precio_total, moneda):
    try:
        if precio_total is None:
            raise ValueError("Precio total no valido")
        
        if moneda.upper() == "MXN":
            impuesto = precio_total * 0.16
        else:
            impuesto = precio_total * 0.08
        
        return impuesto
    
    except Exception as e:
        print(f"Error en calcular_impuestos: {str(e)}")
        return None

def calcular_seguro(precio_total):
    try:
        if precio_total is None:
            raise ValueError("Precio total no valido")
        
        seguro = precio_total * 0.05
        return seguro
    
    except Exception as e:
        print(f"Error en calcular_seguro: {str(e)}")
        return None

def main():
    try:
        destino = sys.argv[1] if len(sys.argv) > 1 else "Europa"
        duracion = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        tipo_de_viaje = sys.argv[3] if len(sys.argv) > 3 else "internacional"
        moneda = sys.argv[4] if len(sys.argv) > 4 else "USD"
        
        precio_base = calcular_precio_base(destino, duracion, tipo_de_viaje)
        if precio_base is not None:
            precio_total = calcular_precio_total(precio_base, moneda)
            if precio_total is not None:
                impuesto = calcular_impuestos(precio_total, moneda)
                seguro = calcular_seguro(precio_total)
                print(f"Destino: {destino}")
                print(f"Duracion: {duracion} dias")
                print(f"Tipo de viaje: {tipo_de_viaje}")
                print(f"Moneda: {moneda}")
                print(f"Precio base: {moneda} {precio_base:.2f}")
                print(f"Precio total: {moneda} {precio_total:.2f}")
                print(f"Impuesto: {moneda} {impuesto:.2f}")
                print(f"Seguro: {moneda} {seguro:.2f}")
                print(f"Total a pagar: {moneda} {precio_total + impuesto + seguro:.2f}")
                print(f"Resumen ejecutivo: Viaje a {destino} por {duracion} dias, tipo de viaje {tipo_de_viaje}, moneda {moneda}, precio total {precio_total:.2f}, impuesto {impuesto:.2f}, seguro {seguro:.2f}, total a pagar {precio_total + impuesto + seguro:.2f}")
    
    except Exception as e:
        print(f"Error en main: {str(e)}")

if __name__ == "__main__":
    main()