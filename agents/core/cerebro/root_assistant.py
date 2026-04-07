"""
ÁREA: CEREBRO
DESCRIPCIÓN: Asistente raíz con permisos de administrador. Procesa consultas
             generales, busca en internet via DuckDuckGo, consulta la base de
             conocimiento vectorial (ChromaDB) y responde usando llm_router
             con rotación automática entre Groq, Cerebras, Gemini, Mistral.
TECNOLOGÍA: llm_router (multi-proveedor), ChromaDB, DuckDuckGo
"""

import os
import re
import sys
import time
import logging

import chromadb
from duckduckgo_search import DDGS

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

# Importar router — si no existe, fallback a Groq directo
try:
    from agencia.agents.cerebro.llm_router import completar_simple
    USAR_ROUTER = True
except Exception:
    try:
        from groq import Groq
    except Exception:
        pass
    USAR_ROUTER = False

# ============================================================
# CONFIGURACIÓN
# ============================================================
API_KEY_GROQ   = "GROQ_API_KEY_PLACEHOLDER"
MODELO_GROQ    = "llama-3.3-70b-versatile"
LOG_EVOLUCION  = "registro_noche.txt"
MAX_REINTENTOS = 3
PAUSA_REINTENTO = 3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================================
# LOGGING AL ARCHIVO CENTRAL
# ============================================================
def registrar_log(mensaje):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    linea = f"[{timestamp}] [ROOT_ASSISTANT] {mensaje}"
    try:
        with open(LOG_EVOLUCION, "a", encoding="utf-8") as f:
            f.write(linea + "\n")
    except Exception:
        pass
    print(linea)

