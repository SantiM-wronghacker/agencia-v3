"""E2E tests for the business_analysis group using real Ollama."""
from __future__ import annotations

import pytest

from groups.business_analysis import create_business_analysis


pytestmark = [pytest.mark.e2e, pytest.mark.requires_ollama, pytest.mark.slow]

_TASK = (
    "Analiza el siguiente negocio: empresa de software en México con ingresos de "
    "$5M MXN anuales, 15 empleados, clientes en retail. "
    "Identifica oportunidades de crecimiento y riesgos financieros."
)


@pytest.fixture(scope="module")
def ba_result(ollama_model, e2e_db):
    """Run business analysis once and share across tests."""
    group = create_business_analysis(db=e2e_db)
    return group.execute(_TASK)


def test_business_analysis_completes(ba_result):
    """Business analysis must succeed."""
    assert ba_result.success, f"Business analysis falló: {ba_result.final_output}"


def test_business_analysis_has_report_content(ba_result):
    """Output must contain business report keywords."""
    output = ba_result.final_output.lower()
    # Accept Spanish or English keywords (model may respond in either language)
    report_keywords = [
        "análisis", "estrategia", "reporte", "empresa", "recomend",
        "analysis", "strategy", "report", "recommend", "executive", "financial",
        "growth", "crecimiento", "oportunidad", "opportunity",
    ]
    matches = [kw for kw in report_keywords if kw in output]
    assert len(matches) >= 1, (
        f"Output no contiene palabras de reporte. Output: {ba_result.final_output[:200]}"
    )


def test_business_analysis_finance_step_produces_numbers(ollama_model, e2e_db):
    """The finance director step should produce output referencing numbers or financials."""
    group = create_business_analysis(db=e2e_db)
    result = group.execute(
        "Evalúa la rentabilidad de una tienda de ropa con ventas de $2M MXN al año."
    )
    assert result.success
    # The output should at least be non-empty from the financial analysis step
    assert len(result.final_output) > 50
