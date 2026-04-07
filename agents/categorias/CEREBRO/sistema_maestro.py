"""
ÁREA: CEREBRO
DESCRIPCIÓN: Sistema Maestro v2.0 — Integrador total de la Agencia Santi.
             Arranca automáticamente al iniciar Windows. Gestiona en paralelo:
             fábrica de agentes, modo noche, monitor de salud, limpieza de logs,
             y consola central de control. Un solo proceso que hace funcionar todo.
             v2.0: watchdog, persistencia, throttle, shutdown limpio, file locking.
TECNOLOGÍA: Python estándar, threading, subprocess
"""

import os
import sys
import json
import time
import signal
import threading
import subprocess
import shutil
import re
from datetime import datetime

# File locking nativo de Windows (sin pip)
try:
    import msvcrt
    _WINDOWS = True
except ImportError:
    import fcntl
    _WINDOWS = False

# Fix Unicode para Windows (cp1252) — necesario para imprimir caracteres de caja ╔═╗║╚╝
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stdout, "buffer"):
    sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stderr, "buffer"):
    sys.stderr = open(sys.stderr.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)

# ─────────────────────────────────────────────
#  CONFIGURACIÓN
# ─────────────────────────────────────────────

BASE_DIR         = os.path.dirname(os.path.abspath(__file__))
LOG              = os.path.join(BASE_DIR, "registro_noche.txt")
HABILIDADES      = os.path.join(BASE_DIR, "habilidades.json")
HABILIDADES_BAK  = os.path.join(BASE_DIR, "habilidades.json.bak")
BUS              = os.path.join(BASE_DIR, "bus_mensajes.json")
MISIONES         = os.path.join(BASE_DIR, "misiones.txt")
MISIONES_LOCK    = os.path.join(BASE_DIR, "misiones.txt.lock")
RUNS_DIR         = os.path.join(BASE_DIR, "runs")
PROYECTOS_QUEUE  = os.path.join(BASE_DIR, "proyectos_queue")
PROYECTOS_DONE   = os.path.join(BASE_DIR, "proyectos_queue", "procesados")
ESTADO_FILE      = os.path.join(BASE_DIR, "estado_maestro.json")
MAX_LOG_MB       = 5       # Limpiar log si supera este tamaño
CICLO_MONITOR    = 60      # Segundos entre chequeos de salud
CICLO_LIMPIEZA   = 300     # Segundos entre limpiezas automáticas
CICLO_PROYECTOS  = 30      # Segundos entre chequeos de proyectos_queue
TIMEOUT_PROCESO  = 180     # Timeout para scripts cortos
TIMEOUT_NOCHE    = 1800    # 30 min para ciclo noche antes de kill
TIMEOUT_FABRICA  = 900     # 15 min para lote fabrica antes de kill
TIMEOUT_MISIONES = 1800    # 30 min para auto_run (200+ misiones)
HEARTBEAT_MAX    = 300     # 5 min sin heartbeat = hilo muerto
DISCO_WARN_GB    = 2       # Alerta si disco libre < 2GB
DISCO_CRITICO_GB = 0.5     # Pausar fabrica si disco libre < 500MB

os.makedirs(RUNS_DIR, exist_ok=True)
os.makedirs(PROYECTOS_QUEUE, exist_ok=True)
os.makedirs(PROYECTOS_DONE, exist_ok=True)

# ─────────────────────────────────────────────
#  ESTADO GLOBAL + SHUTDOWN + HEARTBEATS
# ─────────────────────────────────────────────

SHUTDOWN = threading.Event()  # Flag global de apagado limpio

_ESTADO_DEFAULTS = {
    "inicio":           datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "fabrica_activa":   False,
    "noche_activa":     False,
    "proyectos_activo": False,
    "lotes_generados":  0,
    "agentes_total":    0,
    "agentes_con_web":  0,
    "ciclos_noche":     0,
    "errores":          0,
    "errores_consecutivos_fabrica": 0,
    "ultimo_ciclo":     "—",
    "ultimo_agente":    "—",
    "log_size_mb":      0,
    "misiones_pendientes": 0,
    "proyectos_creados": 0,
    "ultimo_proyecto":  "—",
    "disco_libre_gb":   0,
    "ultimo_guardado":  "—",
}

estado = dict(_ESTADO_DEFAULTS)

# Heartbeats: cada hilo actualiza su timestamp al inicio de cada ciclo
heartbeats = {}
heartbeats_lock = threading.Lock()

# Subprocesos activos: para shutdown limpio
subprocesos_activos = []
subprocesos_lock = threading.Lock()

log_lock = threading.Lock()

# ─────────────────────────────────────────────
#  PERSISTENCIA DE ESTADO
# ─────────────────────────────────────────────

