"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: API REST de la Agencia Santi v1.0. Expone todos los agentes
             como endpoints HTTP. Permite conectar WhatsApp, dashboard web,
             apps externas y sistema de clientes. Corre en localhost:8000.
TECNOLOGÍA: http.server (stdlib), json, subprocess
"""



import os
import sys
import json
import time
import re
import subprocess
import threading
import io as _io
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Servidor HTTP multi-threaded: cada request en su propio hilo."""
    daemon_threads = True
    allow_reuse_address = True

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

# Fix Unicode para Windows (cp1252)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stdout, "buffer"):
    sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stderr, "buffer"):
    sys.stderr = open(sys.stderr.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)

# ---------------------------------------------
#  CONFIGURACION
# ---------------------------------------------

BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
HABILIDADES    = os.path.join(BASE_DIR, "habilidades.json")
LOG_API        = os.path.join(BASE_DIR, "registro_noche.txt")
PROYECTOS_DIR  = os.path.join(BASE_DIR, "proyectos")
PROYECTOS_QUEUE = os.path.join(BASE_DIR, "proyectos_queue")
PUERTO         = 8000
API_KEY        = "santi-agencia-2026"   # Cambiar en produccion
TIMEOUT_AGENTE = 30
MAX_HISTORIAL  = 100

# Cache de resultados (evita recalcular lo mismo)
cache = {}
cache_lock = threading.Lock()
historial_requests = []

# ---------------------------------------------
#  UTILIDADES
# ---------------------------------------------

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    linea = f"[{ts}] [API] {msg}"
    print(linea)
    try:
        with open(LOG_API, "a", encoding="utf-8") as f:
            f.write(linea + "\n")
    except Exception:
        pass

def cargar_habilidades():
    try:
        with open(HABILIDADES, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except Exception:
        return {}

def ejecutar_agente(archivo, params="", timeout=TIMEOUT_AGENTE):
    ruta = os.path.join(BASE_DIR, archivo)
    if not os.path.exists(ruta):
        return False, f"Agente {archivo} no encontrado"
    cmd = [sys.executable, ruta]
    if params:
        cmd.extend(str(p) for p in params.split() if p)
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            timeout=timeout, cwd=BASE_DIR
        )
        salida = (r.stdout or "").strip()
        if not salida and r.stderr:
            return False, r.stderr[:300]
        return True, salida or "Sin output"
    except subprocess.TimeoutExpired:
        return False, f"Timeout ({timeout}s)"
    except Exception as e:
        return False, str(e)

def respuesta_json(handler, status, data):
    body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", len(body))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
    handler.end_headers()
    handler.wfile.write(body)

def verificar_auth(handler):
    auth = handler.headers.get("Authorization", "")
    if not auth:
        # Tambien aceptar via query param ?key=
        parsed = urlparse(handler.path)
        params = parse_qs(parsed.query)
        key = params.get("key", [""])[0]
        return key == API_KEY
    return auth.replace("Bearer ", "").strip() == API_KEY

def registrar_request(metodo, ruta, status, duracion_ms):
    historial_requests.append({
        "ts": datetime.now().strftime('%H:%M:%S'),
        "metodo": metodo,
        "ruta": ruta,
        "status": status,
        "ms": duracion_ms
    })
    if len(historial_requests) > MAX_HISTORIAL:
        historial_requests.pop(0)

# ---------------------------------------------
#  HANDLER PRINCIPAL
# ---------------------------------------------

class AgenciaHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass  # Silenciar log por defecto del servidor

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        self.end_headers()

    def do_GET(self):
        inicio = time.time()
        parsed = urlparse(self.path)
        ruta   = parsed.path.rstrip("/")
        params = parse_qs(parsed.query)

        # -- Rutas publicas (sin auth) --------------
        if ruta == "" or ruta == "/":
            data = {
                "nombre": "Agencia Santi API",
                "version": "1.0",
                "status": "online",
                "timestamp": datetime.now().isoformat(),
                "endpoints": [
                    "GET  /dashboard.html   — dashboard principal (HTML)",
                    "GET  /agentes.html     — pestaña de agentes (HTML)",
                    "GET  /agentes          — lista todos los agentes (JSON)",
                    "GET  /agentes-list     — JSON para la pestaña de agentes",
                    "GET  /agentes/{nombre} — info de un agente",
                    "GET  /areas            — agentes agrupados por area",
                    "GET  /status           — estado del sistema",
                    "GET  /categorias       — todas las categorías con conteo",
                    "GET  /proyectos        — proyectos existentes (completo)",
                    "GET  /proyectos/contar — solo conteo de proyectos",
                    "GET  /catalogo         — catálogo de agentes por area",
                    "GET  /historial        — ultimas requests",
                    "POST /ejecutar         — ejecutar un agente",
                    "POST /crear-proyecto   — crear nuevo proyecto",
                    "POST /consulta         — lenguaje natural al Clawbot",
                ]
            }
            respuesta_json(self, 200, data)
            registrar_request("GET", ruta, 200, int((time.time()-inicio)*1000))
            return

        if ruta == "/ping":
            respuesta_json(self, 200, {"pong": True, "ts": datetime.now().isoformat()})
            return

        if ruta == "/test-19-cats":
            TEST_CATS = [
                "FINANZAS", "REAL ESTATE", "CEREBRO", "HERRAMIENTAS",
                "LEGAL", "MARKETING", "VENTAS", "OPERACIONES",
                "RECURSOS HUMANOS", "TECNOLOGÍA", "SALUD", "EDUCACIÓN",
                "LOGÍSTICA", "TURISMO", "RESTAURANTES",
                "BIENES RAÍCES COMERCIALES", "SEGUROS", "CONTABILIDAD",
                "MICRO_TAREAS"
            ]
            respuesta_json(self, 200, {
                "test": True,
                "count": len(TEST_CATS),
                "categorias": sorted(TEST_CATS)
            })
            return

        # -- Dashboard (publica, sin auth) --------
        if ruta == "/dashboard" or ruta == "/dashboard.html":
            dashboard_path = os.path.join(BASE_DIR, "dashboard_standalone.html")
            if os.path.exists(dashboard_path):
                try:
                    with open(dashboard_path, "r", encoding="utf-8") as f:
                        html_content = f.read()
                    body = html_content.encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", len(body))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(body)
                    registrar_request("GET", ruta, 200, int((time.time()-inicio)*1000))
                    return
                except Exception as e:
                    respuesta_json(self, 500, {"error": f"Error sirviendo dashboard: {e}"})
                    return
            else:
                respuesta_json(self, 404, {"error": "dashboard_standalone.html no encontrado"})
                return

        # -- Pestaña de Agentes (publica, sin auth) --------
        if ruta == "/agentes.html":
            agentes_path = os.path.join(BASE_DIR, "agentes.html")
            if os.path.exists(agentes_path):
                try:
                    with open(agentes_path, "r", encoding="utf-8") as f:
                        html_content = f.read()
                    body = html_content.encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", len(body))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(body)
                    registrar_request("GET", ruta, 200, int((time.time()-inicio)*1000))
                    return
                except Exception as e:
                    respuesta_json(self, 500, {"error": f"Error sirviendo agentes.html: {e}"})
                    return
            else:
                respuesta_json(self, 404, {"error": "agentes.html no encontrado"})
                return

        # -- Rutas con auth -------------------------
        if not verificar_auth(self):
            respuesta_json(self, 401, {"error": "No autorizado. Usa header Authorization: Bearer santi-agencia-2026"})
            registrar_request("GET", ruta, 401, int((time.time()-inicio)*1000))
            return

        habilidades = cargar_habilidades()
        resp_status = 200  # rastrear status real para registrar_request

        # GET /agentes
        if ruta == "/agentes":
            agentes = []
            for archivo, info in habilidades.items():
                agentes.append({
                    "archivo": archivo,
                    "descripcion": info.get("descripcion", ""),
                    "categoria": info.get("categoria", ""),
                    "area": info.get("categoria", ""),  # backwards compatibility
                    "salud": info.get("salud", "OK"),
                    "ordenes": info.get("ordenes", [])
                })
            respuesta_json(self, 200, {
                "total": len(agentes),
                "agentes": agentes
            })

        # GET /agentes/{nombre}
        elif ruta.startswith("/agentes/"):
            nombre = ruta.split("/agentes/")[1]
            if nombre in habilidades:
                info = habilidades[nombre]
                # Leer primeras lineas del codigo
                preview = ""
                ruta_py = os.path.join(BASE_DIR, nombre)
                if os.path.exists(ruta_py):
                    with open(ruta_py, "r", encoding="utf-8", errors="replace") as f:
                        preview = "".join(f.readlines()[:15])
                respuesta_json(self, 200, {
                    "archivo": nombre,
                    "info": info,
                    "preview_codigo": preview
                })
            else:
                resp_status = 404
                respuesta_json(self, 404, {"error": f"Agente '{nombre}' no encontrado"})

        # GET /areas
        elif ruta == "/areas":
            areas = {}
            for archivo, info in habilidades.items():
                area = info.get("categoria", "GENERAL")
                if area not in areas:
                    areas[area] = []
                areas[area].append(archivo)
            respuesta_json(self, 200, {
                "total_areas": len(areas),
                "total_agentes": len(habilidades),
                "areas": {k: {"cantidad": len(v), "agentes": v} for k, v in sorted(areas.items())}
            })

        # GET /status
        elif ruta == "/status":
            total = len(habilidades)
            ok    = sum(1 for v in habilidades.values() if v.get("salud") == "OK")
            log_size = 0
            if os.path.exists(LOG_API):
                log_size = round(os.path.getsize(LOG_API) / (1024*1024), 2)

            # Leer ultimas lineas del log
            ultimas_lineas = []
            try:
                with open(LOG_API, "r", encoding="utf-8", errors="replace") as f:
                    ultimas_lineas = [l.strip() for l in f.readlines()[-10:] if l.strip()]
            except Exception:
                pass

            respuesta_json(self, 200, {
                "status": "online",
                "timestamp": datetime.now().isoformat(),
                "agentes": {"total": total, "saludables": ok},
                "log_size_mb": log_size,
                "ultimas_actividades": ultimas_lineas,
                "requests_recientes": len(historial_requests)
            })

        # GET /historial
        elif ruta == "/historial":
            respuesta_json(self, 200, {
                "total": len(historial_requests),
                "requests": list(reversed(historial_requests[-20:]))
            })

        # GET /categorias — todas las categorias con conteo
        # Incluye TODAS las areas del plan (incluso las que aun no tienen agentes)
        elif ruta == "/categorias":
            # Areas del plan completo (de fabrica_agentes.py AREAS_TEMAS)
            TODAS_LAS_AREAS = [
                "FINANZAS", "REAL ESTATE", "CEREBRO", "HERRAMIENTAS",
                "LEGAL", "MARKETING", "VENTAS", "OPERACIONES",
                "RECURSOS HUMANOS", "TECNOLOGÍA", "SALUD", "EDUCACIÓN",
                "LOGÍSTICA", "TURISMO", "RESTAURANTES",
                "BIENES RAÍCES COMERCIALES", "SEGUROS", "CONTABILIDAD",
                "MICRO_TAREAS"
            ]
            cats = {}
            # Inicializar todas las areas con 0
            for area in TODAS_LAS_AREAS:
                cats[area] = {"total": 0, "ok": 0, "agentes": []}
            # Contar agentes existentes
            for archivo, info in habilidades.items():
                cat = info.get("categoria", "SIN_CATEGORIA")
                if cat not in cats:
                    cats[cat] = {"total": 0, "ok": 0, "agentes": []}
                cats[cat]["total"] += 1
                if info.get("salud") == "OK":
                    cats[cat]["ok"] += 1
                cats[cat]["agentes"].append(archivo)
            # Categorias con agentes (activas) vs sin agentes (pendientes)
            activas = sum(1 for v in cats.values() if v["total"] > 0)
            respuesta_json(self, 200, {
                "total_categorias": len(cats),
                "categorias_activas": activas,
                "categorias": {k: {"total": v["total"], "ok": v["ok"]} for k, v in sorted(cats.items())}
            })

        # GET /agentes-list — JSON para la pestaña de agentes (formato filtrado)
        elif ruta == "/agentes-list":
            # Todas las categorías del plan (de fabrica_agentes.py AREAS_TEMAS)
            TODAS_LAS_CATEGORIAS = [
                "FINANZAS", "REAL ESTATE", "CEREBRO", "HERRAMIENTAS",
                "LEGAL", "MARKETING", "VENTAS", "OPERACIONES",
                "RECURSOS HUMANOS", "TECNOLOGÍA", "SALUD", "EDUCACIÓN",
                "LOGÍSTICA", "TURISMO", "RESTAURANTES",
                "BIENES RAÍCES COMERCIALES", "SEGUROS", "CONTABILIDAD",
                "MICRO_TAREAS"
            ]
            agentes_dict = {}
            for archivo, info in habilidades.items():
                categoria = info.get("categoria", "SIN_CATEGORIA")
                agentes_dict[archivo] = {
                    "categoria": categoria,
                    "salud": info.get("salud", "OK"),
                    "descripcion": info.get("descripcion", ""),
                    "tecnologia": info.get("tecnologia", ["Python"])
                }
            categorias_finales = sorted(TODAS_LAS_CATEGORIAS)
            log(f"[AGENTES-LIST] Enviando {len(agentes_dict)} agentes con {len(categorias_finales)} categorías")
            respuesta_json(self, 200, {
                "agentes": agentes_dict,
                "categorias": categorias_finales
            })

        # GET /credenciales?proyecto=xxx — listar credenciales de un proyecto
        elif ruta == "/credenciales":
            proyecto = params.get("proyecto", [""])[0]
            try:
                from gestor_credenciales import listar_credenciales_proyecto, listar_plataformas, listar_categorias_plataformas
                creds = listar_credenciales_proyecto(proyecto) if proyecto else []
                plataformas = listar_plataformas()
                cats = listar_categorias_plataformas()
                respuesta_json(self, 200, {
                    "proyecto": proyecto,
                    "credenciales_configuradas": creds,
                    "total_configuradas": len(creds),
                    "plataformas_soportadas": len(plataformas),
                    "categorias": cats,
                    "plataformas": plataformas,
                })
            except Exception as e:
                respuesta_json(self, 500, {"error": str(e)})

        # GET /expansion — plan de expansion con progreso
        elif ruta == "/expansion":
            plan_path = os.path.join(BASE_DIR, "expansion_plan.json")
            if not os.path.exists(plan_path):
                respuesta_json(self, 404, {"error": "expansion_plan.json no encontrado"})
            else:
                try:
                    with open(plan_path, "r", encoding="utf-8") as f:
                        plan = json.load(f)
                    micros = plan.get("micros", [])
                    # Calcular progreso: cuales ya existen en habilidades.json
                    existentes = set(habilidades.keys())
                    creados = []
                    pendientes = []
                    for m in micros:
                        if m["nombre"] in existentes:
                            creados.append(m)
                        else:
                            pendientes.append(m)
                    # Agrupar pendientes por categoria
                    por_cat = {}
                    for m in pendientes:
                        cat = m["categoria"]
                        if cat not in por_cat:
                            por_cat[cat] = []
                        por_cat[cat].append(m)
                    respuesta_json(self, 200, {
                        "total_planificados": len(micros),
                        "creados": len(creados),
                        "pendientes": len(pendientes),
                        "progreso_pct": round(len(creados) / max(len(micros), 1) * 100, 1),
                        "agentes_actuales": len(habilidades),
                        "meta_total": len(habilidades) + len(pendientes),
                        "por_categoria": {k: {"pendientes": len(v), "ejemplos": [x["nombre"] for x in v[:3]]} for k, v in sorted(por_cat.items())},
                        "categorias_nuevas": plan.get("categorias_nuevas", []),
                        "lista_pendientes": pendientes,
                        "lista_creados": creados
                    })
                except Exception as e:
                    respuesta_json(self, 500, {"error": f"Error leyendo expansion_plan.json: {e}"})

        # GET /estadisticas — stats detalladas por categoria
        elif ruta == "/estadisticas":
            cats = {}
            techs = {}
            for archivo, info in habilidades.items():
                cat = info.get("categoria", "SIN_CATEGORIA")
                if cat not in cats:
                    cats[cat] = {"total": 0, "ok": 0, "no_ok": 0, "tecnologias": {}}
                cats[cat]["total"] += 1
                if info.get("salud") == "OK":
                    cats[cat]["ok"] += 1
                else:
                    cats[cat]["no_ok"] += 1
                for tech in info.get("tecnologia", []):
                    cats[cat]["tecnologias"][tech] = cats[cat]["tecnologias"].get(tech, 0) + 1
                    techs[tech] = techs.get(tech, 0) + 1
            respuesta_json(self, 200, {
                "total_agentes": len(habilidades),
                "total_categorias": len(cats),
                "por_categoria": cats,
                "tecnologias_globales": dict(sorted(techs.items(), key=lambda x: x[1], reverse=True))
            })

        # GET /modo — obtener modo actual de fábrica
        elif ruta == "/modo":
            try:
                modo_file = os.path.join(BASE_DIR, ".fabricamode")
                if os.path.exists(modo_file):
                    with open(modo_file, "r", encoding="utf-8") as f:
                        modo = f.read().strip().upper()
                else:
                    modo = "NOCHE"  # Default
                respuesta_json(self, 200, {
                    "modo_actual": modo,
                    "modos_disponibles": ["CREAR", "MEJORAR", "BALANCEADO", "EXPANSION", "NOCHE"],
                    "descripcion": {
                        "CREAR": "Generar nuevos agentes hasta 500",
                        "MEJORAR": "Optimizar agentes existentes",
                        "BALANCEADO": "60% crear, 40% mejorar",
                        "EXPANSION": "Solo los 206 micros del plan",
                        "NOCHE": "Todas las tareas (default)"
                    }
                })
            except Exception as e:
                respuesta_json(self, 500, {"error": str(e)})

        # GET /proyectos/contar (debe estar ANTES de /proyectos genérico)
        if ruta == "/proyectos/contar":
            conteo = 0
            try:
                if os.path.exists(PROYECTOS_DIR):
                    conteo += len([n for n in os.listdir(PROYECTOS_DIR) if os.path.isdir(os.path.join(PROYECTOS_DIR, n))])
                if os.path.exists(PROYECTOS_QUEUE):
                    conteo += len([f for f in os.listdir(PROYECTOS_QUEUE) if f.endswith(".txt")])
            except Exception:
                pass
            respuesta_json(self, 200, {"total": conteo})

        # GET /proyectos
        elif ruta == "/proyectos":
            proyectos = []
            try:
                # 1. Proyectos COMPLETADOS (carpetas en proyectos/)
                if os.path.exists(PROYECTOS_DIR):
                    for nombre in os.listdir(PROYECTOS_DIR):
                        ruta_prj = os.path.join(PROYECTOS_DIR, nombre)
                        if os.path.isdir(ruta_prj):
                            desc = ""
                            # Leer descripcion del README.md
                            ruta_readme = os.path.join(ruta_prj, "README.md")
                            if os.path.exists(ruta_readme):
                                try:
                                    with open(ruta_readme, "r", encoding="utf-8") as f:
                                        lineas = f.readlines()
                                    # Buscar linea de "Modelo de Negocio"
                                    for i, l in enumerate(lineas):
                                        if "Modelo de Negocio" in l and i + 1 < len(lineas):
                                            desc = lineas[i + 1].strip().strip('"')[:200]
                                            break
                                    if not desc and len(lineas) > 0:
                                        desc = lineas[0].strip().lstrip("# ")[:200]
                                except Exception:
                                    pass
                            # Contar agentes del proyecto
                            agentes_dir = os.path.join(ruta_prj, "agentes")
                            n_agentes = 0
                            if os.path.exists(agentes_dir):
                                n_agentes = len([f for f in os.listdir(agentes_dir) if f.endswith(".py")])
                            stat = os.stat(ruta_prj)
                            fecha = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                            proyectos.append({
                                "nombre": nombre,
                                "descripcion": desc,
                                "fecha": fecha,
                                "status": "activo",
                                "agentes": n_agentes
                            })

                # 2. Proyectos PENDIENTES (.txt en proyectos_queue/ raiz)
                if os.path.exists(PROYECTOS_QUEUE):
                    for archivo in os.listdir(PROYECTOS_QUEUE):
                        ruta_txt = os.path.join(PROYECTOS_QUEUE, archivo)
                        if archivo.endswith(".txt") and os.path.isfile(ruta_txt):
                            desc = ""
                            try:
                                with open(ruta_txt, "r", encoding="utf-8") as f:
                                    desc = f.read().strip()[:200]
                            except Exception:
                                pass
                            stat = os.stat(ruta_txt)
                            fecha = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                            proyectos.append({
                                "nombre": archivo.replace(".txt", ""),
                                "descripcion": desc,
                                "fecha": fecha,
                                "status": "pendiente",
                                "agentes": 0
                            })
            except Exception as e:
                log(f"Error cargando proyectos: {e}")

            respuesta_json(self, 200, {
                "total": len(proyectos),
                "proyectos": sorted(proyectos, key=lambda x: x["fecha"], reverse=True)
            })

        # GET /catalogo
        elif ruta == "/catalogo":
            areas = {}
            for archivo, info in habilidades.items():
                area = info.get("categoria", "GENERAL")
                if area not in areas:
                    areas[area] = []
                areas[area].append({
                    "archivo": archivo,
                    "descripcion": info.get("descripcion", ""),
                    "salud": info.get("salud", "OK")
                })

            respuesta_json(self, 200, {
                "total_areas": len(areas),
                "total_agentes": len(habilidades),
                "areas": {k: sorted(v, key=lambda x: x["archivo"]) for k, v in sorted(areas.items())}
            })

        else:
            resp_status = 404
            respuesta_json(self, 404, {"error": f"Ruta '{ruta}' no encontrada"})

        registrar_request("GET", ruta, resp_status, int((time.time()-inicio)*1000))

    def do_POST(self):
        inicio = time.time()
        parsed = urlparse(self.path)
        ruta   = parsed.path.rstrip("/")

        if not verificar_auth(self):
            respuesta_json(self, 401, {"error": "No autorizado"})
            return

        # Leer body
        body = {}
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length > 0:
                raw = self.rfile.read(length)
                body = json.loads(raw.decode("utf-8"))
        except Exception as e:
            respuesta_json(self, 400, {"error": f"Body JSON invalido: {e}"})
            return

        resp_status = 200  # rastrear status real

        # POST /ejecutar
        # Body: {"agente": "calculadora_roi.py", "params": "2000000 14000 2800 20000"}
        if ruta == "/ejecutar":
            agente = body.get("agente", "")
            params = body.get("params", "")
            usar_cache = body.get("cache", True)

            if not agente:
                respuesta_json(self, 400, {"error": "Falta campo 'agente'"})
                return

            habilidades = cargar_habilidades()
            if agente not in habilidades:
                respuesta_json(self, 404, {"error": f"Agente '{agente}' no registrado"})
                return

            # Revisar cache
            cache_key = f"{agente}:{params}"
            if usar_cache:
                with cache_lock:
                    if cache_key in cache:
                        cached = cache[cache_key]
                        if time.time() - cached["ts"] < 300:  # 5 min cache
                            respuesta_json(self, 200, {**cached["data"], "cache": True})
                            return

            log(f"Ejecutando {agente} params='{params}'")
            exito, output = ejecutar_agente(agente, params)

            data = {
                "agente": agente,
                "params": params,
                "exito": exito,
                "output": output,
                "timestamp": datetime.now().isoformat(),
                "cache": False
            }

            if exito and usar_cache:
                with cache_lock:
                    cache[cache_key] = {"ts": time.time(), "data": data}

            resp_status = 200 if exito else 500
            respuesta_json(self, resp_status, data)

        # POST /ejecutar/batch
        # Body: {"tareas": [{"agente": "x.py", "params": "..."}, ...]}
        elif ruta == "/ejecutar/batch":
            tareas = body.get("tareas", [])
            if not tareas:
                respuesta_json(self, 400, {"error": "Falta campo 'tareas'"})
                return
            if len(tareas) > 10:
                respuesta_json(self, 400, {"error": "Maximo 10 tareas por batch"})
                return

            resultados = []
            for tarea in tareas:
                agente = tarea.get("agente", "")
                params = tarea.get("params", "")
                exito, output = ejecutar_agente(agente, params)
                resultados.append({
                    "agente": agente,
                    "exito": exito,
                    "output": output
                })
                time.sleep(0.5)

            respuesta_json(self, 200, {
                "batch": len(resultados),
                "resultados": resultados,
                "timestamp": datetime.now().isoformat()
            })

        # POST /consulta
        # Body: {"mensaje": "analiza depa de 2M en Polanco"}
        elif ruta == "/consulta":
            mensaje = body.get("mensaje", "").strip()
            if not mensaje:
                respuesta_json(self, 400, {"error": "Falta campo 'mensaje'"})
                return

            log(f"Consulta Clawbot: {mensaje[:60]}")
            exito, output = ejecutar_agente(
                "orquestador_clawbot.py",
                mensaje.replace('"', '').replace("'", ""),
                timeout=60
            )

            respuesta_json(self, 200, {
                "consulta": mensaje,
                "respuesta": output,
                "exito": exito,
                "timestamp": datetime.now().isoformat()
            })

        # POST /cache/limpiar
        elif ruta == "/cache/limpiar":
            with cache_lock:
                n = len(cache)
                cache.clear()
            respuesta_json(self, 200, {"limpiado": n, "mensaje": f"{n} entradas eliminadas del cache"})

        # POST /crear-proyecto
        # Body: {"nombre": "tienda_online", "descripcion": "Tienda online CDMX..."}
        elif ruta == "/crear-proyecto":
            nombre = body.get("nombre", "").strip()
            descripcion = body.get("descripcion", "").strip()

            if not nombre or len(nombre) < 3:
                respuesta_json(self, 400, {"error": "Nombre debe tener al menos 3 caracteres", "exito": False})
                return

            # Sanitizar nombre para usar como filename
            nombre_sanitizado = re.sub(r'[^a-z0-9_-]', '_', nombre.lower())
            nombre_sanitizado = re.sub(r'_+', '_', nombre_sanitizado).strip('_-')[:50]
            if not nombre_sanitizado:
                respuesta_json(self, 400, {"error": "Nombre contiene solo caracteres especiales", "exito": False})
                return

            try:
                # Crear archivo en proyectos_queue/
                if not os.path.exists(PROYECTOS_QUEUE):
                    os.makedirs(PROYECTOS_QUEUE, exist_ok=True)

                archivo = os.path.join(PROYECTOS_QUEUE, f"{nombre_sanitizado}.txt")
                with open(archivo, "w", encoding="utf-8") as f:
                    f.write(descripcion)

                log(f"Proyecto creado: {nombre_sanitizado} ({len(descripcion)} chars)")
                respuesta_json(self, 200, {
                    "exito": True,
                    "nombre": nombre_sanitizado,
                    "archivo": f"{nombre_sanitizado}.txt",
                    "mensaje": f"✅ Proyecto '{nombre_sanitizado}' creado. El orquestador lo procesará en breve."
                })
            except Exception as e:
                log(f"Error creando proyecto: {e}")
                resp_status = 500
                respuesta_json(self, 500, {
                    "exito": False,
                    "error": f"Error al crear proyecto: {str(e)}"
                })

        # POST /agentes/crear
        # Body: {"nombre": "mi_agente.py", "descripcion": "...", "categoria": "MARKETING", "tecnologias": [...], "ordenes": [...]}
        elif ruta == "/agentes/crear":
            nombre = body.get("nombre", "").strip()
            descripcion = body.get("descripcion", "").strip()
            categoria = body.get("categoria", "HERRAMIENTAS").strip().upper()
            tecnologias = body.get("tecnologias", ["Python estandar"])
            ordenes = body.get("ordenes", [])

            if not nombre:
                respuesta_json(self, 400, {"error": "Falta campo 'nombre'"}); return
            if not nombre.endswith(".py"):
                nombre += ".py"
            nombre = re.sub(r'[^a-z0-9_.]', '_', nombre.lower())
            if len(descripcion) < 10:
                respuesta_json(self, 400, {"error": "Descripcion debe tener al menos 10 caracteres"}); return

            habilidades = cargar_habilidades()
            if nombre in habilidades:
                respuesta_json(self, 409, {"error": f"Agente '{nombre}' ya existe"}); return

            # Registrar en habilidades.json
            habilidades[nombre] = {
                "descripcion": descripcion,
                "categoria": categoria,
                "salud": "OK",
                "tecnologia": tecnologias if isinstance(tecnologias, list) else [tecnologias],
                "ultima_actualizacion": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "ordenes": ordenes if isinstance(ordenes, list) else [ordenes]
            }
            try:
                with open(HABILIDADES, "w", encoding="utf-8") as f:
                    json.dump(habilidades, f, indent=4, ensure_ascii=False)
                log(f"Agente creado via API: {nombre} [{categoria}]")
                respuesta_json(self, 200, {"exito": True, "mensaje": f"Agente '{nombre}' creado", "agente": habilidades[nombre]})
            except Exception as e:
                resp_status = 500
                respuesta_json(self, 500, {"error": f"Error guardando: {e}"})

        # POST /agentes/editar
        # Body: {"nombre": "mi_agente.py", "descripcion": "...", "categoria": "...", "tecnologias": [...], "ordenes": [...]}
        elif ruta == "/agentes/editar":
            nombre = body.get("nombre", "").strip()
            if not nombre:
                respuesta_json(self, 400, {"error": "Falta campo 'nombre'"}); return

            habilidades = cargar_habilidades()
            if nombre not in habilidades:
                respuesta_json(self, 404, {"error": f"Agente '{nombre}' no encontrado"}); return

            cambios = 0
            if "descripcion" in body and body["descripcion"].strip():
                habilidades[nombre]["descripcion"] = body["descripcion"].strip()
                cambios += 1
            if "categoria" in body and body["categoria"].strip():
                habilidades[nombre]["categoria"] = body["categoria"].strip().upper()
                cambios += 1
            if "tecnologias" in body:
                habilidades[nombre]["tecnologia"] = body["tecnologias"] if isinstance(body["tecnologias"], list) else [body["tecnologias"]]
                cambios += 1
            if "ordenes" in body:
                habilidades[nombre]["ordenes"] = body["ordenes"] if isinstance(body["ordenes"], list) else [body["ordenes"]]
                cambios += 1
            if "salud" in body:
                habilidades[nombre]["salud"] = body["salud"]
                cambios += 1

            habilidades[nombre]["ultima_actualizacion"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            try:
                with open(HABILIDADES, "w", encoding="utf-8") as f:
                    json.dump(habilidades, f, indent=4, ensure_ascii=False)
                log(f"Agente editado via API: {nombre} ({cambios} cambios)")
                respuesta_json(self, 200, {"exito": True, "cambios": cambios, "agente": habilidades[nombre]})
            except Exception as e:
                resp_status = 500
                respuesta_json(self, 500, {"error": f"Error guardando: {e}"})

        # POST /agentes/eliminar
        # Body: {"nombre": "mi_agente.py"}
        elif ruta == "/agentes/eliminar":
            nombre = body.get("nombre", "").strip()
            if not nombre:
                respuesta_json(self, 400, {"error": "Falta campo 'nombre'"}); return

            habilidades = cargar_habilidades()
            if nombre not in habilidades:
                respuesta_json(self, 404, {"error": f"Agente '{nombre}' no encontrado"}); return

            info_eliminada = habilidades.pop(nombre)
            try:
                with open(HABILIDADES, "w", encoding="utf-8") as f:
                    json.dump(habilidades, f, indent=4, ensure_ascii=False)
                log(f"Agente eliminado via API: {nombre}")
                respuesta_json(self, 200, {"exito": True, "mensaje": f"Agente '{nombre}' eliminado", "info": info_eliminada})
            except Exception as e:
                resp_status = 500
                respuesta_json(self, 500, {"error": f"Error guardando: {e}"})

        # POST /categorias/crear
        # Body: {"nombre": "MARKETING"}
        elif ruta == "/categorias/crear":
            cat_nombre = body.get("nombre", "").strip().upper()
            if not cat_nombre or len(cat_nombre) < 2:
                respuesta_json(self, 400, {"error": "Nombre de categoria debe tener al menos 2 caracteres"}); return
            # Verificar si ya existe
            habilidades = cargar_habilidades()
            cats_existentes = set(info.get("categoria", "") for info in habilidades.values())
            if cat_nombre in cats_existentes:
                respuesta_json(self, 409, {"error": f"Categoria '{cat_nombre}' ya existe"}); return
            log(f"Categoria creada via API: {cat_nombre}")
            respuesta_json(self, 200, {"exito": True, "mensaje": f"Categoria '{cat_nombre}' registrada. Asigna agentes a ella."})

        # POST /categorias/renombrar
        # Body: {"viejo": "HERRAMIENTAS", "nuevo": "TOOLS"}
        elif ruta == "/categorias/renombrar":
            viejo = body.get("viejo", "").strip().upper()
            nuevo = body.get("nuevo", "").strip().upper()
            if not viejo or not nuevo:
                respuesta_json(self, 400, {"error": "Faltan campos 'viejo' y 'nuevo'"}); return
            habilidades = cargar_habilidades()
            reasignados = 0
            for arch, info in habilidades.items():
                if info.get("categoria", "").upper() == viejo:
                    info["categoria"] = nuevo
                    reasignados += 1
            if reasignados == 0:
                respuesta_json(self, 404, {"error": f"Categoria '{viejo}' no tiene agentes"}); return
            try:
                with open(HABILIDADES, "w", encoding="utf-8") as f:
                    json.dump(habilidades, f, indent=4, ensure_ascii=False)
                log(f"Categoria renombrada: {viejo} -> {nuevo} ({reasignados} agentes)")
                respuesta_json(self, 200, {"exito": True, "reasignados": reasignados, "mensaje": f"'{viejo}' -> '{nuevo}' ({reasignados} agentes)"})
            except Exception as e:
                resp_status = 500
                respuesta_json(self, 500, {"error": f"Error: {e}"})

        # POST /categorias/eliminar
        # Body: {"nombre": "VIEJA", "reasignar_a": "HERRAMIENTAS"}
        elif ruta == "/categorias/eliminar":
            cat_nombre = body.get("nombre", "").strip().upper()
            reasignar = body.get("reasignar_a", "HERRAMIENTAS").strip().upper()
            if not cat_nombre:
                respuesta_json(self, 400, {"error": "Falta campo 'nombre'"}); return
            habilidades = cargar_habilidades()
            reasignados = 0
            for arch, info in habilidades.items():
                if info.get("categoria", "").upper() == cat_nombre:
                    info["categoria"] = reasignar
                    reasignados += 1
            if reasignados == 0:
                respuesta_json(self, 404, {"error": f"Categoria '{cat_nombre}' no tiene agentes"}); return
            try:
                with open(HABILIDADES, "w", encoding="utf-8") as f:
                    json.dump(habilidades, f, indent=4, ensure_ascii=False)
                log(f"Categoria eliminada: {cat_nombre} -> {reasignar} ({reasignados} agentes)")
                respuesta_json(self, 200, {"exito": True, "reasignados": reasignados})
            except Exception as e:
                resp_status = 500
                respuesta_json(self, 500, {"error": f"Error: {e}"})

        # POST /modo — cambiar modo de fabrica
        # Body: {"modo": "CREAR"}
        elif ruta == "/modo":
            nuevo_modo = body.get("modo", "").strip().upper()
            modos_validos = ["CREAR", "MEJORAR", "BALANCEADO", "EXPANSION", "NOCHE"]
            if nuevo_modo not in modos_validos:
                respuesta_json(self, 400, {
                    "error": f"Modo '{nuevo_modo}' no válido",
                    "modos_validos": modos_validos
                }); return

            try:
                modo_file = os.path.join(BASE_DIR, ".fabricamode")
                with open(modo_file, "w", encoding="utf-8") as f:
                    f.write(nuevo_modo)
                log(f"Modo de fabrica cambiado a: {nuevo_modo}")
                respuesta_json(self, 200, {
                    "exito": True,
                    "modo_nuevo": nuevo_modo,
                    "mensaje": f"Modo cambiado a {nuevo_modo}. La fabrica lo aplicara en el proximo ciclo."
                })
            except Exception as e:
                resp_status = 500
                respuesta_json(self, 500, {"error": f"Error guardando modo: {e}"})

        # POST /credenciales/guardar
        # Body: {"proyecto": "...", "plataforma": "...", "credenciales": {...}}
        elif ruta == "/credenciales/guardar":
            try:
                from gestor_credenciales import guardar_credencial
                proyecto = body.get("proyecto", "")
                plataforma = body.get("plataforma", "")
                creds = body.get("credenciales", {})
                if not proyecto or not plataforma:
                    respuesta_json(self, 400, {"error": "Falta proyecto o plataforma"})
                else:
                    r = guardar_credencial(proyecto, plataforma, creds)
                    respuesta_json(self, 200 if r["exito"] else 400, r)
            except Exception as e:
                respuesta_json(self, 500, {"error": str(e)})

        # POST /credenciales/verificar
        # Body: {"proyecto": "...", "tarea": "publicar en facebook"}
        elif ruta == "/credenciales/verificar":
            try:
                from gestor_credenciales import credenciales_faltantes
                proyecto = body.get("proyecto", "")
                tarea = body.get("tarea", "")
                faltantes = credenciales_faltantes(proyecto, tarea)
                respuesta_json(self, 200, {
                    "puede_ejecutar": len(faltantes) == 0,
                    "faltantes": faltantes,
                    "total_faltantes": len(faltantes),
                })
            except Exception as e:
                respuesta_json(self, 500, {"error": str(e)})

        # POST /credenciales/eliminar
        # Body: {"proyecto": "...", "plataforma": "..."}
        elif ruta == "/credenciales/eliminar":
            try:
                from gestor_credenciales import eliminar_credencial
                r = eliminar_credencial(body.get("proyecto", ""), body.get("plataforma", ""))
                respuesta_json(self, 200, r)
            except Exception as e:
                respuesta_json(self, 500, {"error": str(e)})

        # POST /detectar-hosting
        # Body: {"url": "way2theunknown.com", "proyecto": "way2theunknown"}
        elif ruta == "/detectar-hosting":
            try:
                from detector_plataforma import analisis_completo
                url = body.get("url", "")
                proyecto = body.get("proyecto", "")
                if not url:
                    respuesta_json(self, 400, {"error": "Falta campo 'url'"})
                else:
                    r = analisis_completo(url, proyecto or None)
                    respuesta_json(self, 200, r)
            except Exception as e:
                respuesta_json(self, 500, {"error": str(e)})

        # POST /tarea
        # Body: {"descripcion": "...", "proyecto": "way2theunknown", "prioridad": "normal"}
        elif ruta == "/tarea":
            descripcion = body.get("descripcion", "").strip()
            proyecto = body.get("proyecto", "").strip()
            prioridad = body.get("prioridad", "normal")

            if not descripcion:
                respuesta_json(self, 400, {"error": "Falta campo 'descripcion'"}); return

            log(f"TAREA RECIBIDA: {descripcion[:100]}...")
            if proyecto:
                log(f"  Proyecto: {proyecto} | Prioridad: {prioridad}")

            # Guardar tarea en archivo de cola
            tareas_file = os.path.join(BASE_DIR, "tareas_pendientes.json")
            try:
                tareas = []
                if os.path.exists(tareas_file):
                    with open(tareas_file, "r", encoding="utf-8") as f:
                        tareas = json.load(f)
            except Exception:
                tareas = []

            nueva_tarea = {
                "id": int(time.time() * 1000),
                "descripcion": descripcion,
                "proyecto": proyecto or None,
                "prioridad": prioridad,
                "fecha": datetime.now().isoformat(),
                "status": "pendiente",
                "resultado": None
            }

            # Si hay un proyecto, intentar ejecutar el orquestador
            resultado_texto = ""
            if proyecto:
                orq_path = os.path.join(PROYECTOS_DIR, proyecto, "orquestador.py")
                if os.path.exists(orq_path):
                    try:
                        log(f"  Ejecutando orquestador: {orq_path}")
                        r = subprocess.run(
                            [sys.executable, orq_path, descripcion],
                            capture_output=True, text=True,
                            encoding="utf-8", errors="replace",
                            timeout=120,
                            cwd=os.path.join(PROYECTOS_DIR, proyecto)
                        )
                        resultado_texto = (r.stdout or "").strip()
                        if r.returncode != 0:
                            err = (r.stderr or "").strip()
                            resultado_texto = f"Error: {err[:500]}" if err else "Error sin detalle"
                            nueva_tarea["status"] = "error"
                        else:
                            nueva_tarea["status"] = "completada"
                    except subprocess.TimeoutExpired:
                        resultado_texto = "Timeout: La tarea excedio 120 segundos"
                        nueva_tarea["status"] = "error"
                    except Exception as e:
                        resultado_texto = f"Error ejecutando: {e}"
                        nueva_tarea["status"] = "error"
                else:
                    resultado_texto = f"Tarea registrada para proyecto '{proyecto}'. El orquestador la procesara."
                    nueva_tarea["status"] = "pendiente"
            else:
                # Tarea general - intentar procesarla con consulta
                try:
                    from llm_router import completar_simple as ia_router
                    respuesta_ia = ia_router(f"Eres el asistente de Agencia Santi. El usuario solicita: {descripcion}\n\nResponde de forma concisa que harás y como.")
                    resultado_texto = respuesta_ia or "Tarea registrada"
                    nueva_tarea["status"] = "completada"
                except Exception:
                    resultado_texto = "Tarea registrada en cola. Se procesara en el proximo ciclo."
                    nueva_tarea["status"] = "pendiente"

            nueva_tarea["resultado"] = resultado_texto
            tareas.append(nueva_tarea)

            try:
                with open(tareas_file, "w", encoding="utf-8") as f:
                    json.dump(tareas[-50:], f, indent=2, ensure_ascii=False)
            except Exception:
                pass

            log(f"  Resultado: {resultado_texto[:100]}")
            respuesta_json(self, 200, {
                "exito": nueva_tarea["status"] != "error",
                "tarea_id": nueva_tarea["id"],
                "status": nueva_tarea["status"],
                "resultado": resultado_texto,
                "mensaje": f"Tarea {'completada' if nueva_tarea['status']=='completada' else 'registrada'}"
            })

        else:
            resp_status = 404
            respuesta_json(self, 404, {"error": f"Ruta POST '{ruta}' no encontrada"})

        registrar_request("POST", ruta, resp_status, int((time.time()-inicio)*1000))


# ---------------------------------------------
#  SERVIDOR
# ---------------------------------------------

def iniciar_servidor():
    log("=" * 55)
    log("AGENCIA SANTI — API REST v1.0")
    log(f"Puerto: {PUERTO}")
    log(f"URL:    http://localhost:{PUERTO}")
    log(f"Auth:   Bearer {API_KEY}")
    log("=" * 55)
    log("Endpoints disponibles:")
    log("  GET  /              — info de la API")
    log("  GET  /agentes       — lista todos los agentes")
    log("  GET  /areas         — agentes por area")
    log("  GET  /status        — estado del sistema")
    log("  GET  /proyectos     — proyectos existentes (completo)")
    log("  GET  /proyectos/contar — solo conteo de proyectos")
    log("  GET  /catalogo      — catálogo de agentes por area")
    log("  POST /ejecutar      — ejecutar un agente")
    log("  POST /ejecutar/batch— ejecutar varios agentes")
    log("  POST /crear-proyecto— crear nuevo proyecto")
    log("  POST /consulta      — consulta en lenguaje natural")
    log("=" * 55)

    servidor = ThreadedHTTPServer(("0.0.0.0", PUERTO), AgenciaHandler)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        log("API detenida.")
        servidor.server_close()

if __name__ == "__main__":
    iniciar_servidor()