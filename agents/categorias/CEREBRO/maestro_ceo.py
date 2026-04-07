"""
ÁREA: CEREBRO
DESCRIPCIÓN: CEO orquestador principal. Recibe órdenes del usuario, coordina agentes especializados en cadena y sintetiza un resultado final coherente usando Groq. Comunicación multi-agente real vía bus_mensajes.py.
TECNOLOGÍA: Groq (Nube)
"""

import json
import os
import subprocess
import sys
import time
from groq import Groq
import bus_mensajes as bus

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

# === CONFIGURACIÓN ===
API_KEY = "GROQ_API_KEY_PLACEHOLDER"
MODELO = "llama-3.3-70b-versatile"
MAX_CONTEXTO_CHARS = 800  # Límite de caracteres del output que viaja entre agentes
client = Groq(api_key=API_KEY)

# ─────────────────────────────────────────────
#  CADENAS MULTI-AGENTE PREDEFINIDAS
# ─────────────────────────────────────────────

CADENAS = {
    "analisis_inversion": [
        "calculadora_roi_mexico.py",
        "simulador_hipoteca.py",
    ],
    "reporte_fiscal": [
        "calculadora_isr.py",
        "calculadora_iva.py",
    ],
    "campana_real_estate": [
        "generador_copy_inmobiliario.py",
        "simulador_hipotecario.py",
    ]
}

# ─────────────────────────────────────────────
#  UTILIDADES
# ─────────────────────────────────────────────

def registrar_log(mensaje):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open("registro_noche.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [CEO] {mensaje}\n")

def resumir_output(texto, max_chars=MAX_CONTEXTO_CHARS):
    """
    Reduce el output de un agente a lo esencial antes de pasarlo al siguiente.
    Extrae las primeras líneas significativas, no el bloque completo.
    """
    if len(texto) <= max_chars:
        return texto

    lineas = [l.strip() for l in texto.split('\n') if l.strip()]
    resumen = []
    total = 0
    for linea in lineas:
        if total + len(linea) > max_chars:
            break
        resumen.append(linea)
        total += len(linea)

    return "\n".join(resumen) + "\n[...output resumido para contexto...]"

