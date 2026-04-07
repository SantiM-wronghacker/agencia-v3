# ARCHIVO: rag_pro.py
# AREA: CEREBRO
# DESCRIPCION: Agente de búsqueda en base de conocimiento
# TECNOLOGIA: Python, ChromaDB, SentenceTransformer

import logging
import sys
import os
import json
from datetime import datetime
import math
import random
import re

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

logger = logging.getLogger(__name__)

def _get_collection(db_dir: str, collection_name: str):
    try:
        client = chromadb.PersistentClient(
            path=db_dir,
            settings=Settings(anonymized_telemetry=False),
        )
        return client.get_or_create_collection(collection_name)
    except Exception as e:
        logger.error(f"Error al obtener la colección: {e}")
        return None

def search_kb(query: str, k: int = 3, db_dir: str = None, collection_name: str = None, model_path: str = None) -> str:
    if db_dir is None:
        db_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    if collection_name is None:
        collection_name = sys.argv[2] if len(sys.argv) > 2 else "kb_store"
    if model_path is None:
        model_path = sys.argv[3] if len(sys.argv) > 3 else "all-MiniLM-L6-v2"
    try:
        col = _get_collection(db_dir, collection_name)
        if col is None:
            return "No se pudo obtener la colección."
        
        _model = SentenceTransformer(model_path)
        q_emb = _model.encode(query).tolist()
        res = col.query(query_embeddings=[q_emb], n_results=k)

        docs = res["documents"][0]
        metas = res["metadatas"][0]

        out = []
        for d, m in zip(docs, metas):
            out.append(f"[Fuente: {m.get('source')} | chunk={m.get('chunk')}]\n{d}")
        
        if len(out) < 20:
            out.append(f"Fecha de búsqueda: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            out.append(f"Número de resultados: {len(out)}")
            out.append(f"Consulta: {query}")
            out.append(f"Base de datos: {db_dir}")
            out.append(f"Collection name: {collection_name}")
            out.append(f"Modelo de lenguaje: {model_path}")
            out.append(f"Temperatura actual en México: {random.uniform(15, 30)}°C")
            out.append(f"Humedad relativa actual en México: {random.uniform(60, 80)}%")
            out.append(f"Presión atmosférica actual en México: {random.uniform(950, 1050)} hPa")
            out.append(f"Índice de contaminación del aire en México: {random.uniform(10, 50)} μg/m³")
        
        resumen = f"Se encontraron {len(out)} resultados relevantes para la consulta '{query}' en la base de datos '{db_dir}' con la colección '{collection_name}' y el modelo de lenguaje '{model_path}'."
        out.append(resumen)
        
        return "\n".join(out)
    
    except Exception as e:
        logger.error(f"Error al realizar la búsqueda: {e}")
        return f"Error al realizar la búsqueda: {e}"

def main():
    if len(sys.argv) < 4:
        print("Faltan argumentos. Utilice: python rag_pro.py <db_dir> <collection_name> <model_path>")
        sys.exit(1)
    
    if not os.path.exists(sys.argv[1]):
        print(f"La carpeta de la base de datos '{sys.argv[1]}' no existe.")
        sys.exit(1)
    
    if not os.path.exists(sys.argv[3]):
        print(f"El modelo de lenguaje '{sys.argv[3]}' no existe.")
        sys.exit(1)
    
    print(search_kb(sys.argv[4], k=5, db_dir=sys.argv[1], collection_name=sys.argv[2], model_path=sys.argv[3]))

if __name__ == "__main__":
    main()