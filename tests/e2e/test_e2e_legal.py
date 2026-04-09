"""E2E tests for the legal_review group using real Ollama."""
from __future__ import annotations

import pytest

from groups.legal_review import create_legal_review


pytestmark = [pytest.mark.e2e, pytest.mark.requires_ollama, pytest.mark.slow]

_CONTRACT = (
    "CONTRATO DE PRESTACIÓN DE SERVICIOS\n"
    "Entre TechCorp SA de CV (proveedor) y MiEmpresa SA de CV (cliente).\n"
    "OBJETO: Desarrollo de sistema de inventarios.\n"
    "VIGENCIA: 12 meses a partir de la firma.\n"
    "MONTO: $150,000 MXN más IVA.\n"
    "PENALIDADES: 5% mensual por incumplimiento.\n"
    "CONFIDENCIALIDAD: Ambas partes, indefinida.\n"
    "JURISDICCIÓN: Ciudad de México.\n"
    "Revisa este contrato, identifica riesgos y proporciona un resumen ejecutivo."
)


@pytest.fixture(scope="module")
def legal_result(ollama_model, e2e_db):
    """Run legal review once and share across tests."""
    group = create_legal_review(db=e2e_db)
    return group.execute(_CONTRACT)


def test_legal_review_completes(legal_result):
    """Legal review must succeed."""
    assert legal_result.success, f"Legal review falló: {legal_result.final_output}"


def test_legal_review_identifies_risks(legal_result):
    """Output should mention risk-related terms."""
    output = legal_result.final_output.lower()
    # Accept Spanish or English keywords (model may respond in either language)
    risk_keywords = [
        "riesgo", "riesg", "penalidad", "obligaci", "clausula", "cláusula", "incumplimiento",
        "risk", "penalty", "breach", "obligation", "clause", "liability", "compliance",
    ]
    matches = [kw for kw in risk_keywords if kw in output]
    assert len(matches) >= 1, (
        f"Output no menciona riesgos contractuales. Output: {legal_result.final_output[:300]}"
    )


def test_legal_review_summarizer_produces_output(ollama_model, e2e_db):
    """Summarizer (last step) must produce a non-trivial output."""
    group = create_legal_review(db=e2e_db)
    result = group.execute(
        "Analiza este acuerdo de confidencialidad: duración 2 años, aplica a código fuente "
        "y datos de clientes, penalidad de $50,000 USD por violación."
    )
    assert result.success
    assert len(result.final_output) > 50, (
        f"Summarizer produjo output muy corto: '{result.final_output}'"
    )
