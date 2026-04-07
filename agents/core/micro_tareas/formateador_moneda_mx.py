# ARCHIVO: formateador_moneda_mx.py
# AREA: HERRAMIENTAS
# DESCRIPCION: Formateador Moneda Mx

import sys
import os
import json
import datetime
import math
import re

def formateador_moneda_mx(entrada, tipo_cambio, *args):
    """Función pura, sin prints, sin side effects."""
    try:
        valor = float(entrada)
        if valor < 0:
            return "ERROR: valor no puede ser negativo"
        elif valor > 1e25:
            return "ERROR: valor excede el límite de 1 quintillón de pesos mexicanos"
        elif valor < -1e22:
            return "ERROR: valor muy pequeño"
        elif tipo_cambio <= 0:
            return "ERROR: tipo de cambio no puede ser cero o negativo"
        else:
            return f"${valor * tipo_cambio:,.2f} MXN"
    except ValueError:
        return "ERROR: no numérico"
    except Exception as e:
        return f"ERROR: {str(e)}"

def obtener_tipo_cambio(sys_arg=False):
    # Obtenemos el tipo de cambio actual desde el ambiente
    tipo_cambio = float(os.environ.get('TIPO_CAMBIO', 20.35))  # Tipo de cambio actual (MXN/USD)
    if sys_arg:
        tipo_cambio = float(sys.argv[2])  # Tipo de cambio actual (MXN/USD)
    return tipo_cambio

def obtener_entrada(sys_arg=False):
    # Obtenemos la entrada desde los argumentos de la línea de comandos
    if sys_arg:
        entrada = sys.argv[1]
    elif os.environ.get('ENTRADA'):
        entrada = os.environ.get('ENTRADA')
    else:
        entrada = "1000"
    return entrada

def obtener_fecha_hora():
    return datetime.datetime.now()

def obtener_resumen_ejecutivo():
    return "Formateador de moneda MX: convierte valores numéricos a pesos mexicanos."

def obtener_resumen_detalle():
    return {
        "Tipo de cambio": obtener_tipo_cambio(sys_arg=True),
        "Entrada": obtener_entrada(sys_arg=True),
        "Resultado": formateador_moneda_mx(obtener_entrada(sys_arg=True), obtener_tipo_cambio(sys_arg=True)),
        "Fecha y hora": obtener_fecha_hora(),
        "Límite superior": 1e25,
        "Límite inferior": -1e22
    }

def obtener_informacion_adicional():
    return {
        "Información adicional": "Este formateador puede convertir valores numéricos a pesos mexicanos.",
        "Límites de valor": "Entre -1e22 y 1e25",
        "Tipo de cambio": "MXN/USD"
    }

def main():
    if len(sys.argv) > 1:
        print("Entrada:", sys.argv[1])
        print("Tipo de cambio:", sys.argv[2])
        print("Resultado:", formateador_moneda_mx(sys.argv[1], sys.argv[2]))
        print("Fecha y hora:", obtener_fecha_hora())
        print("Resumen ejecutivo:", obtener_resumen_ejecutivo())
        print("Resumen detalle:", obtener_resumen_detalle())
        print("Información adicional:", obtener_informacion_adicional())
    else:
        print("Entrada:", obtener_entrada())
        print("Tipo de cambio:", obtener_tipo_cambio())
        print("Resultado:", formateador_moneda_mx(obtener_entrada(), obtener_tipo_cambio()))
        print("Fecha y hora:", obtener_fecha_hora())
        print("Resumen ejecutivo:", obtener_resumen_ejecutivo())
        print("Resumen detalle:", obtener_resumen_detalle())
        print("Información adicional:", obtener_informacion_adicional())

if __name__ == "__main__":
    main()