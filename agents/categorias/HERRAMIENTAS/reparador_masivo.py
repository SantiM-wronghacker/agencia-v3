"""
ÁREA: CEREBRO
DESCRIPCIÓN: Reparador masivo automático. Analiza todos los agentes con problemas y los repara uno por uno usando Groq. Elimina input(), agrega sys.argv, corrige imports prohibidos y añade encabezados de área.
TECNOLOGÍA: Groq (Nube)
"""

import os
import sys
import ast
import time
import shutil
import json
from datetime import datetime
from llm_router import completar

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

# === CONFIGURACIÓN ===
LOG = "registro_noche.txt"
REPORTE = "reporte_reparacion.txt"
PAUSA_ENTRE_AGENTES = 5  # segundos entre agentes

# Agentes del sistema que NO se deben tocar
EXCLUIR = {
    "noche_total.py", "auto_run.py", "patcher_pro.py", "supervisor_qa.py",
    "mapeador_capacidades.py", "agente_estrategia.py", "maestro_ceo.py",
    "bus_mensajes.py", "agent_router.py", "reparador_masivo.py",
    "llm_router.py", "integrador_router.py", "orquestador_clawbot.py"
}

# Imports prohibidos — YA MIGRADOS A GROQ (2026-02-28)
IMPORTS_PROHIBIDOS = set()  # Vacío: todo está en Groq ahora

# ─────────────────────────────────────────────
#  LOGGING
# ─────────────────────────────────────────────

def log(mensaje):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    linea = f"[{timestamp}] [REPARADOR] {mensaje}"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(linea + "\n")
    print(linea)

def log_reporte(linea):
    with open(REPORTE, "a", encoding="utf-8") as f:
        f.write(linea + "\n")

# ─────────────────────────────────────────────
#  DIAGNÓSTICO
# ─────────────────────────────────────────────

def diagnosticar(archivo):
    """Detecta todos los problemas de un agente."""
    problemas = []
    try:
        with open(archivo, 'r', encoding='utf-8', errors='replace') as f:
            code = f.read()

        if 'input(' in code:
            problemas.append("USA_INPUT")

        if 'def main' in code and 'sys.argv' not in code:
            problemas.append("SIN_ARGV")

        try:
            arbol = ast.parse(code)
            for nodo in ast.walk(arbol):
                if isinstance(nodo, ast.Import):
                    for alias in nodo.names:
                        if any(p in alias.name.lower() for p in IMPORTS_PROHIBIDOS):
                            problemas.append(f"IMPORT_PROHIBIDO:{alias.name}")
                elif isinstance(nodo, ast.ImportFrom) and nodo.module:
                    if any(p in nodo.module.lower() for p in IMPORTS_PROHIBIDOS):
                        problemas.append(f"IMPORT_PROHIBIDO:{nodo.module}")
        except Exception:
            pass

        if 'ÁREA:' not in code and 'AREA:' not in code:
            problemas.append("SIN_ENCABEZADO")

    except Exception as e:
        problemas.append(f"ERROR_LECTURA:{e}")

    return problemas

def inferir_area(archivo, code):
    """Infiere el área del agente por nombre y contenido."""
    nombre = archivo.lower()
    if any(w in nombre for w in ['ceo', 'router', 'memory', 'rag', 'agent', 'hub', 'maestro', 'consola']):
        return "CEREBRO"
    if any(w in nombre for w in ['isr', 'iva', 'roi', 'balance', 'finanza', 'utilidad', 'contable', 'conversor']):
        return "FINANZAS"
    if any(w in nombre for w in ['hipoteca', 'vivienda', 'plusvalia', 'copy', 'lead', 'contrato', 'ficha', 'inmueble', 'arrendamiento', 'propiedad', 'whatsapp', 'clasificador']):
        return "REAL ESTATE"
    return "HERRAMIENTAS"

# ─────────────────────────────────────────────
#  REPARACIÓN CON GROQ
# ─────────────────────────────────────────────