def guardar_estado():
    """Guarda estado a disco (escritura atómica)."""
    estado["ultimo_guardado"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        tmp = ESTADO_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(estado, f, indent=2, ensure_ascii=False)
        os.replace(tmp, ESTADO_FILE)
    except Exception:
        pass

def cargar_estado():
    """Carga estado desde disco, merge con defaults para campos nuevos."""
    if not os.path.exists(ESTADO_FILE):
        return
    try:
        with open(ESTADO_FILE, "r", encoding="utf-8", errors="replace") as f:
            guardado = json.load(f)
        # Solo restaurar contadores acumulativos (no flags de sesion)
        for clave in ("lotes_generados", "ciclos_noche", "errores",
                       "proyectos_creados", "agentes_total", "agentes_con_web"):
            if clave in guardado:
                estado[clave] = guardado[clave]
        log(f"Estado restaurado: {estado['lotes_generados']} lotes, {estado['ciclos_noche']} ciclos noche, {estado['errores']} errores", "OK")
    except Exception as e:
        log(f"No se pudo restaurar estado: {e}", "WARN")

# ─────────────────────────────────────────────
#  LOGGING
# ─────────────────────────────────────────────

def log(msg, nivel="INFO"):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    iconos = {"INFO": "ℹ", "OK": "✅", "WARN": "⚠", "ERROR": "❌", "MASTER": "🏭"}
    icono = iconos.get(nivel, "ℹ")
    linea = f"[{ts}] [{nivel}] {icono} [MAESTRO] {msg}"
    with log_lock:
        try:
            print(linea)
        except Exception:
            pass
        try:
            with open(LOG, "a", encoding="utf-8") as f:
                f.write(linea + "\n")
        except Exception:
            pass

# ─────────────────────────────────────────────
#  FILE LOCKING PARA MISIONES.TXT
# ─────────────────────────────────────────────

def _lock_file(f):
    """Lock exclusivo sobre un archivo abierto."""
    if _WINDOWS:
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
    else:
        fcntl.flock(f, fcntl.LOCK_EX)

def _unlock_file(f):
    """Unlock de un archivo abierto."""
    if _WINDOWS:
        try:
            f.seek(0)
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except Exception:
            pass
    else:
        fcntl.flock(f, fcntl.LOCK_UN)

def leer_misiones_seguro():
    """Lee misiones.txt con file locking."""
    if not os.path.exists(MISIONES):
        return []
    try:
        with open(MISIONES, "r+", encoding="utf-8", errors="replace") as f:
            _lock_file(f)
            try:
                lineas = [l.strip() for l in f if l.strip()]
            finally:
                _unlock_file(f)
        return lineas
    except Exception:
        return []

# ─────────────────────────────────────────────
#  EJECUTOR SEGURO DE SCRIPTS
# ─────────────────────────────────────────────

def ejecutar(script, args=None, timeout=TIMEOUT_PROCESO):
    ruta = os.path.join(BASE_DIR, script)
    if not os.path.exists(ruta):
        return False, f"{script} no encontrado"
    cmd = [sys.executable, ruta] + (args or [])
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            timeout=timeout, cwd=BASE_DIR
        )
        return r.returncode == 0, (r.stdout or r.stderr or "")[:300]
    except subprocess.TimeoutExpired as e:
        # Matar proceso zombie que excedio timeout
        if hasattr(e, 'cmd'):
            try:
                import psutil
                for p in psutil.process_iter():
                    if p.cmdline() == cmd:
                        p.kill()
            except Exception:
                pass  # psutil no disponible, subprocess.run ya maneja kill
        return False, f"Timeout {timeout}s — proceso terminado"
    except Exception as e:
        return False, str(e)

# ─────────────────────────────────────────────
#  VALIDACIÓN Y LECTURA DE HABILIDADES
# ─────────────────────────────────────────────

def contar_agentes():
    try:
        with open(HABILIDADES, "r", encoding="utf-8", errors="replace") as f:
            h = json.load(f)
        return len(h), sum(1 for v in h.values() if v.get("salud") == "OK")
    except (json.JSONDecodeError, ValueError):
        # JSON corrupto — intentar restaurar desde backup
        if os.path.exists(HABILIDADES_BAK):
            try:
                shutil.copy2(HABILIDADES_BAK, HABILIDADES)
                log("habilidades.json corrupto — restaurado desde backup", "WARN")
                with open(HABILIDADES, "r", encoding="utf-8", errors="replace") as f:
                    h = json.load(f)
                return len(h), sum(1 for v in h.values() if v.get("salud") == "OK")
            except Exception:
                pass
        log("habilidades.json corrupto y sin backup valido", "ERROR")
        return 0, 0
    except Exception:
        return 0, 0

def validar_habilidades():
    """Valida habilidades.json al arranque: JSON valido + archivos existen."""
    try:
        with open(HABILIDADES, "r", encoding="utf-8", errors="replace") as f:
            h = json.load(f)
    except (json.JSONDecodeError, ValueError):
        # Intentar restaurar
        if os.path.exists(HABILIDADES_BAK):
            try:
                shutil.copy2(HABILIDADES_BAK, HABILIDADES)
                log("habilidades.json corrupto al arranque — restaurado desde .bak", "WARN")
                with open(HABILIDADES, "r", encoding="utf-8", errors="replace") as f:
                    h = json.load(f)
            except Exception:
                log("habilidades.json irrecuperable", "ERROR")
                return
        else:
            log("habilidades.json corrupto y sin backup", "ERROR")
            return
    except FileNotFoundError:
        log("habilidades.json no existe aun", "WARN")
        return

    # Verificar que los archivos .py referenciados existen
    faltantes = [k for k in h if not os.path.exists(os.path.join(BASE_DIR, k))]
    if faltantes:
        log(f"{len(faltantes)} agentes registrados pero sin archivo .py", "WARN")

    # Crear backup si todo esta bien
    try:
        shutil.copy2(HABILIDADES, HABILIDADES_BAK)
    except Exception:
        pass

    log(f"habilidades.json validado: {len(h)} agentes, {len(faltantes)} sin archivo", "OK")

def contar_agentes_con_web():
    """Cuenta agentes que importan web_bridge (tienen acceso a internet)."""
    count = 0
    try:
        for f in os.listdir(BASE_DIR):
            if f.endswith(".py") and not f.startswith("__"):
                ruta = os.path.join(BASE_DIR, f)
                try:
                    with open(ruta, "r", encoding="utf-8", errors="replace") as fh:
                        contenido = fh.read(2000)  # Solo primeros 2KB
                    if "import web_bridge" in contenido or "from web_bridge" in contenido:
                        count += 1
                except Exception:
                    pass
    except Exception:
        pass
    return count

def contar_misiones():
    try:
        with open(MISIONES, "r", encoding="utf-8", errors="replace") as f:
            lineas = [l for l in f.readlines() if l.strip()]
        return len(lineas)
    except Exception:
        return 0

# ─────────────────────────────────────────────
#  MONITOREO DE DISCO
# ─────────────────────────────────────────────

def verificar_disco():
    """Verifica espacio libre en disco. Retorna GB libres."""
    try:
        uso = shutil.disk_usage(BASE_DIR)
        libre_gb = round(uso.free / (1024**3), 2)
        estado["disco_libre_gb"] = libre_gb
        return libre_gb
    except Exception:
        return 999  # Asumir OK si no se puede checar

# ─────────────────────────────────────────────
#  HEARTBEAT DE HILOS
# ─────────────────────────────────────────────

def heartbeat(nombre):
    """Registra que un hilo sigue vivo."""
    with heartbeats_lock:
        heartbeats[nombre] = time.time()

