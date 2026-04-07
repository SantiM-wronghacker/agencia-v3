"""
AREA: CEREBRO
DESCRIPCION: Orquestador de Proyectos v3.0. Recibe descripcion de un negocio,
             busca agentes utiles en el catalogo por keywords (sin LLM extra),
             crea los que faltan con timeout de 60s un solo intento, y los que
             fallen van a misiones.txt para que la fabrica los complete despues.
TECNOLOGIA: llm_router, habilidades.json, ast, subprocess
"""

import os
import sys
import ast
import json
import time
import shutil
import subprocess
import re
import io as _io
from datetime import datetime

# File locking nativo
try:
    import msvcrt
    _WINDOWS = True
except ImportError:
    import fcntl
    _WINDOWS = False

# Fix Unicode para Windows (cp1252)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stdout, "buffer"):
    sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stderr, "buffer"):
    sys.stderr = open(sys.stderr.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)

try:
    from agencia.agents.cerebro.llm_router import completar_simple as ia
except ImportError:
    from groq import Groq
    _g = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
    def ia(prompt, **kw):
        r = _g.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3, max_tokens=3000
        )
        return r.choices[0].message.content.strip()

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
HABILIDADES = os.path.join(BASE_DIR, "habilidades.json")
MISIONES    = os.path.join(BASE_DIR, "misiones.txt")
LOG         = os.path.join(BASE_DIR, "registro_noche.txt")
PROYECTOS   = os.path.join(BASE_DIR, "proyectos")

# ─────────────────────────────────────────────
#  LOGGING
# ─────────────────────────────────────────────

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    linea = "[" + ts + "] [PROYECTOS] " + str(msg)
    try:
        print(linea, flush=True)
    except Exception:
        pass
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(linea + "\n")
    except Exception:
        pass

# ─────────────────────────────────────────────
#  JSON ROBUSTO — nunca falla por formato
# ─────────────────────────────────────────────

def extraer_json(texto, tipo="objeto"):
    """
    Extrae JSON de una respuesta del LLM aunque venga con markdown,
    texto extra, o formato sucio. tipo = 'objeto' o 'lista'
    """
    if not texto:
        return None

    # Limpiar markdown
    for bloque in texto.split("```"):
        limpio = bloque.strip().lstrip("json").strip()
        if tipo == "objeto" and limpio.startswith("{"):
            try:
                return json.loads(limpio)
            except Exception:
                pass
        if tipo == "lista" and limpio.startswith("["):
            try:
                return json.loads(limpio)
            except Exception:
                pass

    # Buscar directamente en el texto
    if tipo == "objeto":
        match = re.search(r'\{[\s\S]*\}', texto)
    else:
        match = re.search(r'\[[\s\S]*\]', texto)

    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass

    # Intentar reparar JSON comun: comillas simples, comas finales
    try:
        reparado = texto
        reparado = re.sub(r"'", '"', reparado)
        reparado = re.sub(r',\s*([}\]])', r'\1', reparado)
        if tipo == "objeto":
            match = re.search(r'\{[\s\S]*\}', reparado)
        else:
            match = re.search(r'\[[\s\S]*\]', reparado)
        if match:
            return json.loads(match.group())
    except Exception:
        pass

    return None

# ─────────────────────────────────────────────
#  CATALOGO
# ─────────────────────────────────────────────

