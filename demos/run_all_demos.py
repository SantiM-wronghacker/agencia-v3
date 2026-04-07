"""
Script maestro para ejecutar los demos de Agencia v3.

Uso:
  python demos/run_all_demos.py              — todos los demos en secuencia
  python demos/run_all_demos.py content      — Content Pipeline
  python demos/run_all_demos.py business     — Business Analysis
  python demos/run_all_demos.py legal        — Legal Review
  python demos/run_all_demos.py ops          — Ops Automation
"""
import sys
import time
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_DEMOS = {
    "content": {
        "module": "demos.demo_content_pipeline",
        "name":   "Content Pipeline",
        "desc":   "Researcher → Writer → SEO Optimizer → Reviewer",
    },
    "business": {
        "module": "demos.demo_business_analysis",
        "name":   "Business Analysis",
        "desc":   "Data Analyst → Strategy Director → Finance Director → Reporter",
    },
    "legal": {
        "module": "demos.demo_legal_review",
        "name":   "Legal Review",
        "desc":   "Legal Analyst → Compliance Checker → Risk Assessor → Summarizer",
    },
    "ops": {
        "module": "demos.demo_ops_automation",
        "name":   "Ops Automation",
        "desc":   "Process Mapper → Optimizer → Implementation Planner",
    },
}


def _run_demo(key: str) -> tuple[bool, float]:
    """Import and run a demo's main(). Returns (success, elapsed_seconds)."""
    import importlib
    meta = _DEMOS[key]
    print(f"\n  Iniciando: {meta['name']}")
    print(f"  Pipeline:  {meta['desc']}")
    print()
    start = time.time()
    try:
        mod = importlib.import_module(meta["module"])
        # Reload to avoid stale state between runs
        importlib.reload(mod)
        success = mod.main()
    except SystemExit as e:
        success = (e.code == 0)
    except Exception as e:
        print(f"\n  ERROR inesperado: {e}")
        success = False
    elapsed = round(time.time() - start, 1)
    return success, elapsed


def _print_summary(results: dict) -> None:
    width = 62
    print()
    print("  " + "═" * width)
    print(f"  {'RESUMEN FINAL':^{width}}")
    print("  " + "═" * width)
    print(f"  {'Demo':<22} {'Estado':<12} {'Tiempo':>8}")
    print("  " + "─" * width)
    all_ok = True
    for key, (success, elapsed) in results.items():
        meta = _DEMOS[key]
        status = "✓ OK" if success else "✗ ERROR"
        if not success:
            all_ok = False
        print(f"  {meta['name']:<22} {status:<12} {elapsed:>6.1f}s")
    print("  " + "─" * width)
    total_time = sum(e for _, e in results.values())
    print(f"  {'TOTAL':<22} {'':12} {total_time:>6.1f}s")
    print("  " + "═" * width)
    print()
    if all_ok:
        print("  ✓ Todos los demos completados exitosamente.")
    else:
        print("  ✗ Algunos demos fallaron. Revisa la salida arriba.")
    print()


def main():
    args = sys.argv[1:]

    # Determine which demos to run
    if not args:
        keys = list(_DEMOS.keys())
    else:
        key = args[0].lower()
        if key not in _DEMOS:
            print(f"\n  Demo '{key}' no reconocido.")
            print(f"  Opciones: {', '.join(_DEMOS.keys())}")
            sys.exit(1)
        keys = [key]

    # Run each demo
    results = {}
    for key in keys:
        success, elapsed = _run_demo(key)
        results[key] = (success, elapsed)
        if len(keys) > 1:
            # Small pause between demos to avoid terminal flooding
            time.sleep(1)

    # Print summary only when running multiple
    if len(keys) > 1:
        _print_summary(results)

    all_ok = all(s for s, _ in results.values())
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
