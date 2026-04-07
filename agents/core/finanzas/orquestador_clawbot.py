"""
ÁREA: CEREBRO
DESCRIPCIÓN: Orquestador estilo Clawbot v4.0. Memoria entre órdenes, extracción
             de parámetros con regex, detección de órdenes de seguimiento,
             recorte inteligente de outputs, validación de agentes con fallback,
             historial de sesión completo. Sin agentes hardcodeados.
TECNOLOGÍA: llm_router (multi-proveedor), habilidades.json, regex
"""

import os
import sys
import re
import json
import time
import subprocess
import io as _io
from datetime import datetime

try:
    import agencia.agents.herramientas.web_bridge as web
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

# ============================================================
# ROUTER
# ============================================================
try:
    from agencia.agents.cerebro.llm_router import completar_simple
    def ia_call(prompt, temperatura=0.3, max_tokens=1500):
        try:
            return completar_simple(prompt)
        except Exception as e:
            log(f"Error router: {e}")
            return None
except ImportError:
    from groq import Groq
    _groq = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
    def ia_call(prompt, temperatura=0.3, max_tokens=1500):
        try:
            resp = _groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperatura,
                max_tokens=max_tokens,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            log(f"Error Groq: {e}")
            return None

try:
    import agencia.agents.herramientas.bus_mensajes as bus
    BUS_DISPONIBLE = True
except ImportError:
    BUS_DISPONIBLE = False

# ============================================================
# CONFIGURACIÓN
# ============================================================
LOG            = "registro_noche.txt"
ARCHIVO_HAB    = "habilidades.json"
MAX_AGENTES    = 4
TIMEOUT_AGENTE = 45

# ============================================================
# LOGGING
# ============================================================
def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    linea = f"[{ts}] [CLAWBOT] {msg}"
    print(linea)
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(linea + "\n")
    except Exception:
        pass

# ============================================================
# EXTRACTOR DE PARÁMETROS CON REGEX
# ============================================================
def extraer_parametros(orden, params_previos=None):
    """
    Extrae parámetros numéricos con regex.
    Si hay params_previos (orden de seguimiento), los hereda y solo
    actualiza los que cambien en la nueva orden.
    """
    orden_lower = orden.lower()
    params = dict(params_previos) if params_previos else {}

    # MONTO
    for patron in [
        r'(\d+(?:\.\d+)?)\s*m(?:illones?|dp|xn)?\b',
        r'\$?\s*(\d{1,3}(?:[,\.]\d{3})+)',
        r'\$?\s*(\d{6,})',
    ]:
        m = re.search(patron, orden_lower)
        if m:
            val = float(m.group(1).replace(',', '').replace('.', ''))
            if val < 10000:  # Es multiplicador "2M"
                val *= 1_000_000
            params['monto'] = val
            break

    # TASA — asociada a %, "tasa", "interés"
    for patron in [
        r'(?:tasa|interés|interes|al)\s+(?:del?\s+)?(\d+(?:\.\d+)?)\s*%',
        r'(\d+(?:\.\d+)?)\s*%\s*(?:anual|de\s+inter)',
        r'baj[ae]\s+(?:la\s+tasa\s+)?(?:a\s+)?(\d+(?:\.\d+)?)\s*%',
        r'tasa\s+(?:de\s+)?(\d+(?:\.\d+)?)',
    ]:
        m = re.search(patron, orden_lower)
        if m:
            params['tasa'] = float(m.group(1))
            break

    # PLAZO — asociado a "años", "plazo"
    for patron in [
        r'(?:a\s+)?(\d+)\s*años?\b',
        r'plazo\s+(?:de\s+)?(\d+)',
    ]:
        m = re.search(patron, orden_lower)
        if m:
            val = int(m.group(1))
            if 1 <= val <= 40:
                params['plazo'] = val
                break

    # RENTA
    for patron in [
        r'renta\s+(?:de\s+)?\$?\s*(\d+(?:[,\.]\d+)*)',
        r'\$?\s*(\d+(?:[,\.]\d+)*)\s*(?:de\s+)?renta',
    ]:
        m = re.search(patron, orden_lower)
        if m:
            params['renta'] = float(m.group(1).replace(',', ''))
            break

    # DEFAULTS
    monto = params.get('monto', 2_000_000)
    params.setdefault('tasa',   10.5)
    params.setdefault('plazo',  20)
    params.setdefault('renta',  monto * 0.007)
    params.setdefault('seguro', 500)

    log(f"Params: monto=${params['monto']:,.0f} | tasa={params['tasa']}% | plazo={params['plazo']}a | renta=${params['renta']:,.0f}/mes")
    return params

