#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║  DIRECTOR.PY — TeamDirector CLI Profesional                  ║
║  Agencia Santi v2 · Super Agente Orquestador                 ║
╚══════════════════════════════════════════════════════════════╝

Herramienta de línea de comandos para interactuar con el
TeamDirector y sus 6 roles especializados con IA real.

USO:
  python director.py --rol strategy --tarea "Plan de 90 días para duplicar ingresos"
  python director.py --rol finance   --tarea "ROI de inversión $50k en 12 meses"
  python director.py --rol marketing --tarea "Campaña de lanzamiento Q2 2026"
  python director.py --rol tech      --tarea "Arquitectura para 100k usuarios concurrentes"
  python director.py --rol legal     --tarea "Revisar cumplimiento GDPR"
  python director.py --rol ops       --tarea "Optimizar ciclo de onboarding"
  python director.py --roles         (ver todos los roles disponibles)
  python director.py --status        (verificar API y servicios)
  python director.py --interactivo   (modo conversación)

ALTERNATIVA via API (si el sistema está corriendo):
  curl -X POST http://localhost:8000/director/asignar \\
    -H "Authorization: Bearer santi-agencia-2026" \\
    -H "Content-Type: application/json" \\
    -d '{"rol": "strategy", "tarea": "Plan de crecimiento"}'
