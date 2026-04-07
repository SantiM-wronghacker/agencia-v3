"""
AREA: LEGAL
DESCRIPCION: Agente que realiza generador poder notarial
TECNOLOGIA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def calcular_impuestos(monto):
    return round(monto * 0.16, 2)

def calcular_total(monto, impuestos):
    return round(monto + impuestos, 2)

def calcular_tipo_cambio():
    return round(random.uniform(19.50, 21.50), 2)

def calcular_isr(monto):
    if monto <= 400000:
        return round(monto * 0.01, 2)
    elif monto <= 800000:
        return round(monto * 0.02, 2)
    elif monto <= 2000000:
        return round(monto * 0.03, 2)
    elif monto <= 3000000:
        return round(monto * 0.04, 2)
    else:
        return round(monto * 0.05, 2)

def calcular_iva(monto):
    return round(monto * 0.16, 2)

def calcular_retencion(monto):
    return round(monto * 0.10, 2)

def main():
    try:
        # Parámetros por defecto
        nombre = sys.argv[1] if len(sys.argv) > 1 else "Juan Pérez"
        direccion = sys.argv[2] if len(sys.argv) > 2 else "Calle 123, Colonia Centro, Ciudad de México"
        rfc = sys.argv[3] if len(sys.argv) > 3 else "PEMJ800101HTCSDN09"
        fecha = datetime.datetime.now().strftime("%d/%m/%Y")

        # Datos concretos y números reales mexicanos
        monto = round(random.uniform(1000, 100000), 2)
        impuestos = calcular_impuestos(monto)
        isr = calcular_isr(monto)
        iva = calcular_iva(monto)
        retencion = calcular_retencion(monto)
        total = calcular_total(monto, impuestos)
        tipo_cambio = calcular_tipo_cambio()

        # Agregar más datos útiles
        poder_notarial = {
            "Nombre": nombre,
            "Dirección": direccion,
            "RFC": rfc,
            "Fecha": fecha,
            "Monto": monto,
            "Impuestos": impuestos,
            "ISR": isr,
            "IVA": iva,
            "Retención": retencion,
            "Total": total,
            "Tipo de Cambio": tipo_cambio,
            "Moneda": "MXN",
            "Banco": "Banco de México",
            "Número de Cuenta": "1234567890",
            "Clave de Autorización": "123456",
            "Número de Factura": "001",
            "Número de Comprobante": "001",
            "Tipo de Comprobante": "Factura",
            "Monto en USD": round(monto / tipo_cambio, 2),
            "ISR en USD": round(isr / tipo_cambio, 2),
            "IVA en USD": round(iva / tipo_cambio, 2),
            "Retención en USD": round(retencion / tipo_cambio, 2),
            "Total en USD": round(total / tipo_cambio, 2),
        }

        # Agregar resumen ejecutivo
        resumen_ejecutivo = f"""
        Resumen Ejecutivo:
        El Sr. {nombre} con RFC {rfc} ha realizado una transacción por un monto de {monto} MXN.
        El impuesto a pagar es de {impuestos} MXN, el ISR es de {isr} MXN y el IVA es de {iva} MXN.
        La retención es de {retencion} MXN y el total a pagar es de {total} MXN.
        El tipo de cambio utilizado es de {tipo_cambio} MXN/USD.
        """

        # Mostrar resultados
        print("Poder Notarial:")
        for key, value in poder_notarial.items():
            print(f"{key}: {value}")
        print("\nResumen Ejecutivo:")
        print(resumen_ejecutivo)

    except IndexError:
        print("Error: Faltan parámetros por sys.argv")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()