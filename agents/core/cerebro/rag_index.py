"""Index knowledge base files into ChromaDB.

Usage:
    python rag_index.py                          # index global kb/
    python rag_index.py --project acme/webapp    # index projects/acme/webapp/kb/
"""
import argparse
import logging
from pathlib import Path

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from agencia.agents.herramientas.config import (
    KB_DIR, MEMORY_DB_DIR, COLLECTION_NAME, EMBEDDING_MODEL,
    CHUNK_SIZE, CHUNK_OVERLAP, PROJECTS_DIR,
)
from agencia.agents.herramientas.logging_config import setup_logging

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

logger = logging.getLogger(__name__)


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i + chunk_size])
        i += chunk_size - overlap
    return chunks


def index_kb(kb_dir: Path, db_dir: Path, collection_name: str = COLLECTION_NAME):
    """Index all files in kb_dir into ChromaDB at db_dir."""
    model = SentenceTransformer(EMBEDDING_MODEL)

    files = [f for f in kb_dir.glob("*") if f.is_file()]
    if not files:
        logger.warning("No files found in %s. Add files and retry.", kb_dir)
        return

    ids, docs, metas, embs = [], [], [], []
    for f in files:
        txt = f.read_text(encoding="utf-8", errors="ignore")
        chunks = chunk_text(txt)
        for j, ch in enumerate(chunks):
            ids.append(f"{f.name}__{j}")
            docs.append(ch)
            metas.append({"source": f.name, "chunk": j})
            embs.append(model.encode(ch).tolist())

    db_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(
        path=str(db_dir),
        settings=Settings(anonymized_telemetry=False),
    )

    # Clean re-index: delete existing collection if present
    try:
        client.delete_collection(collection_name)
        logger.info("Deleted existing collection '%s' for clean re-index.", collection_name)
    except ValueError:
        logger.info("No existing collection '%s' to delete; creating fresh.", collection_name)

    col = client.get_or_create_collection(collection_name)
    col.add(ids=ids, documents=docs, metadatas=metas, embeddings=embs)
    logger.info("Indexed %d chunks from %d files in %s", len(ids), len(files), kb_dir)


def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="Index KB files into ChromaDB")
    parser.add_argument(
        "--project",
        type=str,
        default=None,
        help="company/project to index (e.g. acme/webapp). Indexes projects/acme/webapp/kb/",
    )
    args = parser.parse_args()

    if args.project:
        parts = args.project.split("/", 1)
        if len(parts) != 2:
            logger.error("--project must be in format company/project")
            return
        company, project = parts
        kb = PROJECTS_DIR / company / project / "kb"
        db = PROJECTS_DIR / company / project / "memory_db"
    else:
        kb = KB_DIR
        db = MEMORY_DB_DIR

    index_kb(kb, db)


if __name__ == "__main__":
    main()
