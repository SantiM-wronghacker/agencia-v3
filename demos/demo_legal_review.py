"""
Demo: Legal Review — Legal Analyst → Compliance Checker → Risk Assessor → Summarizer

Servicio: Revisión jurídica automatizada de contratos con análisis de riesgos.
Caso de uso: Despachos legales, empresas que firman muchos contratos, startups.
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
        "DEMO: Legal Review",
        "Legal Analyst → Compliance Checker → Risk Assessor → Summarizer",
    )

    print(f"  Modelo: {model}")
    print(f"  Servicio: Revisión jurídica de contratos con análisis de riesgos")
    print()

    task = """
CONTRATO DE PRESTACIÓN DE SERVICIOS

Entre: TechSolutions México S.A. de C.V. (EL PRESTADOR)
Y: Comercial Hernández e Hijos S.A. de C.V. (EL CLIENTE)

CLÁUSULAS PRINCIPALES:
1. El prestador desarrollará un sistema de gestión de inventario en 60 días naturales.
2. El costo total es de $180,000 MXN pagaderos: 50% al inicio, 50% a la entrega.
3. El cliente proporcionará acceso a sus sistemas actuales en los primeros 5 días.
4. Cualquier modificación al alcance tendrá un costo adicional a negociar.
5. En caso de incumplimiento del prestador, se aplicará pena convencional del 10%
   por cada semana de retraso, hasta un máximo del 30% del contrato.
6. La garantía del sistema es de 30 días naturales después de la entrega.
7. Este contrato se rige por las leyes del Estado de México.
8. Las disputas se resolverán por arbitraje en la CANACO de Toluca.

Vigencia: 90 días naturales a partir de la firma.
""".strip()

    print("  CONTRATO A REVISAR:")
    print("  " + "─" * 60)
    for line in task.splitlines():
        print(f"  {line}")
    print()
    print("  " + "═" * 60)
    print()

    agents = [
        BaseAgent("legal_analyst",      task_type="long_doc"),
        BaseAgent("compliance_checker", task_type="reasoning"),
        BaseAgent("risk_assessor",      task_type="reasoning"),
        BaseAgent("summarizer",         task_type="simple"),
    ]

    results, final_output, total = _run_live(agents, task)

    successful = sum(1 for r in results if r.success)

    print("  " + "═" * 60)
    print("  DICTAMEN LEGAL FINAL")
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
