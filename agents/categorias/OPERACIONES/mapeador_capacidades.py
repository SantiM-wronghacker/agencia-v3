"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Inspector de la agencia. Analiza todos los archivos .py, detecta
             tecnologías, categoriza automáticamente, detecta contaminantes 
             y actualiza habilidades.json con el semáforo de salud real de cada agente.
TECNOLOGÍA: Python estándar, ast, json, Groq
"""

import os
import json
import ast
import time
import datetime
import requests

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

# ============================================================
# CONFIGURACIÓN
# ============================================================
ARCHIVO_HABILIDADES = "habilidades.json"
LOG_EVOLUCION       = "registro_noche.txt"

# Scripts del sistema que NO se mapean (infraestructura pura)
EXCLUIR_MAPEO = []  # Mapeamos todo, incluso los scripts de control

# Palabras contaminantes que marcan salud roja
# Nota: ollama/openai/langchain ya fueron migrados a Groq (2026-02-28)
CONTAMINANTES = []  # Vacío: ya migramos el stack completo

# URL de Groq
GROQ_URL = "https://api.groq.com/v1/models/llama-3.3-70b-versatile"

# ============================================================
# LOGGING
# ============================================================
def registrar_log(mensaje):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    linea = f"[{timestamp}] [MAPEADOR] {mensaje}"
    with open(LOG_EVOLUCION, "a", encoding="utf-8") as f:
        f.write(linea + "\n")
    print(linea)

# ============================================================
# DETECCIÓN DE TECNOLOGÍA
# ============================================================
def analizar_tecnologia(contenido):
    """Detecta qué herramientas usa el agente."""
    tecnos = []
    c = contenido.lower()
    if "groq" in c:                                      tecnos.append("Groq (Nube)")
    if "pandas" in c or "openpyxl" in c:                tecnos.append("Excel/Datos")
    if "requests" in c:                                  tecnos.append("Web")
    if "flask" in c or "fastapi" in c:                   tecnos.append("Web/API")
    if "sqlite" in c or "database" in c:                 tecnos.append("Base de Datos")
    if "subprocess" in c:                                tecnos.append("Sistema")
    if not tecnos:                                       tecnos.append("Python estándar")
    return tecnos

# ============================================================
# DETECCIÓN DE CONTAMINANTES
# ============================================================
def detectar_contaminantes(contenido):
    """Retorna lista de contaminantes encontrados en el código."""
    c = contenido.lower()
    return [cont for cont in CONTAMINANTES if cont in c]

# ============================================================
# CATEGORIZACIÓN AUTOMÁTICA
# ============================================================
def categorizar(archivo, contenido):
    """
    Categoriza el agente en una de las 4 áreas según su nombre y contenido.
    Orden de prioridad: nombre del archivo primero, luego contenido.
    """
    nombre = archivo.lower()
    c = contenido.lower()

    # ── CEREBRO ───────────────────────────────────────────────────────
    palabras_cerebro = [
        "agent", "router", "memory", "rag", "maestro", "ceo",
        "orquesta", "hub", "mapeador", "estrategia", "arquitecto",
        "supervisor", "patcher", "auto_run", "noche", "evolucion",
        "auto_evolucion", "root", "consola", "resumen", "team"
    ]
    if any(p in nombre for p in palabras_cerebro):
        return "CEREBRO"

    # ── FINANZAS ──────────────────────────────────────────────────────
    palabras_finanzas = [
        "iva", "isr", "balance", "finanza", "roi", "contable",
        "contador", "utilidad", "impuesto", "factura", "contrato",
        "arrendamiento", "pesos", "dolar", "conversor", "proyeccion",
        "verificador", "documentacion", "estudio_finanzas", "calculadora"
    ]
    if any(p in nombre for p in palabras_finanzas):
        return "FINANZAS"

    # ── REAL ESTATE ───────────────────────────────────────────────────
    palabras_re = [
        "vivienda", "inmueble", "hipoteca", "plusvalia", "propiedad",
        "lead", "whatsapp", "copy", "ficha", "clasificador",
        "simulador", "buscador", "mapa_competencia", "generador_copy",
        "generador_ficha", "validador", "seguimiento", "amerimed"
    ]
    if any(p in nombre for p in palabras_re):
        return "REAL ESTATE"

    # ── HERRAMIENTAS (fallback) ───────────────────────────────────────
    return "HERRAMIENTAS"

# ============================================================
# EXTRACCIÓN DE DESCRIPCIÓN
# ============================================================
def extraer_descripcion(archivo, contenido, arbol):
    """
    Extrae la descripción del agente en este orden:
    1. Docstring del módulo
    2. Campo DESCRIPCIÓN del encabezado
    3. Primeros comentarios
    4. Nombre del archivo humanizado
    """
    # 1. Docstring del módulo
    docstring = ast.get_docstring(arbol)
    if docstring:
        # Si el docstring tiene campo DESCRIPCIÓN extraerlo
        for linea in docstring.split("\n"):
            if "DESCRIPCIÓN:" in linea or "DESCRIPCION:" in linea:
                desc = linea.split(":", 1)[1].strip()
                if len(desc) > 10:
                    return desc[:150]
        # Si no, usar las primeras 150 chars del docstring
        primera_linea = docstring.strip().split("\n")[0]
        if len(primera_linea) > 10:
            return primera_linea[:150]

    # 2. Buscar comentario # DESCRIPCIÓN: en las primeras 15 líneas
    for linea in contenido.split("\n")[:15]:
        if "DESCRIPCIÓN:" in linea or "DESCRIPCION:" in linea:
            partes = linea.split(":", 1)
            if len(partes) > 1:
                desc = partes[1].strip().lstrip("#").strip()
                if len(desc) > 10:
                    return desc[:150]

    # 3. Primeros comentarios útiles
    comentarios = []
    for linea in contenido.split("\n")[:10]:
        stripped = linea.strip()
        if stripped.startswith("#") and len(stripped) > 5:
            texto = stripped.lstrip("#").strip()
            if texto and not texto.startswith("!") and len(texto) > 5:
                comentarios.append(texto)
    if comentarios:
        return " ".join(comentarios)[:150]

    # 4. Fallback: nombre humanizado
    return archivo.replace(".py", "").replace("_", " ").title()

# ============================================================
# ANÁLISIS DE UN ARCHIVO
# ============================================================
def analizar_archivo(archivo):
    """
    Analiza un archivo .py y retorna su entrada para habilidades.json.
    Retorna None si el archivo no es válido.
    """
    try:
        with open(archivo, "r", encoding="utf-8", errors="replace") as f:
            contenido = f.read()

        # Parsear AST
        try:
            arbol = ast.parse(contenido)
        except SyntaxError as e:
            registrar_log(f"  ⚠️  Sintaxis rota en {archivo}: {e.msg} línea {e.lineno}")
            return {
                "descripcion": f"ERROR DE SINTAXIS línea {e.lineno}: {e.msg}",
                "categoria": categorizar(archivo, contenido),
                "salud": "Requiere Migración (Sintaxis Rota)",
                "tecnologia": analizar_tecnologia(contenido),
                "ultima_actualizacion": time.strftime('%Y-%m-%d %H:%M:%S')
            }

        # Extraer info
        descripcion  = extraer_descripcion(archivo, contenido, arbol)
        categoria    = categorizar(archivo, contenido)
        tecnologia   = analizar_tecnologia(contenido)
        contaminantes = detectar_contaminantes(contenido)

        # Determinar salud
        if contaminantes:
            salud = f"Requiere Migración ({', '.join(contaminantes)})"
        else:
            salud = "OK"

        return {
            "descripcion": descripcion,
            "categoria": categoria,
            "salud": salud,
            "tecnologia": tecnologia,
            "ultima_actualizacion": time.strftime('%Y-%m-%d %H:%M:%S')
        }

    except Exception as e:
        registrar_log(f"  ❌ Error analizando {archivo}: {e}")
        return None

# ============================================================
# ANÁLISIS COMPLETO DE LA AGENCIA
# ============================================================
def analizar_archivos():
    """Escanea todos los .py y retorna el diccionario de habilidades."""
    registrar_log("📡 Escaneando agencia completa...")

    habilidades = {}
    archivos = sorted([f for f in os.listdir(".") if f.endswith(".py")])

    verdes  = []
    rojos   = []
    errores = []

    for archivo in archivos:
        info = analizar_archivo(archivo)
        if info:
            habilidades[archivo] = info
            if info["salud"] == "OK":
                verdes.append(archivo)
                registrar_log(f"  ✅ {archivo} → {info['categoria']}")
            else:
                rojos.append(archivo)
                registrar_log(f"  🔴 {archivo} → {info['salud']}")
        else:
            errores.append(archivo)
            registrar_log(f"  ❌ {archivo} → No se pudo analizar")

    registrar_log(f"📊 Resultado: {len(verdes)} verdes | {len(rojos)} rojos | {len(errores)} errores")
    return habilidades

# ============================================================
# GUARDAR HABILIDADES
# ============================================================
def guardar_habilidades(habilidades):
    """Guarda el JSON de habilidades preservando campos existentes."""
    # Si ya existe, preservar campos que el mapeador no genera
    campos_preservar = ["ordenes"]  # Campos que otros sistemas escriben
    existente = {}

    if os.path.exists(ARCHIVO_HABILIDADES):
        try:
            with open(ARCHIVO_HABILIDADES, "r", encoding="utf-8", errors="replace") as f:
                existente = json.load(f)
        except Exception:
            pass

    # Mergear preservando campos especiales
    for archivo, info in habilidades.items():
        if archivo in existente:
            for campo in campos_preservar:
                if campo in existente[archivo]:
                    info[campo] = existente[archivo][campo]
        habilidades[archivo] = info

    try:
        with open(ARCHIVO_HABILIDADES, "w", encoding="utf-8") as f:
            json.dump(habilidades, f, indent=4, ensure_ascii=False)
        registrar_log(f"✅ habilidades.json actualizado con {len(habilidades)} agentes.")
    except Exception as e:
        registrar_log(f"❌ Error guardando habilidades.json: {e}")

# ============================================================
# PUNTO DE ENTRADA
# ============================================================
def main():
    habilidades = analizar_archivos()
    if habilidades:
        guardar_habilidades(habilidades)
    else:
        registrar_log("❌ No se encontraron agentes válidos.")

if __name__ == "__main__":
    main()