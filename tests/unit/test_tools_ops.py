"""Tests for tools/productivity/, tools/accounting/ and ops/HR/accounting groups."""
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tools.productivity.notion import NotionTool
from tools.productivity.slack import SlackTool
from tools.productivity.trello import TrelloTool
from tools.accounting.sat_mexico import SATMexicoTool
from tools.accounting.excel_reports import ExcelReportsTool
from tools.accounting.csv_processor import CSVProcessorTool
from groups.hr_onboarding import create_hr_onboarding
from groups.accounting_report import create_accounting_report
from groups.ops_daily import create_ops_daily


# ---------------------------------------------------------------------------
# Notion
# ---------------------------------------------------------------------------

def test_notion_missing_token_returns_error():
    tool = NotionTool({})
    result = tool.run(action="create_page", title="test", content="contenido")
    assert not result.success
    assert "token" in result.error


def test_notion_missing_database_id_returns_error():
    tool = NotionTool({"token": "x"})
    result = tool.run(action="create_page", title="test", content="contenido")
    assert not result.success
    assert "database_id" in result.error


def test_notion_uses_default_database_id():
    """default_database_id from credentials is used when no explicit db_id given."""
    tool = NotionTool({"token": "x", "default_database_id": "db_123"})
    with patch("tools.productivity.notion.HTTPClient") as MockHTTP:
        instance = MockHTTP.return_value
        instance.post.return_value = {"id": "page_abc"}
        result = tool._create_page(title="Mi Página", content="contenido")
    assert result.success
    assert "Mi Página" in result.output


def test_notion_unknown_action():
    tool = NotionTool({"token": "x"})
    result = tool.run(action="delete_page")
    assert not result.success
    assert "no soportada" in result.error


def test_notion_query_database_success():
    tool = NotionTool({"token": "x", "default_database_id": "db_1"})
    with patch("tools.productivity.notion.HTTPClient") as MockHTTP:
        instance = MockHTTP.return_value
        instance.post.return_value = {
            "results": [
                {
                    "id": "page_001",
                    "properties": {
                        "Name": {
                            "type": "title",
                            "title": [{"text": {"content": "Tarea 1"}}],
                        }
                    },
                }
            ]
        }
        result = tool._query_database()
    assert result.success
    assert "Tarea 1" in result.output


# ---------------------------------------------------------------------------
# Slack
# ---------------------------------------------------------------------------

def test_slack_missing_token_returns_error():
    tool = SlackTool({})
    result = tool.run(action="send_message", channel="general", text="test")
    assert not result.success
    assert "bot_token" in result.error


def test_slack_send_message_success():
    tool = SlackTool({"bot_token": "xoxb-test"})
    with patch("tools.productivity.slack.HTTPClient") as MockHTTP:
        instance = MockHTTP.return_value
        instance.post.return_value = {"ok": True, "ts": "1234.5678"}
        result = tool._send_message(channel="general", text="Hola equipo")
    assert result.success
    assert "general" in result.output


def test_slack_send_message_api_error():
    tool = SlackTool({"bot_token": "xoxb-test"})
    with patch("tools.productivity.slack.HTTPClient") as MockHTTP:
        instance = MockHTTP.return_value
        instance.post.return_value = {"ok": False, "error": "channel_not_found"}
        result = tool._send_message(channel="nonexistent", text="test")
    assert not result.success
    assert "channel_not_found" in result.error


def test_slack_unknown_action():
    tool = SlackTool({"bot_token": "x"})
    result = tool.run(action="delete_message")
    assert not result.success
    assert "no soportada" in result.error


# ---------------------------------------------------------------------------
# Trello
# ---------------------------------------------------------------------------

def test_trello_missing_credentials_returns_error():
    tool = TrelloTool({})
    result = tool.run(action="create_card", list_id="x", name="test")
    assert not result.success
    assert "api_key" in result.error


def test_trello_missing_token_returns_error():
    tool = TrelloTool({"api_key": "key"})
    result = tool.run(action="create_card", list_id="x", name="test")
    assert not result.success
    assert "token" in result.error


def test_trello_create_card_success():
    tool = TrelloTool({"api_key": "key", "token": "tok"})
    with patch("tools.productivity.trello.HTTPClient") as MockHTTP:
        instance = MockHTTP.return_value
        instance.post.return_value = {"id": "card_123", "url": "https://trello.com/c/abc"}
        result = tool._create_card(list_id="list_1", name="Nueva tarea")
    assert result.success
    assert "Nueva tarea" in result.output
    assert result.raw_data["card_id"] == "card_123"


def test_trello_unknown_action():
    tool = TrelloTool({"api_key": "k", "token": "t"})
    result = tool.run(action="delete_board")
    assert not result.success
    assert "no soportada" in result.error


# ---------------------------------------------------------------------------
# SAT México
# ---------------------------------------------------------------------------

