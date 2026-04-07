"""
ÁREA: CEREBRO
DESCRIPCIÓN: Fábrica de agentes en bucle infinito. Genera lotes de 15 agentes,
             prueba cada uno, repara los que fallan hasta que pasen, y en cuanto
             los 15 están aprobados arranca automáticamente el siguiente lote.
             Nunca para. Cubre todas las áreas de negocio posibles.
TECNOLOGÍA: llm_router (multi-proveedor), ast, subprocess
"""

import os
import sys
import ast
import json
import time
import random
import subprocess
import shutil
from datetime import datetime
import io as _io

# Fix Unicode para Windows (cp1252) — hace print() seguro con cualquier caracter
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
            temperature=0.4, max_tokens=3000
        )
        return r.choices[0].message.content.strip()

# Intenta importar fabrica_config para leer modo del usuario
try:
    from agencia.agents.herramientas.fabrica_config import leer_modo_usuario, traducir_modo
    USAR_CONFIG_USUARIO = True
except ImportError:
    USAR_CONFIG_USUARIO = False

LOG          = "registro_noche.txt"
HABILIDADES  = "habilidades.json"
EXPANSION_PLAN = "expansion_plan.json"
CARPETA_LOTE = "lote_nuevo"
TAMAÑO_LOTE  = 15
PAUSA_AGENTE = 3
PAUSA_LOTE   = 5

# ---------------------------------------------
#  MODO: "crear" hasta 500 agentes, luego "mejorar"
#  Forzar modo: python fabrica_agentes.py mejorar
#               python fabrica_agentes.py crear
# TARGET: 500 agentes totales + 206 micros del plan de expansion
# ---------------------------------------------
UMBRAL_MODO_MEJORA = 500
TARGET_TOTAL_AGENTES = 500

