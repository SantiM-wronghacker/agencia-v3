import json
import logging
import numpy as np
import re
from datetime import datetime
from pathlib import Path
import sys
import time

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

MODEL_FAST = "llama-3.3-70b-versatile"
MODEL_STRONG = "llama-3.3-70b-versatile"
KB_EMBEDDING_MODEL = "llama-3.3-70b-versatile"
USE_STRONG_FOR_TASK = True

RUNS_DIR = Path("runs")
KB_DIR = Path("kb")
KB_EMBEDDINGS_CACHE = Path(".kb_embeddings_cache.json")

GROQ_COMM_ERROR_PREFIX = "Error al comunicarse con Groq"
GROQ_COMM_ERROR_MSG = GROQ_COMM_ERROR_PREFIX + " ({model}): {e}. Asegúrate de que el modelo esté corriendo."
KB_EMPTY_ERROR = "La base de conocimiento está vacía. No se puede realizar la búsqueda."
EMBEDDING_ERROR_MSG = "Error al generar embedding con Groq ({model}): {e}. Asegúrate de que el modelo esté corriendo."
SAVE_FILE_ERROR_MSG = "Error al guardar el archivo en {path}: {e}"

RUNS_DIR.mkdir(exist_ok=True)
KB_DIR.mkdir(exist_ok=True)

SYSTEM_CHAT = """Eres un asistente dentro de un SISTEMA DE AGENTES DE SOFTWARE (Python + Groq). Tu función principal es guiar al usuario a través de las capacidades del sistema y resolver dudas generales.

REGLAS:
- "router" significa router de agentes, NO Wi-Fi.
- PROHIBIDO mencionar Wi-Fi, IPs, routers físicos o estándares de red.
- SOLO existen estas rutas: CHAT, SAVE, TASK, RAG. Explica sus propósitos.
- NO sugieras acciones que el usuario no pidió explícitamente.
- Si hay confusión sobre qué hacer, explica las opciones disponibles (CHAT, SAVE, TASK, RAG) y pregunta CLARAMENTE cuál desea usar, pidiéndole que elija un número o nombre.

Estilo: claro, breve, técnico y siempre útil.
"""

SYSTEM_PLANNER = """Eres un Planner profesional.
Tu objetivo es transformar una petición de usuario en un plan estructurado y accionable.

Devuelve:
1) Objetivo claro y conciso de la tarea.
2) Pasos detallados (5–10) para alcanzar el objetivo. Cada paso debe ser una acción concreta y lógica.
3) Entregables esperados al finalizar la tarea.
4) Riesgos potenciales o supuestos clave que podrían afectar la ejecución.

Utiliza formato Markdown claro y legible.
"""

SYSTEM_EXEC = """Eres un Executor.
Tu misión es generar un entregable real basado en una petición y un plan previos.

Tu respuesta debe ser un documento en Markdown profesional. Incluye:
- Un título claro del entregable.
- Una introducción breve.
- El contenido principal del entregable siguiendo el plan.
- Al final, un checklist de validación o pasos siguientes si aplica.

Asegúrate de que el entregable sea coherente con el plan y la petición original.
"""

def llm(system: str, user: str, model: str) -> str:
    try:
        import requests
        response = requests.post(
            f"https://api.groq.com/v1/models/{model}/completions",
            json={
                "prompt": system + "\n\n" + user,
                "max_tokens": 2048,
                "temperature": 0.7
            }
        )
        if response.status_code == 200:
            return response.json()["text"].strip()
        else:
            log.error(GROQ_COMM_ERROR_MSG.format(model=model, e=response.text))
            return GROQ_COMM_ERROR_MSG.format(model=model, e=response.text)
    except Exception as e:
        log.error(GROQ_COMM_ERROR_MSG.format(model=model, e=e))
        return GROQ_COMM_ERROR_MSG.format(model=model, e=e)

def llm_embed(text: str, model: str = KB_EMBEDDING_MODEL) -> list[float]:
    try:
        import requests
        response = requests.post(
            f"https://api.groq.com/v1/models/{model}/embeddings",
            json={
                "prompt": text
            }
        )
        if response.status_code == 200:
            return response.json()["embedding"]
        else:
            log.error(EMBEDDING_ERROR_MSG.format(model=model, e=response.text))
            return []
    except Exception as e:
        log.error(EMBEDDING_ERROR_MSG.format(model=model, e=e))
        return []

def task_model() -> str:
    return MODEL_STRONG if USE_STRONG_FOR_TASK else MODEL_FAST

def is_ux_confusion(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in [
        "ux", "confus", "no se que agente", "no sé qué agente",
        "cual agente", "qué agente", "no se cual", "no sé cuál",
        "menu", "menú", "ayuda"
    ])