"""

import os
import sys
import json
import argparse
import time
from datetime import datetime

# ─── Configuración ──────────────────────────────────────────────────────────
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
API_URL  = "http://localhost:8000"
API_KEY  = "santi-agencia-2026"

ROLES = {
    "strategy":  {"emoji": "📊", "desc": "Estrategia de negocio, planes, OKRs, ventaja competitiva"},
    "finance":   {"emoji": "💰", "desc": "ROI, flujo de caja, EBITDA, proyecciones financieras"},
    "legal":     {"emoji": "⚖️",  "desc": "Contratos, GDPR, propiedad intelectual, compliance"},
    "marketing": {"emoji": "📢", "desc": "Growth hacking, campañas digitales, branding, funnels"},
    "tech":      {"emoji": "⚙️",  "desc": "Arquitectura, cloud, APIs, escalabilidad, DevOps"},
    "ops":       {"emoji": "🔧", "desc": "Procesos, automatización, KPIs operacionales, Lean"},
}

# ─── Colores ANSI ────────────────────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
BLUE    = "\033[94m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
CYAN    = "\033[96m"
GRAY    = "\033[90m"
WHITE   = "\033[97m"


def _c(text, color):
    """Colorear texto (detecta si terminal soporta colores)."""
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
    print(_c("  ║  Agencia Santi v2  ·  6 Roles Especializados          ║", CYAN))
    print(_c("  ╚══════════════════════════════════════════════════════╝", CYAN))
    print()


def mostrar_roles():
    """Muestra todos los roles disponibles."""
    header()
    print(_c("  Roles Especializados Disponibles:", BOLD + WHITE))
    print()
    for rol, info in ROLES.items():
        emoji = info["emoji"]
        desc  = info["desc"]
        print(f"    {emoji}  {_c(rol.upper(), BLUE + BOLD)}")
        print(f"       {_c(desc, GRAY)}")
        print()
    print(_c("  Uso:", WHITE))
    print(f"    {_c('python director.py --rol strategy --tarea \"Optimiza el modelo de monetización\"', YELLOW)}")
    print()


def verificar_estado():
    """Verifica el estado de la API y servicios."""
    header()
    print(_c("  Estado de Servicios:", BOLD + WHITE))
    print()

    try:
        import urllib.request
        req = urllib.request.Request(
            f"{API_URL}/status",
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            total = data.get("agentes", {}).get("total", "?")
            saludables = data.get("agentes", {}).get("saludables", "?")
            print(f"    {_c('API (puerto 8000):', WHITE)}  {_c('ACTIVA', GREEN + BOLD)}")
            print(f"    {_c('Agentes:', WHITE)}  {_c(str(total), CYAN)} registrados, {_c(str(saludables), GREEN)} saludables")
    except Exception as e:
        print(f"    {_c('API (puerto 8000):', WHITE)}  {_c('NO RESPONDE', RED + BOLD)}")
        print(f"    {_c(str(e)[:60], GRAY)}")

    try:
        import urllib.request
        with urllib.request.urlopen(f"http://localhost:8080/", timeout=5) as resp:
            if resp.status == 200:
                print(f"    {_c('Dashboard (8080):', WHITE)}  {_c('ACTIVO', GREEN + BOLD)}")
    except Exception:
        print(f"    {_c('Dashboard (8080):', WHITE)}  {_c('NO RESPONDE', RED + BOLD)}")

    # Verificar LLM providers
    print()
    print(_c("  Proveedores LLM (.env):", BOLD + WHITE))
    env_path = os.path.join(ROOT_DIR, ".env")
    if os.path.exists(env_path):
        keys_found = []
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "API_KEY" in line and "=" in line and not line.startswith("#"):
                    key_name, _, key_val = line.partition("=")
                    key_name = key_name.strip()
                    key_val = key_val.strip().strip('"').strip("'")
                    if key_val and key_val not in ("", "tu_key_aqui"):
                        provider = key_name.replace("_API_KEY", "").title()
                        keys_found.append(provider)
                        preview = key_val[:8] + "..." if len(key_val) > 8 else key_val
                        print(f"    {_c(provider + ':', WHITE):20} {_c('Configurado', GREEN)} {_c('(' + preview + ')', GRAY)}")
        if not keys_found:
            print(f"    {_c('⚠️ Sin API keys configuradas', YELLOW)}")
    else:
        print(f"    {_c('⚠️ .env no encontrado', YELLOW)}")
    print()


def llamar_api(rol: str, tarea: str) -> dict:
    """Llama a la API REST del sistema si está activa."""
    import urllib.request
    import urllib.error

    payload = json.dumps({"rol": rol, "tarea": tarea}).encode("utf-8")
    req = urllib.request.Request(
        f"{API_URL}/director/asignar",
        data=payload,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        raise RuntimeError(f"API error: {e}")


def llamar_directo(rol: str, tarea: str) -> dict:
    """Llama al TeamDirector directamente (sin API REST)."""
    # Añadir el root al path
    if ROOT_DIR not in sys.path:
        sys.path.insert(0, ROOT_DIR)

    # Importar team_director
    try:
        team_dir_path = os.path.join(ROOT_DIR, "src", "agencia", "api", "dashboard")
        if team_dir_path not in sys.path:
            sys.path.insert(0, team_dir_path)
        sys.path.insert(0, os.path.join(ROOT_DIR, "src"))

        from agencia.api.dashboard.team_director import TeamDirector  # type: ignore
        director = TeamDirector()
        return director.assign(rol, tarea)
    except ImportError:
        # Fallback: importar directamente
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "team_director",
            os.path.join(ROOT_DIR, "src", "agencia", "api", "dashboard", "team_director.py")
        )
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)  # type: ignore
            director = mod.TeamDirector()
            return director.assign(rol, tarea)
        raise


def asignar_tarea(rol: str, tarea: str, verbose: bool = False) -> None:
    """Asigna una tarea a un rol Director y muestra la respuesta."""
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

    # Intentar via API REST primero
    resultado = None
    metodo = "none"
    try:
        data = llamar_api(rol, tarea)
        resultado = data.get("resultado", "")
        metodo = f"API ({data.get('proveedor', '?')})"
    except Exception:
        # Fallback: llamar directamente
        try:
            data = llamar_directo(rol, tarea)
            resultado = data.get("result", "")
            metodo = f"Directo ({data.get('provider', '?')})"
        except Exception as e:
            print(_c(f"  ❌ Error: {e}", RED))
            print()
            return

    duracion = round(time.time() - inicio, 1)

    if resultado:
        print(resultado)
        print()
        if verbose:
            print(_c(f"  {'─'*52}", GRAY))
            print(_c(f"  Método: {metodo}  |  Tiempo: {duracion}s  |  {datetime.now().strftime('%H:%M:%S')}", GRAY))
    else:
        print(_c("  Sin respuesta del Director.", YELLOW))

    print()


def modo_interactivo() -> None:
    """Modo conversación interactiva con el Director."""
    header()
    print(_c("  Modo Interactivo — TeamDirector", BOLD + WHITE))
    print(_c("  Escribe 'exit' o Ctrl+C para salir", GRAY))
    print(_c("  Escribe 'roles' para ver roles disponibles", GRAY))
    print()

    # Seleccionar rol
    print("  Roles: " + " | ".join(f"{v['emoji']} {k}" for k, v in ROLES.items()))
    print()

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


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="TeamDirector CLI — Super Agente Orquestador con IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--rol", "--role",
        choices=list(ROLES.keys()),
        help="Rol especializado: strategy, finance, legal, marketing, tech, ops"
    )
    parser.add_argument(
        "--tarea", "--task",
        help="Tarea o pregunta para el Director"
    )
    parser.add_argument(
        "--roles",
        action="store_true",
        help="Mostrar todos los roles disponibles"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Verificar estado de API y servicios"
    )
    parser.add_argument(
        "--interactivo", "-i",
        action="store_true",
        help="Modo conversación interactiva"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mostrar detalles adicionales (método, tiempo, proveedor)"
    )

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
        # Sin args: mostrar ayuda interactiva
        header()
        print(_c("  Uso rápido:", BOLD + WHITE))
        print()
        print(f"    {_c('python director.py --rol strategy --tarea \"Optimiza el modelo de monetización\"', YELLOW)}")
        print(f"    {_c('python director.py --rol finance   --tarea \"ROI de inversión $50k en 12 meses\"', YELLOW)}")
        print(f"    {_c('python director.py --roles', CYAN)}          Ver todos los roles")
        print(f"    {_c('python director.py --status', CYAN)}         Estado de servicios")
        print(f"    {_c('python director.py --interactivo', CYAN)}    Modo conversación")
        print(f"    {_c('python director.py --help', CYAN)}           Ayuda completa")
        print()
        print(_c("  Roles disponibles:", WHITE))
        for rol, info in ROLES.items():
            print(f"    {info['emoji']}  {_c(rol, BLUE)}  —  {_c(info['desc'][:55], GRAY)}")
        print()


if __name__ == "__main__":
    main()