def verificar_heartbeats():
    """
    Verifica que todos los hilos reportaron recientemente.
    Si TODOS los hilos tienen heartbeat muy viejo (>30min), asume sleep/wake del equipo
    y resetea los timestamps en lugar de spamear alertas falsas.
    """
    ahora = time.time()
    SLEEP_THRESHOLD = 1800  # 30 min: si todos duermen tanto, fue sleep del equipo

    with heartbeats_lock:
        if not heartbeats:
            return []

        edades = {nombre: ahora - ts for nombre, ts in heartbeats.items()}
        todos_viejos = all(e > SLEEP_THRESHOLD for e in edades.values())

        if todos_viejos and len(heartbeats) >= 2:
            # Sistema durmio — resetear todos los heartbeats a ahora
            log("Sleep/wake detectado — reseteando heartbeats de todos los hilos", "WARN")
            for nombre in heartbeats:
                heartbeats[nombre] = ahora
            return []  # No reportar muertos falsos

        muertos = []
        for nombre, edad in edades.items():
            if edad > HEARTBEAT_MAX:
                muertos.append((nombre, int(edad)))
    return muertos

# ─────────────────────────────────────────────
#  LECTOR DE STDOUT NO-BLOQUEANTE
# ─────────────────────────────────────────────

def lector_stdout(proc, nombre, callback):
    """
    Hilo daemon que lee stdout de un subproceso línea por línea.
    Llama callback(linea) para cada línea. Termina cuando el pipe se cierra.
    """
    try:
        for linea in proc.stdout:
            linea = linea.strip()
            if linea:
                callback(linea)
    except Exception:
        pass

# ─────────────────────────────────────────────
#  REGISTRO DE SUBPROCESOS ACTIVOS
# ─────────────────────────────────────────────

def registrar_subproceso(proc):
    with subprocesos_lock:
        subprocesos_activos.append(proc)

def desregistrar_subproceso(proc):
    with subprocesos_lock:
        if proc in subprocesos_activos:
            subprocesos_activos.remove(proc)

def matar_subproceso(proc, nombre=""):
    """Intenta terminar limpiamente, luego force-kill."""
    try:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=3)
        if nombre:
            log(f"Subproceso {nombre} terminado", "INFO")
    except Exception:
        pass
    finally:
        desregistrar_subproceso(proc)

# ─────────────────────────────────────────────
#  LIMPIADOR AUTOMÁTICO
# ─────────────────────────────────────────────

def limpiar_sistema():
    """Limpia logs pesados, backups viejos y archivos temporales."""
    log("Iniciando limpieza automática...")

    # Limpiar log si supera MAX_LOG_MB
    if os.path.exists(LOG):
        size_mb = os.path.getsize(LOG) / (1024 * 1024)
        estado["log_size_mb"] = round(size_mb, 2)
        if size_mb > MAX_LOG_MB:
            try:
                with open(LOG, "r", encoding="utf-8", errors="replace") as f:
                    lineas = f.readlines()
                ultimas = lineas[-500:]
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                archivo_hist = os.path.join(RUNS_DIR, f"log_historico_{ts}.txt")
                with open(archivo_hist, "w", encoding="utf-8") as f:
                    f.writelines(lineas[:-500])
                with open(LOG, "w", encoding="utf-8") as f:
                    f.writelines(ultimas)
                log(f"Log archivado ({size_mb:.1f}MB -> 500 lineas activas)", "OK")
            except Exception as e:
                log(f"Error limpiando log: {e}", "WARN")

    # Mover .bak antiguos (más de 3 días) a runs/historico
    historico = os.path.join(RUNS_DIR, "historico")
    os.makedirs(historico, exist_ok=True)
    ahora = time.time()
    movidos = 0
    for f in os.listdir(BASE_DIR):
        es_bak = f.endswith(".bak") or ".bak.mejora_" in f or ".bak." in f
        if es_bak and not f.startswith(".") and f != "habilidades.json.bak":
            ruta = os.path.join(BASE_DIR, f)
            edad = (ahora - os.path.getmtime(ruta)) / 86400
            if edad > 3:
                try:
                    shutil.move(ruta, os.path.join(historico, f))
                    movidos += 1
                except Exception:
                    pass
    if movidos:
        log(f"{movidos} archivos .bak archivados", "OK")

    # Limpiar bus_mensajes.json si supera 500KB
    if os.path.exists(BUS):
        size_bus = os.path.getsize(BUS) / 1024
        if size_bus > 500:
            try:
                with open(BUS, "r", encoding="utf-8", errors="replace") as f:
                    bus_data = json.load(f)
                if isinstance(bus_data, list) and len(bus_data) > 50:
                    bus_data = bus_data[-50:]
                    with open(BUS, "w", encoding="utf-8") as f:
                        json.dump(bus_data, f, indent=2, ensure_ascii=False)
                    log(f"Bus limpiado ({size_bus:.0f}KB -> 50 mensajes)", "OK")
            except Exception:
                pass

    # Limpiar carpeta lote_nuevo si quedó con archivos
    lote_dir = os.path.join(BASE_DIR, "lote_nuevo")
    if os.path.exists(lote_dir):
        for f in os.listdir(lote_dir):
            try:
                os.remove(os.path.join(lote_dir, f))
            except Exception:
                pass

    # Limpiar archivos historicos de log >7 dias en runs/historico
    if os.path.exists(historico):
        for f in os.listdir(historico):
            ruta = os.path.join(historico, f)
            edad = (ahora - os.path.getmtime(ruta)) / 86400
            if edad > 7:
                try:
                    os.remove(ruta)
                except Exception:
                    pass

    log("Limpieza completada", "OK")


def hilo_limpieza():
    """Hilo que limpia el sistema cada CICLO_LIMPIEZA segundos."""
    while not SHUTDOWN.is_set():
        try:
            SHUTDOWN.wait(CICLO_LIMPIEZA)
            if SHUTDOWN.is_set():
                break
            heartbeat("Limpieza")
            limpiar_sistema()
        except Exception as e:
            log(f"Error en limpieza: {e}", "WARN")

# ─────────────────────────────────────────────
#  MONITOR DE SALUD + WATCHDOG + DISCO
# ─────────────────────────────────────────────