def route_user_input(user_text: str) -> tuple[str, str, list[str]]:
    u = user_text.strip().lower()
    signals = []

    explicit = {
        "1": "CHAT", "chat": "CHAT",
        "2": "SAVE", "save": "SAVE",
        "3": "TASK", "task": "TASK",
        "4": "RAG",  "rag": "RAG",
        "menu": "CHAT", "menú": "CHAT", "ayuda": "CHAT"
    }
    if u in explicit:
        return explicit[u], f"Elección explícita del usuario: {explicit[u]}.", ["explicit_choice"]

    if u.startswith("guardar:") or any(x in u for x in ["guarda esto", "anota esto", "haz una nota", "memoriza esto", "archiva esto"]):
        return "SAVE", "Solicitud explícita de guardado de información.", ["save_request"]

    if any(x in u for x in ["plan", "paso", "checklist", "estrategia", "propuesta", "entregable", "estructura", "desarrolla", "crea un plan", "genera un informe", "diseña un sistema"]):
        return "TASK", "Solicitud de planificación o generación de un entregable estructurado.", ["task_request"]

    if any(x in u for x in ["kb/", "manual", "proceso", "política", "precio", "documento", "información sobre", "dame datos de", "refiérete a", "base de conocimiento", "busca en los documentos", "busca sobre", "qué es"]):
        return "RAG", "Consulta que requiere base de conocimiento (kb/) para contexto.", ["rag_query"]

    if is_ux_confusion(user_text):
        return "CHAT", "Confusión detectada: se orienta al usuario a través del menú de opciones.", ["ux_confusion"]

    return "CHAT", "Conversación general o pregunta que no encaja en otras rutas.", []

def split_text_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    if not text:
        return []

    chunks = []

    segments = text.split('\n\n')
    current_chunk_text = ""

    for segment in segments:
        if not segment.strip():
            continue

        if len(current_chunk_text) + len(segment) > chunk_size and current_chunk_text:
            chunks.append(current_chunk_text.strip())
            current_chunk_text = current_chunk_text[-overlap:].strip() + "\n\n" + segment
        else:
            current_chunk_text += "\n\n" + segment

    if current_chunk_text:
        chunks.append(current_chunk_text.strip())

    final_chunks = []
    for chunk in chunks:
        if len(chunk) > chunk_size + overlap:
            sub_current_position = 0
            while sub_current_position < len(chunk):
                sub_end_position = min(sub_current_position + chunk_size, len(chunk))
                final_chunks.append(chunk[sub_current_position:sub_end_position].strip())
                sub_current_position += chunk_size - overlap
                if sub_current_position >= len(chunk):
                    break
        elif chunk.strip():
            final_chunks.append(chunk.strip())

    return final_chunks

