"""E2E tests for the ops_automation group using real Ollama."""
from __future__ import annotations

import pytest

from groups.ops_automation import create_ops_automation


pytestmark = [pytest.mark.e2e, pytest.mark.requires_ollama, pytest.mark.slow]

_PROCESS = (
    "Proceso actual de ventas: el cliente llama, el vendedor anota en papel, "
    "luego transcribe a Excel, envía cotización por correo, espera aprobación 3-5 días, "
    "genera factura manualmente. Hay errores frecuentes y demoras. "
    "Propón un plan de automatización y mejoras operativas."
)


@pytest.fixture(scope="module")
def ops_result(ollama_model, e2e_db):
    """Run ops automation once and share across tests."""
    group = create_ops_automation(db=e2e_db)
    return group.execute(_PROCESS)


def test_ops_automation_completes(ops_result):
    """Ops automation must complete successfully."""
    assert ops_result.success, f"Ops automation falló: {ops_result.final_output}"


def test_ops_automation_produces_action_plan(ops_result):
    """Output should reference automation or improvement actions."""
    output = ops_result.final_output.lower()
    # Accept Spanish or English keywords (model may respond in either language)
    action_keywords = [
        "automatiz", "proceso", "mejora", "implementa", "plan",
        "optimiz", "paso", "sistema", "herramienta",
        "automat", "process", "improve", "implement", "step",
        "system", "tool", "workflow", "solution",
    ]
    matches = [kw for kw in action_keywords if kw in output]
    assert len(matches) >= 2, (
        f"Output no contiene plan de acción suficiente. "
        f"Matches: {matches}. Output: {ops_result.output[:300]}"
    )
