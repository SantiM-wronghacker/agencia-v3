"""
Demo: Business Analysis — Data Analyst → Strategy Director → Finance Director → Reporter

Servicio: Análisis de negocio completo con recomendaciones estratégicas y financieras.
Caso de uso: Empresas que necesitan diagnóstico y plan de acción rápido.
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
        "DEMO: Business Analysis",
        "Data Analyst → Strategy Director → Finance Director → Reporter",
    )

    print(f"  Modelo: {model}")
    print(f"  Servicio: Análisis empresarial con estrategia y proyecciones")
    print()

    task = """
Empresa: Distribuidora El Sol S.A. de C.V.
Giro: Distribución de abarrotes en CDMX y zona metropolitana
Empleados: 45
Ventas mensuales promedio: $2,800,000 MXN
Situación actual:
- Ventas bajaron 18% en los últimos 3 meses
- Competencia de nuevos distribuidores con precios más bajos
- 3 clientes grandes (30% de las ventas) amenazando con cambiar de proveedor
- Inventario con 15% de productos de baja rotación
- Equipo de ventas desmotivado (2 vendedores renunciaron este mes)

Pregunta: ¿Qué debemos hacer para recuperar las ventas y estabilizar el negocio?
""".strip()

    print("  CASO DE NEGOCIO:")
    print("  " + "─" * 60)
    for line in task.splitlines():
        print(f"  {line}")
    print()
    print("  " + "═" * 60)
    print()

    agents = [
        BaseAgent("data_analyst",       task_type="reasoning"),
        BaseAgent("strategy_director",  task_type="reasoning"),
        BaseAgent("finance_director",   task_type="reasoning"),
        BaseAgent("reporter",           task_type="simple"),
    ]

    results, final_output, total = _run_live(agents, task)

    successful = sum(1 for r in results if r.success)

    print("  " + "═" * 60)
    print("  REPORTE EJECUTIVO FINAL")
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