# ============================================================
# CLASE PRINCIPAL
# ============================================================
class RootAssistant:
    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.db_path   = os.path.join(self.base_path, "vector_db")

        # Cliente Groq directo (fallback si no hay router)
        if not USAR_ROUTER:
            self.client_groq = Groq(api_key=API_KEY_GROQ)

        # Inicializar ChromaDB
        try:
            self.chroma_client = chromadb.PersistentClient(path=self.db_path)
            self.collection    = self.chroma_client.get_or_create_collection(name="knowledge_base")
            registrar_log("ChromaDB inicializado correctamente.")
        except Exception as e:
            registrar_log(f"Advertencia ChromaDB: {e}. Continuando sin base vectorial.")
            self.chroma_client = None
            self.collection    = None

        modo = "llm_router (multi-proveedor)" if USAR_ROUTER else "Groq directo"
        registrar_log(f"Root Assistant iniciado — Motor: {modo}")

    # ──────────────────────────────────────────────────────────
    # BÚSQUEDA WEB
    # ──────────────────────────────────────────────────────────
    def buscar_web(self, query, max_resultados=3):
        try:
            registrar_log(f"Buscando en web: {query[:60]}...")
            with DDGS() as ddgs:
                resultados = list(ddgs.text(query, max_results=max_resultados))
            if resultados:
                contexto = "\n".join([
                    f"- {r.get('title', '')}: {r.get('body', '')}"
                    for r in resultados
                ])
                registrar_log(f"Web: {len(resultados)} resultados.")
                return contexto
            return ""
        except Exception as e:
            registrar_log(f"Error en búsqueda web: {e}")
            return ""

    # ──────────────────────────────────────────────────────────
    # CONSULTA VECTORIAL
    # ──────────────────────────────────────────────────────────
    def consultar_vectorial(self, query, n_resultados=3):
        if not self.collection:
            return ""
        try:
            resultados = self.collection.query(query_texts=[query], n_results=n_resultados)
            documentos = resultados.get("documents", [[]])[0]
            if documentos:
                registrar_log(f"ChromaDB: {len(documentos)} documentos relevantes.")
                return "\n".join(documentos)
            return ""
        except Exception as e:
            registrar_log(f"Error consultando ChromaDB: {e}")
            return ""

    # ──────────────────────────────────────────────────────────
    # LLAMADA A IA (ROUTER O GROQ DIRECTO)
    # ──────────────────────────────────────────────────────────
    def llamar_ia(self, prompt, system_prompt=None):
        if system_prompt is None:
            system_prompt = (
                "Eres el Asistente Raíz de la Agencia Santi. "
                "Respondes de forma clara, precisa y en español. "
                "Si tienes contexto web o de documentos, úsalo para enriquecer tu respuesta."
            )

        if USAR_ROUTER:
            try:
                registrar_log("Llamando via llm_router...")
                prompt_completo = f"{system_prompt}\n\n{prompt}"
                respuesta = completar_simple(prompt_completo)
                registrar_log(f"Router respondió ({len(respuesta)} chars).")
                return respuesta
            except Exception as e:
                registrar_log(f"Error en router: {e}")
                return None
        else:
            # Fallback Groq directo
            for intento in range(1, MAX_REINTENTOS + 1):
                try:
                    registrar_log(f"Llamando Groq directo (intento {intento})...")
                    completion = self.client_groq.chat.completions.create(
                        model=MODELO_GROQ,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=4096,
                        stream=False
                    )
                    respuesta = completion.choices[0].message.content
                    registrar_log(f"Groq respondió ({len(respuesta)} chars).")
                    return respuesta
                except Exception as e:
                    registrar_log(f"Error Groq (intento {intento}): {e}")
                    time.sleep(PAUSA_REINTENTO * intento)
            return None

    # ──────────────────────────────────────────────────────────
    # LIMPIEZA DE RESPUESTA
    # ──────────────────────────────────────────────────────────
    def limpiar_respuesta(self, texto):
        if not texto:
            return texto
        if "```" in texto:
            bloque = re.search(r"```(?:python)?\s*\n(.*?)\n```", texto, re.DOTALL)
            if bloque:
                return bloque.group(1).strip()
        return texto.strip()

    # ──────────────────────────────────────────────────────────
    # PROCESAMIENTO PRINCIPAL
    # ──────────────────────────────────────────────────────────
    def process_query(self, query, session_id=None, usar_web=False):
        registrar_log(f"Procesando: {query[:80]}...")

        contexto_partes = []

        ctx_vectorial = self.consultar_vectorial(query)
        if ctx_vectorial:
            contexto_partes.append(f"CONOCIMIENTO BASE:\n{ctx_vectorial}")

        if usar_web:
            ctx_web = self.buscar_web(query)
            if ctx_web:
                contexto_partes.append(f"INFORMACIÓN WEB:\n{ctx_web}")

        if contexto_partes:
            prompt_completo = (
                "CONTEXTO DISPONIBLE:\n"
                + "\n\n".join(contexto_partes)
                + f"\n\nCONSULTA:\n{query}"
            )
        else:
            prompt_completo = query

        respuesta_raw    = self.llamar_ia(prompt_completo)
        respuesta_limpia = self.limpiar_respuesta(respuesta_raw)
        session          = session_id or f"sess_{int(time.time())}"

        registrar_log(f"Consulta procesada. Sesión: {session}")
        return respuesta_limpia, session

    # ──────────────────────────────────────────────────────────
    # AGREGAR CONOCIMIENTO
    # ──────────────────────────────────────────────────────────
    def agregar_conocimiento(self, texto, doc_id=None):
        if not self.collection:
            registrar_log("ChromaDB no disponible.")
            return False
        try:
            id_doc = doc_id or f"doc_{int(time.time())}"
            self.collection.add(documents=[texto], ids=[id_doc])
            registrar_log(f"Conocimiento agregado: {id_doc}")
            return True
        except Exception as e:
            registrar_log(f"Error agregando conocimiento: {e}")
            return False

# ============================================================
# PUNTO DE ENTRADA
# ============================================================
if __name__ == "__main__":
    asistente = RootAssistant()

    if len(sys.argv) > 1:
        consulta  = " ".join([a for a in sys.argv[1:] if a != "--web"])
        usar_web  = "--web" in sys.argv
        respuesta, session = asistente.process_query(consulta, usar_web=usar_web)
        print(f"\n{'='*50}")
        print(f"RESPUESTA:\n{respuesta}")
        print(f"{'='*50}")
    else:
        registrar_log("Modo interactivo. Escribe 'salir' para terminar.")
        print("\nRoot Assistant listo. Escribe tu consulta (añade --web para buscar en internet):\n")
        while True:
            try:
                entrada = input("Tú: ").strip()
                if not entrada:
                    continue
                if entrada.lower() in ["salir", "exit", "quit"]:
                    break
                usar_web = "--web" in entrada
                consulta = entrada.replace("--web", "").strip()
                respuesta, _ = asistente.process_query(consulta, usar_web=usar_web)
                print(f"\nAsistente: {respuesta}\n")
            except KeyboardInterrupt:
                break