AREAS_TEMAS = {
    "FINANZAS": [
        "analisis_estados_financieros", "control_presupuesto_mensual",
        "calculo_depreciacion_activos", "analisis_punto_equilibrio",
        "simulador_inversion_cetes", "calculo_rendimiento_fondos",
        "analizador_deuda_empresarial", "proyector_flujo_caja_3_años",
        "calculo_capital_trabajo", "comparador_instrumentos_inversion",
        "calculo_nomina_mensual_mexico", "analizador_razones_financieras",
        "estimador_valor_empresa", "calculadora_afore_retiro",
        "calculo_impuesto_sobre_renta_mensual", "simulador_fondo_emergencia",
    ],
    "REAL ESTATE": [
        "comparador_zonas_inversion_cdmx", "calculadora_renta_justa_m2",
        "reporte_avaluo_basico", "detector_oportunidades_compra",
        "analizador_tendencias_mercado_inmobiliario",
        "calculadora_retorno_desarrollo_obra",
        "simulador_crowdfunding_inmobiliario", "evaluador_credito_puente",
        "plan_comercializacion_propiedad", "calculadora_gastos_escrituracion",
        "analizador_cartera_propiedades", "estimador_costos_remodelacion",
        "calculadora_ocupacion_renta", "comparador_hipotecas_bancos_mexico",
    ],
    "CEREBRO": [
        "orquestador_agentes_industria", "router_consultas_complejidad",
        "agente_memoria_contextual", "generador_prompts_optimizados",
        "coordinador_pipeline_datos", "monitor_performance_agentes",
        "agente_resumen_ejecutivo", "clasificador_intencion_usuario",
        "dispatcher_multiagente", "agente_validacion_resultados",
    ],
    "HERRAMIENTAS": [
        "generador_reportes_csv", "scheduler_tareas_programadas",
        "validador_datos_entrada", "compresor_archivador_logs",
        "monitor_uso_apis", "generador_backups_automaticos",
        "parser_archivos_configuracion", "monitor_salud_sistema",
        "notificador_alertas_consola", "limpiador_archivos_temporales",
        "generador_hash_verificacion", "conversor_formatos_datos",
    ],
    "LEGAL": [
        "generador_carta_poder", "checklist_requisitos_notariales",
        "convenio_prestacion_servicios", "analizador_clausulas_riesgo",
        "guia_constitucion_empresa_mexico", "generador_finiquito_laboral",
        "calculadora_indemnizacion_imss", "checklist_cumplimiento_sat",
        "generador_acta_acuerdos", "template_contrato_servicios_profesionales",
    ],
    "MARKETING": [
        "generador_plan_contenidos", "analizador_buyer_persona",
        "calculadora_presupuesto_publicitario", "generador_propuesta_valor",
        "analizador_funnel_ventas", "generador_copy_facebook_ads",
        "calculadora_cac_ltv", "generador_estrategia_referidos",
        "analizador_metricas_campana", "generador_calendario_editorial",
        "generador_bio_redes_sociales", "analizador_hashtags_instagram",
    ],
    "VENTAS": [
        "calculadora_pipeline_ventas", "generador_propuesta_comercial",
        "analizador_objeciones", "tracker_seguimiento_prospectos",
        "calculadora_forecast_mensual", "generador_argumentario_ventas",
        "analizador_ciclo_venta", "script_cierre_ventas",
        "calculadora_descuentos_margen", "generador_email_cotizacion",
    ],
    "OPERACIONES": [
        "gestor_inventario_basico", "calculadora_costo_operacion",
        "generador_procedimientos_sop", "analizador_kpis_operativos",
        "calculadora_capacidad_instalada", "gestor_ordenes_trabajo",
        "analizador_cuellos_botella", "calculadora_eficiencia_operativa",
        "generador_checklist_procesos", "calculadora_tiempo_produccion",
    ],
    "RECURSOS HUMANOS": [
        "calculadora_costo_empleado_mexico", "generador_descripcion_puesto",
        "calculadora_prestaciones_ley", "generador_evaluacion_desempenio",
        "calculadora_liquidacion_laboral", "analizador_clima_organizacional",
        "generador_plan_onboarding", "calculadora_horas_extra",
        "generador_encuesta_satisfaccion", "calculadora_rotacion_personal",
    ],
    "TECNOLOGÍA": [
        "calculadora_costo_infraestructura_cloud",
        "generador_especificaciones_tecnicas", "analizador_stack_tecnologico",
        "calculadora_roi_automatizacion", "plan_migracion_cloud",
        "analizador_deuda_tecnica", "calculadora_sla_uptime",
        "generador_documentacion_api", "calculadora_licencias_software",
        "analizador_seguridad_basica",
    ],
    "SALUD": [
        "calculadora_imc_riesgo", "generador_plan_nutricional",
        "calculadora_calorias_actividad", "analizador_costos_seguro_medico",
        "checklist_consulta_medica", "calculadora_dosis_medicamento",
        "generador_recordatorio_medicamentos", "analizador_habitos_saludables",
    ],
    "EDUCACIÓN": [
        "generador_plan_estudio", "calculadora_costo_carrera_mexico",
        "generador_ejercicios_practica", "analizador_tecnicas_aprendizaje",
        "calculadora_roi_educativo", "generador_rubrica_evaluacion",
        "generador_temario_curso", "calculadora_becas_disponibles",
    ],
    "LOGÍSTICA": [
        "calculadora_costo_envio_mexico", "optimizador_ruta_entregas",
        "calculadora_tiempo_transito", "analizador_costo_ultima_milla",
        "generador_manifiesto_carga", "calculadora_capacidad_almacen",
        "tracker_pedidos_basico", "calculadora_costo_importacion",
    ],
    "TURISMO": [
        "calculadora_presupuesto_viaje", "generador_itinerario_viaje",
        "comparador_hospedaje", "calculadora_roi_renta_vacacional",
        "analizador_temporadas", "generador_paquete_turistico",
    ],
    "RESTAURANTES": [
        "calculadora_costo_platillo", "generador_menu_precios",
        "calculadora_punto_equilibrio_restaurante",
        "analizador_merma_desperdicio", "generador_receta_estandarizada",
        "calculadora_precio_venta_platillo",
    ],
    "BIENES RAÍCES COMERCIALES": [
        "calculadora_renta_oficina_cdmx", "analizador_local_comercial",
        "calculadora_roi_bodega_industrial", "comparador_zonas_comerciales",
        "estimador_aforo_local", "calculadora_contrato_arrendamiento_comercial",
    ],
    "SEGUROS": [
        "calculadora_seguro_vida_mexico", "comparador_seguros_auto",
        "analizador_cobertura_gastos_medicos", "calculadora_prima_seguro",
        "generador_reporte_siniestro", "checklist_contratacion_seguro",
    ],
    "CONTABILIDAD": [
        "calculadora_iva_desglosado", "generador_factura_conceptos",
        "calculadora_ptu_empleados", "analizador_deducciones_fiscales",
        "calculadora_regimen_fiscal_adecuado", "generador_balance_general_simple",
    ],
    # ─── UTILIDADES REUTILIZABLES ───────────────────────────────────────────
    # Agentes micro-tarea: max 60 lineas, output 1 linea parseable,
    # con funcion importable del mismo nombre para que otros agentes los usen.
    "MICRO_TAREAS": [
        "formateador_moneda_mx",          # float → "$1,234.56 MXN"
        "validador_rfc_mexico",           # string → "VALIDO" / "INVALIDO:razon"
        "validador_curp_mexico",          # string → "VALIDO" / "INVALIDO:razon"
        "calculadora_iva_rapida",         # monto → "subtotal|IVA|total"
        "parseador_fecha_espanol",        # "15 enero 2026" → "2026-01-15"
        "formateador_telefono_mx",        # "5512345678" → "+52-55-1234-5678"
        "extractor_numeros_texto",        # texto → JSON array de numeros
        "calculadora_isr_mensual_rapido", # ingreso → "base|retencion|neto"
        "normalizador_nombre_persona",    # "juan garcia" → "Garcia, Juan"
        "generador_folio_consecutivo",    # "FACT" 1 → "FACT-2026-0001"
        "calculadora_descuento_precio",   # precio pct → "original|descuento|final"
        "calculadora_diferencia_fechas",  # fecha1 fecha2 → "X dias"
        "detector_tipo_contribuyente",    # rfc → "PERSONA_FISICA"/"PERSONA_MORAL"
        "calculadora_comision_rapida",    # monto pct → "comision|total"
        "validador_clabe_bancaria",       # clabe → "VALIDO:BBVA" / "INVALIDO"
        "calculadora_imss_empleado",      # salario_diario → "obrero|patron|total"
        "parseador_monto_texto",          # "me costo 2 mil 500" → "2500.0"
        "formateador_numero_palabras_mx", # 2500 → "dos mil quinientos pesos"
        "generador_clave_producto",       # "Zapato Sport Blanco" → "ZAP-SPO-BLA"
        "calculadora_plazo_vencimiento",  # fecha_inicio dias → "YYYY-MM-DD"
    ],
}