def hilo_monitor():
    """Monitorea estado del sistema, heartbeats de hilos, y disco."""
    while not SHUTDOWN.is_set():
        try:
            heartbeat("Monitor")

            total, ok = contar_agentes()
            misiones = contar_misiones()
            estado["agentes_total"]      = total
            estado["misiones_pendientes"] = misiones
            estado["agentes_con_web"]    = contar_agentes_con_web()

            if os.path.exists(LOG):
                estado["log_size_mb"] = round(os.path.getsize(LOG) / (1024*1024), 2)

            # Alerta si hay agentes con problemas
            if total > 0 and ok < total * 0.8:
                log(f"Solo {ok}/{total} agentes saludables", "WARN")

            # Verificar disco
            libre_gb = verificar_disco()
            if libre_gb < DISCO_CRITICO_GB:
                log(f"DISCO CRITICO: {libre_gb}GB libre — pausando fabrica", "ERROR")
                limpiar_sistema()  # Limpieza agresiva
            elif libre_gb < DISCO_WARN_GB:
                log(f"Disco bajo: {libre_gb}GB libre", "WARN")

            # WATCHDOG: verificar heartbeats de hilos
            muertos = verificar_heartbeats()
            for nombre, edad_seg in muertos:
                log(f"ALERTA: hilo '{nombre}' sin heartbeat hace {edad_seg//60}min", "ERROR")
                estado["errores"] += 1

            # Persistir estado cada ciclo
            guardar_estado()

            SHUTDOWN.wait(CICLO_MONITOR)
        except Exception as e:
            log(f"Error monitor: {e}", "WARN")
            SHUTDOWN.wait(CICLO_MONITOR)

# ─────────────────────────────────────────────
#  HILO: MODO NOCHE
# ─────────────────────────────────────────────

def hilo_noche():
    """
    Corre noche_total.py como subproceso persistente.
    Usa hilo lector + timeout para evitar bloqueos.
    """
    estado["noche_activa"] = True
    log("Modo Noche activado como proceso persistente", "OK")

    while not SHUTDOWN.is_set():
        heartbeat("Noche")
        try:
            ruta = os.path.join(BASE_DIR, "noche_total.py")
            if not os.path.exists(ruta):
                log("noche_total.py no encontrado, esperando 60s...", "WARN")
                SHUTDOWN.wait(60)
                continue

            estado["ultimo_ciclo"] = datetime.now().strftime('%H:%M:%S')
            proc = subprocess.Popen(
                [sys.executable, ruta],
                cwd=BASE_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace"
            )
            registrar_subproceso(proc)

            # Callback para el lector de stdout
            def procesar_linea_noche(linea):
                heartbeat("Noche")  # Output = sigue vivo
                if any(k in linea for k in ["CICLO", "completado", "ERROR"]):
                    if "completado" in linea.lower():
                        estado["ciclos_noche"] += 1
                    with log_lock:
                        try:
                            with open(LOG, "a", encoding="utf-8") as f:
                                f.write("[NOCHE] " + linea + "\n")
                        except Exception:
                            pass

            # Lanzar hilo lector de stdout (no bloqueante)
            t = threading.Thread(target=lector_stdout, args=(proc, "Noche", procesar_linea_noche), daemon=True)
            t.start()

            # Esperar con POLL LOOP de 30s — heartbeat aunque noche esté mudo (LLM lento)
            inicio_noche = time.time()
            terminado_ok = False
            while not SHUTDOWN.is_set():
                try:
                    proc.wait(timeout=30)
                    terminado_ok = True
                    break
                except subprocess.TimeoutExpired:
                    heartbeat("Noche")  # Sigo vivo aunque noche_total no produzca output
                    if time.time() - inicio_noche > TIMEOUT_NOCHE:
                        log(f"noche_total.py excedio timeout de {TIMEOUT_NOCHE}s — matando", "ERROR")
                        matar_subproceso(proc, "noche_total")
                        estado["errores"] += 1
                        break

            if terminado_ok:
                desregistrar_subproceso(proc)
                rc = proc.returncode
                if rc != 0:
                    log(f"noche_total.py termino con codigo {rc}", "WARN")

            log("noche_total.py termino, reiniciando en 30s...", "WARN")
            SHUTDOWN.wait(30)

        except Exception as e:
            log(f"Error en noche: {e}", "ERROR")
            estado["errores"] += 1
            SHUTDOWN.wait(30)

# ─────────────────────────────────────────────
#  HILO: FÁBRICA DE AGENTES (con throttle)
# ─────────────────────────────────────────────

def auto_ajustar_modo_fabrica():
    """
    Scheduler: ajusta el modo de la fabrica segun metricas actuales.
    - Si hay 500+ agentes y modo=CREAR -> cambia a MEJORAR
    - Si es horario nocturno (22-07h) y no hay errores -> sugiere NOCHE
    - Si errores_consecutivos >= 5 -> cambia a BALANCEADO para estabilizarse
    """
    fabrica_mode_file = os.path.join(BASE_DIR, ".fabricamode")
    fabrica_config_file = os.path.join(BASE_DIR, "fabrica_config.py")

    try:
        modo_actual = ""
        if os.path.exists(fabrica_mode_file):
            with open(fabrica_mode_file, "r") as f:
                modo_actual = f.read().strip().upper()

        total, _ = contar_agentes()
        errores = estado.get("errores_consecutivos_fabrica", 0)
        hora = datetime.now().hour

        cambio = None

        if modo_actual == "CREAR" and total >= 500:
            cambio = "MEJORAR"
            log(f"Auto-scheduler: {total} agentes alcanzados -> modo MEJORAR", "OK")

        elif errores >= 5 and modo_actual not in ("BALANCEADO", "NOCHE"):
            cambio = "BALANCEADO"
            log(f"Auto-scheduler: {errores} errores consecutivos -> modo BALANCEADO", "WARN")

        elif modo_actual == "BALANCEADO" and errores == 0 and not (22 <= hora or hora < 7):
            cambio = "MEJORAR"
            log("Auto-scheduler: errores resueltos -> modo MEJORAR", "OK")

        if cambio:
            with open(fabrica_mode_file, "w") as f:
                f.write(cambio)
            # Actualizar tambien fabrica_config.py si existe
            if os.path.exists(fabrica_config_file):
                with open(fabrica_config_file, "r", encoding="utf-8") as f:
                    cfg = f.read()
                import re as _re
                cfg2 = _re.sub(r'MODO_USUARIO\s*=\s*["\'][^"\']+["\']',
                               f'MODO_USUARIO = "{cambio}"', cfg)
                if cfg2 != cfg:
                    with open(fabrica_config_file, "w", encoding="utf-8") as f:
                        f.write(cfg2)

    except Exception as e:
        log(f"Auto-scheduler error: {e}", "WARN")


