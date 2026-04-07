# ARCHIVO: agent_rag.py
# AREA: CEREBRO
# DESCRIPCION: Agente con memoria (RAG) que responde preguntas utilizando un modelo de lenguaje y una base de conocimiento.
# TECNOLOGIA: Python, chromadb, llama-3.3-70b

from llm_router import completar
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
import sys
import time
import os
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

MODEL = sys.argv[1] if len(sys.argv) > 1 else "llama-3.3-70b"
KB_DIR = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("kb")
MAX_RESULTS = int(sys.argv[3]) if len(sys.argv) > 3 else 5
INDEXING_INTERVAL = int(sys.argv[4]) if len(sys.argv) > 4 else 60  # intervalo de indexacion en segundos

client = chromadb.Client()
collection = client.get_or_create_collection("knowledge")

embed = embedding_functions.DefaultEmbeddingFunction()

def index_kb():
    try:
        start_time = time.time()
        num_docs = 0
        for file in KB_DIR.glob("*"):
            text = file.read_text(encoding="utf-8")
            collection.add(
                documents=[text],
                ids=[file.name]
            )
            num_docs += 1
        end_time = time.time()
        print(f"Base de conocimiento indexada con éxito. Total de documentos: {num_docs}")
        print(f"Tiempo de indexación: {end_time - start_time:.2f} segundos")
        print(f"Velocidad de indexación: {num_docs / (end_time - start_time):.2f} docs/seg")
        print(f"Intervalo de indexación: {INDEXING_INTERVAL} segundos")
    except Exception as e:
        print(f"Error al indexar la base de conocimiento: {e}")

def query_kb(question: str):
    try:
        results = collection.query(
            query_texts=[question],
            n_results=MAX_RESULTS
        )
        docs = results["documents"][0]
        return "\n".join(docs)
    except Exception as e:
        print(f"Error al consultar la base de conocimiento: {e}")
        return ""

def _groq_compat_create(**kwargs):
    """Compatibilidad con llamadas antiguas a client.chat.co"""

def main():
    print(f"Modelo de lenguaje: {MODEL}")
    print(f"Directorio de la base de conocimiento: {KB_DIR}")
    print(f"Número máximo de resultados: {MAX_RESULTS}")
    print(f"Intervalo de indexación: {INDEXING_INTERVAL} segundos")
    index_kb()
    while True:
        try:
            question = sys.argv[5] if len(sys.argv) > 5 else "¿Cuál es el significado de la vida?"
            print(f"Pregunta: {question}")
            answer = query_kb(question)
            print(f"Respuesta: {answer}")
            time.sleep(INDEXING_INTERVAL)
        except KeyboardInterrupt:
            print("Interrupción del usuario. Saliendo...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
    print("Resumen ejecutivo:")
    print(f"Modelo de lenguaje: {MODEL}")
    print(f"Directorio de la base de conocimiento: {KB_DIR}")
    print(f"Número máximo de resultados: {MAX_RESULTS}")
    print(f"Intervalo de indexación: {INDEXING_INTERVAL} segundos")