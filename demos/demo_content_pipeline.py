"""Demo: Content Pipeline completo — Researcher → Writer → SEO → Reviewer"""
import sys
import time
from pathlib import Path

# Asegura root en path al ejecutar directamente
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from groups.content_pipeline import create_content_pipeline
from memory.db import AgenciaDB


def main():
    print("=== DEMO: Content Pipeline ===\n")
    db = AgenciaDB()
    group = create_content_pipeline(db)

    task = "Inteligencia artificial en pequeñas empresas mexicanas en 2026"
    print(f"Tarea: {task}\n")
    print("Ejecutando pipeline: Researcher → Writer → SEO → Reviewer\n")
    print("-" * 50)

    start = time.time()
    result = group.execute(task)
    elapsed = round(time.time() - start, 1)

    print(f"\n{'='*50}")
    print(f"Pipeline completado en {elapsed}s")
    print(f"Steps: {len(result.steps)}")
    print(f"Success: {result.success}")
    print(f"\n--- OUTPUT FINAL ---\n")
    print(result.final_output)

    if not result.success:
        print(f"\nError: {result.error}")


if __name__ == "__main__":
    main()
