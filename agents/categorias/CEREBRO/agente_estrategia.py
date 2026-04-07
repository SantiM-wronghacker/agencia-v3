"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Estratega v2.1. Genera misiones por área simultáneamente con prioridad
             por impacto real en la cadena de la agencia. CEREBRO tiene máxima
             prioridad, luego FINANZAS, REAL ESTATE y HERRAMIENTAS.
             Detecta Ollama, openai y langchain por AST como imports reales.
             Acumula misiones sin sobrescribir las existentes (preserva misiones manuales).
TECNOLOGÍA: Python estándar, ast, json
"""

import json
import time
import os
import ast

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

# ============================================================
# CONFIGURACIÓN
# ============================================================
MAX_MISIONES_POR_AREA  = 4    # Misiones por cada área simultánea
MAX_TOTAL_MISIONES     = 15   # Límite total por ciclo
LOG_EVOLUCION          = "registro_noche.txt"
ARCHIVO_HABILIDADES    = "habilidades.json"
ARCHIVO_MISIONES       = "misiones.txt"

# Prioridad de áreas por impacto en la cadena
PRIORIDAD_AREAS = {
    "CEREBRO":      1,   # Máxima — si falla, todo falla
    "FINANZAS":     2,   # Alta — core del negocio
    "REAL ESTATE":  3,   # Media — vertical principal
    "HERRAMIENTAS": 4    # Normal — soporte
}

# Imports prohibidos (detección por AST)
# NOTA: ollama, openai, langchain se migraron a Groq el 2026-02-28
IMPORTS_PROHIBIDOS = set()  # Vacío: ya migramos todo a Groq

# ============================================================
# LOGGING
# ============================================================
def registrar_log(mensaje):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    linea = f"[{timestamp}] [ESTRATEGIA] {mensaje}"
    with open(LOG_EVOLUCION, "a", encoding="utf-8") as f:
        f.write(linea + "\n")
    print(linea)

# ============================================================
# DETECCIÓN DE IMPORTS PROHIBIDOS POR AST
# ============================================================
def tiene_imports_prohibidos(archivo):
    """Detecta imports prohibidos REALES via AST — sin falsos positivos."""
    if not os.path.exists(archivo):
        return False, []
    try:
        with open(archivo, "r", encoding="utf-8", errors="replace") as f:
            contenido = f.read()
        arbol = ast.parse(contenido)
        imports = set()
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.Import):
                for alias in nodo.names:
                    imports.add(alias.name.split(".")[0].lower())
            elif isinstance(nodo, ast.ImportFrom) and nodo.module:
                imports.add(nodo.module.split(".")[0].lower())
        encontrados = [i for i in imports if any(p in i for p in IMPORTS_PROHIBIDOS)]
        return len(encontrados) > 0, encontrados
    except Exception:
        return False, []

def descripcion_pobre(descripcion):
    if not descripcion:
        return True
    desc = descripcion.strip()
    if len(desc) < 15:
        return True
    pobres = ["script operativo", "sin descripción", "sin descripcion", "n/a", "todo", ""]
    return any(p in desc.lower() for p in pobres)

def salud_roja(info):
    salud = info.get("salud", "OK")
    return "Migración" in salud or "Rojo" in salud or "rojo" in salud or "CRITICO" in salud

# ============================================================
# GENERACIÓN DE MISIONES POR ÁREA
# ============================================================
def generar_misiones_por_area(habilidades, area, max_por_area):
    """
    Genera misiones específicas para un área ordenadas por prioridad de impacto.
    Prioridad dentro del área: Rojo > Sin doc > Optimización
    """
    agentes_area = {
        arch: info for arch, info in habilidades.items()
        if info.get("categoria", "").upper() == area.upper()
    }

    misiones_rojo = []
    misiones_doc  = []
    misiones_opt  = []

    for archivo, info in agentes_area.items():
        tiene_prob, libs = tiene_imports_prohibidos(archivo)

        if salud_roja(info) or tiene_prob:
            libs_str = ", ".join(libs) if libs else "Ollama/openai"
            mision = (
                f"{archivo};"
                f"URGENTE [{area}]: Elimina imports prohibidos ({libs_str}). "
                f"Migra toda la lógica de IA a Groq con modelo llama-3.3-70b-versatile. "
                f"Usa encoding='utf-8' en todos los open(). "
                f"Añade encabezado ÁREA/DESCRIPCIÓN/TECNOLOGÍA al inicio."
            )
            misiones_rojo.append(mision)

        elif descripcion_pobre(info.get("descripcion", "")):
            mision = (
                f"{archivo};"
                f"DOCUMENTAR [{area}]: Añade docstring detallado explicando qué hace, "
                f"parámetros y retornos. Añade comentarios inline en funciones principales. "
                f"Actualiza encabezado ÁREA/DESCRIPCIÓN/TECNOLOGÍA."
            )
            misiones_doc.append(mision)

        else:
            mision = (
                f"{archivo};"
                f"OPTIMIZAR [{area}]: Revisa y mejora el código. Reduce tokens en prompts, "
                f"añade manejo de excepciones donde falte, verifica encoding='utf-8' en "
                f"todos los open(), añade time.sleep(1) entre llamadas a Groq si hay varias."
            )
            misiones_opt.append(mision)

    todas = misiones_rojo + misiones_doc + misiones_opt
    return todas[:max_por_area]

# ============================================================
# ACUMULACIÓN SIN SOBRESCRIBIR
# ============================================================
def acumular_misiones(misiones_finales):
    """
    Agrega misiones nuevas a misiones.txt sin borrar las existentes.
    Evita duplicados comparando el archivo objetivo de cada misión.
    """
    # Leer archivos que ya están en cola para no duplicar
    archivos_en_cola = set()
    if os.path.exists(ARCHIVO_MISIONES):
        with open(ARCHIVO_MISIONES, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea and ";" in linea:
                    archivos_en_cola.add(linea.split(";")[0].strip())

    # Filtrar solo las misiones cuyo archivo no está ya en cola
    nuevas = [m for m in misiones_finales if m.split(";")[0].strip() not in archivos_en_cola]

    if nuevas:
        with open(ARCHIVO_MISIONES, "a", encoding="utf-8") as f:
            f.write("\n".join(nuevas) + "\n")

    return nuevas

# ============================================================
# MOTOR PRINCIPAL
# ============================================================
def generar_misiones_auto():
    registrar_log("🧠 Estratega v2.1 — Generando misiones por área con prioridad de impacto...")

    if not os.path.exists(ARCHIVO_HABILIDADES):
        registrar_log(f"❌ No se encontró {ARCHIVO_HABILIDADES}. Abortando.")
        return

    try:
        with open(ARCHIVO_HABILIDADES, "r", encoding="utf-8", errors="replace") as f:
            habilidades = json.load(f)
    except json.JSONDecodeError as e:
        registrar_log(f"❌ Error de formato en {ARCHIVO_HABILIDADES}: {e}")
        return
    except Exception as e:
        registrar_log(f"❌ Error leyendo {ARCHIVO_HABILIDADES}: {e}")
        return

    # Generar misiones por área ordenadas por prioridad de impacto
    todas_misiones = []
    areas_ordenadas = sorted(PRIORIDAD_AREAS.keys(), key=lambda a: PRIORIDAD_AREAS[a])

    resumen_areas = {}
    for area in areas_ordenadas:
        misiones_area = generar_misiones_por_area(habilidades, area, MAX_MISIONES_POR_AREA)
        resumen_areas[area] = len(misiones_area)
        todas_misiones.extend(misiones_area)
        if misiones_area:
            registrar_log(f"  📋 {area}: {len(misiones_area)} misiones generadas")

    # Respetar límite total
    misiones_finales = todas_misiones[:MAX_TOTAL_MISIONES]

    # Diagnóstico
    registrar_log(
        f"📊 Por área — CEREBRO: {resumen_areas.get('CEREBRO',0)} | "
        f"FINANZAS: {resumen_areas.get('FINANZAS',0)} | "
        f"REAL ESTATE: {resumen_areas.get('REAL ESTATE',0)} | "
        f"HERRAMIENTAS: {resumen_areas.get('HERRAMIENTAS',0)}"
    )
    registrar_log(f"📋 Total generadas: {len(misiones_finales)} de {len(todas_misiones)} posibles")

    if misiones_finales:
        nuevas = acumular_misiones(misiones_finales)
        registrar_log(f"✅ {len(nuevas)} misiones nuevas acumuladas (sin sobrescribir existentes)")
        for m in nuevas:
            nombre = m.split(";")[0]
            tipo = "🔴" if "URGENTE" in m else ("📝" if "DOCUMENTAR" in m else "🟢")
            area = m.split("[")[1].split("]")[0] if "[" in m else "?"
            registrar_log(f"  {tipo} [{area}] → {nombre}")
        if len(nuevas) < len(misiones_finales):
            saltadas = len(misiones_finales) - len(nuevas)
            registrar_log(f"  ⏭️ {saltadas} misiones omitidas (ya estaban en cola)")
    else:
        registrar_log("✨ Todos los agentes están sanos. No se generaron misiones.")

# ============================================================
# PUNTO DE ENTRADA
# ============================================================
if __name__ == "__main__":
    generar_misiones_auto()