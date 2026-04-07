#!/usr/bin/env python
"""Check which api_agencia.py file is being used
AREA: HERRAMIENTAS
DESCRIPCION: Verificar la existencia y contenido del archivo api_agencia.py
TECNOLOGIA: Python"""

import sys
import os
import datetime
import math
import json
import re

# Add current dir to path
sys.path.insert(0, os.getcwd())

def main():
    try:
        # Check file location
        api_path = os.path.join(os.getcwd(), 'api_agencia.py')
        print(f"Current directory: {os.getcwd()}")
        print(f"API file path: {api_path}")
        print(f"File exists: {os.path.exists(api_path)}")

        if os.path.exists(api_path):
            with open(api_path, 'r', encoding='utf-8') as f:
                content = f.read()

            has_test = '/test-19-cats' in content
            print(f"\n/test-19-cats endpoint exists: {has_test}")

            # Find the position
            if has_test:
                idx = content.find('/test-19-cats')
                section = content[max(0, idx-200):idx+500]
                print(f"\nContext around /test-19-cats:")
                print(section)

            # Calculate file size in megabytes
            file_size_bytes = os.path.getsize(api_path)
            file_size_mb = math.ceil(file_size_bytes / (1024 * 1024))
            print(f"\nAPI file size: {file_size_mb} MB")

            # Calculate file modification time
            mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(api_path))
            print(f"API file modification time: {mod_time}")

            # Get file permissions
            permissions = oct(os.stat(api_path).st_mode)[-3:]
            print(f"API file permissions: {permissions}")

            # Get file owner
            owner = os.stat(api_path).st_uid
            print(f"API file owner: {owner}")

            # Get file last access time
            last_access_time = datetime.datetime.fromtimestamp(os.path.getatime(api_path))
            print(f"API file last access time: {last_access_time}")

            # Get file creation time
            creation_time = datetime.datetime.fromtimestamp(os.path.getctime(api_path))
            print(f"API file creation time: {creation_time}")

            # Get file metadata
            metadata = os.stat(api_path)
            print(f"API file metadata: {metadata}")

            # Get file lines of code
            lines_of_code = len(content.splitlines())
            print(f"API file lines of code: {lines_of_code}")

            # Get file functions and classes
            functions = re.findall(r'def\s+\w+\s*\(', content)
            classes = re.findall(r'class\s+\w+\s*:', content)
            print(f"API file functions: {len(functions)}")
            print(f"API file classes: {len(classes)}")

            # Get file imports
            imports = re.findall(r'import\s+\w+', content)
            print(f"API file imports: {len(imports)}")

            # Resumen ejecutivo
            print("\nResumen ejecutivo:")
            print(f"Archivo: {api_path}")
            print(f"Tamano: {file_size_mb} MB")
            print(f"Ultima modificacion: {mod_time}")
            print(f"Numero de lineas de codigo: {lines_of_code}")
            print(f"Numero de funciones: {len(functions)}")
            print(f"Numero de clases: {len(classes)}")
            print(f"Numero de imports: {len(imports)}")

        else:
            print("El archivo api_agencia.py no existe")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()