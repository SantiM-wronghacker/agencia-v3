"""
AREA: CEREBRO
DESCRIPCION: Agente de búsqueda de información en una base de conocimiento con mejoras en manejo de errores, parámetros y salida de información
TECNOLOGIA: chromadb, sentence_transformers
"""
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from pathlib import Path
import sys
import time
import json
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

DB_DIR = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("memory_db")
COLLECTION_NAME = sys.argv[3] if len(sys.argv) > 3 else "kb_store"
MODEL_NAME = sys.argv[4] if len(sys.argv) > 4 else "all-MiniLM-L6-v2"
MAX_RESULTS = int(sys.argv[5]) if len(sys.argv) > 5 else 3

model = SentenceTransformer(MODEL_NAME)

client = chromadb.PersistentClient(
    path=str(DB_DIR),
    settings=Settings(anonymized_telemetry=False)
)
col = client.get_or_create_collection(COLLECTION_NAME)

def search(query: str, k=MAX_RESULTS):
    try:
        if not query or not isinstance(query, str):
            raise ValueError("La consulta debe ser una cadena no vacía")

        q_emb = model.encode(query).tolist()
        res = col.query(query_embeddings=[q_emb], n_results=k)

        if not res or not res["documents"] or not res["metadatas"]:
            return "No se encontraron resultados relevantes para la consulta"

        docs = res["documents"][0]
        metas = res["metadatas"][0]

        out = []
        for d, m in zip(docs, metas):
            source = m.get('source', 'desconocida')
            chunk = m.get('chunk', '0')
            timestamp = m.get('timestamp', datetime.now().isoformat())
            out.append(f"[Fuente: {source} | chunk={chunk} | fecha={timestamp}]\n{d}")

        return "\n\n---\n\n".join(out)

    except Exception as e:
        return f"Error en la búsqueda: {str(e)}. Tipo: {type(e).__name__}"

def generate_additional_info(query, results):
    info = [
        f"Consulta: {query}",
        f"Base de conocimiento: {str(DB_DIR)}",
        f"Colección: {COLLECTION_NAME}",
        f"Modelo de lenguaje: {MODEL_NAME}",
        f"Número de resultados: {MAX_RESULTS}",
        f"Fecha de búsqueda: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Tamaño de la colección: {col.count()}",
        "Información adicional: Si la consulta es muy amplia, puede ser útil reformularla para obtener resultados más precisos."
    ]
    return "\n".join(info)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python rag_query.py <pregunta> [db_dir] [collection_name] [model_name] [max_results]")
        pregunta = "¿Cuál es el propósito de la vida?"
    else:
        pregunta = sys.argv[1]

    result = search(pregunta)

    if len(result.split('\n')) < 20:
        result += "\n\n" + generate_additional_info(pregunta, result)

    print("\n" + result + "\n")
    print("Resumen ejecutivo: Se ha realizado una búsqueda en la base de conocimiento con la pregunta '" +
          pregunta + "' a las " + datetime.now().strftime('%H:%M:%S') +
          ". Se encontraron " + str(len(result.split('---')) - 1) + " resultados relevantes.")
    time.sleep(2)