# ============================================================
# DETECCIÓN DE ORDEN DE SEGUIMIENTO
# ============================================================
def es_seguimiento(orden, historial):
    """
    Detecta si la orden hace referencia a una conversación previa.
    Ej: "¿y si bajo la tasa a 8%?", "¿qué pasa si pago 30% de enganche?"
    """
    if not historial:
        return False
    indicadores = [
        "y si", "qué pasa si", "que pasa si", "y con", "ahora con",
        "cambia", "baja", "sube", "reduce", "aumenta", "mejor con",
        "peor con", "en cambio", "en vez", "en lugar"
    ]
    orden_lower = orden.lower()
    return any(ind in orden_lower for ind in indicadores)

# ============================================================
# EXTRACCIÓN INTELIGENTE DE NÚMEROS DEL OUTPUT
# ============================================================
def extraer_numeros_clave(output_raw, max_chars=600):
    """
    En lugar de cortar el output a X caracteres (perdiendo datos útiles),
    extrae las líneas que contienen números relevantes.
    """
    if not output_raw:
        return "[Sin output]"

    lineas = output_raw.split('\n')
    lineas_con_numeros = []
    lineas_resumen = []

    for linea in lineas:
        linea_strip = linea.strip()
        if not linea_strip:
            continue
        # Priorizar líneas con $ o números con comas o porcentajes
        if re.search(r'\$[\d,]+|\d+[\.,]\d+%?|\d{4,}', linea_strip):
            lineas_con_numeros.append(linea_strip)
        # También tomar líneas de resumen/total
        elif any(kw in linea_strip.lower() for kw in [
            'total', 'pago', 'mensual', 'roi', 'flujo', 'interés',
            'recomend', 'resultado', 'costo', 'ganancia', 'pérdida'
        ]):
            lineas_resumen.append(linea_strip)

    # Combinar: resumen primero, luego números
    resultado = lineas_resumen[:5] + lineas_con_numeros[:10]

    if resultado:
        return '\n'.join(resultado)
    # Fallback: primeras líneas del output
    return '\n'.join(lineas[:15])

# ============================================================
# CATÁLOGO DINÁMICO
# ============================================================
def cargar_catalogo():
    if not os.path.exists(ARCHIVO_HAB):
        return {}
    try:
        with open(ARCHIVO_HAB, "r", encoding="utf-8", errors="replace") as f:
            habilidades = json.load(f)
    except Exception:
        return {}

    catalogo = {}
    for archivo, info in habilidades.items():
        if not archivo.endswith(".py") or not os.path.exists(archivo):
            continue
        salud = info.get("salud", "OK")
        if "CRITICO" in salud or "Sintaxis" in salud:
            continue
        catalogo[archivo] = {
            "area":        info.get("categoria", "HERRAMIENTAS"),
            "descripcion": info.get("descripcion", "Agente especializado"),
            "salud":       salud
        }

    log(f"Catálogo: {len(catalogo)} agentes disponibles.")
    return catalogo

