import json
import os
import sys
import subprocess
import time
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def cargar_habilidades():
    try:
        with open('habilidades.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: Archivo habilidades.json no encontrado. Asegúrate de ejecutar primero mapeador_capacidades.py")
        return {}
    except json.JSONDecodeError:
        print("Error: Formato JSON inválido en habilidades.json")
        return {}
    except Exception as e:
        print(f"Error crítico al cargar habilidades: {str(e)}")
        return {}

def mostrar_menu():
    habilidades = cargar_habilidades()
    if not habilidades:
        print("No hay agentes mapeados. Ejecuta primero mapeador_capacidades.py")
        return

    categorias = {}
    for archivo, info in habilidades.items():
        cat = info.get('categoria', 'Otros')
        if cat not in categorias:
            categorias[cat] = []
        categorias[cat].append((archivo, info))

    print("\n" + "="*60)
    print("        HUB CENTRAL DE AGENTES - AGENCIA SANTI")
    print("="*60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Ubicación: {os.getenv('COMPUTERNAME', 'Servidor Central')}")
    print("="*60)

    indice_global = 1
    mapeo_opciones = {}

    for cat in sorted(categorias.keys()):
        print(f"\nAREA: {cat.upper()}")
        print("-" * 30)
        for archivo, info in categorias[cat]:
            desc = info.get('descripcion', 'Sin descripción')
            salud = info.get('salud', 'OK')
            tecno = ", ".join(info.get('tecnologia', []))
            version = info.get('version', '1.0')
            autor = info.get('autor', 'Agencia Santi')

            estado = "[CRITICO]" if "Requiere" in salud else "[OK]"
            if "Deprecado" in salud:
                estado = "[DEPRECADO]"

            print(f"{indice_global}. {archivo:<35} {estado}")
            print(f"   {desc[:65]}...")
            if tecno:
                print(f"   Tech: {tecno}")
            print(f"   Versión: {version} | Autor: {autor}")

            mapeo_opciones[str(indice_global)] = archivo
            indice_global += 1

    print("\n" + "="*60)
    print("RESUMEN EJECUTIVO")
    print("="*60)
    print(f"Total de agentes disponibles: {len(mapeo_opciones)}")
    print(f"Categorías mapeadas: {len(categorias)}")
    print(f"Última actualización: {datetime.now().strftime('%Y-%m-%d')}")
    print("="*60)

    if len(sys.argv) > 1:
        opcion = sys.argv[1]
    else:
        print("No se proporcionó un agente para ejecutar. Salir.")
        sys.exit()

    if opcion in mapeo_opciones:
        archivo_elegido = mapeo_opciones[opcion]
        print(f"\nIniciando: {archivo_elegido}...")
        try:
            subprocess.run([sys.executable, archivo_elegido], check=True)
            time.sleep(2)
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar {archivo_elegido}: Código de salida {e.returncode}")
        except FileNotFoundError:
            print(f"Error: Archivo {archivo_elegido} no encontrado")
        except Exception as e:
            print(f"Error crítico al ejecutar {archivo_elegido}: {str(e)}")
    else:
        print(f"Opción {opcion} no válida. Agentes disponibles: {', '.join(mapeo_opciones.keys())}")

if __name__ == "__main__":
    mostrar_menu()