"""
AREA: HERRAMIENTAS
DESCRIPCION: Centralized configuration for the multi-agent system.
TECNOLOGIA: Python
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(os.getenv("AGENTS_BASE_DIR", "."))
RUNS_DIR = BASE_DIR / "runs"
KB_DIR = BASE_DIR / "kb"
MEMORY_DB_DIR = BASE_DIR / "memory_db"
PROJECTS_DIR = BASE_DIR / "projects"

RUNS_DIR.mkdir(exist_ok=True)
KB_DIR.mkdir(exist_ok=True)

# Modelos Groq (nombres internos, se mapean en core.py)
MODEL_FAST = os.getenv("MODEL_FAST", "llama3:8b")
MODEL_STRONG = os.getenv("MODEL_STRONG", "gpt-oss:20b")

# Groq API (ya no necesitamos Ollama local)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "gsk_configurar_en_env")
GROQ_TIMEOUT = int(os.getenv("GROQ_TIMEOUT", "30"))

MAX_RECENT_TURNS = int(os.getenv("MAX_RECENT_TURNS", "10"))
STATE_FILE = RUNS_DIR / "state.json"

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "kb_store")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "900"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))

API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))


def load_config():
    return {
        "BASE_DIR": str(BASE_DIR),
        "RUNS_DIR": str(RUNS_DIR),
        "KB_DIR": str(KB_DIR),
        "MEMORY_DB_DIR": str(MEMORY_DB_DIR),
        "PROJECTS_DIR": str(PROJECTS_DIR),
        "MODEL_FAST": MODEL_FAST,
        "MODEL_STRONG": MODEL_STRONG,
        "GROQ_API_KEY": GROQ_API_KEY,
        "GROQ_TIMEOUT": GROQ_TIMEOUT,
        "MAX_RECENT_TURNS": MAX_RECENT_TURNS,
        "STATE_FILE": str(STATE_FILE),
        "EMBEDDING_MODEL": EMBEDDING_MODEL,
        "COLLECTION_NAME": COLLECTION_NAME,
        "CHUNK_SIZE": CHUNK_SIZE,
        "CHUNK_OVERLAP": CHUNK_OVERLAP,
        "API_HOST": API_HOST,
        "API_PORT": API_PORT,
    }

def main():
    config = load_config()
    if config is None:
        return

    print("Configuración del sistema de agentes:")
    print(f"Directorio base: {config['BASE_DIR']}")
    print(f"Directorio de ejecuciones: {config['RUNS_DIR']}")
    print(f"Directorio de conocimiento: {config['KB_DIR']}")
    print(f"Directorio de memoria: {config['MEMORY_DB_DIR']}")
    print(f"Directorio de proyectos: {config['PROJECTS_DIR']}")
    print(f"Modelo rápido: {config['MODEL_FAST']}")
    print(f"Modelo fuerte: {config['MODEL_STRONG']}")
    print(f"API Groq: {config['GROQ_API_KEY'][:10]}..." if len(config['GROQ_API_KEY']) > 10 else "NO CONFIGURADA")
    print(f"Tiempo de espera de Groq: {config['GROQ_TIMEOUT']} segundos")
    print(f"Número máximo de turnos recientes: {config['MAX_RECENT_TURNS']}")
    print(f"Archivo de estado: {config['STATE_FILE']}")
    print(f"Modelo de embedding: {config['EMBEDDING_MODEL']}")
    print(f"Nombre de la colección: {config['COLLECTION_NAME']}")
    print(f"Tamaño de chunk: {config['CHUNK_SIZE']}")
    print(f"Sobreposición de chunk: {config['CHUNK_OVERLAP']}")
    print(f"Host de la API: {config['API_HOST']}")
    print(f"Puerto de la API: {config['API_PORT']}")

    print("\nResumen ejecutivo:")
    print(f"Fecha y hora actual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Sistema operativo: {os.name}")
    print(f"Versión de Python: {sys.version}")

if __name__ == "__main__":
    main()