# ---------------------------------------------
#  UTILIDADES
# ---------------------------------------------

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    linea = f"[{ts}] [FÁBRICA] {msg}"
    print(linea)
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(linea + "\n")
    except Exception:
        pass

def cargar_habilidades():
    if not os.path.exists(HABILIDADES):
        return {}
    try:
        with open(HABILIDADES, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except Exception:
        return {}

def registrar_en_habilidades(archivo, area, descripcion):
    habilidades = cargar_habilidades()
    habilidades[archivo] = {
        "descripcion": descripcion,
        "categoria": area,
        "salud": "OK",
        "tecnologia": ["Python estándar"],
        "ultima_actualizacion": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "ordenes": [archivo.replace(".py", "").replace("_", " ")]
    }
    # Backup antes de escribir para proteger ante crashes durante json.dump
    bak = HABILIDADES + ".bak"
    if os.path.exists(HABILIDADES):
        try:
            shutil.copy2(HABILIDADES, bak)
        except Exception:
            pass
    tmp = HABILIDADES + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(habilidades, f, indent=4, ensure_ascii=False)
    os.replace(tmp, HABILIDADES)  # atomico en mismo filesystem

def agentes_existentes():
    return set(cargar_habilidades().keys())

# ─────────────────────────────────────────────────────────────────────────────
#  EXPANSION PLAN — Gestión del plan de 206 micros
# ─────────────────────────────────────────────────────────────────────────────

def cargar_expansion_plan():
    """Carga el plan de expansión con los 206 micros planificados."""
    if not os.path.exists(EXPANSION_PLAN):
        return {"micros": []}
    try:
        with open(EXPANSION_PLAN, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log(f"Error cargando {EXPANSION_PLAN}: {e}")
        return {"micros": []}

def obtener_micros_pendientes(plan):
    """Retorna lista de micros del plan que aún no están creados."""
    existentes = agentes_existentes()
    pendientes = []
    for micro in plan.get("micros", []):
        nombre = micro.get("nombre", "")
        if nombre and nombre not in existentes:
            pendientes.append(micro)
    return pendientes

def obtener_progreso_expansion():
    """Retorna estadísticas del progreso de expansión."""
    plan = cargar_expansion_plan()
    total_planificados = len(plan.get("micros", []))
    existentes = agentes_existentes()

    creados = sum(1 for m in plan.get("micros", [])
                  if m.get("nombre", "") in existentes)
    pendientes = total_planificados - creados

    return {
        "total_planificados": total_planificados,
        "creados": creados,
        "pendientes": pendientes,
        "progreso_pct": int(creados * 100 / total_planificados) if total_planificados > 0 else 0
    }

def validar_sintaxis(codigo):
    try:
        ast.parse(codigo)
        return True, None
    except SyntaxError as e:
        return False, str(e)

def limpiar_codigo(texto):
    if "```python" in texto:
        return texto.split("```python")[1].split("```")[0].strip()
    if "```" in texto:
        return texto.split("```")[1].split("```")[0].strip()
    return texto.strip()

def probar_agente(ruta, area=""):
    # Micro-tareas: output de 1 sola linea es valido (puede ser "0" o un string corto)
    min_output = 1 if area == "MICRO_TAREAS" else 10
    try:
        r = subprocess.run(
            [sys.executable, ruta],
            capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=25
        )
        salida = (r.stdout or "").strip()
        if len(salida) < min_output:
            err = (r.stderr or "").strip()
            return False, err[:200] or "Output vacío o muy corto"
        return True, salida[:200]
    except subprocess.TimeoutExpired:
        return False, "Timeout de 25s"
    except Exception as e:
        return False, str(e)

# ---------------------------------------------
#  GENERADOR DE PLAN
# ---------------------------------------------

def generar_plan_lote(numero_lote, existentes, modo="crear", plan_expansion=None):
    """
    Genera un plan de lote inteligente:
    - En modo CREAR con expansion plan: prioriza micros pendientes primero
    - Luego llena con agentes de MICRO_TAREAS de AREAS_TEMAS
    - Finalmente llena con otras áreas para alcanzar TAMAÑO_LOTE
    """
    plan = []
    usados = set()

    # ─ PASO 1: Si en modo CREAR y hay plan de expansión, priorizar micros pendientes ─
    if modo.lower() == "crear" and plan_expansion:
        pendientes = obtener_micros_pendientes(plan_expansion)
        # Agregar hasta 5 micros del plan de expansión por lote
        micros_a_agregar = pendientes[:5]
        for micro in micros_a_agregar:
            nombre = micro.get("nombre", "")
            categoria = micro.get("categoria", "MARKETING")
            descripcion = micro.get("descripcion", "")
            if nombre and nombre not in existentes:
                plan.append({
                    "archivo": nombre,
                    "area": categoria,
                    "tema": nombre.replace(".py", "").replace("_", " "),
                    "descripcion": descripcion,
                    "es_expansion": True
                })
                usados.add(nombre)

    # ─ PASO 2: Llenar resto del lote con áreas base (incluyendo MICRO_TAREAS) ─
    areas_base   = ["FINANZAS", "REAL ESTATE", "CEREBRO", "HERRAMIENTAS", "MICRO_TAREAS"]
    areas_extras = [a for a in AREAS_TEMAS if a not in areas_base]

    for area in areas_base:
        if len(plan) >= TAMAÑO_LOTE:
            break
        temas = list(AREAS_TEMAS.get(area, []))
        random.shuffle(temas)
        agregados = 0
        for tema in temas:
            if len(plan) >= TAMAÑO_LOTE:
                break
            nombre = tema + ".py"
            if nombre not in existentes and nombre not in usados:
                plan.append({"archivo": nombre, "area": area, "tema": tema.replace("_", " ")})
                usados.add(nombre)
                agregados += 1
                if agregados >= 2:
                    break

    # ─ PASO 3: Completar con otras áreas ─
    random.shuffle(areas_extras)
    for area in areas_extras * 3:
        if len(plan) >= TAMAÑO_LOTE:
            break
        temas = list(AREAS_TEMAS.get(area, []))
        random.shuffle(temas)
        for tema in temas:
            if len(plan) >= TAMAÑO_LOTE:
                break
            nombre = tema + ".py"
            if nombre not in existentes and nombre not in usados:
                plan.append({"archivo": nombre, "area": area, "tema": tema.replace("_", " ")})
                usados.add(nombre)
                break

    return plan[:TAMAÑO_LOTE]

# ---------------------------------------------
#  GENERADOR DE CÓDIGO
# ---------------------------------------------

def generar_codigo(spec):
    # ── Prompt especial para MICRO_TAREAS ─────────────────────────────────
    if spec.get("area") == "MICRO_TAREAS":
        nombre_fn = spec['archivo'].replace(".py", "")
        prompt = f"""Eres experto Python creando utilidades reutilizables para Agencia Santi.

ARCHIVO: {spec['archivo']}
ÁREA: MICRO_TAREAS
FUNCIÓN: {spec['tema']}

ESTRUCTURA EXACTA QUE DEBES SEGUIR:

```python
\"\"\"
ÁREA: MICRO_TAREAS
DESCRIPCIÓN: {spec['tema']}
TECNOLOGÍA: Python estándar
\"\"\"

import sys
import re
import json
from math import *

def {nombre_fn}(entrada, *args):
    \"\"\"Función pura, sin prints, sin side effects.\"\"\"
    # Tu lógica aquí
    # Procesar 'entrada' (el primer parámetro recibido)
    # RETORNAR un resultado simple (string, número, JSON, o "VALIDO"/"INVALIDO")
    resultado = "resultado aqui"
    return resultado

def main():
    entrada = sys.argv[1] if len(sys.argv) > 1 else "default_value"
    resultado = {nombre_fn}(entrada)
    print(resultado)

if __name__ == "__main__":
    main()
```

REGLAS ABSOLUTAS:
1. La función {nombre_fn} DEBE aceptar como primer parámetro 'entrada'
2. NO usar 'valor', 'param', 'data' — usar SIEMPRE 'entrada' como primer parámetro
3. NUNCA usar variables globales o imports externos (solo sys, re, json, math, datetime)
4. NUNCA usar input() — SIEMPRE sys.argv
5. Imprime EXACTAMENTE 1 línea con el resultado final limpio
6. Máximo 50 líneas de código
7. El resultado debe ser parseable: número, "VALIDO"/"INVALIDO", o JSON válido
8. Corre en menos de 100ms (sin sleeps, sin web requests)

EJEMPLOS CORRECTOS:

Ejemplo 1 - Validador:
def validador_curp_mexico(entrada):
    # entrada es un string como "ABCD123456HDFRXYZ01"
    if not entrada or len(entrada) != 18:
        return "INVALIDO:longitud"
    return "VALIDO"

def main():
    curp = sys.argv[1] if len(sys.argv) > 1 else "ABCD123456HDFRXYZ01"
    print(validador_curp_mexico(curp))

Ejemplo 2 - Formateador:
def formateador_moneda_mx(entrada):
    try:
        valor = float(entrada)
        return f"${{valor:,.2f}} MXN"
    except:
        return "ERROR:no_numerico"

def main():
    monto = sys.argv[1] if len(sys.argv) > 1 else "1000"
    print(formateador_moneda_mx(monto))

DEVUELVE SOLO EL CÓDIGO. Sin markdown. Sin explicaciones."""
        r = ia(prompt)
        return limpiar_codigo(r) if r else None

    # ── Prompt estándar para todas las demás áreas ─────────────────────────
    prompt = f"""Eres experto Python creando agentes para Agencia Santi (México).

ARCHIVO: {spec['archivo']}
ÁREA: {spec['area']}
FUNCIÓN: {spec['tema']}

REGLAS ABSOLUTAS:
1. Encabezado al inicio:
\"\"\"
ÁREA: {spec['area']}
DESCRIPCIÓN: Agente que realiza {spec['tema']}
TECNOLOGÍA: Python estándar, web_bridge (opcional)
\"\"\"
2. NUNCA uses input() — solo sys.argv con defaults realistas
3. Output: mínimo 5 líneas con datos concretos y números reales mexicanos
4. Solo stdlib: os, sys, json, datetime, math, re, random
5. Función main() + if __name__ == "__main__": main()
6. try/except en main
7. Completamente autónomo — corre solo sin intervención humana
8. INTERNET OPCIONAL — Si el agente se beneficiaria de datos en tiempo real
   (precios, tipo de cambio, noticias, cotizaciones), agrega este bloque
   al inicio del archivo despues de los imports de stdlib:

   try:
       import agencia.agents.herramientas.web_bridge as web
       WEB = web.WEB  # True si hay conexion
   except ImportError:
       WEB = False

   Luego en main() usa "if WEB:" para buscar datos reales con web.buscar(),
   web.fetch_texto(), web.extraer_precios(). Si WEB es False, usa datos
   de ejemplo hardcodeados como fallback.

DEVUELVE SOLO CÓDIGO PYTHON. Sin markdown. Sin explicaciones."""

    r = ia(prompt)
    return limpiar_codigo(r) if r else None

def reparar_codigo(spec, codigo_roto, error, intento):
    # ── Reparación especial para MICRO_TAREAS ──
    if spec.get("area") == "MICRO_TAREAS":
        nombre_fn = spec['archivo'].replace(".py", "")
        prompt = f"""Repara esta micro-tarea Python. Intento #{intento}.

ARCHIVO: {spec['archivo']}
FUNCIÓN: {spec['tema']}
ERROR: {error}

CÓDIGO ACTUAL:
{codigo_roto[:2000]}

PROBLEMAS COMUNES EN MICRO-TAREAS:
1. NameError 'valor' is not defined → Cambiar a 'entrada' (primer parámetro)
2. main() no recibe parámetro correctamente → Usar: entrada = sys.argv[1] if len(sys.argv) > 1 else "default"
3. Función no retorna nada → Agregar return al final de {nombre_fn}()
4. print() dentro de la función → Sacar prints de la función, dejar solo en main()
5. Variables no definidas → Asegurar que TODAS las variables estén inicializadas antes de usarse

ESTRUCTURA CORRECTA:
def {nombre_fn}(entrada, *args):
    # Procesar 'entrada'
    # SIEMPRE retornar un resultado
    return resultado

def main():
    entrada = sys.argv[1] if len(sys.argv) > 1 else "default"
    resultado = {nombre_fn}(entrada)
    print(resultado)

if __name__ == "__main__":
    main()

DEVUELVE SOLO EL CÓDIGO CORREGIDO. Sin markdown."""

    else:
        # ── Reparación estándar para otras áreas ──
        prompt = f"""Repara este agente Python. Intento #{intento}.

ARCHIVO: {spec['archivo']}
FUNCIÓN: {spec['tema']}
ERROR: {error}

CÓDIGO ACTUAL:
{codigo_roto[:2500]}

SOLUCIONES COMUNES:
- input() -> reemplazar con sys.argv[1] if len(sys.argv) > 1 else "default"
- Output vacío -> agregar print() con cálculos y datos
- ImportError -> usar solo os/sys/json/math/re/datetime/random
- SyntaxError -> corregir indentación y paréntesis

DEVUELVE SOLO EL CÓDIGO CORREGIDO. Sin markdown."""

    r = ia(prompt)
    return limpiar_codigo(r) if r else None

# ---------------------------------------------
#  PROCESAR UN AGENTE — bucle hasta aprobar
# ---------------------------------------------

def procesar_agente(spec, numero, total, etiqueta=""):
    archivo = spec["archivo"]
    area    = spec["area"]
    tema    = spec["tema"]

    log(f"\n  [{numero}/{total}] {etiqueta}{archivo} [{area}]")

    os.makedirs(CARPETA_LOTE, exist_ok=True)
    ruta_temp    = os.path.join(CARPETA_LOTE, archivo)
    codigo       = None
    ultimo_error = "Sin código generado aún"
    intento      = 0

    while True:
        intento += 1

        # Generar o reparar
        if codigo is None:
            log(f"    -> Generando...")
            codigo = generar_codigo(spec)
        else:
            log(f"    [FIX] Reparando (intento {intento})...")
            codigo_nuevo = reparar_codigo(spec, codigo, ultimo_error, intento)
            if codigo_nuevo:
                codigo = codigo_nuevo

        if not codigo:
            log(f"    [WARN] Sin respuesta del LLM, reintentando en 5s...")
            time.sleep(5)
            codigo = None
            continue

        # Validar sintaxis
        valido, err_sintaxis = validar_sintaxis(codigo)
        if not valido:
            ultimo_error = f"SyntaxError: {err_sintaxis}"
            log(f"    [WARN] Sintaxis: {err_sintaxis[:80]}")
            time.sleep(2)
            continue

        # Guardar y probar
        with open(ruta_temp, "w", encoding="utf-8") as f:
            f.write(codigo)

        exito, output = probar_agente(ruta_temp, area=area)

        if exito:
            # ¡Aprobado!
            shutil.copy2(ruta_temp, archivo)
            try:
                os.remove(ruta_temp)
            except Exception:
                pass
            registrar_en_habilidades(archivo, area, f"Agente que realiza {tema}")
            log(f"    [OK] APROBADO tras {intento} intento(s): {output[:80]}...")
            return

        ultimo_error = output
        log(f"    [WARN] Falló: {output[:80]}")
        time.sleep(2)

# ---------------------------------------------
#  PROCESAR LOTE COMPLETO
# ---------------------------------------------

def procesar_lote(plan, numero_lote, modo="crear", plan_expansion=None):
    log(f"\n{'='*55}")
    log(f"LOTE #{numero_lote} — {len(plan)} agentes")
    log(f"Áreas: {', '.join(sorted(set(s['area'] for s in plan)))}")

    # Mostrar info de expansion si está activo
    if modo.lower() == "crear" and plan_expansion:
        progreso = obtener_progreso_expansion()
        expansion_info = f"Expansion: {progreso['creados']}/{progreso['total_planificados']} micros ({progreso['progreso_pct']}%)"
        log(expansion_info)

    log(f"{'='*55}")

    inicio = time.time()

    for i, spec in enumerate(plan, 1):
        es_expansion = spec.get("es_expansion", False)
        etiqueta = "[EXPANSION] " if es_expansion else ""
        procesar_agente(spec, i, len(plan), etiqueta)
        time.sleep(PAUSA_AGENTE)

    duracion = int(time.time() - inicio)
    total_hab = len(cargar_habilidades())

    if modo.lower() == "crear" and plan_expansion:
        progreso = obtener_progreso_expansion()
        log(f"\n[OK] LOTE #{numero_lote} COMPLETO en {duracion}s — Total: {total_hab} agentes")
        log(f"    Expansion: {progreso['creados']}/{progreso['total_planificados']} micros ({progreso['progreso_pct']}%)")
    else:
        log(f"\n[OK] LOTE #{numero_lote} COMPLETO en {duracion}s — Total en agencia: {total_hab} agentes")

# ---------------------------------------------
#  BUCLE INFINITO
# ---------------------------------------------

# ---------------------------------------------
#  MODO MEJORA — Mejora agentes existentes
# ---------------------------------------------

def seleccionar_agentes_a_mejorar(n=15):
    """Selecciona N agentes existentes para mejorar, priorizando los más cortos."""
    hab = cargar_habilidades()
    candidatos = []
    for archivo, info in hab.items():
        if not archivo.endswith(".py") or not os.path.exists(archivo):
            continue
        try:
            size = os.path.getsize(archivo)
            candidatos.append((size, archivo, info))
        except Exception:
            continue
    # Priorizar archivos más cortos (menos desarrollados)
    candidatos.sort(key=lambda x: x[0])
    return candidatos[:n]

def mejorar_agente(archivo, info):
    """Pide al LLM que mejore un agente existente."""
    try:
        with open(archivo, "r", encoding="utf-8", errors="replace") as f:
            codigo_actual = f.read()
    except Exception as e:
        log(f"    No se pudo leer {archivo}: {e}")
        return None

    area = info.get("categoria", "GENERAL")
    descripcion = info.get("descripcion", "")

    prompt = f"""Mejora este agente Python de la Agencia Santi.

ARCHIVO: {archivo}
AREA: {area}
DESCRIPCION: {descripcion}

CODIGO ACTUAL:
{codigo_actual[:2000]}

MEJORAS A APLICAR (elige las mas relevantes):
1. Si tiene menos de 20 lineas de output, ampliar con mas datos utiles
2. Si le faltan casos edge, agregarlos con try/except
3. Si los calculos son muy simples, hacerlos mas precisos y realistas para Mexico
4. Si no tiene encabezado AREA/DESCRIPCION/TECNOLOGIA, agregarlo
5. Si usa valores hardcodeados, permitir parametros por sys.argv
6. Agregar un resumen ejecutivo al final del output

REGLAS:
- Mantener la funcion main() y if __name__ == "__main__"
- Solo stdlib: os, sys, json, datetime, math, re, random
- NUNCA usar input()
- Output minimo 5 lineas con datos concretos

DEVUELVE SOLO EL CODIGO MEJORADO. Sin markdown. Sin explicaciones."""

    respuesta = ia(prompt)
    return limpiar_codigo(respuesta) if respuesta else None

def procesar_lote_mejora(numero_lote):
    """Procesa un lote de mejoras a agentes existentes."""
    candidatos = seleccionar_agentes_a_mejorar(TAMAÑO_LOTE)
    if not candidatos:
        log("Sin agentes para mejorar")
        return

    log(f"LOTE MEJORA #{numero_lote} — {len(candidatos)} agentes a mejorar")
    mejorados = 0

    for i, (size, archivo, info) in enumerate(candidatos, 1):
        log(f"  [{i}/{len(candidatos)}] Mejorando {archivo} ({size} bytes)...")

        codigo_mejorado = mejorar_agente(archivo, info)
        if not codigo_mejorado:
            log(f"    Sin respuesta del LLM")
            time.sleep(2)
            continue

        valido, err = validar_sintaxis(codigo_mejorado)
        if not valido:
            log(f"    Sintaxis invalida: {err[:60]}")
            time.sleep(2)
            continue

        # Hacer backup y guardar mejora
        bak = archivo.replace(".py", f".bak.mejora_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        try:
            shutil.copy2(archivo, bak)
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(codigo_mejorado)
            nuevo_size = os.path.getsize(archivo)
            delta = nuevo_size - size
            log(f"    Mejorado: {size} -> {nuevo_size} bytes ({'+' if delta>0 else ''}{delta})")
            mejorados += 1
        except Exception as e:
            log(f"    Error guardando: {e}")

        time.sleep(PAUSA_AGENTE)

    total_hab = len(cargar_habilidades())
    log(f"LOTE MEJORA #{numero_lote} COMPLETO — {mejorados}/{len(candidatos)} mejorados — {total_hab} agentes totales")


# ---------------------------------------------
#  BUCLE INFINITO CON MODO AUTOMATICO
# ---------------------------------------------

def detectar_modo(arg=None):
    """
    Detecta qué modo usar:
    - 'crear'  : forzar creacion de agentes nuevos
    - 'mejorar': forzar mejora de agentes existentes
    - 'balanceado': 60% crear, 40% mejorar
    - 'expansion': solo micros del plan
    - 'noche'  : todas las tareas
    - None     : leer de fabrica_config.py o automatico segun cantidad de agentes
    """
    if arg:
        return arg.lower()

    # Intenta leer modo del usuario desde fabrica_config.py
    if USAR_CONFIG_USUARIO:
        try:
            modo_usuario = leer_modo_usuario()
            if modo_usuario in ("CREAR", "MEJORAR", "BALANCEADO", "EXPANSION", "NOCHE"):
                log(f"Modo usuario: {modo_usuario} ({traducir_modo(modo_usuario)})")
                return modo_usuario.lower()
        except Exception as e:
            log(f"Error leyendo modo usuario: {e}")

    # Fallback: automatico segun cantidad de agentes
    total = len(cargar_habilidades())
    return "crear" if total < UMBRAL_MODO_MEJORA else "mejorar"

def bucle_infinito(modo_forzado=None):
    log("=" * 55)
    log("FABRICA DE AGENTES — BUCLE INFINITO")
    log(f"Target total: {TARGET_TOTAL_AGENTES} agentes")
    log(f"Target expansion: 206 micros planificados")
    log(f"Umbral auto-switch: {UMBRAL_MODO_MEJORA} agentes")
    log(f"Modo forzado: {modo_forzado or 'automatico'}")
    log("Ctrl+C para detener")
    log("=" * 55)

    numero_lote   = 1
    total_creados = 0
    total_mejorados = 0

    # Cargar plan de expansión al inicio
    plan_expansion = cargar_expansion_plan()
    if plan_expansion.get("micros"):
        progreso = obtener_progreso_expansion()
        log(f"\nExpansion Plan Cargado:")
        log(f"  Total micros: {progreso['total_planificados']}")
        log(f"  Creados: {progreso['creados']}")
        log(f"  Pendientes: {progreso['pendientes']}")
        log(f"  Progreso: {progreso['progreso_pct']}%\n")
    else:
        plan_expansion = None

    while True:
        try:
            modo = modo_forzado or detectar_modo()
            total_actual = len(cargar_habilidades())

            # ─ MODO CREAR: Priorizar expansion plan, luego llegar a 500 ─
            if modo == "crear":
                log(f"MODO CREAR | Agentes: {total_actual}/{TARGET_TOTAL_AGENTES}")

                existentes = agentes_existentes()
                plan = generar_plan_lote(numero_lote, existentes, modo="crear",
                                        plan_expansion=plan_expansion)

                if not plan:
                    log("Catalogo agotado — cambiando a modo MEJORAR")
                    modo_forzado = "mejorar"
                    continue

                procesar_lote(plan, numero_lote, modo="crear", plan_expansion=plan_expansion)
                total_creados += len(plan)

                # Mostrar progreso
                total_actual = len(cargar_habilidades())
                if plan_expansion:
                    progreso = obtener_progreso_expansion()
                    log(f"Acumulado: {total_creados} creados | Expansion: {progreso['creados']}/{progreso['total_planificados']} ({progreso['progreso_pct']}%)")
                else:
                    log(f"Acumulado: {total_creados} creados | Total: {total_actual}/{TARGET_TOTAL_AGENTES}")

                # Si alcanzamos 500 y todos los micros están creados, cambiar a MEJORAR
                if total_actual >= TARGET_TOTAL_AGENTES and plan_expansion:
                    progreso = obtener_progreso_expansion()
                    if progreso['pendientes'] == 0:
                        log(f"\n[HITO] 500 agentes alcanzados + {progreso['creados']} micros completados!")
                        log("Cambiando a modo MEJORAR...")
                        modo_forzado = "mejorar"

            # ─ MODO EXPANSION: Solo los micros del plan ─
            elif modo == "expansion":
                log(f"MODO EXPANSION | Agentes: {total_actual}")

                if not plan_expansion:
                    log("Sin plan de expansión disponible")
                    modo_forzado = "crear"
                    continue

                existentes = agentes_existentes()
                # En expansion mode, SOLO crear micros del plan
                pendientes = obtener_micros_pendientes(plan_expansion)

                if not pendientes:
                    log("Todos los micros del plan han sido creados!")
                    modo_forzado = "crear"
                    continue

                plan = []
                usados = set()
                # Agregar hasta TAMAÑO_LOTE micros pendientes
                for micro in pendientes[:TAMAÑO_LOTE]:
                    nombre = micro.get("nombre", "")
                    if nombre not in existentes:
                        plan.append({
                            "archivo": nombre,
                            "area": micro.get("categoria", "MARKETING"),
                            "tema": nombre.replace(".py", "").replace("_", " "),
                            "descripcion": micro.get("descripcion", ""),
                            "es_expansion": True
                        })
                        usados.add(nombre)

                if plan:
                    procesar_lote(plan, numero_lote, modo="expansion", plan_expansion=plan_expansion)
                    total_creados += len(plan)
                    progreso = obtener_progreso_expansion()
                    log(f"Expansion: {progreso['creados']}/{progreso['total_planificados']} ({progreso['progreso_pct']}%)")

            # ─ MODO MEJORAR: Optimizar agentes existentes ─
            elif modo == "mejorar":
                log(f"MODO MEJORAR | Agentes: {total_actual}")

                procesar_lote_mejora(numero_lote)
                total_mejorados += TAMAÑO_LOTE
                log(f"Acumulado: {total_mejorados} mejoras en {numero_lote} lotes")

            # ─ MODO BALANCEADO: 60% crear, 40% mejorar ─
            elif modo == "balanceado":
                log(f"MODO BALANCEADO | Agentes: {total_actual}/{TARGET_TOTAL_AGENTES}")

                if numero_lote % 5 <= 2:  # 60% de los lotes: crear (3 de 5)
                    existentes = agentes_existentes()
                    plan = generar_plan_lote(numero_lote, existentes, modo="crear",
                                            plan_expansion=plan_expansion)
                    if plan:
                        procesar_lote(plan, numero_lote, modo="crear", plan_expansion=plan_expansion)
                        total_creados += len(plan)
                else:  # 40% de los lotes: mejorar (2 de 5)
                    procesar_lote_mejora(numero_lote)
                    total_mejorados += TAMAÑO_LOTE

                total_actual = len(cargar_habilidades())
                log(f"Creados: {total_creados} | Mejorados: {total_mejorados} | Total: {total_actual}")

            # ─ MODO NOCHE: Todas las tareas (default) ─
            elif modo == "noche" or modo is None:
                log(f"MODO NOCHE (COMPLETO) | Agentes: {total_actual}/{TARGET_TOTAL_AGENTES}")

                # Lógica similar a balanceado pero puede incluir otras tareas
                if numero_lote % 5 <= 2:  # 60% crear
                    existentes = agentes_existentes()
                    plan = generar_plan_lote(numero_lote, existentes, modo="crear",
                                            plan_expansion=plan_expansion)
                    if plan:
                        procesar_lote(plan, numero_lote, modo="crear", plan_expansion=plan_expansion)
                        total_creados += len(plan)
                else:  # 40% mejorar
                    procesar_lote_mejora(numero_lote)
                    total_mejorados += TAMAÑO_LOTE

            numero_lote += 1
            log(f"Siguiente lote en {PAUSA_LOTE}s...")
            time.sleep(PAUSA_LOTE)

        except KeyboardInterrupt:
            log(f"\nFabrica detenida.")
            log(f"Lotes procesados: {numero_lote-1}")
            log(f"Agentes creados: {total_creados}")
            log(f"Agentes mejorados: {total_mejorados}")
            total_actual = len(cargar_habilidades())
            log(f"Total en agencia: {total_actual}")
            if plan_expansion:
                progreso = obtener_progreso_expansion()
                log(f"Expansion: {progreso['creados']}/{progreso['total_planificados']} micros ({progreso['progreso_pct']}%)")
            sys.exit(0)
        except Exception as e:
            log(f"Error en lote #{numero_lote}: {e}")
            log("Reintentando en 10s...")
            time.sleep(10)


if __name__ == "__main__":
    # Modo: python fabrica_agentes.py           -> automatico (leer de fabrica_config o auto)
    #       python fabrica_agentes.py crear     -> solo crear nuevos (con expansion plan)
    #       python fabrica_agentes.py mejorar   -> solo mejorar existentes
    #       python fabrica_agentes.py balanceado -> 60% crear, 40% mejorar
    #       python fabrica_agentes.py expansion  -> solo micros del plan
    #       python fabrica_agentes.py noche     -> todas las tareas
    modo = sys.argv[1] if len(sys.argv) > 1 else None
    modos_validos = ("crear", "mejorar", "balanceado", "expansion", "noche")
    if modo and modo.lower() not in modos_validos:
        print(f"Uso: python fabrica_agentes.py [{' | '.join(modos_validos)}]")
        sys.exit(1)
    bucle_infinito(modo)