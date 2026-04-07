"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza generador hash verificacion
TECNOLOGÍA: Python estándar
"""

import sys
import json
import hashlib
import random
import datetime

def main():
    try:
        # Parámetros por defecto
        num_hash = 5
        longitud_hash = 10
        algoritmo_hash = "sha256"

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
        print("Fecha y hora de generación:", datetime.datetime.now())
        print("Número de hashes generados:", num_hash)
        print("Longitud de cada hash:", longitud_hash)
        print("Algoritmo de hash utilizado:", algoritmo_hash)
        print("Hashes de verificación:")
        for i, hash_value in enumerate(hashes):
            print(f"Hash {i+1}: {hash_value}")
        print("Resumen de operación:")
        print(json.dumps({"num_hash": num_hash, "longitud_hash": longitud_hash, "algoritmo_hash": algoritmo_hash}, indent=4))
        print("Detalle de hashes generados:")
        for i, hash_value in enumerate(hashes):
            print(f"Hash {i+1} (detalles):")
            print(f"  Valor: {hash_value}")
            print(f"  Longitud: {len(hash_value)}")
            print(f"  Tipo: {type(hash_value)}")
        print("Estadísticas de hashes generados:")
        print(f"  Media de longitud: {sum(len(hash_value) for hash_value in hashes) / len(hashes)}")
        print(f"  Desviación estándar de longitud: {math.sqrt(sum((len(hash_value) - sum(len(hash_value) for hash_value in hashes) / len(hashes)) ** 2 for hash_value in hashes) / len(hashes))}")
        print("Resumen ejecutivo:")
        print(f"Se han generado {num_hash} hashes de verificación con un algoritmo {algoritmo_hash} y longitud {longitud_hash}.")
        print(f"Los hashes generados tienen una media de longitud de {sum(len(hash_value) for hash_value in hashes) / len(hashes)} y una desviación estándar de {math.sqrt(sum((len(hash_value) - sum(len(hash_value) for hash_value in hashes) / len(hashes)) ** 2 for hash_value in hashes) / len(hashes))}.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    import math
    main()