def hilo_fabrica():
    """Corre fabrica_agentes.py con throttle adaptativo y timeout + auto-scheduler de modo."""
    estado["fabrica_activa"] = True
    log("Fabrica de agentes activada", "OK")

    while not SHUTDOWN.is_set():
        heartbeat("Fabrica")
        # Ajustar modo antes de cada ciclo
        auto_ajustar_modo_fabrica()
        try:
            # Verificar disco antes de crear agentes
            if estado.get("disco_libre_gb", 999) < DISCO_CRITICO_GB:
                log("Fabrica pausada: disco critico", "WARN")
                SHUTDOWN.wait(60)
                continue

            ruta = os.path.join(BASE_DIR, "fabrica_agentes.py")
            if not os.path.exists(ruta):
                log("fabrica_agentes.py no encontrado, esperando...", "WARN")
                SHUTDOWN.wait(60)
                continue

            proc = subprocess.Popen(
                [sys.executable, ruta],
                cwd=BASE_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace"
            )
            registrar_subproceso(proc)

            # Callback para el lector de stdout
            def procesar_linea_fabrica(linea):
                heartbeat("Fabrica")  # Output = sigue vivo
                if "FABRICA" in linea.upper() or "LOTE" in linea or "APROBADO" in linea:
                    if "APROBADO" in linea:
                        estado["lotes_generados"] += 1
                        match = re.search(r'(\w+\.py)', linea)
                        if match:
                            estado["ultimo_agente"] = match.group(1)
                    if any(k in linea.upper() for k in ["LOTE", "APROBADO", "ERROR", "COMPLETADO", "FABRICA"]):
                        with log_lock:
                            try:
                                with open(LOG, "a", encoding="utf-8") as f:
                                    f.write(linea + "\n")
                            except Exception:
                                pass

            # Lanzar hilo lector de stdout
            t = threading.Thread(target=lector_stdout, args=(proc, "Fabrica", procesar_linea_fabrica), daemon=True)
            t.start()

            # Esperar con timeout
            try:
                proc.wait(timeout=TIMEOUT_FABRICA)
            except subprocess.TimeoutExpired:
                log(f"fabrica_agentes.py excedio timeout de {TIMEOUT_FABRICA}s — matando", "ERROR")
                matar_subproceso(proc, "fabrica")
                estado["errores"] += 1
                estado["errores_consecutivos_fabrica"] += 1
            else:
                desregistrar_subproceso(proc)
                rc = proc.returncode
                if rc != 0:
                    estado["errores_consecutivos_fabrica"] += 1
                    log(f"Fabrica termino con codigo {rc}", "WARN")
                else:
                    estado["errores_consecutivos_fabrica"] = 0  # Exito, reset

            # THROTTLE ADAPTATIVO
            errores = estado["errores_consecutivos_fabrica"]
            if errores > 0:
                pausa = min(300, 10 * (2 ** min(errores, 5)))
                log(f"Fabrica: backoff {pausa}s tras {errores} errores consecutivos", "WARN")
                SHUTDOWN.wait(pausa)
            else:
                SHUTDOWN.wait(10)

        except Exception as e:
            log(f"Error en fabrica: {e}", "ERROR")
            estado["errores"] += 1
            estado["errores_consecutivos_fabrica"] += 1
            errores = estado["errores_consecutivos_fabrica"]
            pausa = min(300, 10 * (2 ** min(errores, 5)))
            SHUTDOWN.wait(pausa)

# ─────────────────────────────────────────────
#  HILO: EJECUTOR DE MISIONES
# ─────────────────────────────────────────────

