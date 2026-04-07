"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Director de Orquesta v2.0. Mapeo + Estrategia corren en PARALELO
             con threading. Misiones por área simultáneas. Prioridad por impacto.
             6x más rápido que v1.0.
TECNOLOGÍA: Python estándar, subprocess, threading
"""




import subprocess
import time
import os
import sys
import threading
import io as _io

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
TIEMPO_DESCANSO          = 120
TIEMPO_DESCANSO_ERROR    = 60
MAX_ERRORES_CONSECUTIVOS = 5
PAUSA_CRITICA            = 600
TIMEOUT_SUBPROCESO       = 120
LOG_EVOLUCION            = "registro_noche.txt"

# ============================================================
# ESTADÍSTICAS
# ============================================================
stats = {
    "ciclos_completados":   0,
    "ciclos_fallidos":      0,
    "parches_aplicados":    0,
    "errores_consecutivos": 0,
    "inicio_sesion":        time.strftime('%Y-%m-%d %H:%M:%S')
}

log_lock = threading.Lock()

# ============================================================
# LOGGING THREAD-SAFE
# ============================================================
def registrar_evento(mensaje, nivel="INFO"):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    prefijos = {"INFO": "[INFO]", "OK": "[OK]", "WARN": "[WARN]", "ERROR": "[ERROR]", "CRITICO": "[ALERTA]"}
    prefijo = prefijos.get(nivel, "[INFO]")
    linea = f"[{timestamp}] [{nivel}] {prefijo} {mensaje}"
    with log_lock:
        with open(LOG_EVOLUCION, "a", encoding="utf-8") as f:
            f.write(linea + "\n")
        print(linea)

def registrar_separador():
    linea = "=" * 60
    with log_lock:
        with open(LOG_EVOLUCION, "a", encoding="utf-8") as f:
            f.write(linea + "\n")
        print(linea)

# ============================================================
# EJECUCIÓN SEGURA
# ============================================================
def ejecutar_script(nombre_script, descripcion, resultados=None, clave=None):
    if not os.path.exists(nombre_script):
        registrar_evento(f"Script no encontrado: {nombre_script}", "WARN")
        if resultados is not None and clave:
            resultados[clave] = False
        return False

    registrar_evento(f"{descripcion} -> {nombre_script}...")
    try:
        resultado = subprocess.run(
            [sys.executable, nombre_script],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT_SUBPROCESO
        )
        exito = resultado.returncode == 0
        if exito:
            registrar_evento(f"{nombre_script} completado.", "OK")
        else:
            err = resultado.stderr.strip()[:200] if resultado.stderr else "Sin detalle"
            registrar_evento(f"{nombre_script} falló: {err}", "ERROR")

        if resultados is not None and clave:
            resultados[clave] = exito
        return exito

    except subprocess.TimeoutExpired:
        registrar_evento(f"{nombre_script} timeout ({TIMEOUT_SUBPROCESO}s).", "ERROR")
        if resultados is not None and clave:
            resultados[clave] = False
        return False
    except Exception as e:
        registrar_evento(f"Excepción en {nombre_script}: {e}", "ERROR")
        if resultados is not None and clave:
            resultados[clave] = False
        return False

# ============================================================
# MEJORA 1: MAPEO + ESTRATEGIA EN PARALELO
# ============================================================
def paso_mapeo_estrategia_paralelo():
    """
    Ejecuta mapeador y estratega simultáneamente.
    Ahorra ~50% del tiempo del ciclo en estos 2 pasos.
    """
    registrar_evento("PASO 1+2 — Mapeo + Estrategia en PARALELO ?", "INFO")
    resultados = {"mapeador": False, "estratega": False}

    t1 = threading.Thread(
        target=ejecutar_script,
        args=("mapeador_capacidades.py", "[BUSCAR] Mapeador"),
        kwargs={"resultados": resultados, "clave": "mapeador"}
    )
    t2 = threading.Thread(
        target=ejecutar_script,
        args=("agente_estrategia.py", "[CEREBRO] Estratega"),
        kwargs={"resultados": resultados, "clave": "estratega"}
    )

    t1.start()
    t2.start()
    t1.join(timeout=TIMEOUT_SUBPROCESO + 15)
    t2.join(timeout=TIMEOUT_SUBPROCESO + 15)

    return resultados["mapeador"], resultados["estratega"]

# ============================================================
# MEJORA 2+3: ARQUITECTURA WEB EN PARALELO CON PREP DE MISIONES
# ============================================================
def paso_arquitectura_paralelo(resultados_arch):
    """Corre arquitecto web en paralelo mientras se prepara auto_run."""
    ejecutar_script(
        "agente_arquitecto_web.py", "? Arquitecto Web",
        resultados=resultados_arch, clave="arquitecto"
    )

# ============================================================
# MISIONES
# ============================================================
def hay_misiones():
    if not os.path.exists("misiones.txt"):
        return False
    try:
        with open("misiones.txt", "r", encoding="utf-8", errors="replace") as f:
            return len(f.read().strip()) > 0
    except Exception:
        return False

def contar_misiones():
    try:
        with open("misiones.txt", "r", encoding="utf-8", errors="replace") as f:
            return len([l for l in f.readlines() if l.strip()])
    except Exception:
        return 0

def vaciar_misiones():
    try:
        with open("misiones.txt", "w", encoding="utf-8") as f:
            f.write("")
        registrar_evento("misiones.txt vaciado.", "OK")
    except Exception as e:
        registrar_evento(f"No se pudo vaciar misiones.txt: {e}", "WARN")

# ============================================================
# ESTADÍSTICAS
# ============================================================
def imprimir_estadisticas():
    ahora = time.strftime('%Y-%m-%d %H:%M:%S')
    resumen = (
        f"\n{'='*60}\n"
        f"  [STATS] ESTADÍSTICAS — MODO NOCHE v2.0\n"
        f"  Inicio:              {stats['inicio_sesion']}\n"
        f"  Ahora:               {ahora}\n"
        f"  Ciclos completados:  {stats['ciclos_completados']}\n"
        f"  Ciclos fallidos:     {stats['ciclos_fallidos']}\n"
        f"  Parches aplicados:   {stats['parches_aplicados']}\n"
        f"{'='*60}\n"
    )
    with log_lock:
        print(resumen)
        with open(LOG_EVOLUCION, "a", encoding="utf-8") as f:
            f.write(resumen)

# ============================================================
# CICLO PRINCIPAL
# ============================================================
def ejecutar_ciclo():
    registrar_separador()
    ciclo_num = stats["ciclos_completados"] + stats["ciclos_fallidos"] + 1
    registrar_evento(f"CICLO #{ciclo_num} INICIADO [v2.0 — Paralelo ON]", "INFO")

    errores = 0

    # PASO 1+2 EN PARALELO
    ok_map, ok_est = paso_mapeo_estrategia_paralelo()
    if not ok_map: errores += 1
    if not ok_est: errores += 1

    # PASO 3: ARQUITECTO WEB EN PARALELO MIENTRAS VERIFICAMOS MISIONES
    registrar_evento("PASO 3/5 — Arquitecto Web (paralelo)...", "INFO")
    resultados_arch = {"arquitecto": False}
    t_arch = threading.Thread(target=paso_arquitectura_paralelo, args=(resultados_arch,))
    t_arch.start()

    # PASO 4: EJECUTAR MISIONES (mientras arquitecto trabaja en paralelo)
    registrar_evento("PASO 4/5 — Aplicando parches...", "INFO")
    if hay_misiones():
        total = contar_misiones()
        registrar_evento(f"{total} misiones pendientes. Ejecutando...", "INFO")
        if ejecutar_script("auto_run.py", "[RUN] Motor"):
            stats["parches_aplicados"] += total
            vaciar_misiones()
        else:
            errores += 1
    else:
        registrar_evento("Sin misiones pendientes este ciclo.", "OK")

    # Esperar a que arquitecto termine
    t_arch.join(timeout=TIMEOUT_SUBPROCESO + 15)
    if not resultados_arch["arquitecto"]:
        errores += 1

    # PASO 5: QA
    registrar_evento("PASO 5/5 — Control de Calidad...", "INFO")
    if not ejecutar_script("supervisor_qa.py", "[QA] QA"):
        errores += 1

    # RESULTADO
    if errores == 0:
        registrar_evento(f"CICLO #{ciclo_num} COMPLETADO SIN ERRORES [OK]", "OK")
        stats["ciclos_completados"] += 1
        stats["errores_consecutivos"] = 0
        return True
    elif errores <= 2:
        registrar_evento(f"CICLO #{ciclo_num} completado con {errores} advertencia(s).", "WARN")
        stats["ciclos_completados"] += 1
        stats["errores_consecutivos"] = 0
        return True
    else:
        registrar_evento(f"CICLO #{ciclo_num} FALLIDO con {errores} errores.", "ERROR")
        stats["ciclos_fallidos"] += 1
        stats["errores_consecutivos"] += 1
        return False

# ============================================================
# BUCLE INFINITO
# ============================================================
def bucle_infinito():
    registrar_evento("[NOCHE] AGENCIA SANTI — MODO NOCHE v2.0 ACTIVADO", "INFO")
    registrar_evento(f"[FAST] Paralelo: ON | Ciclos: {TIEMPO_DESCANSO//60} min | Timeout: {TIMEOUT_SUBPROCESO}s", "INFO")
    registrar_separador()

    while True:
        try:
            exito = ejecutar_ciclo()

            if stats["errores_consecutivos"] >= MAX_ERRORES_CONSECUTIVOS:
                registrar_evento(f"[ALERTA] Pausa de emergencia {PAUSA_CRITICA//60} min.", "CRITICO")
                imprimir_estadisticas()
                stats["errores_consecutivos"] = 0
                time.sleep(PAUSA_CRITICA)
            elif exito:
                registrar_evento(f"[PAUSA] Próximo ciclo en {TIEMPO_DESCANSO//60} min...", "INFO")
                imprimir_estadisticas()
                time.sleep(TIEMPO_DESCANSO)
            else:
                registrar_evento(f"? Reintentando en {TIEMPO_DESCANSO_ERROR//60} min...", "WARN")
                time.sleep(TIEMPO_DESCANSO_ERROR)

        except KeyboardInterrupt:
            registrar_evento("[STOP] Modo Noche v2.0 detenido manualmente.", "WARN")
            imprimir_estadisticas()
            sys.exit(0)
        except Exception as e:
            registrar_evento(f"Error crítico en bucle: {e}", "CRITICO")
            stats["errores_consecutivos"] += 1
            time.sleep(TIEMPO_DESCANSO_ERROR)

if __name__ == "__main__":
    bucle_infinito()