def test_sat_validate_rfc_persona_moral_valid():
    tool = SATMexicoTool()
    result = tool.run(action="validate_rfc", rfc="ABC123456ABC")
    assert result.success
    assert "Moral" in result.output or "válido" in result.output.lower()


def test_sat_validate_rfc_persona_fisica_valid():
    tool = SATMexicoTool()
    result = tool.run(action="validate_rfc", rfc="ABCD123456ABC")
    assert result.success
    assert "Física" in result.output


def test_sat_validate_rfc_invalid():
    tool = SATMexicoTool()
    result = tool.run(action="validate_rfc", rfc="INVALID")
    assert not result.success
    assert "inválido" in result.error


def test_sat_validate_rfc_too_short():
    tool = SATMexicoTool()
    result = tool.run(action="validate_rfc", rfc="AB12345")
    assert not result.success


def test_sat_calculate_iva():
    tool = SATMexicoTool()
    result = tool.run(action="calculate_iva", subtotal=1000.0)
    assert result.success
    assert result.raw_data["iva"] == 160.0
    assert result.raw_data["total"] == 1160.0


def test_sat_calculate_iva_reduced_rate():
    tool = SATMexicoTool()
    result = tool.run(action="calculate_iva", subtotal=1000.0, rate=0.08)
    assert result.success
    assert result.raw_data["iva"] == 80.0
    assert result.raw_data["total"] == 1080.0


def test_sat_calculate_isr_first_bracket():
    tool = SATMexicoTool()
    result = tool.run(action="calculate_isr", ingreso_mensual=500.0)
    assert result.success
    assert "ISR" in result.output
    assert result.raw_data["ingreso_mensual"] == 500.0
    assert result.raw_data["isr_mensual"] >= 0


def test_sat_calculate_isr_middle_bracket():
    tool = SATMexicoTool()
    result = tool.run(action="calculate_isr", ingreso_mensual=20000.0)
    assert result.success
    assert result.raw_data["isr_mensual"] > 0


def test_sat_calculate_retenciones_honorarios():
    tool = SATMexicoTool()
    result = tool.run(action="calculate_retenciones", monto=10000.0, tipo="honorarios")
    assert result.success
    assert result.raw_data["isr_retenido"] == 1000.0
    assert "Honorarios" in result.output


def test_sat_calculate_retenciones_arrendamiento():
    tool = SATMexicoTool()
    result = tool.run(action="calculate_retenciones", monto=5000.0, tipo="arrendamiento")
    assert result.success
    assert result.raw_data["isr_retenido"] == 500.0


def test_sat_generate_cfdi_data():
    tool = SATMexicoTool()
    result = tool.run(
        action="generate_cfdi_data",
        emisor_rfc="ABC123456ABC",
        receptor_rfc="XAXX010101000",
        concepto="Servicios de consultoría",
        subtotal=5000.0,
    )
    assert result.success
    assert result.raw_data["Version"] == "4.0"
    assert result.raw_data["SubTotal"] == 5000.0
    assert result.raw_data["Total"] == 5800.0
    assert result.raw_data["Emisor"]["Rfc"] == "ABC123456ABC"


def test_sat_unknown_action():
    tool = SATMexicoTool()
    result = tool.run(action="pay_taxes")
    assert not result.success


# ---------------------------------------------------------------------------
# Excel Reports
# ---------------------------------------------------------------------------

def test_excel_reports_generates_file(tmp_path):
    tool = ExcelReportsTool()
    result = tool.run(
        action="generate",
        title="Reporte Test",
        headers=["Nombre", "Monto", "Fecha"],
        rows=[
            ["Cliente A", 1000, "2026-01-01"],
            ["Cliente B", 2000, "2026-01-02"],
        ],
        output_path=str(tmp_path / "test.xlsx"),
    )
    if result.success:
        assert (tmp_path / "test.xlsx").exists()
        assert result.raw_data["rows"] == 2
    else:
        assert "openpyxl" in result.error


def test_excel_reports_reads_file(tmp_path):
    tool = ExcelReportsTool()
    xlsx_path = str(tmp_path / "read_test.xlsx")
    # First generate
    gen_result = tool.run(
        action="generate",
        title="ReadTest",
        headers=["Col1", "Col2"],
        rows=[["A", "1"], ["B", "2"]],
        output_path=xlsx_path,
    )
    if not gen_result.success:
        pytest.skip("openpyxl not installed")

    read_result = tool.run(action="read", file_path=xlsx_path)
    assert read_result.success
    assert "Col1" in read_result.output


def test_excel_reports_read_nonexistent_file():
    tool = ExcelReportsTool()
    result = tool.run(action="read", file_path="/nonexistent/file.xlsx")
    assert not result.success
    assert "no encontrado" in result.error