def sintetizar_resultado(orden_original, resultados_por_agente):
    """
    Usa Groq para generar una respuesta final coherente y útil
    basada en los outputs de todos los agentes de la cadena.
    """
    contexto = ""
    for agente, output in resultados_por_agente.items():
        contexto += f"\n--- Datos de {agente} ---\n{resumir_output(output, 600)}\n"

    prompt = f"""Eres el CEO de una agencia de análisis financiero e inmobiliario mexicana.

El usuario preguntó: "{orden_original}"

Tus agentes especializados recopilaron estos datos:
{contexto}

Tu trabajo: Sintetiza toda esa información y da una respuesta directa, clara y útil al usuario.
- Responde en español
- Sé concreto con números cuando los tengas
- Da una recomendación clara al final
- No menciones los nombres técnicos de los agentes
- No uses frases genéricas como "espero que esto te ayude" o "buena suerte"
- Máximo 300 palabras
"""

    for intento in range(3):
        try:
            completion = client.chat.completions.create(
                model=MODELO,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=600,
                top_p=1,
                stream=False
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            if "rate_limit" in str(e).lower():
                time.sleep(10)
            elif intento < 2:
                time.sleep(3)
            else:
                return f"[Error al sintetizar resultado]: {e}"

# ─────────────────────────────────────────────
#  CLASE PRINCIPAL
# ─────────────────────────────────────────────

class MaestroCEO:
    def __init__(self):
        self.habilidades = self._cargar_habilidades()

    def _cargar_habilidades(self):
        try:
            if not os.path.exists('habilidades.json'):
                return {}
            with open('habilidades.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[CEO] Error cargando habilidades: {e}")
            return {}

    def _decidir_agentes(self, orden):
        """Usa Groq para decidir qué agentes activar."""
        habilidades_txt = "\n".join([
            f"- {k}: {v.get('descripcion', 'Agente especializado')}"
            for k, v in self.habilidades.items()
        ])

        prompt = f"""Eres el CEO de una agencia de IA con 64 agentes especializados.

Orden recibida: "{orden}"

Agentes disponibles:
{habilidades_txt}

Decide qué agentes activar. Reglas:
- Responde SOLO los nombres de archivos .py separados por comas
- Máximo 3 agentes por cadena
- Si ningún agente especializado aplica claramente, responde: ROUTER
- NO incluyas agentes de estudio o documentación para tareas de análisis
"""
        try:
            completion = client.chat.completions.create(
                model=MODELO,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=100
            )
            res = completion.choices[0].message.content.strip()

            if "ROUTER" in res or not res:
                return ["ROUTER"]

            agentes = [s.strip() for s in res.replace("`", "").split(',')
                      if s.strip().endswith('.py')]
            return agentes[:3] if agentes else ["ROUTER"]

        except Exception as e:
            registrar_log(f"Error en decisión Groq: {e}")
            return ["ROUTER"]

    def _ejecutar_agente(self, script, contexto=""):
        """Ejecuta un agente como subproceso y captura su resultado."""
        if not os.path.exists(script):
            return f"[ERROR] {script} no existe."

        try:
            registrar_log(f"Ejecutando: {script}")
            cmd = [sys.executable, script]

            resultado = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=60
            )

            salida = resultado.stdout.strip()
            if resultado.returncode != 0 and resultado.stderr:
                salida += f"\n[ALERTA]: {resultado.stderr[:200]}"

            return salida if salida else "[Sin output]"

        except subprocess.TimeoutExpired:
            return f"[TIMEOUT] {script} tardó más de 60 segundos."
        except Exception as e:
            return f"[ERROR] {script}: {e}"

    def _ejecutar_via_router(self, orden):
        """Delega al agent_router para clasificación inteligente."""
        try:
            resultado = subprocess.run(
                [sys.executable, "agent_router.py", orden],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=90
            )
            return resultado.stdout.strip() or "[Router sin output]"
        except Exception as e:
            return f"[ERROR Router]: {e}"

    def _ejecutar_cadena(self, agentes, orden):
        """
        Ejecuta agentes en cadena. El resultado de cada uno se resume
        antes de pasarse al siguiente para evitar contextos gigantes.
        Sintetiza al final con Groq.
        """
        resultados_por_agente = {}

        for i, agente in enumerate(agentes):
            print(f"   [{i+1}/{len(agentes)}] {agente}...")

            # Depositar orden en el bus
            id_msg = bus.depositar(
                de="maestro_ceo",
                para=agente.replace(".py", ""),
                tipo="orden",
                contenido=orden,
                contexto={"paso": i+1, "total": len(agentes)}
            )

            # Ejecutar el agente
            output = self._ejecutar_agente(agente)
            resultados_por_agente[agente] = output

            # Registrar en el bus
            bus.depositar(
                de=agente.replace(".py", ""),
                para="maestro_ceo",
                tipo="resultado",
                contenido=resumir_output(output),
                respuesta_a=id_msg
            )

            time.sleep(2)

        # Síntesis final con Groq — respuesta coherente al usuario
        print("   Sintetizando resultado final...")
        return sintetizar_resultado(orden, resultados_por_agente)

    def procesar_orden(self, orden):
        """Punto de entrada principal."""
        print(f"\n🤖 CEO procesando: {orden[:80]}...")
        registrar_log(f"Orden recibida: {orden[:100]}")

        id_orden = bus.depositar(
            de="usuario",
            para="maestro_ceo",
            tipo="orden",
            contenido=orden
        )

        agentes = self._decidir_agentes(orden)

        if agentes == ["ROUTER"]:
            print("   Delegando al Router...")
            resultado = self._ejecutar_via_router(orden)
        elif len(agentes) == 1:
            print(f"   Delegando a: {agentes[0]}")
            output = self._ejecutar_agente(agentes[0])
            resultado = sintetizar_resultado(orden, {agentes[0]: output})
        else:
            print(f"   Cadena: {' → '.join(agentes)}")
            resultado = self._ejecutar_cadena(agentes, orden)

        bus.depositar(
            de="maestro_ceo",
            para="usuario",
            tipo="resultado",
            contenido=resultado[:1000],
            respuesta_a=id_orden
        )

        registrar_log(f"Orden completada. Agentes: {agentes}")
        bus.limpiar_procesados(mantener_ultimos=100)

        return resultado


# ─────────────────────────────────────────────
#  FUNCIÓN PÚBLICA
# ─────────────────────────────────────────────

def procesar_orden(orden):
    ceo = MaestroCEO()
    return ceo.procesar_orden(orden)


# ─────────────────────────────────────────────
#  MODO INTERACTIVO
# ─────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) > 1:
        orden = " ".join(sys.argv[1:])
        print(procesar_orden(orden))
    else:
        print("💡 CEO Agencia Santi — Multi-Agente v2.1")
        print("   'bus' para ver estado del bus de mensajes")
        print("   'salir' para terminar\n")

        while True:
            try:
                orden = input("Orden: ").strip()
                if not orden:
                    continue
                if orden.lower() in ("salir", "exit", "quit"):
                    break
                if orden.lower() == "bus":
                    bus.ver_estado()
                    continue

                resultado = procesar_orden(orden)
                print(f"\n{resultado}\n")
                print("─" * 60)

            except KeyboardInterrupt:
                print("\n[CEO] Apagado ordenado.")
                break