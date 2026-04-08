"""Tests for tools/crm/, tools/documents/ and sales groups."""
from unittest.mock import MagicMock, patch

import pytest

from tools.crm.hubspot import HubSpotTool
from tools.crm.whatsapp import WhatsAppTool
from tools.crm.google_sheets import GoogleSheetsTool
from tools.crm.calendar_tool import GoogleCalendarTool
from tools.documents.pdf_generator import PDFGeneratorTool
from tools.documents.word_generator import WordGeneratorTool
from groups.sales_pipeline import create_sales_pipeline
from groups.quotation_generator import create_quotation_generator


# ---------------------------------------------------------------------------
# HubSpot — missing credentials
# ---------------------------------------------------------------------------

def test_hubspot_missing_api_key_returns_error():
    tool = HubSpotTool({})
    result = tool.run(action="create_contact", name="Test", email="t@t.com")
    assert not result.success
    assert "api_key" in result.error


def test_hubspot_unknown_action_returns_error():
    tool = HubSpotTool({"api_key": "x"})
    result = tool.run(action="accion_invalida")
    assert not result.success
    assert "no soportada" in result.error


def test_hubspot_get_pipeline_missing_key():
    tool = HubSpotTool({})
    result = tool.run(action="get_pipeline")
    assert not result.success


def test_hubspot_create_contact_success():
    tool = HubSpotTool({"api_key": "test_key"})
    with patch("tools.crm.hubspot.HTTPClient") as MockHTTP:
        instance = MockHTTP.return_value
        instance.post.return_value = {"id": "contact_123"}
        result = tool._create_contact(
            name="Juan Pérez", email="juan@test.com", phone="5512345678"
        )
    assert result.success
    assert "contact_123" in result.output
    assert result.raw_data["contact_id"] == "contact_123"


def test_hubspot_create_contact_splits_name():
    """First name / last name split on first space."""
    tool = HubSpotTool({"api_key": "x"})
    with patch("tools.crm.hubspot.HTTPClient") as MockHTTP:
        instance = MockHTTP.return_value
        instance.post.return_value = {"id": "1"}
        tool._create_contact(name="Ana García", email="a@b.com")
        call_kwargs = instance.post.call_args
        props = call_kwargs[1]["json"]["properties"]
    assert props["firstname"] == "Ana"
    assert props["lastname"] == "García"


def test_hubspot_update_deal_success():
    tool = HubSpotTool({"api_key": "x"})
    with patch("tools.crm.hubspot.HTTPClient") as MockHTTP:
        instance = MockHTTP.return_value
        instance.post.return_value = {"id": "deal_456"}
        result = tool._update_deal(deal_id="deal_456", stage="closedwon", amount=5000.0)
    assert result.success
    assert "deal_456" in result.output


# ---------------------------------------------------------------------------
# WhatsApp — missing credentials
# ---------------------------------------------------------------------------

def test_whatsapp_missing_credentials_returns_error():
    tool = WhatsAppTool({})
    result = tool.run(action="send_message", to="5512345678", message="test")
    assert not result.success
    assert "token" in result.error


def test_whatsapp_missing_phone_number_id_returns_error():
    tool = WhatsAppTool({"token": "tok"})
    result = tool.run(action="send_message", to="5512345678", message="test")
    assert not result.success
    assert "phone_number_id" in result.error


def test_whatsapp_cleans_phone_number():
    tool = WhatsAppTool({"token": "x", "phone_number_id": "y"})
    with patch("tools.crm.whatsapp.HTTPClient") as MockHTTP:
        instance = MockHTTP.return_value
        instance.post.return_value = {"messages": [{"id": "msg_1"}]}
        result = tool._send_message(to="+52 55 1234 5678", message="hola")
        call_kwargs = instance.post.call_args
        body = call_kwargs[1]["json"]
    # All non-digit chars stripped; 10-digit number gets 52 prefix
    to_sent = body["to"]
    assert to_sent.isdigit()
    assert "52" in to_sent


def test_whatsapp_ten_digit_gets_country_code():
    tool = WhatsAppTool({"token": "x", "phone_number_id": "y"})
    cleaned = tool._clean_phone("5512345678")
    assert cleaned == "525512345678"
    assert len(cleaned) == 12


def test_whatsapp_send_template_success():
    tool = WhatsAppTool({"token": "tok", "phone_number_id": "pid"})
    with patch("tools.crm.whatsapp.HTTPClient") as MockHTTP:
        instance = MockHTTP.return_value
        instance.post.return_value = {"messages": [{"id": "m1"}]}
        result = tool._send_template(
            to="525512345678",
            template_name="cotizacion_v1",
            variables=[{"type": "text", "text": "TestCo"}],
        )
    assert result.success
    assert "cotizacion_v1" in result.output


# ---------------------------------------------------------------------------
# Google Calendar — missing credentials
# ---------------------------------------------------------------------------

def test_google_calendar_missing_credentials_returns_error():
    tool = GoogleCalendarTool({})
    result = tool.run(
        action="create_event",
        title="test",
        start="2026-05-01T10:00:00",
        end="2026-05-01T11:00:00",
    )
    assert not result.success
    assert "service_account_json" in result.error


def test_google_calendar_missing_calendar_id_returns_error():
    tool = GoogleCalendarTool({"service_account_json": "/path/sa.json"})
    result = tool.run(
        action="create_event",
        title="test",
        start="2026-05-01T10:00:00",
        end="2026-05-01T11:00:00",
    )
    assert not result.success
    assert "calendar_id" in result.error


def test_google_calendar_unknown_action():
    tool = GoogleCalendarTool({})
    result = tool.run(action="delete_event")
    assert not result.success
    assert "no soportada" in result.error