def hilo_misiones():
    """Ejecuta misiones pendientes. Usa Popen + poll loop para mantener heartbeat activo."""
    SHUTDOWN.wait(60)  # Esperar que arranquen los otros hilos primero
    while not SHUTDOWN.is_set():
        try:
            heartbeat("Misiones")
            misiones = contar_misiones()
            if misiones > 0:
                log(f"Ejecutando {misiones} misiones (timeout 30min)...", "INFO")
                ruta_auto = os.path.join(BASE_DIR, "auto_run.py")
                if not os.path.exists(ruta_auto):
                    log("auto_run.py no encontrado", "WARN")
                    SHUTDOWN.wait(60)
                    continue

                # Popen (no bloqueante) + poll loop con heartbeat cada 30s
                proc_mis = subprocess.Popen(
                    [sys.executable, ruta_auto],
                    cwd=BASE_DIR,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                registrar_subproceso(proc_mis)
                inicio_mis = time.time()

                while not SHUTDOWN.is_set():
                    try:
                        proc_mis.wait(timeout=30)
                        break   # Terminó normalmente
                    except subprocess.TimeoutExpired:
                        heartbeat("Misiones")  # Sigo vivo durante la ejecución larga
                        if time.time() - inicio_mis > TIMEOUT_MISIONES:
                            log("auto_run.py excedio timeout — matando", "ERROR")
                            matar_subproceso(proc_mis, "auto_run")
                            estado["errores"] += 1
                            break

                desregistrar_subproceso(proc_mis)
                restantes = contar_misiones()
                log(f"Misiones OK. Restantes: {restantes}", "OK")
                estado["misiones_pendientes"] = restantes

            # Poll loop en lugar de bloqueo: heartbeat cada 50s durante los 10 min de espera
            for _ in range(12):  # 12 x 50s = 600s = 10 min
                if SHUTDOWN.is_set():
                    break
                heartbeat("Misiones")
                SHUTDOWN.wait(50)
        except Exception as e:
            log(f"Error misiones: {e}", "WARN")
            SHUTDOWN.wait(60)

# ─────────────────────────────────────────────
#  HILO: ORQUESTADOR DE PROYECTOS
# ─────────────────────────────────────────────

def hilo_proyectos():
    """Monitorea proyectos_queue/ y ejecuta orquestador_proyectos.py."""
    estado["proyectos_activo"] = True
    log("Orquestador de proyectos activado (monitorea proyectos_queue/)", "OK")

    while not SHUTDOWN.is_set():
        try:
            heartbeat("Proyectos")

            archivos_txt = []
            for f in os.listdir(PROYECTOS_QUEUE):
                if f.endswith(".txt") and os.path.isfile(os.path.join(PROYECTOS_QUEUE, f)):
                    archivos_txt.append(f)

            for archivo in archivos_txt:
                if SHUTDOWN.is_set():
                    break
                ruta = os.path.join(PROYECTOS_QUEUE, archivo)
                try:
                    with open(ruta, "r", encoding="utf-8", errors="replace") as fh:
                        descripcion = fh.read().strip()
                except Exception as e:
                    log(f"Error leyendo {archivo}: {e}", "WARN")
                    continue

                if not descripcion:
                    log(f"Archivo vacio: {archivo}, saltando", "WARN")
                    continue

                log(f"Nuevo proyecto detectado: {archivo}", "INFO")
                log(f"Descripcion: {descripcion[:100]}...", "INFO")

                exito, output = ejecutar(
                    "orquestador_proyectos.py",
                    args=[descripcion],
                    timeout=600
                )

                if exito:
                    estado["proyectos_creados"] += 1
                    estado["ultimo_proyecto"] = archivo.replace(".txt", "")
                    log(f"Proyecto '{archivo}' completado", "OK")
                else:
                    log(f"Proyecto '{archivo}' fallo: {output[:150]}", "ERROR")

                destino = os.path.join(PROYECTOS_DONE, archivo)
                try:
                    shutil.move(ruta, destino)
                except Exception as e:
                    log(f"Error moviendo {archivo}: {e}", "WARN")

            SHUTDOWN.wait(CICLO_PROYECTOS)

        except Exception as e:
            log(f"Error en hilo proyectos: {e}", "WARN")
            SHUTDOWN.wait(CICLO_PROYECTOS)

# ─────────────────────────────────────────────
#  HILO: WORKER DE COLA DE TAREAS
# ─────────────────────────────────────────────

def hilo_tareas():
    """Procesa tareas_pendientes.json enviadas desde el Dashboard."""
    SHUTDOWN.wait(30)  # Esperar que API y Dashboard arranquen
    TAREAS_FILE = os.path.join(BASE_DIR, "tareas_pendientes.json")
    PROYECTOS_DIR = os.path.join(BASE_DIR, "proyectos")
    log("Worker de tareas activado (monitorea tareas_pendientes.json)", "OK")

    while not SHUTDOWN.is_set():
        try:
            heartbeat("Tareas")

            if not os.path.exists(TAREAS_FILE):
                SHUTDOWN.wait(15)
                continue

            with open(TAREAS_FILE, "r", encoding="utf-8", errors="replace") as fh:
                tareas = json.load(fh)

            pendientes = [t for t in tareas if t.get("status") == "pendiente"]

            for tarea in pendientes:
                if SHUTDOWN.is_set():
                    break

                tid   = tarea.get("id")
                desc  = tarea.get("descripcion", "").strip()
                proy  = tarea.get("proyecto", "")
                if not desc:
                    continue

                log(f"Procesando tarea #{tid}: {desc[:80]}...", "INFO")

                resultado = ""
                nuevo_status = "completada"

                if proy:
                    orq_path = os.path.join(PROYECTOS_DIR, proy, "orquestador.py")
                    if os.path.exists(orq_path):
                        exito, output = ejecutar(
                            orq_path,
                            args=[desc],
                            timeout=180
                        )
                        resultado = output[:1000] if output else ("OK" if exito else "Sin output")
                        nuevo_status = "completada" if exito else "error"
                    else:
                        resultado = f"Orquestador de '{proy}' no encontrado"
                        nuevo_status = "error"
                else:
                    # Tarea general: usar llm_router si disponible
                    try:
                        from llm_router import completar_simple as ia
                        resultado = ia(f"Eres el sistema de Agencia Santi. El usuario solicita: {desc}\nResponde brevemente que hiciste.") or "Tarea procesada"
                    except Exception as e_ia:
                        resultado = f"Tarea registrada (sin LLM: {e_ia})"

                # Actualizar estado de la tarea en el archivo
                with open(TAREAS_FILE, "r", encoding="utf-8", errors="replace") as fh:
                    tareas_actuales = json.load(fh)
                for t in tareas_actuales:
                    if t.get("id") == tid:
                        t["status"]    = nuevo_status
                        t["resultado"] = resultado
                        break
                with open(TAREAS_FILE, "w", encoding="utf-8") as fh:
                    json.dump(tareas_actuales[-50:], fh, indent=2, ensure_ascii=False)

                log(f"Tarea #{tid} -> {nuevo_status}", "OK" if nuevo_status == "completada" else "WARN")

            SHUTDOWN.wait(10)

        except Exception as e:
            log(f"Error worker tareas: {e}", "WARN")
            SHUTDOWN.wait(30)

# ─────────────────────────────────────────────
#  HILO: API REST
# ─────────────────────────────────────────────

def hilo_api():
    """Arranca la API REST en puerto 8000."""
    log('API REST activada en puerto 8000', 'OK')
    while not SHUTDOWN.is_set():
        heartbeat("API")
        try:
            ruta = os.path.join(BASE_DIR, 'api_agencia.py')
            if not os.path.exists(ruta):
                log('api_agencia.py no encontrado, esperando...', 'WARN')
                SHUTDOWN.wait(30)
                continue
            proc = subprocess.Popen(
                [sys.executable, ruta],
                cwd=BASE_DIR,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            registrar_subproceso(proc)
            # Esperar a que termine o a SHUTDOWN
            while not SHUTDOWN.is_set():
                try:
                    proc.wait(timeout=5)
                    break  # Termino
                except subprocess.TimeoutExpired:
                    heartbeat("API")
                    continue  # Sigue corriendo
            desregistrar_subproceso(proc)
            if not SHUTDOWN.is_set():
                log('API REST termino, reiniciando en 5s...', 'WARN')
                SHUTDOWN.wait(5)
        except Exception as e:
            log(f'Error en API: {e}', 'ERROR')
            SHUTDOWN.wait(15)

# ─────────────────────────────────────────────
#  HILO: DASHBOARD WEB
# ─────────────────────────────────────────────

def hilo_dashboard():
    """Arranca el dashboard web en puerto 8080."""
    log('Dashboard web activado en puerto 8080', 'OK')
    while not SHUTDOWN.is_set():
        heartbeat("Dashboard")
        try:
            ruta = os.path.join(BASE_DIR, 'dashboard_web.py')
            if not os.path.exists(ruta):
                log('dashboard_web.py no encontrado, esperando...', 'WARN')
                SHUTDOWN.wait(30)
                continue
            proc = subprocess.Popen(
                [sys.executable, ruta],
                cwd=BASE_DIR,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            registrar_subproceso(proc)
            while not SHUTDOWN.is_set():
                try:
                    proc.wait(timeout=5)
                    break
                except subprocess.TimeoutExpired:
                    heartbeat("Dashboard")
                    continue
            desregistrar_subproceso(proc)
            if not SHUTDOWN.is_set():
                log('Dashboard termino, reiniciando en 5s...', 'WARN')
                SHUTDOWN.wait(5)
        except Exception as e:
            log(f'Error en dashboard: {e}', 'ERROR')
            SHUTDOWN.wait(15)

# ─────────────────────────────────────────────
#  CONSOLA CENTRAL
# ─────────────────────────────────────────────

def _uptime():
    """Calcula uptime desde el inicio."""
    try:
        inicio = datetime.strptime(estado['inicio'], '%Y-%m-%d %H:%M:%S')
        delta = datetime.now() - inicio
        horas = int(delta.total_seconds() // 3600)
        mins = int((delta.total_seconds() % 3600) // 60)
        return f"{horas}h {mins}m"
    except Exception:
        return "???"

def _heartbeat_status():
    """Genera lineas de status de heartbeats."""
    ahora = time.time()
    lineas = []
    with heartbeats_lock:
        for nombre in ["API", "Dashboard", "Fabrica", "Noche", "Monitor", "Limpieza", "Misiones", "Proyectos"]:
            ts = heartbeats.get(nombre, 0)
            if ts == 0:
                status = "--"
                edad = ""
            else:
                edad_seg = int(ahora - ts)
                if edad_seg < HEARTBEAT_MAX:
                    status = "OK"
                    if edad_seg < 60:
                        edad = f"({edad_seg}s)"
                    else:
                        edad = f"({edad_seg//60}m)"
                else:
                    status = "MUERTO"
                    edad = f"({edad_seg//60}m)"
            lineas.append((nombre, status, edad))
    return lineas

def mostrar_dashboard():
    total, ok = contar_agentes()
    web_count = contar_agentes_con_web()
    estado["agentes_con_web"] = web_count
    disco = estado.get("disco_libre_gb", "?")
    uptime = _uptime()
    errores_fab = estado.get("errores_consecutivos_fabrica", 0)
    throttle = ""
    if errores_fab > 0:
        pausa = min(300, 10 * (2 ** min(errores_fab, 5)))
        throttle = f" (backoff {pausa}s)"

    hb = _heartbeat_status()

    print(f"""
╔══════════════════════════════════════════════════════════╗
║         AGENCIA SANTI — SISTEMA MAESTRO v2.0             ║
╠══════════════════════════════════════════════════════════╣
║  Inicio:        {estado['inicio']:<20}  Uptime: {uptime:<10}  ║
║  Agentes total: {total:<5}  Saludables: {ok:<5}  Con internet: {web_count:<4}║
║  Ciclos noche:  {estado['ciclos_noche']:<5}  Errores: {estado['errores']:<5}  Disco: {disco}GB{'':<5}║
║  Lotes fabrica: {estado['lotes_generados']:<5}  Ultimo: {str(estado['ultimo_agente']):<20}  ║
║  Misiones:      {estado['misiones_pendientes']:<5}  Log: {estado['log_size_mb']:<5}MB{'':<22}║
║  Proyectos:     {estado['proyectos_creados']:<5}  Ultimo: {str(estado['ultimo_proyecto']):<20}  ║
║  Err fabrica:   {errores_fab:<5}{throttle:<38}  ║
╠══════════════════════════════════════════════════════════╣
║  HILOS (heartbeat):                                      ║""")
    for nombre, status, edad in hb:
        icono = "✅" if status == "OK" else ("❌" if status == "MUERTO" else "⏳")
        linea = f"  {icono} {nombre:<12} {status:<8} {edad}"
        print(f"║{linea:<57}║")
    print(f"""╠══════════════════════════════════════════════════════════╣
║  COMANDOS: status | agentes | limpiar | misiones | log   ║
║            proyecto <desc> | help | q                    ║
╚══════════════════════════════════════════════════════════╝""")

def consola_interactiva():
    """Consola central para controlar el sistema."""
    time.sleep(3)  # Esperar que arranquen los hilos
    mostrar_dashboard()

    while not SHUTDOWN.is_set():
        try:
            cmd = input("\n🏭 Maestro> ").strip()
            cmd_lower = cmd.lower()

            if cmd_lower in ("q", "quit", "exit", "salir"):
                log("Sistema maestro detenido manualmente.", "WARN")
                shutdown_limpio()
                return

            elif cmd_lower == "status":
                mostrar_dashboard()

            elif cmd_lower == "agentes":
                total, ok = contar_agentes()
                try:
                    with open(HABILIDADES, "r", encoding="utf-8", errors="replace") as f:
                        h = json.load(f)
                    areas = {}
                    for v in h.values():
                        area = v.get("categoria", "GENERAL")
                        areas[area] = areas.get(area, 0) + 1
                    print(f"\n📊 AGENTES POR AREA ({total} total, {ok} OK):")
                    for area, count in sorted(areas.items(), key=lambda x: -x[1]):
                        print(f"   {area:<25} {count}")
                except Exception as e:
                    print(f"Error: {e}")

            elif cmd_lower == "limpiar":
                limpiar_sistema()

            elif cmd_lower == "misiones":
                misiones = contar_misiones()
                print(f"\n📋 {misiones} misiones pendientes en misiones.txt")
                if misiones > 0:
                    exito, _ = ejecutar("auto_run.py", timeout=300)
                    print("✅ Ejecutadas" if exito else "❌ Error al ejecutar")

            elif cmd_lower == "log":
                if os.path.exists(LOG):
                    with open(LOG, "r", encoding="utf-8", errors="replace") as f:
                        lineas = f.readlines()
                    print(f"\n📄 Ultimas 20 lineas del log:")
                    for l in lineas[-20:]:
                        print(l.rstrip())

            elif cmd_lower.startswith("proyecto "):
                desc = cmd[len("proyecto "):].strip()
                if not desc:
                    print("Uso: proyecto <descripcion del negocio>")
                else:
                    slug = re.sub(r'[^a-z0-9]+', '_', desc.lower())[:40].strip('_')
                    archivo = os.path.join(PROYECTOS_QUEUE, f"{slug}.txt")
                    with open(archivo, "w", encoding="utf-8") as f:
                        f.write(desc)
                    print(f"✅ Proyecto creado: {slug}.txt")
                    print(f"   El hilo de proyectos lo detectara en los proximos {CICLO_PROYECTOS}s")

            elif cmd_lower in ("help", "?"):
                print("""
Comandos disponibles:
  status         — Ver dashboard completo con heartbeats
  agentes        — Ver agentes por area
  limpiar        — Limpiar logs y backups ahora
  misiones       — Ver y ejecutar misiones pendientes
  log            — Ver ultimas lineas del log
  proyecto <desc> — Crear proyecto desde descripcion
  q              — Detener el sistema (shutdown limpio)""")

            elif cmd_lower == "":
                continue

            else:
                print(f"Comando desconocido: '{cmd}'. Escribe 'help' para ver opciones.")

        except KeyboardInterrupt:
            log("Sistema maestro detenido con Ctrl+C.", "WARN")
            shutdown_limpio()
            return
        except EOFError:
            # Sin consola interactiva (modo daemon)
            SHUTDOWN.wait(60)
        except Exception as e:
            log(f"Error en consola: {e}", "WARN")

# ─────────────────────────────────────────────
#  SHUTDOWN LIMPIO
# ─────────────────────────────────────────────

def shutdown_limpio():
    """Apaga todo de forma ordenada: flag, matar subprocesos, guardar estado."""
    log("Iniciando shutdown limpio...", "MASTER")
    SHUTDOWN.set()

    # Matar todos los subprocesos activos
    with subprocesos_lock:
        procs = list(subprocesos_activos)
    for proc in procs:
        try:
            matar_subproceso(proc)
        except Exception:
            pass

    # Guardar estado final
    guardar_estado()
    log("Estado guardado. Shutdown completado.", "MASTER")

# ─────────────────────────────────────────────
#  REGISTRO EN TAREA DE WINDOWS (arranque automático)
# ─────────────────────────────────────────────

def registrar_tarea_windows():
    """Registra el sistema para arrancar automáticamente con Windows."""
    try:
        python_exe = sys.executable
        script     = os.path.abspath(__file__)
        nombre     = "AgenciaSanti_SistemaMaestro"

        cmd_check = f'schtasks /query /tn "{nombre}" 2>nul'
        existe = os.system(cmd_check) == 0

        if not existe:
            cmd_crear = (
                f'schtasks /create /tn "{nombre}" '
                f'/tr "\\"{python_exe}\\" \\"{script}\\" --daemon" '
                f'/sc onlogon /rl highest /f'
            )
            resultado = os.system(cmd_crear)
            if resultado == 0:
                log(f"Tarea '{nombre}' registrada — arrancara con Windows", "OK")
            else:
                log("No se pudo registrar tarea (ejecuta como administrador)", "WARN")
        else:
            log(f"Tarea '{nombre}' ya registrada en Windows", "INFO")

    except Exception as e:
        log(f"Error registrando tarea: {e}", "WARN")


# ─────────────────────────────────────────────
#  PUNTO DE ENTRADA
# ─────────────────────────────────────────────

def main():
    modo_daemon = "--daemon" in sys.argv

    # Manejar Ctrl+C limpiamente
    def signal_handler(sig, frame):
        log("Ctrl+C recibido", "WARN")
        shutdown_limpio()
        sys.exit(0)

    try:
        signal.signal(signal.SIGINT, signal_handler)
    except Exception:
        pass  # signal puede fallar en algunos contextos de Windows

    log("╔══════════════════════════════════════════════════════╗", "MASTER")
    log("║      AGENCIA SANTI — SISTEMA MAESTRO v2.0           ║", "MASTER")
    log("║      Iniciando todos los sistemas...                ║", "MASTER")
    log("╚══════════════════════════════════════════════════════╝", "MASTER")

    # Cargar estado persistido
    cargar_estado()

    # Validar habilidades.json
    validar_habilidades()

    # Verificar disco
    libre = verificar_disco()
    log(f"Disco libre: {libre}GB", "INFO")

    # Limpieza inicial
    limpiar_sistema()

    # Arrancar todos los hilos en paralelo
    hilos = [
        threading.Thread(target=hilo_api,       daemon=True, name="API"),
        threading.Thread(target=hilo_dashboard, daemon=True, name="Dashboard"),
        threading.Thread(target=hilo_fabrica,   daemon=True, name="Fabrica"),
        threading.Thread(target=hilo_noche,     daemon=True, name="Noche"),
        threading.Thread(target=hilo_monitor,   daemon=True, name="Monitor"),
        threading.Thread(target=hilo_limpieza,  daemon=True, name="Limpieza"),
        threading.Thread(target=hilo_misiones,  daemon=True, name="Misiones"),
        threading.Thread(target=hilo_proyectos, daemon=True, name="Proyectos"),
        threading.Thread(target=hilo_tareas,    daemon=True, name="Tareas"),
    ]

    for hilo in hilos:
        hilo.start()
        heartbeat(hilo.name)  # Heartbeat inicial
        log(f"Hilo '{hilo.name}' iniciado", "OK")
        time.sleep(1)

    log("Todos los sistemas activos. Agencia Santi operando.", "MASTER")

    # En modo daemon no hay consola interactiva
    if modo_daemon:
        log("Modo daemon — sin consola interactiva", "INFO")
        while not SHUTDOWN.is_set():
            SHUTDOWN.wait(300)
            if SHUTDOWN.is_set():
                break
            total, ok = contar_agentes()
            muertos = verificar_heartbeats()
            hilos_muertos = f" | HILOS MUERTOS: {', '.join(n for n,_ in muertos)}" if muertos else ""
            log(f"Heartbeat — Agentes: {total} | Ciclos noche: {estado['ciclos_noche']} | Lotes: {estado['lotes_generados']}{hilos_muertos}", "INFO")
    else:
        consola_interactiva()


if __name__ == "__main__":
    main()
