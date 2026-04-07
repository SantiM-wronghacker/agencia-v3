"""Punto de entrada principal de agencia-v3 API."""
import sys
from pathlib import Path

# Asegura que el root del proyecto esté en el path cuando se ejecuta directamente
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from api.routes import app  # noqa: F401 — re-exportado para uvicorn

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8001, reload=False)