class KnowledgeBase:
    def __init__(self):
        self.documents = {}
        self._load_cache()
        self._all_chunks_flat = []

    def _load_cache(self):
        if KB_EMBEDDINGS_CACHE.exists():
            try:
                with open(KB_EMBEDDINGS_CACHE, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                    for path_str, doc_data in cached_data.items():
                        path_obj = Path(path_str)
                        processed_chunks = []
                        for chunk_data in doc_data.get('chunks', []):
                            processed_chunks.append({
                                'content': chunk_data['content'],
                                'embedding': np.array(chunk_data['embedding']),
                                'chunk_id': chunk_data['chunk_id']
                            })
                        self.documents[path_obj] = {
                            'last_modified': doc_data['last_modified'],
                            'chunks': processed_chunks
                        }
                log.info(f"[KB] Cache de KB cargada con {len(self.documents)} documentos.")
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                log.warning(f"[KB] Advertencia: Cache de KB corrupta o inválida: {e}. Se reconstruirá.")
                self.documents = {}
        self._rebuild_flat_chunks()

    def _save_cache(self):
        serializable_data = {}
        for path, doc_data in self.documents.items():
            serializable_chunks = []
            for chunk_data in doc_data['chunks']:
                serializable_chunks.append({
                    'content': chunk_data['content'],
                    'embedding': chunk_data['embedding'].tolist(),
                    'chunk_id': chunk_data['chunk_id']
                })
            serializable_data[str(path)] = {
                'last_modified': doc_data['last_modified'],
                'chunks': serializable_chunks
            }
        try:
            with open(KB_EMBEDDINGS_CACHE, 'w', encoding='utf-8') as f:
                json.dump(serializable_data, f, ensure_ascii=False, indent=2)
            log.info("[KB] Cache de KB guardada.")
        except IOError as e:
            log.error(f"[KB] Error al guardar la caché de KB: {e}")

    def _rebuild_flat_chunks(self):
        self._all_chunks_flat = []
        for path, doc_data in self.documents.items():
            for chunk in doc_data['chunks']:
                chunk_with_source = chunk.copy()
                chunk_with_source['source_file'] = path.name
                self._all_chunks_flat.append(chunk_with_source)
        log.debug(f"[KB] Lista plana de chunks reconstruida. Total: {len(self._all_chunks_flat)} chunks.")

    def update_kb(self):
        log.info("[KB] Actualizando base de conocimiento...")
        current_files = set(KB_DIR.glob("*"))

        files_to_remove = [path for path in self.documents if path not in current_files]
        for path in files_to_remove:
            log.info(f"[KB] Eliminando documento obsoleto: {path.name}")
            del self.documents[path]

        new_or_modified_count = 0
        for f in current_files:
            if not f.is_file():
                continue

            try:
                last_modified_time = f.stat().st_mtime
                if f in self.documents and self.documents[f]['last_modified'] >= last_modified_time:
                    continue

                log.info(f"[KB] Procesando archivo (nuevo/modificado): {f.name}")
                content = f.read_text(encoding="utf-8", errors="ignore")

                if not content.strip():
                    log.warning(f"[KB] Advertencia: El archivo {f.name} está vacío o solo contiene espacios. Se omitirá.")
                    if f in self.documents:
                        del self.documents[f]
                    continue

                chunks_data = []
                text_chunks = split_text_into_chunks(content)

                if not text_chunks:
                    log.warning(f"[KB] Advertencia: No se pudieron generar chunks para {f.name}. Se omitirá.")
                    if f in self.documents:
                        del self.documents[f]
                    continue

                for i, chunk_text in enumerate(text_chunks):
                    embedding = llm_embed(chunk_text, KB_EMBEDDING_MODEL)
                    if embedding:
                        chunks_data.append({
                            'content': chunk_text,
                            'embedding': np.array(embedding),
                            'chunk_id': f"{f.name}_chunk_{i}"
                        })
                    else:
                        log.error(f"[KB] Error: No se pudo generar el embedding para un chunk de {f.name}. Chunk {i} omitido.")

                if chunks_data:
                    self.documents[f] = {
                        'last_modified': last_modified_time,
                        'chunks': chunks_data
                    }
                    new_or_modified_count += 1
                else:
                    log.error(f"[KB] Error: No se pudieron generar chunks válidos con embeddings para {f.name}. Se omitirá el archivo.")
                    if f in self.documents:
                        del self.documents[f]

            except Exception as e:
                log.error(f"[KB] Error al leer o procesar {f.name}: {e}")
                if f in self.documents:
                    del self.documents[f]

        self._save_cache()
        self._rebuild_flat_chunks()
        log.info(f"[KB] Base de conocimiento actualizada. {len(self.documents)} documentos (conteniendo {len(self._all_chunks_flat)} chunks) cargados.")

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if not self._all_chunks_flat:
            log.warning(KB_EMPTY_ERROR)
            return []

        query_embedding = llm_embed(query, KB_EMBEDDING_MODEL)
        if not query_embedding:
            return []
        query_embedding = np.array(query_embedding)

        similarities = []
        for chunk_data in self._all_chunks_flat:
            doc_embedding = chunk_data['embedding']

            if doc_embedding.size == 0:
                log.warning(f"[KB] Advertencia: Embedding vacío para el chunk {chunk_data.get('chunk_id', 'desconocido')} de {chunk_data.get('source_file', 'desconocido')}. Se omitirá en la búsqueda.")
                continue

            norm_query = np.linalg.norm(query_embedding)
            norm_doc = np.linalg.norm(doc_embedding)

            if norm_query == 0 or norm_doc == 0:
                similarity = 0.0
            else:
                similarity = np.dot(query_embedding, doc_embedding) / (norm_query * norm_doc)

            similarities.append((similarity, chunk_data))

        similarities.sort(key=lambda x: x[0], reverse=True)

        results = []
        for sim, chunk_data in similarities[:top_k]:
            results.append({
                'score': sim,
                'source_file': chunk_data['source_file'],
                'content': chunk_data['content'],
                'chunk_id': chunk_data['chunk_id']
            })
        return results

kb_manager = KnowledgeBase()

def main():
    user_input = sys.argv[1] if len(sys.argv) > 1 else "Hola, ¿cómo puedo ayudarte?"
    print(f"Input procesado: {user_input}")

    route, message, signals = route_user_input(user_input)
    print(f"Ruta seleccionada: {route}")
    print(f"Mensaje: {message}")
    print(f"Señales: {signals}")

    if route == "CHAT":
        response = llm(SYSTEM_CHAT, user_input, MODEL_FAST)
        print(f"Respuesta del modelo: {response}")
    elif route == "SAVE":
        print("Guardar información")
    elif route == "TASK":
        print("Generar un plan")
    elif route == "RAG":
        kb_manager.update_kb()
        results = kb_manager.search(user_input)
        for result in results:
            print(f"Puntuación: {result['score']}, Fuente: {result['source_file']}, Contenido: {result['content']}")

    time.sleep(2)

if __name__ == "__main__":
    main()