def test_excel_reports_unknown_action():
    tool = ExcelReportsTool()
    result = tool.run(action="delete")
    assert not result.success


# ---------------------------------------------------------------------------
# CSV Processor
# ---------------------------------------------------------------------------

def test_csv_processor_read(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("nombre,monto\nA,100\nB,200\n", encoding="utf-8")
    tool = CSVProcessorTool()
    result = tool.run(action="read", file_path=str(csv_file))
    assert result.success
    assert "nombre" in result.output.lower()
    assert result.raw_data["total"] == 2


def test_csv_processor_filter(tmp_path):
    csv_file = tmp_path / "filter_test.csv"
    csv_file.write_text("nombre,tipo\nAlpha,A\nBeta,B\nGamma,A\n", encoding="utf-8")
    tool = CSVProcessorTool()
    result = tool.run(action="filter", file_path=str(csv_file), column="tipo", value="A")
    assert result.success
    assert result.raw_data["count"] == 2


def test_csv_processor_filter_no_results(tmp_path):
    csv_file = tmp_path / "empty_filter.csv"
    csv_file.write_text("nombre,tipo\nAlpha,A\n", encoding="utf-8")
    tool = CSVProcessorTool()
    result = tool.run(action="filter", file_path=str(csv_file), column="tipo", value="Z")
    assert result.success  # No results is success, not error
    assert result.raw_data["count"] == 0


def test_csv_processor_summarize(tmp_path):
    csv_file = tmp_path / "summary.csv"
    csv_file.write_text(
        "nombre,tipo,monto\nA,X,100\nB,Y,200\nC,X,150\n", encoding="utf-8"
    )
    tool = CSVProcessorTool()
    result = tool.run(
        action="summarize",
        file_path=str(csv_file),
        group_by="tipo",
        numeric_column="monto",
    )
    assert result.success
    assert "Total de filas: 3" in result.output
    assert "450" in result.output  # suma


def test_csv_processor_nonexistent_file():
    tool = CSVProcessorTool()
    result = tool.run(action="read", file_path="/nonexistent.csv")
    assert not result.success


def test_csv_processor_unknown_action(tmp_path):
    tool = CSVProcessorTool()
    result = tool.run(action="upload")
    assert not result.success


# ---------------------------------------------------------------------------
# HR Onboarding group
# ---------------------------------------------------------------------------

def test_hr_onboarding_group_created():
    group = create_hr_onboarding()
    assert group.name == "hr_onboarding"
    assert len(group.agents) == 4


def test_hr_onboarding_doc_tools_always_present():
    group = create_hr_onboarding()
    doc_gen = group.agents[1]  # document_generator
    assert any(t.name in ("word_generator", "pdf_generator") for t in doc_gen.tools)


def test_hr_onboarding_no_comm_without_credentials():
    group = create_hr_onboarding()
    communicator = group.agents[3]
    assert len(communicator.tools) == 0


def test_hr_onboarding_slack_injected():
    group = create_hr_onboarding(credentials={"slack": {"bot_token": "xoxb-test"}})
    communicator = group.agents[3]
    assert any(t.name == "slack" for t in communicator.tools)


def test_hr_onboarding_is_pipeline():
    group = create_hr_onboarding()
    assert group.mode == "pipeline"


# ---------------------------------------------------------------------------
# Accounting Report group
# ---------------------------------------------------------------------------

def test_accounting_report_group_has_sat_tools():
    group = create_accounting_report()
    analyst = group.agents[1]  # accounting_analyst
    assert any(t.name == "sat_mexico" for t in analyst.tools)


def test_accounting_report_tax_calculator_has_sat():
    group = create_accounting_report()
    tax_calc = group.agents[2]
    assert any(t.name == "sat_mexico" for t in tax_calc.tools)


def test_accounting_report_data_collector_has_csv():
    group = create_accounting_report()
    collector = group.agents[0]
    assert any(t.name == "csv_processor" for t in collector.tools)


def test_accounting_report_four_agents():
    group = create_accounting_report()
    assert len(group.agents) == 4


# ---------------------------------------------------------------------------
# Ops Daily group
# ---------------------------------------------------------------------------

def test_ops_daily_group_created():
    group = create_ops_daily()
    assert group.name == "ops_daily"
    assert len(group.agents) == 4


def test_ops_daily_no_tools_without_credentials():
    group = create_ops_daily()
    task_reviewer = group.agents[0]
    assert len(task_reviewer.tools) == 0


def test_ops_daily_trello_injected():
    group = create_ops_daily(
        credentials={"trello": {"api_key": "key", "token": "tok"}}
    )
    task_reviewer = group.agents[0]
    assert any(t.name == "trello" for t in task_reviewer.tools)


def test_ops_daily_is_pipeline():
    group = create_ops_daily()
    assert group.mode == "pipeline"
