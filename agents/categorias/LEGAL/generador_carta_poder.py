"""
ÁREA: LEGAL
DESCRIPCIÓN: Agente que realiza generador carta poder
TECNOLOGÍA: Python estándar
"""
import sys
import os
import json
import datetime
import math
import re
import random

def calcular_impuestos(monto, iva, isr):
    """Calcula los impuestos sobre un monto."""
    iva_monto = monto * iva
    isr_monto = monto * isr
    total_monto = monto + iva_monto + isr_monto
    return iva_monto, isr_monto, total_monto

def generar_carta_poder(nombre_cliente, rfc, nombre_representante, fecha, monto, iva, isr):
    """Genera una carta poder."""
    carta_poder = f"""
    CARTA PODER

    Por medio de la presente, yo {nombre_cliente}, con RFC {rfc}, otorgo poder amplio y suficiente
    a {nombre_representante} para que me represente en todos los actos jurídicos y administrativos
    relacionados con el monto de ${monto:.2f} MXN, en la Ciudad de México, a {fecha}.

    Atentamente,
    {nombre_cliente}
    """
    return carta_poder

def guardar_archivo(cartas_poder, nombre_cliente):
    """Guarda las cartas poder en un archivo."""
    filename = f"cartas_poder_{nombre_cliente.replace(' ', '_')}.txt"
    with open(filename, 'w') as f:
        for carta in cartas_poder:
            f.write(carta + "\n\n")

def main():
    try:
        # Parámetros por defecto
        nombre_representante = sys.argv[1] if len(sys.argv) > 1 else "Juan Pérez García"
        nombre_cliente = sys.argv[2] if len(sys.argv) > 2 else "María López Martínez"
        fecha = sys.argv[3] if len(sys.argv) > 3 else datetime.date.today().strftime("%d/%m/%Y")
        rfc = sys.argv[4] if len(sys.argv) > 4 else "PEJU800101"
        monto = float(sys.argv[5]) if len(sys.argv) > 5 else 150000.00
        iva = 0.16  # IVA para México
        isr = 0.10  # ISR para México

        # Validar parámetros
        if not isinstance(monto, (int, float)) or monto <= 0:
            raise ValueError("El monto debe ser un número positivo")
        if not re.match("^[A-Z]{4}[0-9]{6}[A-Z0-9]{3}$", rfc):
            raise ValueError("El RFC es inválido")
        if len(nombre_representante) == 0 or len(nombre_cliente) == 0:
            raise ValueError("El nombre del representante y del cliente no pueden estar vacíos")

        # Calcular impuestos
        iva_monto, isr_monto, total_monto = calcular_impuestos(monto, iva, isr)

        # Generar carta poder
        carta_poder = generar_carta_poder(nombre_cliente, rfc, nombre_representante, fecha, monto, iva, isr)

        # Guardar en archivo
        guardar_archivo([carta_poder], nombre_cliente)

        # Resumen ejecutivo
        resumen_ejecutivo = f"""
        Resumen ejecutivo:
        - Monto: ${monto:.2f} MXN
        - IVA: ${iva_monto:.2f} MXN
        - ISR: ${isr_monto:.2f} MXN
        - Total: ${total_monto:.2f} MXN
        """

        print("Carta poder generada exitosamente.")
        print("Nombre del cliente:", nombre_cliente)
        print("Nombre del representante:", nombre_representante)
        print("Fecha:", fecha)
        print("Monto:", monto)
        print("IVA:", iva_monto)
        print("ISR:", isr_monto)
        print("Total:", total_monto)
        print("Resumen ejecutivo:")
        print(resumen_ejecutivo)

    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()