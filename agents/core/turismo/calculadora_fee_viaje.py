# FINANZAS, Calculadora de fee de viaje, Python
# AREA: FINANZAS
# DESCRIPCION: Calcula el 8% de fee sobre costo total
# TECNOLOGIA: Python

import sys
import json
import datetime
import math
import os

def calcula_fee(costo_total, tasa_fee=0.08):
    try:
        fee = costo_total * tasa_fee
        return fee
    except ValueError:
        return "Error: El costo total debe ser un número"
    except TypeError:
        return "Error: El costo total debe ser un número"
    except Exception as e:
        return f"Error: {str(e)}"

def calcula_iva(costo_total, tasa_iva=0.16):
    try:
        iva = costo_total * tasa_iva
        return iva
    except ValueError:
        return "Error: El costo total debe ser un número"
    except TypeError:
        return "Error: El costo total debe ser un número"
    except Exception as e:
        return f"Error: {str(e)}"

def calcula_isr(costo_total, tasa_isr=0.1):
    try:
        isr = costo_total * tasa_isr
        return isr
    except ValueError:
        return "Error: El costo total debe ser un número"
    except TypeError:
        return "Error: El costo total debe ser un número"
    except Exception as e:
        return f"Error: {str(e)}"

def calcula_total(costo_total, fee, iva, isr):
    try:
        total = costo_total + fee + iva + isr
        return total
    except ValueError:
        return "Error: El costo total debe ser un número"
    except TypeError:
        return "Error: El costo total debe ser un número"
    except Exception as e:
        return f"Error: {str(e)}"

def calcula_impuestos(costo_total):
    try:
        iva = costo_total * 0.16
        isr = costo_total * 0.25
        return iva, isr
    except ValueError:
        return "Error: El costo total debe ser un número"
    except TypeError:
        return "Error: El costo total debe ser un número"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    try:
        if len(sys.argv) < 4:
            print("Error: Faltan argumentos")
            sys.exit(1)
        costo_total = float(sys.argv[1])
        tasa_fee = float(sys.argv[2]) if len(sys.argv) > 2 else 0.08
        tasa_iva = float(sys.argv[3]) if len(sys.argv) > 3 else 0.16
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        iva, isr = calcula_impuestos(costo_total)
        fee = calcula_fee(costo_total, tasa_fee)
        iva_calculado = calcula_iva(costo_total, tasa_iva)
        isr_calculado = calcula_isr(costo_total)
        total = calcula_total(costo_total, fee, iva_calculado, isr_calculado)
        print(f"Costo total: {costo_total}")
        print(f"Fee: {fee}")
        print(f"Iva: {iva}")
        print(f"Isr: {isr}")
        print(f"Total: {total}")
        print(f"Fecha actual: {fecha_actual}")
        print(f"Resumen ejecutivo: El costo total es {costo_total}, el fee es {fee}, el iva es {iva}, el isr es {isr} y el total es {total}.")
    except ValueError:
        print("Error: El costo total debe ser un número")
    except TypeError:
        print("Error: El costo total debe ser un número")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()