def construir_prompt(archivo, code, problemas, area):
    """Construye el prompt de reparación específico para los problemas detectados."""
    
    instrucciones = []

    if "USA_INPUT" in problemas:
        instrucciones.append(
            "- ELIMINA todas las llamadas a input(). "
            "En su lugar, lee los parámetros desde sys.argv. "
            "Si no se pasan argumentos, usa valores por defecto razonables y muéstralos. "
            "El agente debe poder correr SIN interacción del usuario."
        )

    if "SIN_ARGV" in problemas:
        instrucciones.append(
            "- Modifica la función main() para leer parámetros desde sys.argv. "
            "Ejemplo: si el agente calcula hipoteca, acepta: python agente.py 2000000 9.5 20 "
            "Si no se pasan argumentos, usa defaults realistas para México y muéstralos."
        )

    for p in problemas:
        if p.startswith("IMPORT_PROHIBIDO:"):
            lib = p.split(":")[1]
            instrucciones.append(
                f"- ELIMINA el import de '{lib}' completamente. "
                f"Si esa librería se usaba para IA, reemplázala con Groq usando: "
                f"from groq import Groq / client = Groq(api_key='GROQ_API_KEY_PLACEHOLDER') "
                f"/ modelo='llama-3.3-70b-versatile'"
            )

    if "SIN_ENCABEZADO" in problemas:
        instrucciones.append(
            f'- Agrega al INICIO del archivo este encabezado exacto:\n'
            f'"""\nÁREA: {area}\nDESCRIPCIÓN: [describe brevemente qué hace este agente]\nTECNOLOGÍA: [lista las tecnologías principales]\n"""'
        )

    instrucciones_texto = "\n".join(instrucciones)

    return f"""Eres un experto en Python reparando agentes de una agencia de IA.

ARCHIVO: {archivo}
ÁREA: {area}
PROBLEMAS DETECTADOS: {', '.join(problemas)}

REGLAS OBLIGATORIAS:
{instrucciones_texto}

REGLAS GENERALES:
- Mantén TODA la lógica de negocio existente intacta
- Usa encoding='utf-8' en todos los open()
- Agrega time.sleep(2) entre llamadas consecutivas a Groq
- El output debe ser limpio y útil (máximo 20 líneas de output)
- Si el agente hace cálculos, muestra un resumen claro con los números más importantes
- NO uses markdown en el output, solo texto plano con formato simple
- El archivo debe ser ejecutable directamente: python {archivo}

CÓDIGO ACTUAL:
{code}

Devuelve ÚNICAMENTE el código Python corregido y completo. Sin explicaciones, sin bloques markdown, sin comentarios extra."""

def llamar_groq(prompt, intento=0):
    """Llama al LLM con rotacion automatica de proveedores."""
    resultado = completar(
        [{"role": "user", "content": prompt}],
        temperatura=0.3,
        max_tokens=4096,
    )
    if not resultado:
        log("Todos los proveedores LLM fallaron para este agente.")
    return resultado

def limpiar_codigo(texto):
    """Extrae código limpio si viene en bloque markdown."""
    if "```python" in texto:
        return texto.split("```python")[1].split("```")[0].strip()
    if "```" in texto:
        return texto.split("```")[1].split("```")[0].strip()
    return texto.strip()

def validar_sintaxis(codigo):
    """Verifica que el código generado compile."""
    try:
        ast.parse(codigo)
        return True
    except SyntaxError as e:
        return False

