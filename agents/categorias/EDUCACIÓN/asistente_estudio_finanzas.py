"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente de estudio de finanzas que busca información en fuentes confiables y genera resúmenes de estudio sobre conceptos clave de contaduría pública en México.
TECNOLOGÍA: Python, requests, BeautifulSoup, duckduckgo_search, groq
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
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False
API_KEY_GROQ = "GROQ_API_KEY_PLACEHOLDER"
MODELO_GROQ = "llama-3.3-70b-versatile"
LOG_EVOLUCION = "registro_noche.txt"

FUENTES_CONFIABLES = [
    "sat.gob.mx",
    "imcp.org.mx",
    "cinif.org.mx",
    "dof.gob.mx",
    "banxico.org.mx"
]

def registrar_log(mensaje):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    linea = f"[{timestamp}] [ESTUDIO_FINANZAS] {mensaje}"
    try:
        with open(LOG_EVOLUCION, "a", encoding="utf-8") as f:
            f.write(linea + "\n")
    except Exception:
        pass
    print(linea)

def buscar_en_web(query, max_resultados=5):
    try:
        registrar_log(f"Buscando: {query}")
        with DDGS() as ddgs:
            resultados = list(ddgs.text(
                f"{query} site:sat.gob.mx OR site:imcp.org.mx OR site:cinif.org.mx OR finanzas México NIF",
                max_results=max_resultados
            ))

        if not resultados:
            with DDGS() as ddgs:
                resultados = list(ddgs.text(query, max_results=max_resultados))

        contexto = "\n".join([
            f"- {r.get('title', '')}: {r.get('body', '')}"
            for r in resultados
        ])
        registrar_log(f"Se encontraron {len(resultados)} resultados.")
        return contexto

    except Exception as e:
        registrar_log(f"Error en búsqueda web: {e}")
        return ""

def llamar_groq(prompt, max_reintentos=3):
    for intento in range(1, max_reintentos + 1):
        try:
            completion = _groq_compat_create(
                model=MODELO_GROQ,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Eres un tutor experto en Contaduría Pública mexicana. "
                            "Conoces las NIF (Normas de Información Financiera), el SAT, "
                            "ISR, IVA, IMSS, INFONAVIT y toda la legislación fiscal mexicana. "
                            "Explicas de forma clara, estructurada y con ejemplos prácticos. "
                            "Siempre citas las normas o leyes aplicables cuando es relevante."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=4096,
                top_p=1,
                stream=False
            )
            time.sleep(2)
            return completion.choices[0].message.content
        except Exception as e:
            error_str = str(e).lower()
            if "rate limit" in error_str or "429" in error_str:
                registrar_log(f"Rate limit. Esperando {3 * intento}s...")
                time.sleep(3 * intento)
            else:
                registrar_log(f"Error Groq (intento {intento}): {e}")
                time.sleep(3)
    return None

def buscar_conceptos_clave(tema="Contaduría Pública"):
    contexto_web = buscar_en_web(f"conceptos principales {tema} México NIF SAT")

    prompt = f"""
Basándote en esta información de fuentes oficiales:

{contexto_web}

Lista los 8 conceptos más importantes de "{tema}" para estudiar Contaduría Pública en México.
Formato: solo los nombres de los conceptos, uno por línea, sin numeración ni explicaciones.
"""
    respuesta = llamar_groq(prompt)
    if respuesta:
        conceptos = [c.strip() for c in respuesta.strip().split("\n") if c.strip()]
        return conceptos[:8]
    return []

def generar_resumen_estudio(concepto, contexto_adicional=""):
    contexto_web = buscar_en_web(f"{concepto} contaduría México NIF SAT explicación")

    prompt = f"""
Contexto de fuentes oficiales:
{contexto_web}

{f"Contexto adicional: {contexto_adicional}" if contexto_adicional else ""}

Genera una ficha de estudio completa sobre "{concepto}" para un estudiante de Contaduría Pública en México.

Incluye:
1. Definición clara y precisa
2. Base legal o normativa (NIF, LISR, LIVA, etc. si aplica)
3. Ejemplo práctico con números
4. Puntos clave para recordar (máximo 3)
"""
    return llamar_groq(prompt)

def main(tema=None):
    if tema:
        registrar_log(f"Generando ficha de estudio para: {tema}")
        print(f"\nBuscando información sobre '{tema}'...")

        conceptos = buscar_conceptos_clave(tema)
        if conceptos:
            registrar_log(f"Conceptos encontrados: {len(conceptos)}")
            print(f"\nConceptos clave de {tema}:")
            for i, c in enumerate(conceptos, 1):
                print(f"  {i}. {c}")

        print(f"\nGenerando ficha detallada...")
        resumen = generar_resumen_estudio(tema)
        if resumen:
            print(f"\n{'='*60}")
            print(resumen)
            print(f"{'='*60}")
    else:
        tema = "Contaduría Pública"
        registrar_log(f"Generando ficha de estudio para: {tema}")
        print(f"\nBuscando información sobre '{tema}'...")

        conceptos = buscar_conceptos_clave(tema)
        if conceptos:
            registrar_log(f"Conceptos encontrados: {len(conceptos)}")
            print(f"\nConceptos clave de {tema}:")
            for i, c in enumerate(conceptos, 1):
                print(f"  {i}. {c}")

        print(f"\nGenerando ficha detallada...")
        resumen = generar_resumen_estudio(tema)
        if resumen:
            print(f"\n{'='*60}")
            print(resumen)
            print(f"{'='*60}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        tema_arg = " ".join(sys.argv[1:])
        main(tema=tema_arg)
    else:
        main()