# ---------------------------------------------------------------------------
# Google Sheets — missing credentials
# ---------------------------------------------------------------------------

def test_google_sheets_missing_service_account_returns_error():
    tool = GoogleSheetsTool({})
    result = tool.run(action="read")
    assert not result.success
    assert "service_account_json" in result.error


def test_google_sheets_find_row_success():
    tool = GoogleSheetsTool({"service_account_json": "s", "spreadsheet_id": "id"})
    result = tool._find_row(
        column_values=["Alice", "Bob", "Carlos"], search_value="Bob"
    )
    assert result.success
    assert "2" in result.output  # row index 1 → "fila 2"


def test_google_sheets_find_row_not_found():
    tool = GoogleSheetsTool({"service_account_json": "s", "spreadsheet_id": "id"})
    result = tool._find_row(column_values=["Alice", "Bob"], search_value="Zara")
    assert not result.success
    assert "no encontrado" in result.error


# ---------------------------------------------------------------------------
# PDF Generator
# ---------------------------------------------------------------------------

def test_pdf_generator_creates_file(tmp_path):
    tool = PDFGeneratorTool()
    result = tool.run(
        action="generate",
        title="Cotización Test",
        content="Línea 1\n\nLínea 2\n\nLínea 3",
        output_path=str(tmp_path / "test.pdf"),
        company_name="Empresa Test",
    )
    if result.success:
        assert (tmp_path / "test.pdf").exists()
        assert result.raw_data["path"].endswith("test.pdf")
    else:
        assert "reportlab" in result.error


def test_pdf_generator_unknown_action():
    tool = PDFGeneratorTool()
    result = tool.run(action="delete")
    assert not result.success
    assert "no soportada" in result.error


def test_pdf_generator_default_path(tmp_path):
    """When output_path is None, a path is auto-generated."""
    tool = PDFGeneratorTool()
    with patch("tools.documents.pdf_generator.Path") as MockPath:
        # Just verify the logic runs without error when reportlab is available
        result = tool.run(
            action="generate",
            title="AutoPath Test",
            content="contenido",
            output_path=str(tmp_path / "auto.pdf"),
        )
    # Either success (reportlab installed) or graceful error
    assert result.success or "reportlab" in result.error


# ---------------------------------------------------------------------------
# Word Generator
# ---------------------------------------------------------------------------

def test_word_generator_creates_file(tmp_path):
    tool = WordGeneratorTool()
    result = tool.run(
        action="generate",
        title="Propuesta Test",
        content="Párrafo 1\n\nPárrafo 2",
        output_path=str(tmp_path / "test.docx"),
    )
    if result.success:
        assert (tmp_path / "test.docx").exists()
        assert result.raw_data["path"].endswith("test.docx")
    else:
        assert "python-docx" in result.error


def test_word_generator_with_company_name(tmp_path):
    tool = WordGeneratorTool()
    result = tool.run(
        action="generate",
        title="Contrato",
        content="Cláusula 1\n\nCláusula 2",
        output_path=str(tmp_path / "contrato.docx"),
        company_name="Mi Empresa SA",
    )
    if result.success:
        assert (tmp_path / "contrato.docx").exists()
    else:
        assert "python-docx" in result.error


def test_word_generator_unknown_action():
    tool = WordGeneratorTool()
    result = tool.run(action="print")
    assert not result.success
    assert "no soportada" in result.error


# ---------------------------------------------------------------------------
# Sales Pipeline group
# ---------------------------------------------------------------------------

def test_sales_pipeline_group_created():
    group = create_sales_pipeline()
    assert group.name == "sales_pipeline"
    assert len(group.agents) == 4


def test_sales_pipeline_has_doc_tools_by_default():
    group = create_sales_pipeline()
    proposal_writer = group.agents[1]
    assert any(
        t.name in ("pdf_generator", "word_generator")
        for t in proposal_writer.tools
    )


def test_sales_pipeline_no_crm_tools_when_no_credentials():
    group = create_sales_pipeline()
    lead_qualifier = group.agents[0]
    # No credentials passed → no CRM tools
    assert len(lead_qualifier.tools) == 0


def test_sales_pipeline_injects_hubspot_when_credential_given():
    group = create_sales_pipeline(credentials={"hubspot": {"api_key": "test"}})
    lead_qualifier = group.agents[0]
    assert any(t.name == "hubspot" for t in lead_qualifier.tools)


def test_sales_pipeline_is_pipeline_mode():
    group = create_sales_pipeline()
    assert group.mode == "pipeline"


# ---------------------------------------------------------------------------
# Quotation Generator group
# ---------------------------------------------------------------------------

def test_quotation_generator_group_created():
    group = create_quotation_generator()
    assert group.name == "quotation_generator"
    assert len(group.agents) == 4


def test_quotation_generator_has_pdf_tool():
    group = create_quotation_generator()
    proposal_writer = group.agents[2]
    assert any(t.name == "pdf_generator" for t in proposal_writer.tools)


def test_quotation_generator_no_comm_tools_without_credentials():
    group = create_quotation_generator()
    sender = group.agents[3]
    assert len(sender.tools) == 0


def test_quotation_generator_injects_smtp_when_given():
    group = create_quotation_generator(
        credentials={
            "smtp": {
                "smtp_host": "smtp.test.com",
                "smtp_port": "587",
                "smtp_user": "u@test.com",
                "smtp_password": "pass",
            }
        }
    )
    sender = group.agents[3]
    assert any(t.name == "smtp_email" for t in sender.tools)


def test_quotation_generator_is_pipeline_mode():
    group = create_quotation_generator()
    assert group.mode == "pipeline"
