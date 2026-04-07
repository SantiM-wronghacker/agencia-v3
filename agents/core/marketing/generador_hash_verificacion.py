"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza generador hash verificación
TECNOLOGÍA: Python estándar
"""

import sys
import json
import hashlib
import random
import datetime
import math

def main():
    try:
        # Parámetros por defecto
        num_hash = 5
        longitud_hash = 10
        algoritmo_hash = "sha256"
        fecha_inicio = datetime.datetime.now()

        # Obtener parámetros de la línea de comandos
        if len(sys.argv) > 1:
            num_hash = int(sys.argv[1])
        if len(sys.argv) > 2:
            longitud_hash = int(sys.argv[2])
        if len(sys.argv) > 3:
            algoritmo_hash = sys.argv[3]

        # Verificar algoritmo de hash válido
        if algoritmo_hash not in ["sha256", "md5", "sha1"]:
            raise ValueError("Algoritmo de hash no válido")

        # Verificar longitud de hash válida
        if longitud_hash < 1:
            raise ValueError("Longitud de hash debe ser mayor a 0")

        # Verificar número de hashes válidos
        if num_hash < 1:
            raise ValueError("Número de hashes debe ser mayor a 0")

        # Verificar si la longitud del hash es mayor a la longitud del algoritmo de hash
        if longitud_hash > 64:
            raise ValueError("La longitud del hash no puede ser mayor a la longitud del algoritmo de hash")

        # Verificar si la longitud del hash es un número entero
        if not isinstance(longitud_hash, int):
            raise ValueError("La longitud del hash debe ser un número entero")

        # Verificar si el algoritmo de hash es un string
        if not isinstance(algoritmo_hash, str):
            raise ValueError("El algoritmo de hash debe ser un string")

        # Verificar si el número de hashes es un número entero
        if not isinstance(num_hash, int):
            raise ValueError("El número de hashes debe ser un número entero")

        # Generar hashes de verificación
        hashes = []
        for _ in range(num_hash):
            if algoritmo_hash == "sha256":
                hash_object = hashlib.sha256()
            elif algoritmo_hash == "md5":
                hash_object = hashlib.md5()
            elif algoritmo_hash == "sha1":
                hash_object = hashlib.sha1()
            hash_object.update(str(random.random()).encode('utf-8'))
            hash_hex = hash_object.hexdigest()[:longitud_hash]
            hashes.append(hash_hex)

        # Imprimir resultados
        print("ÁREA: HERRAMIENTAS")
        print("DESCRIPCIÓN: Agente que realiza generador hash verificación")
        print("TECNOLOGÍA: Python estándar")
        print("Fecha de inicio:", fecha_inicio)
        print("Número de hashes:", num_hash)
        print("Longitud del hash:", longitud_hash)
        print("Algoritmo de hash:", algoritmo_hash)
        print("Hashes generados:")
        for i, hash in enumerate(hashes):
            print(f"Hash {i+1}: {hash}")
        print("Resumen ejecutivo:")
        print("El agente ha generado", num_hash, "hashes de verificación utilizando el algoritmo", algoritmo_hash, "con una longitud de", longitud_hash, "caracteres.")

    except ValueError as e:
        print("Error:", e)
    except Exception as e:
        print("Error inesperado:", e)

if __name__ == "__main__":
    main()