def hacer_backup(archivo):
    """Crea backup con timestamp."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = archivo.replace('.py', f'.bak.{ts}')
    shutil.copy2(archivo, backup)
    return backup

def restaurar_backup(backup, archivo):
    """Restaura desde backup."""
    shutil.copy2(backup, archivo)

# ─────────────────────────────────────────────
#  MOTOR PRINCIPAL
# ─────────────────────────────────────────────

def reparar_agente(archivo):
    """Repara un agente completo."""
    problemas = diagnosticar(archivo)
    
    if not problemas:
        return "OK"

    try:
        with open(archivo, 'r', encoding='utf-8', errors='replace') as f:
            code = f.read()
    except Exception as e:
        log(f"  Error leyendo {archivo}: {e}")
        return "ERROR_LECTURA"

    area = inferir_area(archivo, code)
    prompt = construir_prompt(archivo, code, problemas, area)

    log(f"  Reparando {archivo} [{area}] — Problemas: {', '.join(problemas)}")

    codigo_nuevo = llamar_groq(prompt)
    if not codigo_nuevo:
        log(f"  Groq no respondió para {archivo}")
        return "ERROR_GROQ"

    codigo_limpio = limpiar_codigo(codigo_nuevo)

    if not validar_sintaxis(codigo_limpio):
        log(f"  Código generado tiene error de sintaxis en {archivo}. Saltando.")
        return "ERROR_SINTAXIS"

    if len(codigo_limpio) < 50:
        log(f"  Código generado demasiado corto para {archivo}. Saltando.")
        return "ERROR_CORTO"

    backup = hacer_backup(archivo)

    try:
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(codigo_limpio)
        log(f"  OK: {archivo} reparado. Backup: {backup}")
        return "REPARADO"
    except Exception as e:
        restaurar_backup(backup, archivo)
        log(f"  Error escribiendo {archivo}. Restaurado desde backup: {e}")
        return "ERROR_ESCRITURA"

def ejecutar_reparacion_masiva():
    """Repara todos los agentes con problemas."""
    log("=" * 60)
    log("REPARADOR MASIVO INICIADO")
    log("=" * 60)

    log_reporte(f"\n{'='*60}")
    log_reporte(f"REPORTE DE REPARACIÓN — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_reporte(f"{'='*60}\n")

    # Obtener todos los agentes a reparar
    todos = [f for f in sorted(os.listdir('.')) if f.endswith('.py') and f not in EXCLUIR]
    
    # Filtrar solo los que tienen problemas
    con_problemas = [(f, diagnosticar(f)) for f in todos]
    con_problemas = [(f, p) for f, p in con_problemas if p]

    log(f"Agentes a reparar: {len(con_problemas)} de {len(todos)}")
    log_reporte(f"Total agentes: {len(todos)}")
    log_reporte(f"Con problemas: {len(con_problemas)}\n")

    resultados = {"REPARADO": [], "OK": [], "ERROR_GROQ": [], "ERROR_SINTAXIS": [], "ERROR_LECTURA": [], "ERROR_ESCRITURA": [], "ERROR_CORTO": []}

    for i, (archivo, problemas) in enumerate(con_problemas):
        log(f"\n[{i+1}/{len(con_problemas)}] {archivo}")
        
        resultado = reparar_agente(archivo)
        resultados[resultado].append(archivo)
        
        log_reporte(f"{archivo}: {resultado} — {', '.join(problemas)}")

        # Pausa entre agentes para no saturar Groq
        if i < len(con_problemas) - 1:
            time.sleep(PAUSA_ENTRE_AGENTES)

    # Resumen final
    log("\n" + "=" * 60)
    log("REPARACIÓN MASIVA COMPLETADA")
    log(f"  Reparados:  {len(resultados['REPARADO'])}")
    log(f"  Errores:    {sum(len(v) for k, v in resultados.items() if k.startswith('ERROR'))}")
    log("=" * 60)

    log_reporte(f"\n{'='*60}")
    log_reporte(f"RESUMEN FINAL:")
    log_reporte(f"  Reparados exitosamente: {len(resultados['REPARADO'])}")
    for k, v in resultados.items():
        if k.startswith('ERROR') and v:
            log_reporte(f"  {k}: {len(v)} — {', '.join(v)}")
    log_reporte(f"{'='*60}\n")

    return resultados

if __name__ == "__main__":
    ejecutar_reparacion_masiva()