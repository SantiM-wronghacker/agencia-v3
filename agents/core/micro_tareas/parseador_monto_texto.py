"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: parseador monto texto
TECNOLOGÍA: Python estándar
"""

import sys
import re
import json
import math
from datetime import datetime
import os

def parseador_monto_texto(entrada, tasa_cambio, iva, isr, descuento_porcentaje, cargo_porcentaje):
    """Función pura, sin prints, sin side effects."""
    try:
        # Remover signos de moneda y separadores de miles
        monto = float(entrada.replace("$", "").replace(",", "").replace(".", "").replace(" ", "").replace("-", ""))
        
        # Aplicar tasa de cambio actual para México
        monto_mex = monto * tasa_cambio
        
        # Calcular impuestos (IVA y ISR)
        iva_calculado = monto_mex * iva / 100
        isr_calculado = monto_mex * isr / 100
        total_impuestos = iva_calculado + isr_calculado
        monto_total = monto_mex + total_impuestos
        
        # Calcular otros impuestos relevantes
        descuento = monto * (descuento_porcentaje / 100)
        cargo = monto * (cargo_porcentaje / 100)
        
        # Calcular otras cantidades útiles
        iva_porcentaje = round(iva_calculado / monto_total * 100, 2)
        isr_porcentaje = round(isr_calculado / monto_total * 100, 2)
        monto_sin_impuestos = round(monto_total - iva_calculado - isr_calculado, 2)
        monto_neto = round(monto_total - descuento + cargo, 2)
        
        # Calcular otros datos relevantes
        utilidad = round(monto_total - monto, 2)
        margen_utilidad = round(utilidad / monto * 100, 2)
        
        # Calcular impuestos en porcentaje
        iva_en_porcentaje = round(iva_calculado / monto * 100, 2)
        isr_en_porcentaje = round(isr_calculado / monto * 100, 2)
        
        # Calcular otros datos relevantes
        ganancia_bruta = round(monto_total - monto_sin_impuestos, 2)
        ganancia_neta = round(monto_neto - monto, 2)
        
        return json.dumps({
            "monto": monto,
            "monto_mex": monto_mex,
            "iva": iva_calculado,
            "isr": isr_calculado,
            "total_impuestos": total_impuestos,
            "monto_total": monto_total,
            "texto": entrada,
            "iva_porcentaje": iva_porcentaje,
            "isr_porcentaje": isr_porcentaje,
            "monto_sin_impuestos": monto_sin_impuestos,
            "descuento": descuento,
            "cargo": cargo,
            "utilidad": utilidad,
            "margen_utilidad": margen_utilidad,
            "iva_en_porcentaje": iva_en_porcentaje,
            "isr_en_porcentaje": isr_en_porcentaje,
            "ganancia_bruta": ganancia_bruta,
            "ganancia_neta": ganancia_neta,
            "monto_neto": monto_neto
        })
    except ValueError as e:
        return json.dumps({"error": str(e)})
    except Exception as e:
        return json.dumps({"error": str(e)})

def main():
    if len(sys.argv) != 7:
        print("Uso: python parseador_monto_texto.py <tasa_cambio> <iva> <isr> <descuento_porcentaje> <cargo_porcentaje> <entrada>")
        sys.exit(1)
    
    tasa_cambio = float(sys.argv[1])
    iva = float(sys.argv[2])
    isr = float(sys.argv[3])
    descuento_porcentaje = float(sys.argv[4])
    cargo_porcentaje = float(sys.argv[5])
    entrada = sys.argv[6]
    
    resultado = parseador_monto_texto(entrada, tasa_cambio, iva, isr, descuento_porcentaje, cargo_porcentaje)
    print(resultado)

if __name__ == "__main__":
    main()