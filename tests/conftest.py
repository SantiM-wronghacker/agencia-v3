"""Global fixtures for the agencia-v3 test suite.

Fixtures defined here are available to all tests/ subdirectories.
Local fixtures in individual test files take precedence if they share the
same name (pytest resolves by closest scope).

No db / fake_llm / fake_tool fixture exists in any existing test file
(they use module-level helpers, not @pytest.fixture), so there are no
name conflicts.
"""
import pytest

from memory.db import AgenciaDB
from tools.base import BaseTool, ToolResult


# ---------------------------------------------------------------------------
# Shared test doubles
# ---------------------------------------------------------------------------

class FakeLLM:
    """In-memory LLM that returns canned responses by role keyword."""

    provider_name = "fake"

    def __init__(self, responses: dict = None, default: str = "respuesta de prueba"):
        self.responses = responses or {}
        self.default = default
        self.calls: list[dict] = []

    def generate(self, system_prompt: str, user_message: str) -> str:
        self.calls.append({"system": system_prompt, "user": user_message})
        for key, response in self.responses.items():
            if key.lower() in system_prompt.lower():
                return response
        return self.default

    def is_available(self) -> bool:
        return True


class FakeTool(BaseTool):
    """BaseTool subclass for tests."""

    name = "fake_tool"
    description = "Herramienta de prueba"

    def __init__(self, response: str = "resultado de tool", should_fail: bool = False):
        super().__init__({})
        self.response = response
        self.should_fail = should_fail
        self.call_count = 0

    def run(self, **kwargs) -> ToolResult:
        self.call_count += 1
        if self.should_fail:
            return self._error("Tool falló intencionalmente")
        return self._success(self.response, raw_data={"kwargs": kwargs})


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def db():
    """AgenciaDB in-memory, isolated per test."""
    return AgenciaDB(":memory:")


@pytest.fixture(scope="session")
def db_session():
    """AgenciaDB in-memory, shared across the whole session."""
    return AgenciaDB(":memory:")


@pytest.fixture
def fake_llm():
    """Basic FakeLLM with default response."""
    return FakeLLM()


@pytest.fixture
def fake_llm_pipeline():
    """FakeLLM with role-keyed responses covering all standard pipeline agents."""
    responses = {
        # content_pipeline
        "researcher":    "Investigación completa: hallazgos clave sobre el tema solicitado.",
        "writer":        "Artículo redactado: contenido profesional y bien estructurado.",
        "seo_optimizer": "SEO optimizado: palabras clave, meta descripción y estructura lista.",
        "reviewer":      "Revisión aprobada: contenido claro, correcto y listo para publicar.",
        # business_analysis
        "data_analyst":  "Análisis de datos completado: tendencias y patrones identificados.",
        "strategy":      "Estrategia definida: plan de acción con OKRs y KPIs.",
        "finance":       "Análisis financiero: ROI proyectado y flujo de caja estimado.",
        "reporter":      "Reporte ejecutivo: resumen con métricas y recomendaciones.",
        # legal_review
        "legal_analyst": "Análisis legal: cláusulas revisadas, sin irregularidades mayores.",
        "compliance":    "Cumplimiento verificado: normativas aplicables revisadas.",
        "risk":          "Evaluación de riesgo: riesgos identificados y mitigados.",
        "summarizer":    "Resumen legal: puntos clave documentados para el cliente.",
        # ops_automation
        "process":    "Proceso analizado: pasos definidos y dependencias mapeadas.",
        "optimizer":  "Optimización propuesta: automatización y mejoras de eficiencia.",
        "planner":    "Plan de implementación: cronograma y recursos asignados.",
    }
    return FakeLLM(responses=responses, default="Tarea completada satisfactoriamente.")


@pytest.fixture
def fake_tool():
    """FakeTool that succeeds and records call count."""
    return FakeTool()


@pytest.fixture
def failing_tool():
    """FakeTool that always returns an error."""
    return FakeTool(should_fail=True)


@pytest.fixture
def sample_contract():
    """Contrato de prueba en español."""
    return """CONTRATO DE PRESTACIÓN DE SERVICIOS PROFESIONALES

Entre las partes:
PROVEEDOR: TechCorp SA de CV, RFC TEC201001AB1
CLIENTE: MiEmpresa SA de CV, RFC MEM180501XYZ

OBJETO DEL CONTRATO:
El Proveedor se compromete a desarrollar e implementar un sistema de gestión
de inventarios para el Cliente, con las especificaciones detalladas en el
Anexo Técnico adjunto.

VIGENCIA: Del 1 de enero al 31 de diciembre de 2026.
MONTO: $150,000.00 MXN más IVA, pagadero en mensualidades.
CONFIDENCIALIDAD: Ambas partes acuerdan mantener confidencialidad.
JURISDICCIÓN: Ciudad de México, México.
"""


@pytest.fixture
def sample_business_data():
    """Datos de empresa mexicana para tests de análisis."""
    return """EMPRESA: MiEmpresa SA de CV
RFC: MEM180501XYZ
PERÍODO: Enero-Diciembre 2025

INGRESOS:
  Q1: $1,200,000 MXN
  Q2: $1,450,000 MXN
  Q3: $1,380,000 MXN
  Q4: $1,620,000 MXN
  TOTAL: $5,650,000 MXN

EGRESOS:
  Nómina: $2,100,000 MXN
  Operaciones: $1,200,000 MXN
  Ventas: $450,000 MXN
  TOTAL: $3,750,000 MXN

UTILIDAD BRUTA: $1,900,000 MXN
MARGEN: 33.6%
"""


@pytest.fixture
def sample_process():
    """Proceso empresarial para tests de automatización."""
    return """PROCESO: Gestión de Pedidos de Cliente

PASO 1: Recepción del pedido (email o WhatsApp)
  - Responsable: Equipo de ventas
  - Tiempo: 30 minutos

PASO 2: Validación de inventario en sistema
  - Responsable: Almacén
  - Tiempo: 1 hora

PASO 3: Generación de cotización
  - Responsable: Ventas
  - Tiempo: 2 horas

PASO 4: Aprobación del cliente
  - Responsable: Cliente
  - Tiempo: 24-48 horas

PASO 5: Procesamiento y envío
  - Responsable: Operaciones
  - Tiempo: 3-5 días hábiles

PROBLEMAS IDENTIFICADOS:
  - Proceso manual y propenso a errores
  - Sin trazabilidad en WhatsApp
  - Cotizaciones en Excel inconsistentes
"""