# ============================================================
# CLASE PRINCIPAL
# ============================================================
class OrquestadorClawbot:

    def __init__(self):
        self.memoria_equipo  = []      # Memoria del equipo en la orden actual
        self.historial       = []      # Historial de todas las órdenes de la sesión
        self.params_previos  = None    # Parámetros de la orden anterior
        self.sesion_id       = str(int(time.time()))[-6:]
        self.catalogo        = cargar_catalogo()

    # -- DIRECTOR: Selecciona agentes --------------------------------------
    def director_seleccionar(self, orden, params, contexto_previo=""):
        catalogo_txt = ""
        for archivo, info in self.catalogo.items():
            catalogo_txt += f"\n- {archivo} [{info['area']}]: {info['descripcion']}"

        monto  = params['monto']
        tasa   = params['tasa']
        plazo  = params['plazo']
        renta  = params['renta']
        seguro = params['seguro']
        gastos = renta * 0.2
        predial = monto * 0.01

        # Parámetros pre-calculados para cada agente
        tabla_params = {
            "simulador_hipoteca.py":          f"{monto:.0f} {tasa} {plazo} {seguro:.0f}",
            "calculadora_roi_mexico.py":       f"{monto:.0f} {renta:.0f} {gastos:.0f} {predial:.0f}",
            "calculadora_roi.py":              f"{monto:.0f} {renta:.0f} {gastos:.0f} {predial:.0f}",
            "calculadora_isr_basica.py":       f"{renta:.0f} 0 0.25",
            "clasificador_viviendas.py":       f"{monto:.0f}",
            "generador_copy_propiedades.py":   f"80 Polanco {monto:.0f}",
            "generador_fichas_tecnicas.py":    f"80 2 {monto:.0f} Polanco",
            "asistente_iva.py":                f"{monto:.0f}",
            "proyeccion_utilidades.py":        "",
            "buscador_plusvalia.py":           "",
            "analizador_balances.py":          "",
        }

        tabla_txt = "\n".join([f"  {k}: \"{v}\"" for k, v in tabla_params.items()])

        contexto_txt = f"\nCONTEXTO PREVIO DE LA SESIÓN:\n{contexto_previo}" if contexto_previo else ""

        prompt = f"""Eres el Director de una agencia de IA.

ORDEN: "{orden}"
PARÁMETROS EXTRAÍDOS: monto=${monto:,.0f} | tasa={tasa}% | plazo={plazo} años | renta=${renta:,.0f}/mes
{contexto_txt}

PARÁMETROS LISTOS (usa estos exactos):
{tabla_txt}

AGENTES DISPONIBLES:{catalogo_txt}

Selecciona máximo {MAX_AGENTES} agentes más útiles para esta orden específica.
Usa EXACTAMENTE los parámetros de la tabla de arriba.
Para agentes no listados en la tabla, usa "" como parámetros.

RESPONDE SOLO este JSON:
{{
  "analisis": "qué pide el usuario en una frase",
  "subtareas": [
    {{
      "paso": 1,
      "agente": "archivo.py",
      "objetivo": "qué debe lograr",
      "parametros": "parámetros exactos de la tabla"
    }}
  ]
}}"""

        respuesta = ia_call(prompt, temperatura=0.1, max_tokens=800)
        if not respuesta:
            return None

        if "```" in respuesta:
            for parte in respuesta.split("```"):
                if "{" in parte:
                    respuesta = parte.strip().lstrip("json").strip()
                    break

        try:
            return json.loads(respuesta.strip())
        except Exception as e:
            log(f"Error parseando plan: {e} | {respuesta[:150]}")
            return None

    # -- EJECUTAR AGENTE CON VALIDACIÓN ------------------------------------
    def ejecutar_agente(self, archivo, parametros=""):
        if not os.path.exists(archivo):
            return None, f"[ERROR] {archivo} no existe."

        cmd = [sys.executable, archivo]
        if parametros and parametros.strip():
            cmd.extend(parametros.split())

        try:
            resultado = subprocess.run(
                cmd, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=TIMEOUT_AGENTE,
            )
            salida = resultado.stdout.strip()
            if not salida and resultado.stderr:
                return False, f"[ERROR] {resultado.stderr[:200]}"
            return True, salida or "[Sin output]"
        except subprocess.TimeoutExpired:
            return False, f"[TIMEOUT] {archivo} tardó más de {TIMEOUT_AGENTE}s."
        except Exception as e:
            return False, f"[ERROR] {e}"

    # -- INTERPRETAR APORTE ------------------------------------------------
    def interpretar_aporte(self, subtarea, output_raw):
        memoria_txt = ""
        for m in self.memoria_equipo:
            memoria_txt += f"\n[{m['agente']}]: {m['aporte'][:200]}"

        # Extraer números clave del output antes de pasarlo a la IA
        output_limpio = extraer_numeros_clave(output_raw)

        prompt = f"""Agente especialista en equipo de IA.

Rol: {subtarea['objetivo']}
Equipo sabe:{memoria_txt if memoria_txt else ' (eres el primero)'}

Datos de tu análisis:
{output_limpio}

Extrae 3-5 datos clave con números exactos en pesos mexicanos.
Máximo 100 palabras. Sin markdown. Sin introducción."""

        return ia_call(prompt, temperatura=0.3, max_tokens=200) or output_limpio[:300]

    # -- SÍNTESIS FINAL ----------------------------------------------------
    def director_sintetizar(self, orden, params, contexto_previo=""):
        aportes_txt = ""
        for m in self.memoria_equipo:
            aportes_txt += f"\n\n[{m['agente']} — {m['area']}]\n{m['aporte']}"

        contexto_txt = f"\nCONTEXTO PREVIO:\n{contexto_previo}" if contexto_previo else ""

        prompt = f"""Director de agencia de IA. Tu equipo analizó esta orden.

ORDEN: "{orden}"
DATOS: ${params['monto']:,.0f} | {params['tasa']}% anual | {params['plazo']} años | renta ${params['renta']:,.0f}/mes
{contexto_txt}

APORTES:{aportes_txt}

Responde directamente al usuario:
1. Resumen en 3 números clave (pago mensual, ROI, costo total)
2. Análisis: ¿conviene? ¿por qué?
3. Recomendación concreta en 1-2 líneas

Máximo 250 palabras. Sin frases genéricas. Sin nombres de archivos.
Si es orden de seguimiento, compara con la situación anterior."""

        return ia_call(prompt, temperatura=0.5, max_tokens=500)

    # -- CONSTRUIR CONTEXTO DE HISTORIAL -----------------------------------
    def construir_contexto(self):
        if not self.historial:
            return ""
        ctx = []
        for h in self.historial[-3:]:  # Últimas 3 órdenes
            ctx.append(f"Orden: {h['orden']}\nResultado: {h['resumen'][:200]}")
        return "\n\n".join(ctx)

    # -- RESPUESTA DIRECTA -------------------------------------------------
    def respuesta_directa(self, orden, contexto=""):
        ctx_txt = f"\nContexto previo: {contexto}" if contexto else ""
        prompt = f"""Experto en finanzas y real estate México.{ctx_txt}
Orden: {orden}
Responde con números concretos. Sin frases genéricas. Máximo 200 palabras."""
        return ia_call(prompt, temperatura=0.6, max_tokens=400) or "No pude procesar la orden."

    # -- FLUJO PRINCIPAL ---------------------------------------------------
    def procesar(self, orden):
        print(f"\n{'-'*60}")
        print(f"[CEREBRO] CLAWBOT v4.0: {orden[:70]}...")
        log(f"Orden: {orden[:100]}")

        if BUS_DISPONIBLE:
            bus.depositar(de="usuario", para="clawbot", tipo="orden", contenido=orden)

        self.catalogo = cargar_catalogo()

        # -- Detectar si es orden de seguimiento --
        seguimiento = es_seguimiento(orden, self.historial)
        contexto    = self.construir_contexto()

        if seguimiento and self.params_previos:
            log("Orden de seguimiento detectada — heredando parámetros previos.")
            params = extraer_parametros(orden, self.params_previos)
        else:
            params = extraer_parametros(orden)

        self.params_previos = params

        # -- Director selecciona equipo --
        print("\n[META] Director seleccionando equipo...")
        plan = self.director_seleccionar(orden, params, contexto if seguimiento else "")

        if not plan:
            log("Director no pudo crear plan.")
            return "No pude analizar la orden. Reformúlala."

        subtareas = plan.get("subtareas", [])
        analisis  = plan.get("analisis", "")

        if not subtareas:
            resultado = self.respuesta_directa(orden, contexto)
            self.historial.append({"orden": orden, "resumen": resultado[:200], "params": params})
            return resultado

        agentes_str = " -> ".join([s["agente"] for s in subtareas])
        print(f"[LISTA] Equipo: {agentes_str}")
        print(f"   {analisis}")
        print(f"   ? ${params['monto']:,.0f} | {params['tasa']}% | {params['plazo']} años")
        if seguimiento:
            print(f"   ? Continuando conversación previa")

        self.memoria_equipo = []
        agentes_fallidos    = []

        for subtarea in subtareas:
            paso   = subtarea["paso"]
            agente = subtarea["agente"]
            params_str = subtarea.get("parametros", "")
            area   = self.catalogo.get(agente, {}).get("area", "GENERAL")

            print(f"\n   [{paso}/{len(subtareas)}] {agente} [{area}]")
            if params_str:
                print(f"   ? Args: {params_str}")

            # -- Ejecución con validación y fallback --
            exito, output_raw = self.ejecutar_agente(agente, params_str)

            if not exito:
                log(f"[WARN] {agente} falló: {output_raw[:100]}. Continuando con el siguiente.")
                agentes_fallidos.append(agente)
                continue

            aporte = self.interpretar_aporte(subtarea, output_raw)
            self.memoria_equipo.append({
                "paso": paso, "agente": agente,
                "area": area, "aporte": aporte,
            })
            print(f"   [OK] {aporte[:120]}...")
            time.sleep(0.5)

        if agentes_fallidos:
            log(f"Agentes que fallaron: {', '.join(agentes_fallidos)}")

        if not self.memoria_equipo:
            resultado = self.respuesta_directa(orden, contexto)
        else:
            print(f"\n? Sintetizando...")
            resultado = self.director_sintetizar(orden, params, contexto if seguimiento else "")
            if not resultado:
                resultado = "\n".join([f"• {m['agente']}: {m['aporte']}" for m in self.memoria_equipo])

        # Guardar en historial de sesión
        self.historial.append({
            "orden":   orden,
            "resumen": (resultado or "")[:300],
            "params":  params,
            "equipo":  agentes_str
        })

        log(f"Completado. Equipo: {agentes_str}")
        return resultado

    def mostrar_historial(self):
        if not self.historial:
            print("Sin historial en esta sesión.")
            return
        print(f"\n{'-'*60}")
        print(f"HISTORIAL DE SESIÓN ({len(self.historial)} órdenes):")
        for i, h in enumerate(self.historial, 1):
            print(f"\n[{i}] {h['orden'][:60]}")
            print(f"    Equipo: {h.get('equipo', 'directo')}")
            print(f"    ${h['params']['monto']:,.0f} | {h['params']['tasa']}% | {h['params']['plazo']}a")

