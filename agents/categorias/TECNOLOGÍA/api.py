#!/usr/bin/env python3
"""
Archivo: api.py
Área: Herramientas
Descripción: FastAPI backend para el sistema multi-agente.
"""

import json
import logging
import os
import random
import re
import sys
from datetime import datetime
from math import pi, sin, cos
from logging_config import setup_logging
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from agent_router_projects import (
    ensure_project,
    load_state,
    save_state,
    add_recent,
    route_intent,
    handle_chat,
    handle_task,
    handle_rag,
    handle_save,
    update_summary,
)
from rag_index import index_kb

# Permite pasar parámetros por línea de comando
if len(sys.argv) > 1:
    GROQ_API_KEY = sys.argv[1]
else:
    from config import GROQ_API_KEY

setup_logging()
logger = logging.getLogger(__name__)

# Título y versión de la API
app = FastAPI(title="Agentes Locales API", version="0.2.0")

# Modelo de solicitud de chat
class ChatRequest(BaseModel):
    company: str
    project: str
    message: str

# Modelo de solicitud de indexación
class IndexRequest(BaseModel):
    company: str
    project: str

# Verifica la salud de la API
@app.get("/health")
def health():
    try:
        if not GROQ_API_KEY or GROQ_API_KEY.startswith("gsk_"):
            return {
                "status": "warning",
                "groq": "API_KEY not configured",
                "detail": "Set GROQ_API_KEY in .env",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        return {
            "status": "ok",
            "groq": "configured",
            "backend": "groq-api",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Configuration error: {exc}")

# Procesa una solicitud de chat
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        project_path = ensure_project(req.company, req.project)
        state = load_state(project_path)
        state = add_recent(state, "user", req.message)
        route = route_intent(state, req.message)

        if route == "SAVE":
            out = handle_save(project_path, req.message)
        elif route == "TASK":
            out = handle_task(project_path, state, req.message)
        elif route == "RAG":
            out = handle_rag(project_path, state, req.message)
        else:
            out = handle_chat(state, req.message)

        state = add_recent(state, "assistant", out)
        save_state(project_path, state)

        # Calcula un valor aleatorio para demostrar cálculos precisos
        valor_aleatorio = random.uniform(0, 100)
        return {
            "output": out,
            "valor_aleatorio": valor_aleatorio,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": update_summary(state),
        }
    except Exception as exc:
        logger.error(f"Error procesando solicitud de chat: {exc}")
        return {"error": str(exc), "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

# Indexa un proyecto
@app.post("/index")
def index(req: IndexRequest):
    try:
        project_path = ensure_project(req.company, req.project)
        index_kb(project_path)
        return {"message": "Proyecto indexado con éxito", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    except Exception as exc:
        logger.error(f"Error indexando proyecto: {exc}")
        return {"error": str(exc), "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)