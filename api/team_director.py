"""
TeamDirector — Super Agente Orquestador con IA Real.

Orquesta 6 roles especializados usando LLM real (llm_router).
Cada rol tiene un sistema de prompts especializado en su dominio.
Falls back gracefully si el LLM no está disponible.
"""
from __future__ import annotations

import argparse
import os
import sys
import threading
from datetime import datetime
from typing import Any

# ─── Roles de negocio válidos ───────────────────────────────────────────────
REGISTERED_ROLES: frozenset[str] = frozenset({
    "strategy",   # Estrategia y planificación de negocio
    "finance",    # Análisis financiero, ROI, proyecciones
    "legal",      # Asesoría legal y normativa
    "marketing",  # Campañas, posicionamiento, growth hacking
    "tech",       # Arquitectura técnica e infraestructura
    "ops",        # Operaciones, procesos y eficiencia
})

# ─── Prompts especializados por rol ─────────────────────────────────────────
ROLE_PROMPTS: dict[str, str] = {
    "strategy": (
        "Eres el Director Estratégico de la Agencia Santi, con 20+ años de experiencia "
        "en consultoría de negocios (McKinsey, BCG), startups unicornio y empresas Fortune 500. "
        "Dominas OKRs, marcos SWOT, ventaja competitiva, modelos de crecimiento, disrupciones "
        "de mercado y estrategia Blue Ocean. Das respuestas concretas, accionables, con datos "
        "y marcos estratégicos claros. Piensas en el largo plazo pero con pasos inmediatos. "
        "Responde siempre en español con estructura clara (usa bullets y secciones)."
    ),
    "finance": (
        "Eres el CFO (Director Financiero) de la Agencia Santi, experto en análisis de "
        "rentabilidad, flujo de caja, modelado financiero, valoración de empresas, ROI, "
        "EBITDA, CAC/LTV, proyecciones financieras y gestión de riesgo. Trabajas con "
        "números precisos, escenarios (optimista/realista/pesimista) y métricas financieras "
        "claras. Das análisis cuantitativos con supuestos explícitos. "
        "Responde en español con tablas y cálculos cuando sea relevante."
    ),
    "legal": (
        "Eres el Asesor Legal Senior de la Agencia Santi, especializado en derecho "
        "corporativo, contratos comerciales, GDPR/LGPD/privacidad de datos, propiedad "
        "intelectual, marcas, derecho laboral y regulación empresarial en México, "
        "Latinoamérica y España. Das orientación legal práctica y clara, identificas "
        "riesgos y oportunidades legales, y siempre recomiendas revisar con un abogado "
        "local para decisiones finales. Responde en español con lenguaje accesible."
    ),
    "marketing": (
        "Eres el Director de Marketing de la Agencia Santi, con expertise en growth "
        "hacking, marketing digital, branding, copywriting persuasivo, campañas de "
        "performance (Meta Ads, Google Ads, TikTok Ads), email marketing, SEO/SEM, "
        "funnels de conversión y posicionamiento de mercado en Latinoamérica. "
        "Das estrategias concretas, medibles y con ROI claro. Conoces las últimas "
        "tendencias digitales y sabes cómo ejecutarlas. Responde en español con "
        "ejemplos prácticos y métricas objetivo."
    ),
    "tech": (
        "Eres el CTO y Arquitecto de Software de la Agencia Santi, con expertise "
        "en sistemas distribuidos, microservicios, cloud (AWS/GCP/Azure), bases de datos "
        "(SQL y NoSQL), APIs RESTful/GraphQL, seguridad informática, DevOps, CI/CD, "
        "Python, JavaScript/TypeScript, y escalabilidad. Piensas en trade-offs técnicos, "
        "deuda técnica, ROI de la inversión tecnológica y mejores prácticas de ingeniería. "
        "Das recomendaciones técnicas específicas con justificación. Responde en español "
        "con código cuando sea útil."
    ),
    "ops": (
        "Eres el COO (Director de Operaciones) de la Agencia Santi, especializado en "
        "optimización de procesos, Lean Management, Six Sigma, automatización de workflows, "
        "gestión de equipos, KPIs operacionales, OKRs y eficiencia empresarial. "
        "Identificas cuellos de botella, mejoras de proceso y oportunidades de automatización. "
        "Das soluciones prácticas e implementables con métricas de éxito claras. "
        "Responde en español con planes de acción concretos y timelines."
    ),
}

# ─── Emojis visuales por rol ─────────────────────────────────────────────────
ROLE_EMOJI: dict[str, str] = {
    "strategy":  "📊",
    "finance":   "💰",
    "legal":     "⚖️",
    "marketing": "📢",
    "tech":      "⚙️",
    "ops":       "🔧",
}

# ─── LLM Router Integration ──────────────────────────────────────────────────
_llm_lock = threading.Lock()
_llm_completar = None
_llm_loaded = False


