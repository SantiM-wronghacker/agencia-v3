"""
ÁREA: LEGAL
DESCRIPCIÓN: Genera acuerdos de confidencialidad (NDA) básicos para México. Recibe nombres de las partes, objeto del acuerdo y vigencia. Produce documento en texto listo para firmar.
TECNOLOGÍA: Python estándar
"""

import sys
from datetime import datetime, timedelta

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_fecha_fin(fecha_inicio, vigencia_años):
    try:
        fecha_fin = fecha_inicio + timedelta(days=vigencia_años*365)
        return fecha_fin
    except Exception as e:
        print(f"Error en cálculo de fecha: {str(e)}")
        return None

def validar_parametros(parte_a, parte_b, objeto, vigencia_años):
    if not parte_a or not parte_b or not objeto:
        raise ValueError("Los nombres de las partes y el objeto no pueden estar vacíos")
    if vigencia_años <= 0:
        raise ValueError("La vigencia debe ser mayor a cero")
    return True

def main():
    try:
        if len(sys.argv) == 5:
            parte_a = sys.argv[1]
            parte_b = sys.argv[2]
            objeto = sys.argv[3]
            vigencia_años = int(sys.argv[4])
        else:
            parte_a = 'Juan López'
            parte_b = 'Empresa XYZ'
            objeto = 'proyecto inmobiliario'
            vigencia_años = 2

        validar_parametros(parte_a, parte_b, objeto, vigencia_años)

        fecha_inicio = datetime.now()
        fecha_fin = calcular_fecha_fin(fecha_inicio, vigencia_años)

        if not fecha_fin:
            raise ValueError("No se pudo calcular la fecha de finalización")

        print("="*50)
        print("ACUERDO DE CONFIDENCIALIDAD ENTRE", parte_a, "Y", parte_b)
        print("="*50)
        print(f"OBJETO: {objeto}")
        print(f"VIGENCIA: {vigencia_años} años")
        print(f"FECHA DE INICIO: {fecha_inicio.strftime('%d/%m/%Y')}")
        print(f"FECHA DE FIN: {fecha_fin.strftime('%d/%m/%Y')}")
        print("\nCLÁUSULAS PRINCIPALES:")
        print("1. Las partes se obligan a mantener confidencialidad durante la vigencia del acuerdo.")
        print("2. Las partes no podrán divulgar información confidencial a terceros sin autorización.")
        print("3. La información confidencial deberá ser protegida con el mismo cuidado que la propia.")
        print("4. Al finalizar el acuerdo, toda la información confidencial deberá ser devuelta o destruida.")
        print("5. Las partes acuerdan que cualquier violación a este acuerdo podrá dar lugar a acciones legales.")
        print("\nFIRMAS:")
        print(f"FIRMA DE {parte_a}: ______________________")
        print(f"FIRMA DE {parte_b}: ______________________")
        print("\nRESUMEN EJECUTIVO:")
        print(f"El presente acuerdo de confidencialidad entre {parte_a} y {parte_b} tiene como objeto {objeto}")
        print(f"y tendrá una vigencia de {vigencia_años} años, a partir del {fecha_inicio.strftime('%d/%m/%Y')}")
        print(f"hasta el {fecha_fin.strftime('%d/%m/%Y')}. Las partes acuerdan mantener la confidencialidad")
        print("de toda la información compartida en el marco del objeto del acuerdo.")
        print("="*50)

    except ValueError as ve:
        print(f"Error de validación: {str(ve)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()