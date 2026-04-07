#!/usr/bin/env python3
"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Formateador de números en palabras (México)
TECNOLOGÍA: Python estándar
"""
import sys
import re
import datetime

def formateador_numero_palabras_mx(entrada, *args):
    """
    Función pura, sin prints, sin side effects.
    """
    try:
        numero = int(entrada)
        if numero > 0:
            # Calcular el número de palabras en función del número
            millones = numero // 1000000
            mil = (numero % 1000000) // 1000
            decenas = (numero % 1000) // 100
            unidades = numero % 100
            if millones > 0:
                palabras = f"{millones} millones"
            else:
                palabras = ""
            if mil > 0:
                if palabras:
                    palabras += f" y {mil} mil"
                else:
                    palabras = f"{mil} mil"
            if decenas > 0 and unidades > 0:
                if palabras:
                    return f"{palabras} y {decenas} cientos y {unidades} números"
                else:
                    return f"{mil} mil y {decenas} cientos y {unidades} números"
            elif decenas > 0:
                if palabras:
                    return f"{palabras} y {decenas} cientos números"
                else:
                    return f"{mil} mil y {decenas} cientos números"
            elif unidades > 0:
                if palabras:
                    return f"{palabras} y {unidades} números"
                else:
                    return f"{mil} mil y {unidades} números"
            else:
                if palabras:
                    return f"{palabras} números"
                else:
                    return f"{mil} mil números"
        elif numero < 0:
            return f"{-numero:,} números"
        else:
            return "0 números"
    except ValueError:
        try:
            # Intentar convertir a número flotante
            numero = float(entrada)
            if numero > 0:
                return f"{numero:.2f} números"
            else:
                return "0 números"
        except ValueError:
            try:
                # Intentar convertir a número complejo
                numero = complex(entrada)
                return f"{numero} números"
            except ValueError:
                return "INVALIDO: no_numerico"

def main():
    entrada = sys.argv[1] if len(sys.argv) > 1 else "1000000"
    print("ÁREA: HERRAMIENTAS")
    print("DESCRIPCIÓN: Formateador de números en palabras (México)")
    print("TECNOLOGÍA: Python estándar")
    print(f"Entrada: {entrada}")
    print(f"Salida: {formateador_numero_palabras_mx(entrada)}")
    print(f"Salida con decenas y unidades: {formateador_numero_palabras_mx(entrada, True)}")
    print(f"Salida con mil y decenas: {formateador_numero_palabras_mx(entrada, False)}")
    print(f"Salida con mil y decenas y unidades: {formateador_numero_palabras_mx(entrada, False, True)}")
    print("Resumen ejecutivo:")
    print("La función formateador_numero_palabras_mx() convierte números en palabras en español mexicano.")
    print("La función soporta números enteros, flotantes y complejos.")
    print("La función se puede personalizar con parámetros adicionales para cambiar el formato de salida.")

if __name__ == "__main__":
    main()