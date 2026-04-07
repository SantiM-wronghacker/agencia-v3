"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Formateador de código que revisa la indentación, docstrings y estructura básica en archivos .py
TECNOLOGÍA: Python, ast
"""
import ast
import os
import sys
import time
from datetime import datetime

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def revisar_indentacion(codigo):
    try:
        ast.parse(codigo)
        return True
    except IndentationError as e:
        print(f"Error de indentación en línea {e.lineno}: {e.msg}")
        return False
    except SyntaxError as e:
        print(f"Error de sintaxis en línea {e.lineno}: {e.msg}")
        return False

def revisar_docstrings(codigo):
    try:
        arbol = ast.parse(codigo)
        funciones = [n for n in arbol.body if isinstance(n, ast.FunctionDef)]
        for func in funciones:
            if not func.body or not isinstance(func.body[0], ast.Expr) or not isinstance(func.body[0].value, ast.Str):
                print(f"Función '{func.name}' no tiene docstring")
                return False
        return True
    except Exception as e:
        print(f"Error al analizar docstrings: {str(e)}")
        return False

def revisar_estructura_basica(codigo):
    try:
        arbol = ast.parse(codigo)
        if not arbol.body:
            print("El archivo está vacío")
            return False
        return True
    except Exception as e:
        print(f"Error al analizar estructura básica: {str(e)}")
        return False

def formatear_codigo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()
    except UnicodeDecodeError:
        print(f"Error al leer el archivo {ruta_archivo}. Es posible que tenga caracteres no soportados.")
        return False
    except FileNotFoundError:
        print(f"Archivo {ruta_archivo} no encontrado.")
        return False
    except Exception as e:
        print(f"Error al abrir el archivo {ruta_archivo}: {str(e)}")
        return False

    if not revisar_estructura_basica(codigo):
        return False

    if not revisar_indentacion(codigo):
        return False

    if not revisar_docstrings(codigo):
        return False

    print(f"El archivo {ruta_archivo} está bien formateado.")
    return True

def generar_resumen_ejecutivo(archivos_revisados, archivos_correctos):
    porcentaje = (archivos_correctos / archivos_revisados) * 100 if archivos_revisados > 0 else 0
    print("\n=== RESUMEN EJECUTIVO ===")
    print(f"Archivos revisados: {archivos_revisados}")
    print(f"Archivos correctos: {archivos_correctos}")
    print(f"Porcentaje de archivos válidos: {porcentaje:.2f}%")
    print(f"Fecha de revisión: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    ruta_actual = os.getcwd()
    archivos_revisados = 0
    archivos_correctos = 0

    if len(sys.argv) > 1:
        archivos_a_revisar = [archivo for archivo in sys.argv[1:] if archivo.endswith(".py")]
        if not archivos_a_revisar:
            print("No se encontraron archivos .py en los argumentos proporcionados.")
            return
    else:
        archivos_a_revisar = [archivo for archivo in os.listdir(ruta_actual) if archivo.endswith(".py") and archivo != os.path.basename(__file__)]
        if not archivos_a_revisar:
            print("No se encontraron archivos .py en el directorio actual.")
            return

    for archivo in archivos_a_revisar:
        archivos_revisados += 1
        if formatear_codigo(archivo):
            archivos_correctos += 1

    generar_resumen_ejecutivo(archivos_revisados, archivos_correctos)

if __name__ == "__main__":
    main()