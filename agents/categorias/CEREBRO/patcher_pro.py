"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Cirujano de código de la agencia. Recibe un archivo .py y una misión,
             hace backup, llama a Groq para generar el código mejorado y lo escribe.
             Acepta argumentos por sys.argv para ser llamado como subproceso.
TECNOLOGÍA: Groq (Nube), Python estándar
"""


from llm_router import completar

def _groq_compat_create(**kwargs):
    """Compatibilidad con llamadas antiguas a client.chat.completions.create"""
    messages = kwargs.get('messages', [])
    temperatura = kwargs.get('temperature', 0.5)
    max_tokens = kwargs.get('max_tokens', 1000)

    class _Resp:
        class _Choice:
            class _Msg:
                content = ""
            message = _Msg()
        choices = [_Choice()]

    resultado = completar(messages, temperatura=temperatura, max_tokens=max_tokens)
    resp = _Resp()
    resp.choices[0].message.content = resultado or ""
    return resp

import os
import sys
import time
import shutil
from pathlib import Path
from datetime import datetime
import io as _io

try:
    import web_bridge as web
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
API_KEY_GROQ   = os.environ.get("GROQ_API_KEY", "")  # leer del .env, nunca hardcodear
MODELO_GROQ    = "llama-3.3-70b-versatile"
LOG_EVOLUCION  = "registro_noche.txt"
MAX_REINTENTOS = 3
PAUSA_REINTENTO = 5   # Segundos entre reintentos por rate limit

# ============================================================
# LOGGING
# ============================================================
def registrar_log(mensaje):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    linea = f"[{timestamp}] [PATCHER] {mensaje}"
    with open(LOG_EVOLUCION, "a", encoding="utf-8") as f:
        f.write(linea + "\n")
    print(linea)

# ============================================================
# BACKUP
# ============================================================
def crear_backup(ruta):
    """Crea copia de seguridad con timestamp antes de cualquier modificación."""
    p = Path(ruta)
    if p.exists():
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = p.with_suffix(f".bak.{ts}")
        shutil.copy2(p, backup)
        registrar_log(f"[BACKUP] Backup creado: {backup.name}")
        return str(backup)
    return None

# ============================================================
# LIMPIEZA DE CÓDIGO GENERADO
# ============================================================
def limpiar_codigo(texto):
    """
    Extrae el código Python limpio de la respuesta de Groq.
    Elimina bloques markdown y texto explicativo.
    """
    if not texto:
        return ""

    # Extraer de bloque