# ============================================================
# PUNTO DE ENTRADA
# ============================================================
def procesar_orden(orden):
    return OrquestadorClawbot().procesar(orden)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(procesar_orden(" ".join(sys.argv[1:])))
    else:
        print("+==============================================+")
        print("|   CLAWBOT v4.0 — Multi-Agente Inteligente   |")
        print("+==============================================+")
        print("|  [OK] Memoria entre órdenes de la sesión       |")
        print("|  [OK] Parámetros con regex (nunca se equivoca) |")
        print("|  [OK] Detección de órdenes de seguimiento      |")
        print("|  [OK] Fallback si un agente falla              |")
        print("|  [OK] 69 agentes dinámicos desde habilidades   |")
        print("|  'historial' -> ver órdenes de la sesión     |")
        print("|  'equipo'    -> ver último equipo            |")
        print("|  'salir'     -> terminar                     |")
        print("+==============================================+\n")

        orq = OrquestadorClawbot()
        while True:
            try:
                orden = input("Orden: ").strip()
                if not orden:
                    continue
                if orden.lower() in ("salir", "exit", "quit"):
                    break
                if orden.lower() == "equipo":
                    if orq.memoria_equipo:
                        for m in orq.memoria_equipo:
                            print(f"  [{m['paso']}] {m['agente']} -> {m['aporte'][:120]}")
                    else:
                        print("Sin equipo activo.")
                    continue
                if orden.lower() == "historial":
                    orq.mostrar_historial()
                    continue

                resultado = orq.procesar(orden)
                print(f"\n{'='*60}")
                print(resultado)
                print(f"{'='*60}\n")

            except KeyboardInterrupt:
                print("\n[CLAWBOT] Apagado.")
                break