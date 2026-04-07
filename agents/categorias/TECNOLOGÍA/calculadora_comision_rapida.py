"""
ÁREA: FINANZAS
DESCRIPCIÓN: calculadora comision rapida
TECNOLOGÍA: Python estándar
"""

import sys
import json
import math
import os
from datetime import date
import locale

locale.setlocale(locale.LC_ALL, 'es_MX.UTF-8')

def calculadora_comision_rapida(entrada, tasa_comision=0.1, tipo_cambio=20.35):
    """Función pura, sin prints, sin side effects."""
    try:
        # Verificar si la entrada es un número positivo
        if float(entrada) <= 0:
            raise ValueError
        
        # Calcular la comisión rápida
        comision = float(entrada) * tasa_comision
        
        # Calcular el monto total con comisión
        monto_total = float(entrada) + comision
        
        # Calcular el porcentaje de comisión
        porcentaje_comision = (comision / float(entrada)) * 100
        
        # Calcular la cantidad de pesos mexicanos
        cantidad_pesos = float(entrada) * tipo_cambio
        
        # Calcular la comisión en pesos mexicanos
        comision_pesos = comision * tipo_cambio
        
        # Calcular el monto total en pesos mexicanos
        monto_total_pesos = cantidad_pesos + comision_pesos
        
        # Calcular el impuesto al valor agregado (IVA) en pesos mexicanos
        iva_pesos = monto_total_pesos * 0.16
        
        # Calcular el monto total en pesos mexicanos con IVA
        monto_total_pesos_iva = monto_total_pesos + iva_pesos
        
        # Calcular la cantidad de días para el pago de la comisión
        dias_pago = 30
        
        # Calcular el monto total en pesos mexicanos con IVA y días de pago
        monto_total_pesos_iva_dias = monto_total_pesos_iva * (1 + (dias_pago / 365))
        
        # Calcular el monto total en pesos mexicanos con IVA y días de pago, redondeado a 2 decimales
        monto_total_pesos_iva_dias = round(monto_total_pesos_iva_dias, 2)
        
        # Calcular el monto total en pesos mexicanos con IVA y días de pago, formateado con separador de miles
        monto_total_pesos_iva_dias = locale.format_string('%d.%d', (monto_total_pesos_iva_dias // 100, monto_total_pesos_iva_dias % 100), grouping=True)
        
        return f"""
ÁREA: FINANZAS
DESCRIPCIÓN: calculadora comision rapida
TECNOLOGÍA: Python estándar

Comisión: ${comision:,.2f}
Monto total: ${monto_total:,.2f}
Porcentaje de comisión: {porcentaje_comision:.2f}%
Cantidad de pesos mexicanos: ${cantidad_pesos:,.2f}
Comisión en pesos mexicanos: ${comision_pesos:,.2f}
Monto total en pesos mexicanos: ${monto_total_pesos:,.2f}
IVA en pesos mexicanos: ${iva_pesos:,.2f}
Monto total en pesos mexicanos con IVA: ${monto_total_pesos_iva:,.2f}
Monto total en pesos mexicanos con IVA y días de pago: ${monto_total_pesos_iva_dias}
Fecha de cálculo: {date.today().strftime('%d/%m/%Y')}
Resumen ejecutivo: El monto total en pesos mexicanos con IVA y días de pago es de ${monto_total_pesos_iva_dias}.
"""
    
    except ValueError:
        return "Error: La entrada debe ser un número positivo."
    
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    if len(sys.argv) > 1:
        entrada = sys.argv[1]
    else:
        entrada = input("Ingrese el monto a calcular: ")
        
    print(calculadora_comision_rapida(entrada))

if __name__ == "__main__":
    main()