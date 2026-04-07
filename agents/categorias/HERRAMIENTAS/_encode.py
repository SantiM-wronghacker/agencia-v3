# ARCHIVO: _encode.py
# AREA: HERRAMIENTAS
# DESCRIPCION: Encode y decode de cadenas utilizando base64
# TECNOLOGIA: Python

import base64
import sys
import datetime
import os

def main():
    try:
        if len(sys.argv) != 3:
            print("Uso: python _encode.py <cadena> <accion>")
            print("Accion: encode/decode")
            print("Ejemplo: python _encode.py 'Hola Mundo' encode")
            sys.exit(1)

        cadena = sys.argv[1]
        accion = sys.argv[2]

        if accion == "encode":
            encoded = base64.b64encode(cadena.encode()).decode()
            print(f"Cadena original: {cadena}")
            print(f"Cadena encoded: {encoded}")
            print(f"Tipo de dato: {type(encoded)}")
            print(f"Longitud de la cadena encoded: {len(encoded)}")
            print(f"Fecha y hora de ejecucion: {datetime.datetime.now()}")
            print(f"Directorio actual: {os.getcwd()}")
            print(f"Nombre del archivo: {__file__}")
            print(f"Version de Python: {sys.version}")
        elif accion == "decode":
            try:
                decoded = base64.b64decode(cadena.encode()).decode()
                print(f"Cadena original encoded: {cadena}")
                print(f"Cadena decoded: {decoded}")
                print(f"Tipo de dato: {type(decoded)}")
                print(f"Longitud de la cadena decoded: {len(decoded)}")
                print(f"Fecha y hora de ejecucion: {datetime.datetime.now()}")
                print(f"Directorio actual: {os.getcwd()}")
                print(f"Nombre del archivo: {__file__}")
                print(f"Version de Python: {sys.version}")
            except Exception as e:
                print(f"Error al decodificar: {e}")
                print(f"Detalle del error: {str(e)}")
                print(f"Tipo de error: {type(e)}")
        else:
            print("Accion no valida")
            print("Acciones disponibles: encode, decode")

        print("\nResumen ejecutivo:")
        print(f"Se ha {accion}ado la cadena con exito")
        print(f"Fecha y hora de fin de ejecucion: {datetime.datetime.now()}")
        print(f"Memoria utilizada: {sys.getsizeof(cadena)} bytes")
    except Exception as e:
        print(f"Error: {e}")
        print(f"Detalle del error: {str(e)}")
        print(f"Tipo de error: {type(e)}")
        print(f"Fecha y hora de error: {datetime.datetime.now()}")

if __name__ == "__main__":
    main()