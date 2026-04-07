"""
AREA: CEREBRO
DESCRIPCION: Router inteligente de tareas entre proyectos. Recibe una tarea en lenguaje
             natural, detecta a que proyecto pertenece y la delega al orquestador
             correspondiente. Agente #500 del sistema.
TECNOLOGIA: Python stdlib (subprocess, json, os, re)
"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path

BASE_DIR     = Path(__file__).parent
PROYECTOS    = BASE_DIR / "proyectos"
HABILIDADES  = BASE_DIR / "habilidades.json"

# Palabras clave por proyecto (se construye dinamicamente)
def detectar_proyecto(consulta: str) -> str | None:
    """Detecta a qué proyecto pertenece la consulta. Devuelve el nombre del directorio."""
    consulta_lower = consulta.lower()

    if not PROYECTOS.exists():
        return None

    # 1. Busqueda directa por nombre de proyecto en la consulta
    for proyecto in PROYECTOS.iterdir():
        if not proyecto.is_dir():
            continue
        nombre = proyecto.name.lower().replace("_", " ")
        variantes = [proyecto.name.lower(), nombre]
        # Agrega variante sin numeros/guiones al final (way2theunknown_ -> way2theunknown)
        clean = re.sub(r'[_\d]+$', '', proyecto.name.lower())
        if clean:
            variantes.append(clean)
        for v in variantes:
            if v in consulta_lower:
                return proyecto.name

    # 2. Si solo hay un proyecto con orquestador, usarlo por defecto
    proyectos_con_orq = [
        p.name for p in PROYECTOS.iterdir()
        if (p / "orquestador.py").exists()
    ]
    if len(proyectos_con_orq) == 1:
        return proyectos_con_orq[0]

    # 3. El mas reciente (mayor mtime)
    if proyectos_con_orq:
        proyectos_con_orq.sort(
            key=lambda p: (PROYECTOS / p / "orquestador.py").stat().st_mtime,
            reverse=True
        )
        return proyectos_con_orq[0]

    return None


def listar_proyectos() -> list[dict]:
    """Lista todos los proyectos con su orquestador."""
    resultado = []
    if not PROYECTOS.exists():
        return resultado
    for p in sorted(PROYECTOS.iterdir()):
        if p.is_dir() and (p / "orquestador.py").exists():
            agentes = list((p / "agentes").glob("*.py")) if (p / "agentes").exists() else []
            resultado.append({
                "nombre": p.name,
                "agentes": len(agentes),
                "orquestador": str(p / "orquestador.py"),
            })
    return resultado


def router_tareas_proyectos(consulta: str, proyecto: str | None = None) -> str:
    """
    Enruta una tarea al proyecto correcto y devuelve el resultado.
    Si proyecto=None, lo detecta automaticamente.
    """
    if not consulta.strip():
        return "ERROR: consulta vacia"

    # Detectar proyecto si no se especifica
    if not proyecto:
        proyecto = detectar_proyecto(consulta)

    if not proyecto:
        proyectos = listar_proyectos()
        if not proyectos:
            return "ERROR: No hay proyectos con orquestador disponibles"
        lista = ", ".join(p["nombre"] for p in proyectos)
        return f"ERROR: No pude detectar el proyecto. Disponibles: {lista}"

    orq_path = PROYECTOS / proyecto / "orquestador.py"
    if not orq_path.exists():
        return f"ERROR: orquestador.py no encontrado en {proyecto}"

    try:
        result = subprocess.run(
            [sys.executable, str(orq_path), consulta],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
            cwd=str(PROYECTOS / proyecto),
        )
        output = (result.stdout or "").strip()
        if result.returncode != 0:
            err = (result.stderr or "").strip()
            return f"ERROR en {proyecto}: {err[:500]}" if err else f"ERROR en {proyecto} (codigo {result.returncode})"
        return output or f"Tarea ejecutada en {proyecto} sin output"
    except subprocess.TimeoutExpired:
        return f"TIMEOUT: {proyecto} excedio 120 segundos"
    except Exception as e:
        return f"ERROR: {e}"


if __name__ == "__main__":
    args = sys.argv[1:]

    # Modo --listar
    if args and args[0] == "--listar":
        proyectos = listar_proyectos()
        if not proyectos:
            print("No hay proyectos con orquestador")
        else:
            print(f"Proyectos disponibles ({len(proyectos)}):")
            for p in proyectos:
                print(f"  - {p['nombre']} ({p['agentes']} agentes)")
        sys.exit(0)

    # Modo --proyecto <nombre> <consulta>
    proyecto_arg = None
    if len(args) >= 2 and args[0] == "--proyecto":
        proyecto_arg = args[1]
        consulta = " ".join(args[2:])
    else:
        consulta = " ".join(args)

    if not consulta.strip():
        print("Uso: python router_tareas_proyectos.py [--proyecto <nombre>] <tarea>")
        print("     python router_tareas_proyectos.py --listar")
        sys.exit(1)

    resultado = router_tareas_proyectos(consulta, proyecto_arg)
    print(resultado)
