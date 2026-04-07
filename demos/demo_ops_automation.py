"""
Demo: Ops Automation — Process Mapper → Optimizer → Implementation Planner

Servicio: Diagnóstico y optimización de procesos operativos con plan de implementación.
Caso de uso: Empresas con procesos manuales que quieren digitalizarse y escalar.
"""
import sys
import time
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _detect_model() -> str:
    from llm.ollama import OllamaLLM
    llm = OllamaLLM()
    if not llm.is_available():
        print("\n  ERROR: Ollama no está corriendo.")
        print("  Ejecuta: ollama serve && ollama pull llama3:8b")
        sys.exit(1)
    models = llm.list_models()
    if not models:
        print("\n  ERROR: No hay modelos. Ejecuta: ollama pull llama3:8b")
        sys.exit(1)
    for preferred in ["llama3:8b", "gpt-oss:20b", "mistral:7b", "phi3:mini"]:
        if preferred in models:
            return preferred
    return models[0]


def _banner(title: str, subtitle: str = "") -> None:
    width = 62
    print()
    print("  ╔" + "═" * width + "╗")
    print(f"  ║  {title:<{width - 2}}║")
    if subtitle:
        print(f"  ║  {subtitle:<{width - 2}}║")
    print("  ╚" + "═" * width + "╝")
    print()


def _run_live(agents: list, task: str) -> tuple[list, str, float]:
    current_input = task
    results = []
    total_start = time.time()

    for i, agent in enumerate(agents, 1):
        label = f"  ▶  Step {i}/{len(agents)}: {agent.role.replace('_', ' ').upper()}"
        print(label)
        print("  " + "─" * 60)
        step_start = time.time()
        result = agent.run(current_input)
        elapsed = round(time.time() - step_start, 1)

        if result.success:
            for line in result.output.splitlines():
                print(f"  {line}")
            print()
            print(f"  ✓  {elapsed}s · modelo: {result.provider}")
            current_input = result.output
        else:
            print(f"  ✗  Error: {result.error}")
            results.append(result)
            break

        results.append(result)
        print()

    total = round(time.time() - total_start, 1)
    return results, current_input, total


def main():
    model = _detect_model()

    from config.settings import settings
    settings.OLLAMA_MODEL = model

    from core.agent import BaseAgent

    _banner(
        "DEMO: Ops Automation",
        "Process Mapper → Optimizer → Implementation Planner",
    )

    print(f"  Modelo: {model}")
    print(f"  Servicio: Diagnóstico y optimización de procesos operativos")
    print()

    task = """
Proceso actual: Onboarding de nuevos clientes en una agencia de publicidad

Pasos actuales:
1. Cliente contacta por WhatsApp o email (tiempo: variable, a veces tarda días)
2. Vendedor agenda cita manualmente revisando su agenda personal en papel
3. En la reunión se toma nota a mano de los requerimientos
4. El vendedor pide cotización al área de diseño por WhatsApp
5. Diseño responde en 2-5 días con un precio en mensaje de WhatsApp
6. El vendedor escribe la cotización en Word y la manda por email
7. Si el cliente acepta, se le pide que firme contrato impreso y lo escanee
8. El contrato escaneado se guarda en una carpeta de Drive sin nombre estándar
9. Se crea el proyecto en una hoja de Excel compartida
10. Se avisa al equipo de producción por WhatsApp grupal

Problemas conocidos:
- Tiempo promedio de onboarding: 2 semanas
- 30% de los leads se pierden en el proceso
- Información se pierde entre WhatsApps
- No hay seguimiento sistemático
- El equipo no sabe el status de proyectos nuevos
""".strip()

    print("  PROCESO A OPTIMIZAR:")
    print("  " + "─" * 60)
    for line in task.splitlines():
        print(f"  {line}")
    print()
    print("  " + "═" * 60)
    print()

    agents = [
        BaseAgent("process_mapper",          task_type="general"),
        BaseAgent("optimizer",               task_type="reasoning"),
        BaseAgent("implementation_planner",  task_type="general"),
    ]

    results, final_output, total = _run_live(agents, task)

    successful = sum(1 for r in results if r.success)

    print("  " + "═" * 60)
    print("  PLAN DE IMPLEMENTACIÓN FINAL")
    print("  " + "─" * 60)
    if successful == len(agents):
        for line in final_output.splitlines():
            print(f"  {line}")
    print()
    print("  " + "─" * 60)
    print(f"  Steps completados : {successful}/{len(agents)}")
    print(f"  Tiempo total      : {total}s")
    print(f"  Modelo usado      : {model}")
    print(f"  Éxito             : {'✓ Sí' if successful == len(agents) else '✗ Parcial'}")
    print()

    return successful == len(agents)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
