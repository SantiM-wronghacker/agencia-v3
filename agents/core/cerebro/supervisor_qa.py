"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Auditor de calidad de la agencia. Verifica sintaxis, detecta imports
             prohibidos reales via AST (no por texto libre), hace rollback automático
             si un parche rompió un archivo y actualiza habilidades.json.
             Fix clave: detección por AST elimina falsos positivos en listas de strings.
TECNOLOGÍA: Python estándar, ast, json
"""

import ast
import os
import sys
import json
import time
import shutil
import importlib
from pathlib import Path
from glob import glob

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

# ============================================================
# CONFIGURACIÓN
# ============================================================
LOG_EVOLUCION        = "registro_noche.txt"
ARCHIVO_HABILIDADES  = "habilidades.json"

# Imports reales prohibidos — detectados por AST, no por texto
# NOTA: Todos fueron migrados a Groq el 2026-02-28
IMPORTS_PROHIBIDOS = set()  # Vacío: stack completo migrado

# ============================================================
# LOGGING
# ============================================================
def registrar_log(mensaje):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    linea = f"[{timestamp}] [QA] {mensaje}"
    with open(LOG_EVOLUCION, "a", encoding="utf-8") as f:
        f.write(linea + "\n")
    print(linea)

# ============================================================
# VERIFICACIONES
# ============================================================
def verificar_sintaxis(ruta):
    try:
        with open(ruta, "r", encoding="utf-8", errors="replace") as f:
            contenido = f.read()
        ast.parse(contenido)
        return True, None
    except SyntaxError as e:
        return False, f"SyntaxError línea {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)

def detectar_imports_prohibidos(ruta):
    """
    Detecta imports prohibidos usando AST.
    Solo detecta imports REALES, no palabras dentro de strings o comentarios.
    Esto evita que supervisor_qa.py, mapeador_capacidades.py o patcher_pro.py
    se marquen a sí mismos como rojos por tener 'ollama' en sus listas de detección.
    """
    try:
        with open(ruta, "r", encoding="utf-8", errors="replace") as f:
            contenido = f.read()
        arbol = ast.parse(contenido)
    except Exception:
        return [], []

    imports_encontrados = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            for alias in nodo.names:
                imports_encontrados.add(alias.name.split(".")[0])
        elif isinstance(nodo, ast.ImportFrom) and nodo.module:
            imports_encontrados.add(nodo.module.split(".")[0])

    prohibidos = [
        imp for imp in imports_encontrados
        if any(p in imp.lower() for p in IMPORTS_PROHIBIDOS)
    ]
    return prohibidos, list(imports_encontrados)

def verificar_librerias(todos_imports):
    ok = []
    faltantes = []
    for lib in todos_imports:
        if any(p in lib.lower() for p in IMPORTS_PROHIBIDOS):
            continue
        try:
            importlib.import_module(lib)
            ok.append(lib)
        except ImportError:
            faltantes.append(lib)
    return ok, faltantes

# ============================================================
# ROLLBACK AUTOMÁTICO
# ============================================================
def buscar_backup_reciente(ruta):
    p = Path(ruta)
    patron = str(p.parent / (p.stem + ".bak.*"))
    backups = sorted(glob(patron), reverse=True)
    return backups[0] if backups else None

def hacer_rollback(ruta):
    backup = buscar_backup_reciente(ruta)
    if backup:
        try:
            shutil.copy2(backup, ruta)
            registrar_log(f"↩️  Rollback exitoso: {os.path.basename(ruta)} ← {os.path.basename(backup)}")
            return True
        except Exception as e:
            registrar_log(f"❌ Rollback falló para {ruta}: {e}")
            return False
    else:
        registrar_log(f"⚠️  No hay backup disponible para {os.path.basename(ruta)}")
        return False

# ============================================================
# ACTUALIZAR HABILIDADES.JSON
# ============================================================
def actualizar_salud(archivo, salud):
    if not os.path.exists(ARCHIVO_HABILIDADES):
        return
    try:
        with open(ARCHIVO_HABILIDADES, "r", encoding="utf-8", errors="replace") as f:
            habilidades = json.load(f)
        nombre = os.path.basename(archivo)
        if nombre in habilidades:
            habilidades[nombre]["salud"] = salud
            habilidades[nombre]["ultima_actualizacion"] = time.strftime('%Y-%m-%d %H:%M:%S')
            with open(ARCHIVO_HABILIDADES, "w", encoding="utf-8") as f:
                json.dump(habilidades, f, ensure_ascii=False, indent=4)
    except Exception as e:
        registrar_log(f"⚠️  No se pudo actualizar habilidades.json: {e}")

# ============================================================
# AUDITAR UN ARCHIVO
# ============================================================
def auditar_archivo(ruta):
    nombre = os.path.basename(ruta)
    resultado = {
        "archivo": nombre,
        "sintaxis_ok": False,
        "imports_prohibidos": [],
        "librerias_faltantes": [],
        "rollback_aplicado": False,
        "estado_final": "❌ ROJO"
    }

    registrar_log(f"🔍 Auditando: {nombre}")

    sintaxis_ok, error_sintaxis = verificar_sintaxis(ruta)
    resultado["sintaxis_ok"] = sintaxis_ok

    if not sintaxis_ok:
        registrar_log(f"  ❌ Sintaxis rota: {error_sintaxis}")
        rollback_ok = hacer_rollback(ruta)
        resultado["rollback_aplicado"] = rollback_ok
        if rollback_ok:
            sintaxis_ok, _ = verificar_sintaxis(ruta)
            resultado["sintaxis_ok"] = sintaxis_ok
            if sintaxis_ok:
                registrar_log(f"  ✅ Rollback restauró el archivo correctamente.")
                actualizar_salud(ruta, "OK (restaurado)")
            else:
                registrar_log(f"  🚨 Backup también roto. Intervención manual requerida.")
                actualizar_salud(ruta, "CRÍTICO - Manual requerido")
        else:
            actualizar_salud(ruta, "CRÍTICO - Sin backup")
        return resultado

    registrar_log(f"  ✅ Sintaxis correcta")

    prohibidos, todos_imports = detectar_imports_prohibidos(ruta)
    resultado["imports_prohibidos"] = prohibidos

    if prohibidos:
        registrar_log(f"  🔴 Imports prohibidos: {prohibidos}")
        actualizar_salud(ruta, f"Requiere Migración ({', '.join(prohibidos)})")
    else:
        registrar_log(f"  ✅ Sin imports prohibidos")

    libs_ok, libs_faltantes = verificar_librerias(todos_imports)
    resultado["librerias_faltantes"] = libs_faltantes

    if libs_faltantes:
        registrar_log(f"  ⚠️  Librerías no instaladas: {libs_faltantes}")
    if libs_ok:
        registrar_log(f"  ✅ Librerías OK: {libs_ok}")

    if sintaxis_ok and not prohibidos:
        resultado["estado_final"] = "✅ VERDE"
        actualizar_salud(ruta, "OK")
    else:
        resultado["estado_final"] = "🔴 ROJO"

    registrar_log(f"  → Estado final: {resultado['estado_final']}")
    return resultado

# ============================================================
# AUDITORÍA COMPLETA
# ============================================================
def auditar_agencia():
    registrar_log("🛡️  QA SUPERVISOR iniciado — auditando agencia completa...")
    archivos = sorted([f for f in os.listdir(".") if f.endswith(".py")])

    if not archivos:
        registrar_log("⚠️  No se encontraron archivos .py.")
        return

    registrar_log(f"📋 {len(archivos)} archivos a auditar...")

    verdes = []
    rojos = []
    rollbacks = []

    for archivo in archivos:
        resultado = auditar_archivo(archivo)
        if resultado["estado_final"] == "✅ VERDE":
            verdes.append(archivo)
        else:
            rojos.append(archivo)
        if resultado["rollback_aplicado"]:
            rollbacks.append(archivo)

    registrar_log(f"\n{'='*55}")
    registrar_log(f"📊 REPORTE QA:")
    registrar_log(f"   ✅ Verdes:    {len(verdes)}")
    registrar_log(f"   🔴 Rojos:     {len(rojos)}")
    registrar_log(f"   ↩️  Rollbacks: {len(rollbacks)}")

    if rojos:
        registrar_log(f"\n   Agentes en Rojo:")
        for r in rojos:
            registrar_log(f"     🔴 {r}")

    if rollbacks:
        registrar_log(f"\n   Rollbacks aplicados:")
        for r in rollbacks:
            registrar_log(f"     ↩️  {r}")

    registrar_log(f"{'='*55}")
    registrar_log("🏁 QA Supervisor completado.")

# ============================================================
# PUNTO DE ENTRADA
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) == 2:
        archivo = sys.argv[1]
        if not os.path.exists(archivo):
            print(f"❌ El archivo {archivo} no existe.")
            sys.exit(1)
        if not archivo.endswith(".py"):
            print(f"❌ {archivo} no es un archivo .py")
            sys.exit(1)
        auditar_archivo(archivo)
    else:
        auditar_agencia()