def cargar_catalogo():
    try:
        with open(HABILIDADES, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except Exception:
        return {}

def guardar_catalogo(catalogo):
    tmp = HABILIDADES + ".tmp"
    bak = HABILIDADES + ".bak"
    if os.path.exists(HABILIDADES):
        shutil.copy2(HABILIDADES, bak)
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(catalogo, f, indent=4, ensure_ascii=False)
    os.replace(tmp, HABILIDADES)

# ─────────────────────────────────────────────
#  PASO 1 — ANALIZAR EL NEGOCIO
# ─────────────────────────────────────────────

def analizar_negocio(descripcion):
    prompt = (
        "Eres arquitecto de sistemas de IA para empresas.\n\n"
        "DESCRIPCION DEL NEGOCIO:\n" + descripcion + "\n\n"
        "Extrae la informacion y devuelve SOLO JSON valido, sin texto extra, sin markdown:\n"
        '{"nombre":"Nombre comercial","slug":"slug_lowercase","dominio":"dominio.com",'
        '"modelo":"descripcion corta del modelo de negocio","idiomas":["es","en"],'
        '"agentes_necesarios":['
        '{"archivo":"nombre.py","funcion":"que hace exactamente","area":"AREA","critico":true}'
        ']}\n\n'
        "Lista 8-12 agentes que este negocio necesita para operar automaticamente.\n"
        "Ejemplos para agencia de viajes: cotizador_viaje.py, buscador_vuelos.py, "
        "buscador_hoteles.py, buscador_restaurantes.py, calculadora_fee.py, "
        "generador_itinerario.py, confirmador_reservas.py, seguimiento_cliente.py\n"
        "DEVUELVE SOLO EL JSON. Sin texto antes ni despues."
    )

    for intento in range(3):
        log("  Intento " + str(intento+1) + " de analisis...")
        respuesta = ia(prompt)
        if not respuesta:
            time.sleep(3)
            continue
        resultado = extraer_json(respuesta, "objeto")
        if resultado and "nombre" in resultado and "agentes_necesarios" in resultado:
            return resultado
        log("  Respuesta no parseable, reintentando...")
        time.sleep(2)

    # Fallback: construir estructura minima desde la descripcion
    log("  Usando fallback para construir estructura del negocio...")
    palabras = descripcion.lower().split()
    nombre = "Empresa"
    for i, p in enumerate(palabras):
        if p in ("llamada", "llamado", "nombre"):
            if i+1 < len(palabras):
                nombre = palabras[i+1].title()
                break

    slug = re.sub(r'[^a-z0-9]', '_', nombre.lower())

    return {
        "nombre": nombre,
        "slug": slug,
        "dominio": None,
        "modelo": descripcion[:100],
        "idiomas": ["es", "en"],
        "agentes_necesarios": [
            {"archivo": "cotizador_viaje.py", "funcion": "Cotiza viajes completos con fee del 8%", "area": "TURISMO", "critico": True},
            {"archivo": "buscador_vuelos.py", "funcion": "Busca y compara opciones de vuelos", "area": "TURISMO", "critico": True},
            {"archivo": "buscador_hoteles.py", "funcion": "Busca hoteles por destino y presupuesto", "area": "TURISMO", "critico": True},
            {"archivo": "buscador_restaurantes.py", "funcion": "Recomienda restaurantes por destino", "area": "TURISMO", "critico": False},
            {"archivo": "calculadora_fee_viaje.py", "funcion": "Calcula el 8% de fee sobre costo total", "area": "FINANZAS", "critico": True},
            {"archivo": "generador_itinerario.py", "funcion": "Genera itinerario dia a dia del viaje", "area": "TURISMO", "critico": True},
            {"archivo": "confirmador_reservas.py", "funcion": "Confirma y registra reservas hechas", "area": "OPERACIONES", "critico": False},
            {"archivo": "seguimiento_cliente_viaje.py", "funcion": "Da seguimiento al cliente durante el viaje", "area": "VENTAS", "critico": False},
        ]
    }

# ─────────────────────────────────────────────
#  PASO 2 — BUSCAR EN CATALOGO (logica Clawbot)
# ─────────────────────────────────────────────

def _extraer_keywords(texto):
    """Extrae keywords normalizadas de un texto para matching."""
    texto = texto.lower().replace(".py", "").replace("_", " ")
    # Quitar palabras comunes sin valor semantico
    stopwords = {"de", "del", "la", "el", "los", "las", "un", "una", "en", "para",
                 "con", "por", "que", "se", "es", "al", "y", "o", "a", "e"}
    palabras = re.findall(r'[a-z0-9]+', texto)
    return set(p for p in palabras if p not in stopwords and len(p) > 2)

def buscar_en_catalogo(agentes_necesarios, catalogo):
    """
    Busca matches por keywords entre agentes necesarios y catalogo.
    Sin LLM — comparacion directa por palabras clave compartidas.
    Match si comparten 2+ keywords relevantes.
    """
    if not catalogo:
        return [], agentes_necesarios

    # Indexar catalogo por keywords
    catalogo_index = {}
    for archivo, info in catalogo.items():
        desc = info.get("descripcion", "")
        keywords = _extraer_keywords(archivo + " " + desc)
        catalogo_index[archivo] = keywords

    reutilizar = []
    crear = []

    for ag in agentes_necesarios:
        nombre = ag.get("archivo", "")
        funcion = ag.get("funcion", "")
        keywords_necesario = _extraer_keywords(nombre + " " + funcion)

        mejor_match = None
        mejor_score = 0

        for archivo_cat, keywords_cat in catalogo_index.items():
            # Contar keywords compartidas
            comunes = keywords_necesario & keywords_cat
            score = len(comunes)
            if score > mejor_score:
                mejor_score = score
                mejor_match = archivo_cat

        # Match si comparten 2+ keywords relevantes
        if mejor_score >= 2 and mejor_match:
            reutilizar.append({
                "necesario": nombre,
                "existente": mejor_match,
                "match": f"{mejor_score} keywords comunes"
            })
        else:
            crear.append(ag)

    return reutilizar, crear

# ─────────────────────────────────────────────
#  PASO 3 — CREAR AGENTE NUEVO
# ─────────────────────────────────────────────

def limpiar_codigo(texto):
    if "```python" in texto:
        return texto.split("```python")[1].split("```")[0].strip()
    if "```" in texto:
        return texto.split("```")[1].split("```")[0].strip()
    return texto.strip()

def validar_sintaxis(codigo):
    try:
        ast.parse(codigo)
        return True, None
    except SyntaxError as e:
        return False, str(e)

def probar_agente(ruta):
    try:
        r = subprocess.run(
            [sys.executable, ruta],
            capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=60  # Fix: 60s timeout
        )
        salida = (r.stdout or "").strip()
        if len(salida) < 5:
            return False, (r.stderr or "Output vacio")[:200]
        return True, salida[:200]
    except subprocess.TimeoutExpired:
        return False, "Timeout 60s"
    except Exception as e:
        return False, str(e)

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

def agregar_a_misiones(archivo, funcion, area):
    """
    Agrega un agente fallido a misiones.txt con file locking.
    Formato: archivo.py;instruccion
    """
    instruccion = f"Crear agente {area}: {funcion}"
    mision = f"{archivo};{instruccion}"
    try:
        # Abrir con locking para evitar race conditions
        modo = "r+" if os.path.exists(MISIONES) else "w+"
        with open(MISIONES, modo, encoding="utf-8", errors="replace") as f:
            _lock_file(f)
            try:
                existentes = set(l.strip() for l in f if l.strip())
                if mision not in existentes:
                    f.seek(0, 2)  # Ir al final
                    f.write(mision + "\n")
                    log("  [MISION] Agregado a misiones.txt: " + archivo)
            finally:
                _unlock_file(f)
    except Exception as e:
        log("  [WARN] No se pudo agregar a misiones: " + str(e))

def crear_agente(spec, contexto_negocio):
    """Crea agente con un solo intento y timeout de 60s en la prueba."""
    prompt = (
        "Crea un agente Python autonomo para este negocio.\n\n"
        "NEGOCIO: " + contexto_negocio + "\n"
        "ARCHIVO: " + spec["archivo"] + "\n"
        "FUNCION: " + spec["funcion"] + "\n"
        "AREA: " + spec.get("area", "HERRAMIENTAS") + "\n\n"
        "REGLAS ABSOLUTAS:\n"
        "1. Encabezado con AREA, DESCRIPCION, TECNOLOGIA\n"
        "2. NUNCA input() — usa sys.argv con defaults realistas\n"
        "3. Output minimo 5 lineas con datos concretos\n"
        "4. Solo stdlib: os, sys, json, datetime, math, re, random\n"
        "5. def main() + if __name__ == '__main__': main()\n"
        "6. try/except en main()\n"
        "7. Datos especificos y utiles para el negocio\n"
        "8. Si se beneficia de datos en tiempo real, usar:\n"
        "   try:\n"
        "       import web_bridge as web\n"
        "       WEB = web.WEB\n"
        "   except ImportError:\n"
        "       WEB = False\n\n"
        "DEVUELVE SOLO CODIGO PYTHON. Sin markdown. Sin explicaciones."
    )

    # Un solo intento — si falla, va a misiones.txt
    respuesta = ia(prompt)
    if not respuesta:
        return None
    codigo = limpiar_codigo(respuesta)
    valido, err = validar_sintaxis(codigo)
    if valido:
        return codigo
    log("    Sintaxis invalida: " + str(err)[:60])
    return None

# ─────────────────────────────────────────────
#  ARMAR CARPETA DEL PROYECTO
# ─────────────────────────────────────────────

def crear_carpeta_proyecto(slug):
    ruta = os.path.join(PROYECTOS, slug)
    os.makedirs(os.path.join(ruta, "agentes"), exist_ok=True)
    os.makedirs(os.path.join(ruta, "outputs"), exist_ok=True)
    return ruta

def copiar_agente_a_proyecto(archivo, carpeta_proyecto):
    origen = os.path.join(BASE_DIR, archivo)
    destino = os.path.join(carpeta_proyecto, "agentes", os.path.basename(archivo))
    if os.path.exists(origen):
        shutil.copy2(origen, destino)
        return True
    return False

# ─────────────────────────────────────────────
#  INFERIR PARAMETROS DEL NEGOCIO (LLM)
# ─────────────────────────────────────────────

def inferir_parametros_negocio(negocio):
    """
    Llama al LLM para obtener 3-5 parametros numericos tipicos del dominio
    con sus patrones regex para extraerlos de consultas en espanol.
    """
    prompt = (
        "Eres experto en sistemas de IA para negocios.\n\n"
        "NEGOCIO: " + negocio["nombre"] + "\n"
        "MODELO: " + negocio["modelo"] + "\n\n"
        "Identifica los 3-5 parametros numericos mas importantes que los clientes\n"
        "mencionan cuando hacen consultas a este negocio.\n\n"
        "Para cada parametro incluye:\n"
        "- nombre: identificador snake_case\n"
        "- patron: regex Python para extraerlo de texto en espanol (usa \\\\d, \\\\s, etc.)\n"
        "- tipo: 'int' o 'float'\n"
        "- default: valor por defecto como string numerico\n"
        "- unidad: descripcion breve (pesos, personas, noches, etc.)\n\n"
        "Ejemplos por tipo de negocio:\n"
        "- Agencia viajes: personas '(\\\\d+)\\\\s*personas?' int 2\n"
        "- Hipotecas: monto '\\\\$?\\\\s*(\\\\d+(?:[,\\\\.]\\\\d+)*)' float 2000000\n"
        "- Restaurante: comensales '(\\\\d+)\\\\s*(?:personas?|comensales?)' int 2\n"
        "- E-commerce: cantidad '(\\\\d+)\\\\s*(?:unidades?|piezas?)' int 1\n\n"
        'DEVUELVE SOLO JSON valido:\n'
        '[{"nombre":"personas","patron":"(\\\\d+)\\\\s*personas?","tipo":"int","default":"2","unidad":"personas"}]\n'
        "Sin texto antes ni despues."
    )
    for intento in range(2):
        respuesta = ia(prompt)
        if not respuesta:
            continue
        resultado = extraer_json(respuesta, "lista")
        if resultado and len(resultado) >= 2:
            log("  Params negocio inferidos: " + str([p.get("nombre") for p in resultado]))
            return resultado
        log("  Intento " + str(intento + 1) + " fallido al inferir params, reintentando...")
        time.sleep(2)

    log("  Fallback: usando parametros genericos")
    return [
        {"nombre": "monto",    "patron": r"\$?\s*(\d+(?:[,\.]\d+)*)",     "tipo": "float", "default": "1000",  "unidad": "pesos"},
        {"nombre": "cantidad", "patron": r"(\d+)\s*(?:unidades?|piezas?)", "tipo": "int",   "default": "1",     "unidad": "unidades"},
        {"nombre": "personas", "patron": r"(\d+)\s*personas?",             "tipo": "int",   "default": "1",     "unidad": "personas"},
    ]


def _generar_codigo_extraer_params(params_lista):
    """
    Genera el cuerpo de la funcion extraer_parametros() con los patrones
    especificos del dominio inferidos por el LLM.
    Devuelve un string de codigo Python con indentacion de 4 espacios.
    """
    L = []
    for p in params_lista:
        nombre = p.get("nombre", "param")
        patron = p.get("patron", r"\d+")
        tipo   = p.get("tipo", "float")
        L.append("    # " + nombre.upper())
        L.append("    m = re.search(" + repr(patron) + ", consulta_lower)")
        L.append("    if m:")
        if tipo == "int":
            L.append("        params['" + nombre + "'] = int(m.group(1).replace(',', '').replace('.', ''))")
        else:
            L.append("        params['" + nombre + "'] = float(m.group(1).replace(',', ''))")
        L.append("")

    L.append("    # Defaults del dominio")
    for p in params_lista:
        nombre  = p.get("nombre", "param")
        default = p.get("default", "0")
        tipo    = p.get("tipo", "float")
        try:
            dv = str(int(default)) if tipo == "int" else str(float(default))
        except Exception:
            dv = repr(default)
        L.append("    params.setdefault('" + nombre + "', " + dv + ")")

    L.append("")
    L.append("    log('Params: ' + str(params))")
    L.append("    return params")
    return "\n".join(L)


def generar_orquestador_proyecto(negocio, agentes_disponibles, carpeta):
    """
    Genera orquestador estilo Clawbot para el proyecto:
    extraccion de params con regex especificos del dominio, memoria de sesion,
    deteccion de seguimiento, director + equipo de agentes.
    """
    log("  Infiriendo parametros especificos del dominio...")
    params_lista = inferir_parametros_negocio(negocio)

    nombre_neg  = negocio["nombre"].replace('"', '\\"')
    modelo_neg  = negocio["modelo"].replace('"', '\\"').replace('\n', ' ')
    lista_str   = json.dumps(agentes_disponibles, ensure_ascii=False)
    params_code = _generar_codigo_extraer_params(params_lista)

    L = []
    # ── Encabezado ─────────────────────────────────────────
    L.append('"""')
    L.append('AREA: CEREBRO')
    L.append('DESCRIPCION: Orquestador de ' + nombre_neg + ' v1.0 — Clawbot-style')
    L.append('             Memoria de sesion, params con regex, deteccion de seguimiento.')
    L.append('TECNOLOGIA: llm_router, subprocess, re')
    L.append('"""')
    L.append('')
    L.append('import os')
    L.append('import sys')
    L.append('import re')
    L.append('import json')
    L.append('import time')
    L.append('import subprocess')
    L.append('from datetime import datetime')
    L.append('')
    L.append('try:')
    L.append('    import web_bridge as web')
    L.append('    WEB = web.WEB')
    L.append('except ImportError:')
    L.append('    WEB = False')
    L.append('')
    L.append('if hasattr(sys.stdout, "reconfigure"):')
    L.append('    sys.stdout.reconfigure(encoding="utf-8", errors="replace")')
    L.append('elif hasattr(sys.stdout, "buffer"):')
    L.append('    sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)')
    L.append('')
    L.append('try:')
    L.append('    from llm_router import completar_simple as ia')
    L.append('except ImportError:')
    L.append('    from groq import Groq')
    L.append('    _g = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))')
    L.append('    def ia(prompt, **kw):')
    L.append('        r = _g.chat.completions.create(')
    L.append('            model="llama-3.3-70b-versatile",')
    L.append('            messages=[{"role": "user", "content": prompt}],')
    L.append('            temperature=0.3, max_tokens=2000')
    L.append('        )')
    L.append('        return r.choices[0].message.content.strip()')
    L.append('')
    # ── Constantes ─────────────────────────────────────────
    L.append('BASE    = os.path.dirname(os.path.abspath(__file__))')
    L.append('NOMBRE  = "' + nombre_neg + '"')
    L.append('MODELO  = "' + modelo_neg + '"')
    L.append('AGENTES = ' + lista_str)
    L.append('')
    L.append('MAX_AGENTES    = 4')
    L.append('TIMEOUT_AGENTE = 45')
    L.append('')
    # ── log ────────────────────────────────────────────────
    L.append('def log(msg):')
    L.append('    ts = datetime.now().strftime("%H:%M:%S")')
    L.append('    print(f"[{ts}] [{NOMBRE[:14]}] {msg}", flush=True)')
    L.append('')
    # ── extraer_parametros ─────────────────────────────────
    L.append('# ============================================')
    L.append('# EXTRACCION DE PARAMETROS — DOMINIO ESPECIFICO')
    L.append('# ============================================')
    L.append('def extraer_parametros(consulta, params_previos=None):')
    L.append('    """Extrae parametros numericos del dominio de ' + nombre_neg + '."""')
    L.append('    consulta_lower = consulta.lower()')
    L.append('    params = dict(params_previos) if params_previos else {}')
    L.append('')
    L.append(params_code)
    L.append('')
    # ── es_seguimiento ─────────────────────────────────────
    L.append('# ============================================')
    L.append('# DETECCION DE SEGUIMIENTO')
    L.append('# ============================================')
    L.append('def es_seguimiento(consulta, historial):')
    L.append('    if not historial:')
    L.append('        return False')
    L.append('    indicadores = [')
    L.append('        "y si", "que pasa si", "que pasaria si", "y con", "ahora con",')
    L.append('        "cambia", "baja", "sube", "reduce", "aumenta", "y para",')
    L.append('        "en cambio", "en vez", "en lugar", "y si fuera", "mejor con"')
    L.append('    ]')
    L.append('    return any(ind in consulta.lower() for ind in indicadores)')
    L.append('')
    # ── extraer_numeros_clave ──────────────────────────────
    L.append('# ============================================')
    L.append('# EXTRACCION INTELIGENTE DE NUMEROS')
    L.append('# ============================================')
    L.append('def extraer_numeros_clave(output_raw):')
    L.append('    if not output_raw:')
    L.append('        return "[Sin output]"')
    L.append('    lineas = output_raw.split("\\n")')
    L.append('    nums, resumen = [], []')
    L.append('    for ln in lineas:')
    L.append('        s = ln.strip()')
    L.append('        if not s: continue')
    L.append('        if re.search(r\'\\$[\\d,]+|\\d+[\\.,]\\d+%?|\\d{4,}\', s):')
    L.append('            nums.append(s)')
    L.append('        elif any(kw in s.lower() for kw in [')
    L.append('            "total", "pago", "mensual", "roi", "flujo", "costo",')
    L.append('            "recomend", "resultado", "ganancia", "precio", "subtotal"')
    L.append('        ]):')
    L.append('            resumen.append(s)')
    L.append('    resultado = resumen[:5] + nums[:10]')
    L.append('    return "\\n".join(resultado) if resultado else "\\n".join(lineas[:15])')
    L.append('')
    # ── clase OrquestadorProyecto ──────────────────────────
    L.append('# ============================================')
    L.append('# ORQUESTADOR PRINCIPAL')
    L.append('# ============================================')
    L.append('class OrquestadorProyecto:')
    L.append('')
    L.append('    def __init__(self):')
    L.append('        self.memoria_equipo = []')
    L.append('        self.historial      = []')
    L.append('        self.params_previos = None')
    L.append('        self.sesion_id      = str(int(time.time()))[-6:]')
    L.append('')
    # director_seleccionar
    L.append('    def director_seleccionar(self, consulta, params, contexto_previo=""):')
    L.append('        agentes_txt = "\\n".join([f"- {a}" for a in AGENTES])')
    L.append('        params_txt  = " | ".join([f"{k}={v}" for k, v in params.items()])')
    L.append('        ctx_txt     = f"\\nCONTEXTO PREVIO:\\n{contexto_previo}" if contexto_previo else ""')
    L.append('        prompt = (')
    L.append('            f"Eres director de {NOMBRE}.\\n"')
    L.append('            f"Negocio: {MODELO}\\n"')
    L.append('            f"Consulta del cliente: {consulta}\\n"')
    L.append('            f"Parametros extraidos: {params_txt}\\n"')
    L.append('            f"{ctx_txt}\\n"')
    L.append('            f"Agentes disponibles:\\n{agentes_txt}\\n\\n"')
    L.append('            f"Selecciona max {MAX_AGENTES} agentes mas utiles. "')
    L.append('            "Para cada uno define los argumentos concretos de sys.argv.\\n"')
    L.append('            \'RESPONDE SOLO este JSON:\\n\'')
    L.append('            \'{"analisis":"que pide el usuario en 1 frase","subtareas":[\'')
    L.append('            \'{"paso":1,"agente":"agentes/archivo.py","objetivo":"que logra","parametros":"args exactos"}\'')
    L.append('            \']}\' ')
    L.append('        )')
    L.append('        respuesta = ia(prompt)')
    L.append('        if not respuesta:')
    L.append('            return None')
    L.append('        if "```" in respuesta:')
    L.append('            for parte in respuesta.split("```"):')
    L.append('                if "{" in parte:')
    L.append('                    respuesta = parte.strip().lstrip("json").strip()')
    L.append('                    break')
    L.append('        try:')
    L.append('            return json.loads(respuesta.strip())')
    L.append('        except Exception as e:')
    L.append('            log(f"Error parseando plan: {e}")')
    L.append('            return None')
    L.append('')
    # ejecutar_agente
    L.append('    def ejecutar_agente(self, archivo, parametros=""):')
    L.append('        ruta = os.path.join(BASE, archivo)')
    L.append('        if not os.path.exists(ruta):')
    L.append('            log(f"[WARN] No existe: {ruta}")')
    L.append('            return False, f"[ERROR] {archivo} no existe"')
    L.append('        cmd = [sys.executable, ruta]')
    L.append('        if parametros and parametros.strip():')
    L.append('            cmd.extend(parametros.split())')
    L.append('        try:')
    L.append('            r = subprocess.run(')
    L.append('                cmd, capture_output=True, text=True,')
    L.append('                encoding="utf-8", errors="replace",')
    L.append('                timeout=TIMEOUT_AGENTE, cwd=BASE')
    L.append('            )')
    L.append('            salida = r.stdout.strip()')
    L.append('            if not salida and r.stderr:')
    L.append('                return False, f"[ERROR] {r.stderr[:200]}"')
    L.append('            return True, salida or "[Sin output]"')
    L.append('        except subprocess.TimeoutExpired:')
    L.append('            return False, f"[TIMEOUT] {archivo} > {TIMEOUT_AGENTE}s"')
    L.append('        except Exception as e:')
    L.append('            return False, f"[ERROR] {e}"')
    L.append('')
    # interpretar_aporte
    L.append('    def interpretar_aporte(self, subtarea, output_raw):')
    L.append('        memoria_txt = ""')
    L.append('        for m in self.memoria_equipo:')
    L.append('            memoria_txt += f\'\\n[{m["agente"]}]: {m["aporte"][:200]}\'')
    L.append('        output_limpio = extraer_numeros_clave(output_raw)')
    L.append('        prompt = (')
    L.append('            f"Agente especialista en {NOMBRE}.\\n"')
    L.append('            f"Rol: {subtarea[\'objetivo\']}\\n"')
    L.append('            f"Equipo sabe:{memoria_txt if memoria_txt else \' (eres el primero)\'}\\n\\n"')
    L.append('            f"Datos:\\n{output_limpio}\\n\\n"')
    L.append('            "Extrae 3-5 datos clave con numeros exactos. Max 100 palabras. Sin markdown."')
    L.append('        )')
    L.append('        return ia(prompt) or output_limpio[:300]')
    L.append('')
    # director_sintetizar
    L.append('    def director_sintetizar(self, consulta, params, contexto_previo=""):')
    L.append('        aportes_txt = ""')
    L.append('        for m in self.memoria_equipo:')
    L.append('            aportes_txt += f\'\\n\\n[{m["agente"]}]\\n{m["aporte"]}\'')
    L.append('        params_txt = " | ".join([f"{k}={v}" for k, v in params.items()])')
    L.append('        ctx_txt    = f"\\nCONTEXTO PREVIO:\\n{contexto_previo}" if contexto_previo else ""')
    L.append('        prompt = (')
    L.append('            f"Director de {NOMBRE} ({MODELO}).\\n"')
    L.append('            f"CONSULTA: {consulta}\\n"')
    L.append('            f"PARAMETROS: {params_txt}\\n"')
    L.append('            f"{ctx_txt}\\n"')
    L.append('            f"APORTES:{aportes_txt}\\n\\n"')
    L.append('            "Responde directamente al cliente:\\n"')
    L.append('            "1. Resumen con 3 datos clave\\n"')
    L.append('            "2. Analisis: conviene? por que?\\n"')
    L.append('            "3. Recomendacion concreta en 1-2 lineas\\n"')
    L.append('            "Max 250 palabras. Sin frases genericas. Sin nombres de archivos."')
    L.append('        )')
    L.append('        fallback = "\\n".join([f"• {m[\'agente\']}: {m[\'aporte\']}" for m in self.memoria_equipo])')
    L.append('        return ia(prompt) or fallback')
    L.append('')
    # construir_contexto
    L.append('    def construir_contexto(self):')
    L.append('        if not self.historial:')
    L.append('            return ""')
    L.append('        ctx = []')
    L.append('        for h in self.historial[-3:]:')
    L.append('            ctx.append(f"Consulta: {h[\'consulta\']}\\nResultado: {h[\'resumen\'][:200]}")')
    L.append('        return "\\n\\n".join(ctx)')
    L.append('')
    # respuesta_directa
    L.append('    def respuesta_directa(self, consulta, contexto=""):')
    L.append('        ctx_txt = f"\\nContexto previo:\\n{contexto}" if contexto else ""')
    L.append('        prompt = f"Eres experto en {NOMBRE} ({MODELO}).{ctx_txt}\\nConsulta: {consulta}\\nDatos concretos. Max 200 palabras."')
    L.append('        return ia(prompt) or "No pude procesar la consulta."')
    L.append('')
    # procesar
    L.append('    def procesar(self, consulta):')
    L.append('        print(f"\\n{\'-\'*55}")')
    L.append('        print(f"[{NOMBRE}] {consulta[:70]}...")')
    L.append('        log(f"Consulta: {consulta[:100]}")')
    L.append('')
    L.append('        seguimiento = es_seguimiento(consulta, self.historial)')
    L.append('        contexto    = self.construir_contexto()')
    L.append('')
    L.append('        if seguimiento and self.params_previos:')
    L.append('            log("Seguimiento detectado — heredando params previos")')
    L.append('            params = extraer_parametros(consulta, self.params_previos)')
    L.append('        else:')
    L.append('            params = extraer_parametros(consulta)')
    L.append('        self.params_previos = params')
    L.append('')
    L.append('        plan = self.director_seleccionar(consulta, params, contexto if seguimiento else "")')
    L.append('        if not plan:')
    L.append('            resultado = self.respuesta_directa(consulta, contexto)')
    L.append('            self.historial.append({"consulta": consulta, "resumen": resultado[:200], "params": params})')
    L.append('            return resultado')
    L.append('')
    L.append('        subtareas = plan.get("subtareas", [])')
    L.append('        analisis  = plan.get("analisis", "")')
    L.append('')
    L.append('        if not subtareas:')
    L.append('            resultado = self.respuesta_directa(consulta, contexto)')
    L.append('            self.historial.append({"consulta": consulta, "resumen": resultado[:200], "params": params})')
    L.append('            return resultado')
    L.append('')
    L.append('        equipo_str = " -> ".join([s["agente"] for s in subtareas])')
    L.append('        print(f"   Equipo: {equipo_str}")')
    L.append('        print(f"   {analisis}")')
    L.append('        if seguimiento:')
    L.append('            print("   (Continuando conversacion previa)")')
    L.append('')
    L.append('        self.memoria_equipo = []')
    L.append('        agentes_fallidos    = []')
    L.append('')
    L.append('        for subtarea in subtareas:')
    L.append('            paso       = subtarea["paso"]')
    L.append('            agente     = subtarea["agente"]')
    L.append('            params_str = subtarea.get("parametros", "")')
    L.append('            print(f"\\n   [{paso}/{len(subtareas)}] {agente}")')
    L.append('            if params_str:')
    L.append('                print(f"   Args: {params_str}")')
    L.append('')
    L.append('            exito, output_raw = self.ejecutar_agente(agente, params_str)')
    L.append('            if not exito:')
    L.append('                log(f"[WARN] {agente} fallo: {output_raw[:80]}")')
    L.append('                agentes_fallidos.append(agente)')
    L.append('                continue')
    L.append('')
    L.append('            aporte = self.interpretar_aporte(subtarea, output_raw)')
    L.append('            self.memoria_equipo.append({"paso": paso, "agente": agente, "aporte": aporte})')
    L.append('            print(f"   [OK] {aporte[:100]}...")')
    L.append('            time.sleep(0.5)')
    L.append('')
    L.append('        if agentes_fallidos:')
    L.append('            log(f"Fallaron: {\', \'.join(agentes_fallidos)}")')
    L.append('')
    L.append('        if not self.memoria_equipo:')
    L.append('            resultado = self.respuesta_directa(consulta, contexto)')
    L.append('        else:')
    L.append('            print("\\n   Sintetizando...")')
    L.append('            resultado = self.director_sintetizar(consulta, params, contexto if seguimiento else "")')
    L.append('')
    L.append('        self.historial.append({')
    L.append('            "consulta": consulta,')
    L.append('            "resumen":  (resultado or "")[:300],')
    L.append('            "params":   params,')
    L.append('            "equipo":   equipo_str')
    L.append('        })')
    L.append('        log(f"Completado. Equipo: {equipo_str}")')
    L.append('        return resultado')
    L.append('')
    # mostrar_historial
    L.append('    def mostrar_historial(self):')
    L.append('        if not self.historial:')
    L.append('            print("Sin historial en esta sesion.")')
    L.append('            return')
    L.append('        print(f"\\n{\'-\'*55}")')
    L.append('        print(f"HISTORIAL ({len(self.historial)} consultas):")')
    L.append('        for i, h in enumerate(self.historial, 1):')
    L.append('            params_txt = " | ".join([f"{k}={v}" for k, v in h["params"].items()])')
    L.append('            print(f"\\n[{i}] {h[\'consulta\'][:60]}")')
    L.append('            print(f"    Equipo: {h.get(\'equipo\', \'directo\')}")')
    L.append('            print(f"    Params: {params_txt}")')
    L.append('')
    # ── Punto de entrada ───────────────────────────────────
    L.append('# ============================================')
    L.append('# PUNTO DE ENTRADA')
    L.append('# ============================================')
    L.append('if __name__ == "__main__":')
    L.append('    if len(sys.argv) > 1 and sys.argv[1] not in ("--interactive", "-i"):')
    L.append('        orq = OrquestadorProyecto()')
    L.append('        print("\\n" + "="*55)')
    L.append('        print(NOMBRE + " — Sistema de IA")')
    L.append('        print("="*55)')
    L.append('        resultado = orq.procesar(" ".join(sys.argv[1:]))')
    L.append('        print("\\n" + resultado)')
    L.append('        print("="*55)')
    L.append('    else:')
    L.append('        orq = OrquestadorProyecto()')
    L.append('        print("+" + "="*53 + "+")')
    L.append('        print(f"|  {NOMBRE:<51}  |")')
    L.append('        print(f"|  {MODELO[:51]:<51}  |")')
    L.append('        print("+" + "="*53 + "+")')
    L.append('        print("|  \'historial\' -> ver consultas previas         |")')
    L.append('        print("|  \'equipo\'    -> ver ultimo equipo             |")')
    L.append('        print("|  \'salir\'     -> terminar                      |")')
    L.append('        print("+" + "="*53 + "+\\n")')
    L.append('        while True:')
    L.append('            try:')
    L.append('                consulta = input("Consulta: ").strip()')
    L.append('                if not consulta: continue')
    L.append('                if consulta.lower() in ("salir", "exit", "quit"): break')
    L.append('                if consulta.lower() == "equipo":')
    L.append('                    for m in orq.memoria_equipo:')
    L.append('                        print(f"  [{m[\'paso\']}] {m[\'agente\']} -> {m[\'aporte\'][:100]}")')
    L.append('                    continue')
    L.append('                if consulta.lower() == "historial":')
    L.append('                    orq.mostrar_historial()')
    L.append('                    continue')
    L.append('                resultado = orq.procesar(consulta)')
    L.append('                print(f"\\n{\'=\'*55}")')
    L.append('                print(resultado)')
    L.append('                print(f"{\'=\'*55}\\n")')
    L.append('            except KeyboardInterrupt:')
    L.append('                print(f"\\n[{NOMBRE}] Apagado.")')
    L.append('                break')

    codigo = "\n".join(L)

    ruta = os.path.join(carpeta, "orquestador.py")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(codigo)
    log("Orquestador Clawbot-style generado: " + ruta)
    return ruta

def generar_readme(negocio, reutilizados, creados, carpeta):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')
    lineas = [
        "# " + negocio["nombre"] + " — Sistema de IA",
        "Generado por Agencia Santi — " + ts,
        "",
        "## Modelo de Negocio",
        negocio["modelo"],
        "",
        "## Dominio",
        str(negocio.get("dominio") or "No especificado"),
        "",
        "## Agentes Reutilizados del Catalogo (" + str(len(reutilizados)) + ")",
    ]
    for r in reutilizados:
        lineas.append("- " + r.get("existente", "") + " -> cubre: " + r.get("necesario", ""))
    lineas += ["", "## Agentes Nuevos Creados (" + str(len(creados)) + ")"]
    for c in creados:
        lineas.append("- " + c.get("archivo", ""))
    lineas += [
        "",
        "## Uso",
        "```",
        "cd proyectos/" + negocio["slug"],
        "python orquestador.py 'quiero ir a japon en marzo para 2 personas'",
        "```",
    ]
    with open(os.path.join(carpeta, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

# ─────────────────────────────────────────────
#  FLUJO PRINCIPAL
# ─────────────────────────────────────────────

def crear_proyecto(descripcion):
    log("=" * 55)
    log("ORQUESTADOR DE PROYECTOS v2.0")
    log("=" * 55)

    # PASO 1: Analizar negocio
    log("Paso 1/5 — Analizando el negocio...")
    negocio = analizar_negocio(descripcion)
    if not negocio:
        log("ERROR: No pude analizar la descripcion.")
        return None

    nombre = negocio["nombre"]
    # Fix: slug limpio — quitar caracteres raros, doble underscore, trailing _
    slug_raw = negocio.get("slug", nombre)
    slug = re.sub(r'[^a-z0-9]', '_', slug_raw.lower())
    slug = re.sub(r'_+', '_', slug).strip('_')  # sin __ ni _ al inicio/final
    if not slug:
        slug = "proyecto_" + datetime.now().strftime("%Y%m%d%H%M%S")
    log("Negocio: " + nombre + " (" + slug + ")")
    log("Modelo: " + negocio["modelo"])
    log("Agentes necesarios: " + str(len(negocio["agentes_necesarios"])))

    # PASO 2: Buscar en catalogo
    log("\nPaso 2/5 — Buscando en catalogo actual...")
    catalogo = cargar_catalogo()
    log("Catalogo actual: " + str(len(catalogo)) + " agentes")

    reutilizar, crear = buscar_en_catalogo(negocio["agentes_necesarios"], catalogo)
    log("Reutilizar: " + str(len(reutilizar)) + " | Crear nuevos: " + str(len(crear)))

    for r in reutilizar:
        log("  [OK] Reutilizar " + r.get("existente", "") + " para " + r.get("necesario", ""))
    for c in crear:
        log("  [+] Crear nuevo: " + c.get("archivo", ""))

    # PASO 3: Crear carpeta
    log("\nPaso 3/5 — Creando carpeta del proyecto...")
    carpeta = crear_carpeta_proyecto(slug)
    log("Carpeta: proyectos/" + slug + "/")

    agentes_en_proyecto = []

    # Copiar reutilizados
    for r in reutilizar:
        archivo = r.get("existente", "")
        if copiar_agente_a_proyecto(archivo, carpeta):
            agentes_en_proyecto.append("agentes/" + os.path.basename(archivo))
            log("  Copiado: " + archivo)

    # PASO 4: Crear agentes nuevos
    log("\nPaso 4/5 — Creando agentes nuevos...")
    contexto = nombre + " — " + negocio["modelo"]
    agentes_creados = []

    for spec in crear:
        archivo = spec.get("archivo", "")
        if not archivo:
            continue
        log("  Creando " + archivo + "...")
        codigo = crear_agente(spec, contexto)

        if not codigo:
            log("  [ERROR] No se pudo crear " + archivo + " — enviando a misiones")
            agregar_a_misiones(archivo, spec.get("funcion", ""), spec.get("area", "HERRAMIENTAS"))
            continue

        # Guardar en proyecto
        ruta_proyecto = os.path.join(carpeta, "agentes", archivo)
        with open(ruta_proyecto, "w", encoding="utf-8") as f:
            f.write(codigo)

        # Probar con 60s timeout
        exito, output = probar_agente(ruta_proyecto)

        if not exito:
            log("  [FAIL] " + archivo + " — " + output[:60] + " — enviando a misiones")
            agregar_a_misiones(archivo, spec.get("funcion", ""), spec.get("area", "HERRAMIENTAS"))
            continue

        log("  [OK] " + archivo + " — " + output[:60])

        # Copiar al BASE_DIR y registrar en catalogo global
        ruta_global = os.path.join(BASE_DIR, archivo)
        shutil.copy2(ruta_proyecto, ruta_global)

        catalogo[archivo] = {
            "descripcion": spec.get("funcion", ""),
            "categoria": spec.get("area", "HERRAMIENTAS"),
            "salud": "OK",
            "tecnologia": ["Python estandar"],
            "ultima_actualizacion": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "ordenes": [archivo.replace(".py", "").replace("_", " ")]
        }
        agentes_creados.append(spec)
        agentes_en_proyecto.append("agentes/" + archivo)
        time.sleep(1)

    # Actualizar catalogo global
    if agentes_creados:
        guardar_catalogo(catalogo)
        log("Catalogo actualizado: +" + str(len(agentes_creados)) + " agentes nuevos")

    # PASO 5: Orquestador y README
    log("\nPaso 5/5 — Generando orquestador y README...")
    generar_orquestador_proyecto(negocio, agentes_en_proyecto, carpeta)
    generar_readme(negocio, reutilizar, agentes_creados, carpeta)

    log("\n" + "=" * 55)
    log("PROYECTO LISTO: " + nombre)
    log("Carpeta:  proyectos/" + slug + "/")
    log("Agentes reutilizados: " + str(len(reutilizar)))
    log("Agentes nuevos: " + str(len(agentes_creados)))
    log("Total en proyecto: " + str(len(agentes_en_proyecto)))
    log("=" * 55)
    log("")
    log("Para probar:")
    log("  cd proyectos/" + slug)
    log("  python orquestador.py 'quiero ir a japon en marzo 2 personas presupuesto 3000 dolares'")

    return {
        "nombre": nombre,
        "slug": slug,
        "carpeta": carpeta,
        "reutilizados": len(reutilizar),
        "creados": len(agentes_creados),
        "total": len(agentes_en_proyecto)
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        descripcion = " ".join(sys.argv[1:])
    else:
        print("Uso: python orquestador_proyectos.py 'descripcion del negocio'")
        print("")
        print("Ejemplo:")
        print("  python orquestador_proyectos.py 'agencia de viajes Way2TheUnknown,")
        print("  cobra 8% de fee, atiende mercado mexicano e internacional'")
        sys.exit(0)

    crear_proyecto(descripcion)