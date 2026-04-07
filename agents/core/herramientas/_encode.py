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
        if len(sys.argv) != 4:
            print("Uso: python _encode.py <cadena> <accion> <modo>")
            print("Accion: encode/decode")
            print("Modo: texto/numerico")
            print("Ejemplo: python _encode.py 'Hola Mundo' encode texto")
            sys.exit(1)

        cadena = sys.argv[1]
        accion = sys.argv[2]
        modo = sys.argv[3]

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
            if modo == "numerico":
                print(f"Valor numerico de la cadena encoded: {ord(encoded[0])}")
                print(f"Valor numerico de la cadena encoded (en hexadecimal): {hex(ord(encoded[0]))}")
                print(f"Valor numerico de la cadena encoded (en decimal): {int(hex(ord(encoded[0])), 16)}")
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
                if modo == "numerico":
                    print(f"Valor numerico de la cadena decoded: {ord(decoded[0])}")
                    print(f"Valor numerico de la cadena decoded (en hexadecimal): {hex(ord(decoded[0]))}")
                    print(f"Valor numerico de la cadena decoded (en decimal): {int(hex(ord(decoded[0])), 16)}")
            except Exception as e:
                print(f"Error al decodificar: {e}")
                print(f"Detalle del error: {str(e)}")
                print(f"Tipo de error: {type(e)}")
        else:
            print("Accion no valida")
            print("Acciones disponibles: encode, decode")
    except Exception as e:
        print(f"Error al ejecutar la accion: {e}")
        print(f"Detalle del error: {str(e)}")
        print(f"Tipo de error: {type(e)}")

    print("\nResumen ejecutivo:")
    print(f"Cadena original: {sys.argv[1]}")
    print(f"Accion realizada: {sys.argv[2]}")
    print(f"Modo de ejecucion: {sys.argv[3]}")
    print(f"Fecha y hora de ejecucion: {datetime.datetime.now()}")
    print(f"Directorio actual: {os.getcwd()}")
    print(f"Nombre del archivo: {__file__}")
    print(f"Version de Python: {sys.version}")

if __name__ == "__main__":
    main()