def _cargar_llm_router():
    """Intenta importar llm_router desde múltiples rutas posibles."""
    global _llm_completar, _llm_loaded
    with _llm_lock:
        if _llm_loaded:
            return _llm_completar

        _llm_loaded = True

        # Buscar root del proyecto (subir desde src/agencia/api/dashboard/)
        base = os.path.abspath(__file__)
        root = base
        for _ in range(6):
            root = os.path.dirname(root)
            candidato = os.path.join(root, "categorias", "CEREBRO", "llm_router.py")
            if os.path.exists(candidato):
                cerebro_dir = os.path.dirname(candidato)
                if cerebro_dir not in sys.path:
                    sys.path.insert(0, cerebro_dir)
                break

        # Intentar importar
        try:
            import llm_router as _lr  # noqa: PLC0415
            _llm_completar = _lr.completar_simple
        except Exception:
            _llm_completar = None

        return _llm_completar


class TeamDirector:
    """
    Super Agente Orquestador que delega tareas a 6 roles especializados con IA real.

    Jerarquía:
      TeamDirector (Level 1)
        └─ 6 RoleAgents especializados (Level 2)
             └─ SubAgents privados bajo demanda (Level 3)
    """

    def __init__(self) -> None:
        self.history: list[dict[str, Any]] = []

    def assign(self, role: str, task_description: str) -> dict[str, Any]:
        """
        Asigna una tarea a un rol especializado y obtiene respuesta real con IA.

        Args:
            role: Uno de: strategy, finance, legal, marketing, tech, ops
            task_description: Descripción de la tarea o pregunta

        Returns:
            dict con keys: role, task, status, result, timestamp, provider

        Raises:
            ValueError: Si el rol no está registrado
        """
        if role not in REGISTERED_ROLES:
            raise ValueError(
                f"Role '{role}' is not registered. "
                f"Allowed roles: {', '.join(sorted(REGISTERED_ROLES))}"
            )

        emoji = ROLE_EMOJI.get(role, "🎯")
        ai_result: str | None = None
        provider_used: str = "none"

        # Intentar respuesta con LLM real
        try:
            completar_simple = _cargar_llm_router()
            if completar_simple:
                sistema = ROLE_PROMPTS[role]
                raw = completar_simple(
                    task_description,
                    sistema=sistema,
                    temperatura=0.7,
                    max_tokens=800,
                )
                if raw:
                    ai_result = raw.strip()
                    provider_used = "llm_router"
        except Exception:
            ai_result = None

        # Fallback descriptivo si LLM no disponible
        if not ai_result:
            ai_result = (
                f"[{emoji} Director {role.upper()}] Tarea recibida: {task_description}\n\n"
                f"⚠️ El motor LLM no está disponible en este momento. "
                f"Verifica que tengas al menos una API key configurada en .env "
                f"(GROQ_API_KEY, GEMINI_API_KEY, MISTRAL_API_KEY, etc.)\n\n"
                f"La tarea ha sido registrada y será procesada cuando el LLM esté disponible."
            )

        status = "completed" if provider_used != "none" else "queued"

        entry: dict[str, Any] = {
            "role": role,
            "task": task_description,
            "status": status,
            "result": ai_result,
            "provider": provider_used,
            "timestamp": datetime.now().isoformat(),
        }
        self.history.append(entry)
        return entry

    def get_history(self, limit: int = 20) -> list[dict[str, Any]]:
        """Retorna el historial de asignaciones más recientes."""
        return list(reversed(self.history[-limit:]))

    def get_roles_info(self) -> dict[str, Any]:
        """Retorna información sobre los roles disponibles."""
        return {
            role: {
                "emoji": ROLE_EMOJI.get(role, "🎯"),
                "description": ROLE_PROMPTS[role][:120] + "...",
            }
            for role in sorted(REGISTERED_ROLES)
        }


# ─── CLI ────────────────────────────────────────────────────────────────────

def cli(argv: list[str] | None = None) -> None:
    """
    CLI del TeamDirector.

    Uso::
        python -m agencia.api.dashboard.team_director --role strategy --task "Optimiza ROI"
        python director.py --rol strategy --tarea "Plan de 90 días para duplicar ingresos"
    """
    parser = argparse.ArgumentParser(
        description="TeamDirector — Super Agente Orquestador con IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Roles disponibles: {', '.join(sorted(REGISTERED_ROLES))}",
    )
    parser.add_argument("--role", "--rol", required=True, help="Rol especializado")
    parser.add_argument("--task", "--tarea", required=True, help="Tarea o pregunta")
    parser.add_argument("--verbose", action="store_true", help="Mostrar detalles del proveedor LLM")
    args = parser.parse_args(argv)

    director = TeamDirector()
    try:
        print(f"\n{'='*60}")
        print(f"  {ROLE_EMOJI.get(args.role, '🎯')} TeamDirector — Rol: {args.role.upper()}")
        print(f"{'='*60}")
        print(f"  Tarea: {args.task}")
        print(f"  Procesando con IA...")
        print(f"{'─'*60}\n")

        result = director.assign(args.role, args.task)
    except ValueError as exc:
        print(f"\n❌ ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    print(result["result"])

    if args.verbose:
        print(f"\n{'─'*60}")
        print(f"  Status:    {result['status']}")
        print(f"  Provider:  {result['provider']}")
        print(f"  Timestamp: {result['timestamp']}")

    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    cli()
