# ARCHIVO: generador_folio_consecutivo.py
# AREA: HERRAMIENTAS
# DESCRIPCION: Generador Folio Consecutivo
# TECNOLOGIA: Python
# REVISION: 1.0

import sys
import os
import datetime
import math
import re

def generador_folio_consecutivo(entrada, min_folio=100000000, max_folio=99999999999, modulos=None):
    """Función pura, sin prints, sin side effects."""
    if not entrada:
        return "INVALIDO:entrada_vacia"
    try:
        folio = int(entrada)
        if folio < 0:
            return "INVALIDO:valor_negativo"
        if folio > max_folio:
            return "INVALIDO:valor_muy_grande"
        if folio < min_folio:
            return "INVALIDO:valor_muy_chico"
        if not (folio % 2 == 0 and folio % 5 == 0):  
            return "INVALIDO:no_multiplo_10"
        if math.log10(folio) != int(math.log10(folio)):  
            return "INVALIDO:no_potencia_de_diez"
        if folio % 10 != 0:  
            return "INVALIDO:no_multiplo_diez"
        if folio > 99999999999:  
            return "INVALIDO:valor_muy_grande_mexico"
        if folio <= 0:  
            return "INVALIDO:valor_invalido"
        if folio > 9999999999 and folio % 5 != 0:  
            return "INVALIDO:no_multiplo_cinco"
        if len(str(folio)) > 10:
            return "INVALIDO:excede_maximo_de_caracteres"
        if folio < 100000000:
            return "INVALIDO:menor_que_minimo_requerido"
        if folio % 3 != 0:  
            return "INVALIDO:no_multiplo_tres"
        if folio % 7 != 0:  
            return "INVALIDO:no_multiplo_siete"
        if folio % 11 != 0:  
            return "INVALIDO:no_multiplo_once"
        if folio % 13 != 0:  
            return "INVALIDO:no_multiplo_trece"
        if folio % 17 != 0:  
            return "INVALIDO:no_multiplo_diecisiete"
        if folio % 19 != 0:  
            return "INVALIDO:no_multiplo_diecinueve"
        if folio % 23 != 0:  
            return "INVALIDO:no_multiplo_veintitrés"
        if folio % 29 != 0:  
            return "INVALIDO:no_multiplo_veintinueve"
        if folio % 31 != 0:  
            return "INVALIDO:no_multiplo_treinta_y_uno"
        if modulos is not None:
            for modulo in modulos:
                if folio % modulo != 0:
                    return f"INVALIDO:no_multiplo_{modulo}"
        return folio + 1
    except ValueError as e:
        return f"INVALIDO:error_de_valor: {str(e)}"
    except Exception as e:
        return f"INVALIDO:error_inesperado: {str(e)}"

def main():
    if len(sys.argv) > 1:
        entrada = sys.argv[1]
    else:
        entrada = "100000000"
    min_folio = 100000000
    max_folio = 99999999999
    modulos = None
    if len(sys.argv) > 2:
        min_folio = int(sys.argv[2])
    if len(sys.argv) > 3:
        max_folio = int(sys.argv[3])
    if len(sys.argv) > 4:
        modulos = [int(x) for x in sys.argv[4].split(',')]
    resultado = generador_folio_consecutivo(entrada, min_folio, max_folio, modulos)
    print(f"AREA: HERRAMIENTAS")
    print(f"DESCRIPCION: Generador Folio Consecutivo")
    print(f"TECNOLOGIA: Python")
    print(f"REVISION: 1.0")
    print(f"ENTRADA: {entrada}")
    print(f"RESULTADO: {resultado}")
    print(f"RESUMEN EJECUTIVO: El generador de folio consecutivo ha sido ejecutado con éxito.")

if __name__ == "__main__":
    main()