#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║  DIRECTOR.PY — TeamDirector CLI Profesional                  ║
║  agencia-v3  ·  Super Agente Orquestador                     ║
╚══════════════════════════════════════════════════════════════╝

Herramienta de línea de comandos para interactuar con el
TeamDirector y sus 6 roles especializados con IA real.

USO:
  python core/director.py --rol strategy --tarea "Plan de 90 días para duplicar ingresos"
  python core/director.py --rol finance   --tarea "ROI de inversión $50k en 12 meses"
  python core/director.py --rol marketing --tarea "Campaña de lanzamiento Q2 2026"
  python core/director.py --rol tech      --tarea "Arquitectura para 100k usuarios concurrentes"
  python core/director.py --rol legal     --tarea "Revisar cumplimiento GDPR"
  python core/director.py --rol ops       --tarea "Optimizar ciclo de onboarding"
  python core/director.py --roles         (ver todos los roles disponibles)
  python core/director.py --status        (verificar LLM y servicios)
  python core/director.py --interactivo   (modo conversación)
"""

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Fuerza UTF-8 en stdout/stderr para los caracteres de caja ANSI en Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Asegura que el root del proyecto esté en el path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# ─── Roles ───────────────────────────────────────────────────────────────────

ROLES = {
    "strategy":  {"emoji": "📊", "desc": "Estrategia de negocio, planes, OKRs, ventaja competitiva", "task_type": "reasoning"},
    "finance":   {"emoji": "💰", "desc": "ROI, flujo de caja, EBITDA, proyecciones financieras",       "task_type": "reasoning"},
    "legal":     {"emoji": "⚖️",  "desc": "Contratos, GDPR, propiedad intelectual, compliance",        "task_type": "long_doc"},
    "marketing": {"emoji": "📢", "desc": "Growth hacking, campañas digitales, branding, funnels",      "task_type": "general"},
    "tech":      {"emoji": "⚙️",  "desc": "Arquitectura, cloud, APIs, escalabilidad, DevOps",          "task_type": "reasoning"},
    "ops":       {"emoji": "🔧", "desc": "Procesos, automatización, KPIs operacionales, Lean",         "task_type": "general"},
}

# ─── Colores ANSI ─────────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
BLUE   = "\033[94m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
GRAY   = "\033[90m"
WHITE  = "\033[97m"


def _c(text: str, color: str) -> str:
    """Colorea texto si la terminal lo soporta."""
    if sys.stdout.isatty() and os.name == "nt":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            return text
    return f"{color}{text}{RESET}" if sys.stdout.isatty() else text


def header():
    print()
    print(_c("  ╔══════════════════════════════════════════════════════╗", CYAN))
    print(_c("  ║  TEAMDIRECTOR — Super Agente Orquestador con IA Real  ║", CYAN))
    print(_c("  ║  agencia-v3  ·  6 Roles Especializados                ║", CYAN))
    print(_c("  ╚══════════════════════════════════════════════════════╝", CYAN))
    print()


# ─── Lazy builders ────────────────────────────────────────────────────────────

def _build_agents():
    """Construye los 6 agentes del director con sus task_types."""
    from core.agent import BaseAgent
    return {rol: BaseAgent(rol, task_type=info["task_type"]) for rol, info in ROLES.items()}


def _get_db():
    from memory.db import AgenciaDB
    return AgenciaDB()


# ─── Comandos CLI ─────────────────────────────────────────────────────────────

def mostrar_roles():
    header()
    print(_c("  Roles Especializados Disponibles:", BOLD + WHITE))
    print()
    for rol, info in ROLES.items():
        print(f"    {info['emoji']}  {_c(rol.upper(), BLUE + BOLD)}")
        print(f"       {_c(info['desc'], GRAY)}")
        print()
    print(_c("  Uso:", WHITE))
    print(f"    {_c('python core/director.py --rol strategy --tarea \"Optimiza el modelo de monetización\"', YELLOW)}")
    print()


def verificar_estado():
    header()
    print(_c("  Estado de Servicios:", BOLD + WHITE))
    print()

    # LLM activo
    try:
        from llm import get_llm
        llm = get_llm()
        print(f"    {_c('LLM activo:', WHITE)}  {_c(llm.provider_name.upper(), GREEN + BOLD)}")
    except Exception as e:
        print(f"    {_c('LLM activo:', WHITE)}  {_c('ERROR — ' + str(e)[:60], RED)}")

    # Ollama
    try:
        import httpx
        from config.settings import settings
        r = httpx.get(f"{settings.OLLAMA_HOST}/api/tags", timeout=3.0)
        if r.status_code == 200:
            modelos = [m["name"] for m in r.json().get("models", [])]
            label = f"ACTIVO — {len(modelos)} modelos: {', '.join(modelos[:3])}"
            print(f"    {_c('Ollama:', WHITE)}      {_c(label, GREEN)}")
        else:
            print(f"    {_c('Ollama:', WHITE)}      {_c('NO RESPONDE', RED + BOLD)}")
    except Exception:
        print(f"    {_c('Ollama:', WHITE)}      {_c('NO RESPONDE', RED + BOLD)}")

    # API keys configuradas
    print()
    print(_c("  Proveedores LLM:", BOLD + WHITE))
    from config.settings import settings
    providers = {
        "Groq":    settings.GROQ_API_KEY,
        "Gemini":  settings.GEMINI_API_KEY,
        "Mistral": settings.MISTRAL_API_KEY,
    }
    for name, key in providers.items():
        if key:
            preview = key[:8] + "..."
            print(f"    {_c(name + ':', WHITE):20} {_c('Configurado', GREEN)} {_c('(' + preview + ')', GRAY)}")
        else:
            print(f"    {_c(name + ':', WHITE):20} {_c('No configurado', GRAY)}")

    # DB
    print()
    print(_c("  Base de datos:", BOLD + WHITE))
    try:
        db = _get_db()
        runs = db.get_recent_runs(limit=1)
        print(f"    {_c('SQLite:', WHITE)}  {_c('OK', GREEN)}  — {_c(settings.DB_PATH, GRAY)}")
        if runs:
            print(f"    {_c('Último run:', WHITE)}  {_c(runs[0].get('created_at', '?')[:19], GRAY)}")
    except Exception as e:
        print(f"    {_c('SQLite:', WHITE)}  {_c('ERROR — ' + str(e)[:60], RED)}")
    print()


def asignar_tarea(rol: str, tarea: str, verbose: bool = False) -> None:
    info = ROLES.get(rol, {})
    emoji = info.get("emoji", "🎯")

    header()
    print(_c(f"  {emoji} Director {rol.upper()}", BOLD + BLUE))
    print(_c(f"  {'─'*52}", GRAY))
    print(f"  {_c('Tarea:', WHITE)} {tarea}")
    print(f"  {_c('Consultando IA...', YELLOW)}")
    print(_c(f"  {'─'*52}", GRAY))
    print()

    inicio = time.time()

    try:
        db = _get_db()
        from core.agent import BaseAgent
        agent = BaseAgent(rol, task_type=info["task_type"], db=db)
        result = agent.run(tarea)
    except Exception as e:
        print(_c(f"  ❌ Error: {e}", RED))
        print()
        return

    duracion = round(time.time() - inicio, 1)

    if result.success and result.output:
        print(result.output)
        print()
        if verbose:
            print(_c(f"  {'─'*52}", GRAY))
            print(_c(
                f"  Proveedor: {result.provider}  |  Tiempo: {duracion}s  |  {datetime.now().strftime('%H:%M:%S')}",
                GRAY
            ))
    else:
        error_msg = result.error or "Sin respuesta del Director."
        print(_c(f"  ❌ {error_msg}", RED))

    print()


def modo_interactivo() -> None:
    header()
    print(_c("  Modo Interactivo — TeamDirector", BOLD + WHITE))
    print(_c("  Escribe 'exit' o Ctrl+C para salir", GRAY))
    print(_c("  Escribe 'roles' para ver roles disponibles", GRAY))
    print()

    print("  Roles: " + " | ".join(f"{v['emoji']} {k}" for k, v in ROLES.items()))
    print()

    rol_input = "strategy"
    while True:
        try:
            rol_input = input(_c("  ¿Qué rol usar? [strategy]: ", CYAN)).strip().lower() or "strategy"
            if rol_input in ("exit", "quit", "salir"):
                break
            if rol_input == "roles":
                mostrar_roles()
                continue
            if rol_input not in ROLES:
                print(_c(f"  Rol '{rol_input}' no válido. Opciones: {', '.join(ROLES.keys())}", RED))
                continue
            break
        except (KeyboardInterrupt, EOFError):
            print()
            break

    print()
    while True:
        try:
            tarea = input(_c(f"  [{rol_input.upper()}] Tarea: ", BLUE)).strip()
            if not tarea or tarea.lower() in ("exit", "quit", "salir"):
                break
            print()
            asignar_tarea(rol_input, tarea, verbose=True)

            cambiar = input(_c("  ¿Cambiar de rol? (Enter para continuar, o escribe otro rol): ", GRAY)).strip().lower()
            if cambiar and cambiar in ROLES:
                rol_input = cambiar
            elif cambiar in ("exit", "quit", "salir"):
                break
        except (KeyboardInterrupt, EOFError):
            print()
            break

    print(_c("\n  Director desconectado. ¡Hasta pronto!\n", GRAY))


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="TeamDirector CLI — Super Agente Orquestador con IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--rol", "--role",
        choices=list(ROLES.keys()),
        help="Rol especializado: strategy, finance, legal, marketing, tech, ops",
    )
    parser.add_argument("--tarea", "--task", help="Tarea o pregunta para el Director")
    parser.add_argument("--roles", action="store_true", help="Mostrar todos los roles disponibles")
    parser.add_argument("--status", action="store_true", help="Verificar estado de LLM y servicios")
    parser.add_argument("--interactivo", "-i", action="store_true", help="Modo conversación interactiva")
    parser.add_argument("--verbose", "-v", action="store_true", help="Mostrar proveedor y tiempo")

    args = parser.parse_args()

    if args.roles:
        mostrar_roles()
    elif args.status:
        verificar_estado()
    elif args.interactivo:
        modo_interactivo()
    elif args.rol and args.tarea:
        asignar_tarea(args.rol, args.tarea, verbose=args.verbose)
    else:
        header()
        print(_c("  Uso rápido:", BOLD + WHITE))
        print()
        print(f"    {_c('python core/director.py --rol strategy --tarea \"Optimiza el modelo de monetización\"', YELLOW)}")
        print(f"    {_c('python core/director.py --rol finance   --tarea \"ROI de inversión $50k en 12 meses\"', YELLOW)}")
        print(f"    {_c('python core/director.py --roles', CYAN)}          Ver todos los roles")
        print(f"    {_c('python core/director.py --status', CYAN)}         Estado de servicios")
        print(f"    {_c('python core/director.py --interactivo', CYAN)}    Modo conversación")
        print(f"    {_c('python core/director.py --help', CYAN)}           Ayuda completa")
        print()
        print(_c("  Roles disponibles:", WHITE))
        for rol, info in ROLES.items():
            print(f"    {info['emoji']}  {_c(rol, BLUE)}  —  {_c(info['desc'][:55], GRAY)}")
        print()


if __name__ == "__main__":
    main()
