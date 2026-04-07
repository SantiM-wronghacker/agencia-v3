"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Motor de ejecución de misiones. Lee misiones.txt línea por línea,
             llama a patcher_pro.py como subproceso independiente por cada misión,
             reporta resultados y termina. Sin bucle infinito propio.
TECNOLOGÍA: Python estándar, subprocess
"""




import subprocess
import sys
import os
import time
import io as _io

# File locking nativo
try:
    import msvcrt
    _WINDOWS = True
except ImportError:
    import fcntl
    _WINDOWS = False

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

# Fix Unicode para Windows (cp1252) — hace print() seguro con cualquier caracter
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stdout, "buffer"):
    sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stderr, "buffer"):
    sys.stderr = open(sys.stderr.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)

# ============================================================
# CONFIGURACIÓN
# ============================================================
ARCHIVO_MISIONES  = "misiones.txt"
LOG_EVOLUCION     = "registro_noche.txt"
TIMEOUT_PATCHER   = 180   # Segundos máximos por misión (3 min)
PAUSA_ENTRE_PARCHES = 5   # Segundos entre misiones para no saturar Groq

# ============================================================
# LOGGING
# ============================================================
def registrar_log(mensaje):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    linea = f"[{timestamp}] [AUTO_RUN] {mensaje}"
    with open(LOG_EVOLUCION, "a", encoding="utf-8") as f:
        f.write(linea + "\n")
    print(linea)

# ============================================================
# LECTURA Y LIMPIEZA DE MISIONES
# ============================================================
def _lock_file(f):
    if _WINDOWS:
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
    else:
        fcntl.flock(f, fcntl.LOCK_EX)

def _unlock_file(f):
    if _WINDOWS:
        try:
            f.seek(0)
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except Exception:
            pass
    else:
        fcntl.flock(f, fcntl.LOCK_UN)

def leer_misiones():
    """
    Lee misiones.txt con file locking, elimina duplicados preservando orden.
    Retorna lista de líneas únicas válidas.
    """
    if not os.path.exists(ARCHIVO_MISIONES):
        registrar_log(f"[WARN] {ARCHIVO_MISIONES} no existe. Nada que procesar.")
        return []
    try:
        with open(ARCHIVO_MISIONES, "r+", encoding="utf-8", errors="replace") as f:
            _lock_file(f)
            try:
                todas = [l.strip() for l in f if l.strip()]
                unicas = list(dict.fromkeys(todas))
                duplicados = len(todas) - len(unicas)
                if duplicados > 0:
                    registrar_log(f"[INFO] Deduplicando: {len(todas):,} lineas -> {len(unicas)} unicas ({duplicados:,} duplicados eliminados)")
                    f.seek(0)
                    f.truncate()
                    f.write("\n".join(unicas) + "\n" if unicas else "")
            finally:
                _unlock_file(f)
        return unicas
    except Exception as e:
        registrar_log(f"[ERROR] Error leyendo {ARCHIVO_MISIONES}: {e}")
        return []

def limpiar_misiones_procesadas():
    """Vacia misiones.txt con file locking tras procesar todas."""
    try:
        with open(ARCHIVO_MISIONES, "r+", encoding="utf-8") as f:
            _lock_file(f)
            try:
                f.seek(0)
                f.truncate()
            finally:
                _unlock_file(f)
        registrar_log("[INFO] misiones.txt vaciado — listo para nuevas misiones.")
    except Exception as e:
        registrar_log(f"[WARN] No se pudo vaciar {ARCHIVO_MISIONES}: {e}")

# ============================================================
# PARSEO DE MISIÓN
# ============================================================
def parsear_mision(linea):
    """
    Parsea una línea del formato: archivo.py;instrucción detallada
    Retorna (archivo, instruccion) o (None, None) si el formato es inválido.
    """
    if ";" not in linea:
        registrar_log(f"[WARN] Misión con formato inválido (falta ';'): {linea[:80]}")
        return None, None

    partes = linea.split(";", 1)
    archivo = partes[0].strip()
    instruccion = partes[1].strip()

    if not archivo.endswith(".py"):
        registrar_log(f"[WARN] El objetivo no es un archivo .py: {archivo}")
        return None, None

    if not instruccion:
        registrar_log(f"[WARN] Instrucción vacía para {archivo}. Saltando.")
        return None, None

    return archivo, instruccion

# ============================================================
# EJECUCIÓN DE MISIÓN VÍA SUBPROCESO
# ============================================================
def ejecutar_mision(archivo, instruccion):
    """
    Llama a patcher_pro.py como subproceso independiente.
    Retorna True si tuvo éxito, False si falló.
    """
    if not os.path.exists("patcher_pro.py"):
        registrar_log("[ERROR] patcher_pro.py no encontrado. No se puede parchear.")
        return False

    registrar_log(f"[FIX] Parcheando: {archivo}")
    registrar_log(f"   Instrucción: {instruccion[:100]}...")

    try:
        resultado = subprocess.run(
            [sys.executable, "patcher_pro.py", archivo, instruccion],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=TIMEOUT_PATCHER
        )

        if resultado.returncode == 0:
            registrar_log(f"[OK] Parche aplicado exitosamente en {archivo}")
            if resultado.stdout.strip():
                registrar_log(f"   Output: {resultado.stdout.strip()[:200]}")
            return True
        else:
            registrar_log(f"[ERROR] Patcher falló en {archivo} (código {resultado.returncode})")
            if resultado.stderr.strip():
                registrar_log(f"   Error: {resultado.stderr.strip()[:200]}")
            return False

    except subprocess.TimeoutExpired:
        registrar_log(f"?? Timeout: {archivo} superó {TIMEOUT_PATCHER}s. Se canceló.")
        return False
    except Exception as e:
        registrar_log(f"[ERROR] Excepción ejecutando patcher en {archivo}: {e}")
        return False

# ============================================================
# MOTOR PRINCIPAL (UNA SOLA PASADA, SIN BUCLE INFINITO)
# ============================================================
def ejecutar_plan_maestro():
    """
    Procesa TODAS las misiones pendientes de una sola pasada y termina.
    El bucle infinito lo maneja noche_total.py.
    """
    registrar_log("[RUN] AUTO_RUN iniciado — procesando misiones pendientes...")

    misiones = leer_misiones()

    if not misiones:
        registrar_log("? No hay misiones pendientes. Auto_run termina.")
        return

    registrar_log(f"[LISTA] {len(misiones)} misiones encontradas. Procesando...")

    exitosas  = 0
    fallidas  = 0
    saltadas  = 0

    for i, linea in enumerate(misiones, 1):
        registrar_log(f"\n--- MISIÓN {i}/{len(misiones)} ---")

        archivo, instruccion = parsear_mision(linea)

        if archivo is None:
            saltadas += 1
            continue

        exito = ejecutar_mision(archivo, instruccion)

        if exito:
            exitosas += 1
        else:
            fallidas += 1

        # Pausa entre misiones para no saturar la API de Groq
        if i < len(misiones):
            registrar_log(f"? Pausa de {PAUSA_ENTRE_PARCHES}s antes de la siguiente misión...")
            time.sleep(PAUSA_ENTRE_PARCHES)

    # -- REPORTE FINAL -------------------------------------------------
    registrar_log(f"\n{'='*50}")
    registrar_log(f"[STATS] REPORTE AUTO_RUN:")
    registrar_log(f"   [OK] Exitosas:  {exitosas}")
    registrar_log(f"   [ERROR] Fallidas:  {fallidas}")
    registrar_log(f"   ??  Saltadas:  {saltadas}")
    registrar_log(f"   Total:       {len(misiones)}")
    registrar_log(f"{'='*50}")
    registrar_log("[OK] AUTO_RUN completado. Control devuelto a noche_total.py")

    # Limpiar misiones procesadas para no repetirlas en el próximo ciclo
    limpiar_misiones_procesadas()

# ============================================================
# PUNTO DE ENTRADA
# ============================================================
if __name__ == "__main__":
    ejecutar_plan_maestro()