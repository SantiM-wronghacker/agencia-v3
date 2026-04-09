"""Extended tests for CRM tools — covers HTTP success & error paths."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from tools.crm.hubspot import HubSpotTool
from tools.crm.google_sheets import GoogleSheetsTool
from tools.crm.calendar_tool import GoogleCalendarTool


# ---------------------------------------------------------------------------
# HubSpotTool
# ---------------------------------------------------------------------------

_HS_CREDS = {"api_key": "hs-api-key-test"}


class TestHubSpotToolExtended:

    # --- create_contact ---

    def test_create_contact_success(self):
        with patch("tools.crm.hubspot.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"id": "contact-001"}
            tool = HubSpotTool(_HS_CREDS)
            result = tool.run(
                action="create_contact",
                name="Juan Pérez",
                email="juan@example.com",
                phone="5551234567",
                company="TechCorp",
            )
        assert result.success
        assert "contact-001" in result.output

    def test_create_contact_single_name(self):
        with patch("tools.crm.hubspot.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"id": "contact-002"}
            tool = HubSpotTool(_HS_CREDS)
            result = tool.run(action="create_contact", name="María")
        assert result.success

    def test_create_contact_http_error(self):
        with patch("tools.crm.hubspot.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = None
            tool = HubSpotTool(_HS_CREDS)
            result = tool.run(action="create_contact", name="Test")
        assert not result.success

    # --- update_deal ---

    def test_update_deal_success(self):
        with patch("tools.crm.hubspot.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"id": "deal-123", "properties": {}}
            tool = HubSpotTool(_HS_CREDS)
            result = tool.run(
                action="update_deal",
                deal_id="deal-123",
                stage="closedwon",
                amount=50000.0,
            )
        assert result.success
        assert "deal-123" in result.output

    def test_update_deal_http_error(self):
        with patch("tools.crm.hubspot.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = None
            tool = HubSpotTool(_HS_CREDS)
            result = tool.run(action="update_deal", deal_id="d-999")
        assert not result.success

    def test_update_deal_no_properties(self):
        with patch("tools.crm.hubspot.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"id": "deal-200"}
            tool = HubSpotTool(_HS_CREDS)
            result = tool.run(action="update_deal", deal_id="deal-200")
        assert result.success

    # --- get_pipeline ---

    def test_get_pipeline_success_with_deals(self):
        with patch("tools.crm.hubspot.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = {
                "results": [
                    {"properties": {"dealname": "Deal A", "dealstage": "presentationscheduled", "amount": "10000"}},
                    {"properties": {"dealname": "Deal B", "dealstage": "closedwon", "amount": "50000"}},
                ]
            }
            tool = HubSpotTool(_HS_CREDS)
            result = tool.run(action="get_pipeline")
        assert result.success
        assert "Deal A" in result.output
        assert "Deal B" in result.output

    def test_get_pipeline_empty(self):
        with patch("tools.crm.hubspot.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = {"results": []}
            tool = HubSpotTool(_HS_CREDS)
            result = tool.run(action="get_pipeline")
        assert result.success
        assert "vacío" in result.output.lower() or "sin deals" in result.output.lower()

    def test_get_pipeline_http_error(self):
        with patch("tools.crm.hubspot.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = None
            tool = HubSpotTool(_HS_CREDS)
            result = tool.run(action="get_pipeline")
        assert not result.success

    # --- create_task ---

    def test_create_task_success(self):
        with patch("tools.crm.hubspot.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"id": "task-001"}
            tool = HubSpotTool(_HS_CREDS)
            result = tool.run(
                action="create_task",
                contact_id="contact-001",
                title="Llamar al cliente",
                due_date="2026-06-01",
            )
        assert result.success
        assert result.raw_data["task_id"] == "task-001"

    def test_create_task_without_due_date(self):
        with patch("tools.crm.hubspot.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"id": "task-002"}
            tool = HubSpotTool(_HS_CREDS)
            result = tool.run(action="create_task", title="Seguimiento")
        assert result.success

    def test_create_task_http_error(self):
        with patch("tools.crm.hubspot.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = None
            tool = HubSpotTool(_HS_CREDS)
            result = tool.run(action="create_task", title="Tarea")
        assert not result.success

    # --- get_contacts ---

    def test_get_contacts_success(self):
        with patch("tools.crm.hubspot.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = {
                "results": [
                    {"properties": {"firstname": "Ana", "lastname": "López", "email": "ana@example.com"}},
                    {"properties": {"firstname": "Carlos", "lastname": "", "email": "carlos@example.com"}},
                ]
            }
            tool = HubSpotTool(_HS_CREDS)
            result = tool.run(action="get_contacts", limit=10)
        assert result.success
        assert "Ana" in result.output

    def test_get_contacts_http_error(self):
        with patch("tools.crm.hubspot.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = None
            tool = HubSpotTool(_HS_CREDS)
            result = tool.run(action="get_contacts")
        assert not result.success

    def test_no_api_key(self):
        tool = HubSpotTool({})
        result = tool.run(action="create_contact", name="Test")
        assert not result.success
        assert "api_key" in result.error


# ---------------------------------------------------------------------------
# GoogleSheetsTool
# ---------------------------------------------------------------------------

_GS_CREDS = {"service_account_json": "fake.json", "spreadsheet_id": "sp-123"}


class TestGoogleSheetsTool:

    def _patched_tool(self, get_return=None, post_return=None):
        """Returns a tool with _get_headers mocked to return fake headers."""
        tool = GoogleSheetsTool(_GS_CREDS)
        return tool

    # --- read ---

    def test_read_success(self):
        with patch.object(GoogleSheetsTool, "_get_headers", return_value={"Authorization": "Bearer fake"}):
            with patch("tools.crm.google_sheets.HTTPClient") as MockHTTP:
                mock_client = MagicMock()
                MockHTTP.return_value = mock_client
                mock_client.get.return_value = {
                    "values": [
                        ["Nombre", "Email", "Teléfono"],
                        ["Juan", "juan@example.com", "5551234567"],
                    ]
                }
                tool = GoogleSheetsTool(_GS_CREDS)
                result = tool.run(action="read", range="Sheet1!A1:C10")

        assert result.success
        assert "Nombre" in result.output
        assert "Juan" in result.output

    def test_read_empty_sheet(self):
        with patch.object(GoogleSheetsTool, "_get_headers", return_value={"Authorization": "Bearer fake"}):
            with patch("tools.crm.google_sheets.HTTPClient") as MockHTTP:
                mock_client = MagicMock()
                MockHTTP.return_value = mock_client
                mock_client.get.return_value = {"values": []}
                tool = GoogleSheetsTool(_GS_CREDS)
                result = tool.run(action="read")

        assert result.success
        assert "vacía" in result.output.lower() or "empty" in result.output.lower()

    def test_read_http_error(self):
        with patch.object(GoogleSheetsTool, "_get_headers", return_value={"Authorization": "Bearer fake"}):
            with patch("tools.crm.google_sheets.HTTPClient") as MockHTTP:
                mock_client = MagicMock()
                MockHTTP.return_value = mock_client
                mock_client.get.return_value = None
                tool = GoogleSheetsTool(_GS_CREDS)
                result = tool.run(action="read")

        assert not result.success

    def test_read_no_credentials(self):
        tool = GoogleSheetsTool({})
        result = tool.run(action="read")
        assert not result.success

    def test_read_no_google_auth(self):
        with patch.object(GoogleSheetsTool, "_get_headers", return_value=None):
            tool = GoogleSheetsTool(_GS_CREDS)
            result = tool.run(action="read")
        assert not result.success
        assert "google-auth" in result.error.lower() or "instalado" in result.error.lower()

    # --- append_row ---

    def test_append_row_success(self):
        with patch.object(GoogleSheetsTool, "_get_headers", return_value={"Authorization": "Bearer fake"}):
            with patch("tools.crm.google_sheets.HTTPClient") as MockHTTP:
                mock_client = MagicMock()
                MockHTTP.return_value = mock_client
                mock_client.post.return_value = {"updates": {"updatedRows": 1}}
                tool = GoogleSheetsTool(_GS_CREDS)
                result = tool.run(action="append_row", values=["Ana", "ana@test.com", "5551111111"])

        assert result.success
        assert "Ana" in result.output

    def test_append_row_http_error(self):
        with patch.object(GoogleSheetsTool, "_get_headers", return_value={"Authorization": "Bearer fake"}):
            with patch("tools.crm.google_sheets.HTTPClient") as MockHTTP:
                mock_client = MagicMock()
                MockHTTP.return_value = mock_client
                mock_client.post.return_value = None
                tool = GoogleSheetsTool(_GS_CREDS)
                result = tool.run(action="append_row", values=["test"])

        assert not result.success

    def test_append_row_no_google_auth(self):
        with patch.object(GoogleSheetsTool, "_get_headers", return_value=None):
            tool = GoogleSheetsTool(_GS_CREDS)
            result = tool.run(action="append_row", values=["data"])
        assert not result.success

    # --- update_cell ---

    def test_update_cell_success(self):
        with patch.object(GoogleSheetsTool, "_get_headers", return_value={"Authorization": "Bearer fake"}):
            with patch("tools.crm.google_sheets.HTTPClient") as MockHTTP:
                mock_client = MagicMock()
                MockHTTP.return_value = mock_client
                mock_client.post.return_value = {"updatedCells": 1}
                tool = GoogleSheetsTool(_GS_CREDS)
                result = tool.run(action="update_cell", cell="B2", value="Nuevo Valor")

        assert result.success
        assert "B2" in result.output
        assert "Nuevo Valor" in result.output

    def test_update_cell_http_error(self):
        with patch.object(GoogleSheetsTool, "_get_headers", return_value={"Authorization": "Bearer fake"}):
            with patch("tools.crm.google_sheets.HTTPClient") as MockHTTP:
                mock_client = MagicMock()
                MockHTTP.return_value = mock_client
                mock_client.post.return_value = None
                tool = GoogleSheetsTool(_GS_CREDS)
                result = tool.run(action="update_cell", cell="A1", value="test")

        assert not result.success

    def test_update_cell_no_google_auth(self):
        with patch.object(GoogleSheetsTool, "_get_headers", return_value=None):
            tool = GoogleSheetsTool(_GS_CREDS)
            result = tool.run(action="update_cell", cell="A1", value="x")
        assert not result.success

    # --- find_row ---

    def test_find_row_found(self):
        tool = GoogleSheetsTool(_GS_CREDS)
        result = tool.run(
            action="find_row",
            column_values=["Alice", "Bob", "Charlie"],
            search_value="Bob",
        )
        assert result.success
        assert "Bob" in result.output
        assert "fila 2" in result.output.lower() or "2" in result.output

    def test_find_row_not_found(self):
        tool = GoogleSheetsTool(_GS_CREDS)
        result = tool.run(
            action="find_row",
            column_values=["Alice", "Bob"],
            search_value="David",
        )
        assert not result.success

    def test_unknown_action(self):
        tool = GoogleSheetsTool(_GS_CREDS)
        result = tool.run(action="nope")
        assert not result.success


# ---------------------------------------------------------------------------
# GoogleCalendarTool
# ---------------------------------------------------------------------------

_CAL_CREDS = {"service_account_json": "fake.json", "calendar_id": "cal@example.com"}


class TestGoogleCalendarTool:

    # --- create_event ---

    def test_create_event_success(self):
        with patch.object(GoogleCalendarTool, "_get_headers",
                          return_value={"Authorization": "Bearer fake", "Content-Type": "application/json"}):
            with patch("tools.crm.calendar_tool.HTTPClient") as MockHTTP:
                mock_client = MagicMock()
                MockHTTP.return_value = mock_client
                mock_client.post.return_value = {"id": "event-abc"}
                tool = GoogleCalendarTool(_CAL_CREDS)
                result = tool.run(
                    action="create_event",
                    title="Reunión de ventas",
                    start="2026-06-15T10:00:00",
                    end="2026-06-15T11:00:00",
                    attendees=["cliente@example.com"],
                    description="Revisión trimestral",
                )

        assert result.success
        assert "Reunión de ventas" in result.output

    def test_create_event_http_error(self):
        with patch.object(GoogleCalendarTool, "_get_headers",
                          return_value={"Authorization": "Bearer fake"}):
            with patch("tools.crm.calendar_tool.HTTPClient") as MockHTTP:
                mock_client = MagicMock()
                MockHTTP.return_value = mock_client
                mock_client.post.return_value = None
                tool = GoogleCalendarTool(_CAL_CREDS)
                result = tool.run(action="create_event", title="Test",
                                  start="2026-01-01T10:00:00", end="2026-01-01T11:00:00")

        assert not result.success

    def test_create_event_no_credentials(self):
        tool = GoogleCalendarTool({})
        result = tool.run(action="create_event", title="Test",
                          start="2026-01-01T10:00:00", end="2026-01-01T11:00:00")
        assert not result.success

    def test_create_event_no_google_auth(self):
        with patch.object(GoogleCalendarTool, "_get_headers", return_value=None):
            tool = GoogleCalendarTool(_CAL_CREDS)
            result = tool.run(action="create_event", title="Test",
                              start="2026-01-01T10:00:00", end="2026-01-01T11:00:00")
        assert not result.success

    # --- get_availability ---

    def test_get_availability_success_with_events(self):
        with patch.object(GoogleCalendarTool, "_get_headers",
                          return_value={"Authorization": "Bearer fake"}):
            with patch("tools.crm.calendar_tool.HTTPClient") as MockHTTP:
                mock_client = MagicMock()
                MockHTTP.return_value = mock_client
                mock_client.get.return_value = {
                    "items": [
                        {
                            "summary": "Reunión",
                            "start": {"dateTime": "2026-06-15T10:00:00Z"},
                            "end": {"dateTime": "2026-06-15T11:00:00Z"},
                        }
                    ]
                }
                tool = GoogleCalendarTool(_CAL_CREDS)
                result = tool.run(action="get_availability", date="2026-06-15")

        assert result.success
        assert "2026-06-15" in result.output

    def test_get_availability_free_day(self):
        with patch.object(GoogleCalendarTool, "_get_headers",
                          return_value={"Authorization": "Bearer fake"}):
            with patch("tools.crm.calendar_tool.HTTPClient") as MockHTTP:
                mock_client = MagicMock()
                MockHTTP.return_value = mock_client
                mock_client.get.return_value = {"items": []}
                tool = GoogleCalendarTool(_CAL_CREDS)
                result = tool.run(action="get_availability", date="2026-07-01")

        assert result.success
        assert "libre" in result.output.lower() or "sin eventos" in result.output.lower()

    def test_get_availability_http_error(self):
        with patch.object(GoogleCalendarTool, "_get_headers",
                          return_value={"Authorization": "Bearer fake"}):
            with patch("tools.crm.calendar_tool.HTTPClient") as MockHTTP:
                mock_client = MagicMock()
                MockHTTP.return_value = mock_client
                mock_client.get.return_value = None
                tool = GoogleCalendarTool(_CAL_CREDS)
                result = tool.run(action="get_availability", date="2026-06-15")

        assert not result.success

    def test_get_availability_no_google_auth(self):
        with patch.object(GoogleCalendarTool, "_get_headers", return_value=None):
            tool = GoogleCalendarTool(_CAL_CREDS)
            result = tool.run(action="get_availability", date="2026-06-15")
        assert not result.success

    # --- list_events ---

    def test_list_events_success(self):
        with patch.object(GoogleCalendarTool, "_get_headers",
                          return_value={"Authorization": "Bearer fake"}):
            with patch("tools.crm.calendar_tool.HTTPClient") as MockHTTP:
                mock_client = MagicMock()
                MockHTTP.return_value = mock_client
                mock_client.get.return_value = {
                    "items": [
                        {
                            "summary": "Demo Producto",
                            "start": {"dateTime": "2026-06-10T14:00:00Z"},
                            "end": {"dateTime": "2026-06-10T15:00:00Z"},
                        },
                        {
                            "summary": "Llamada de seguimiento",
                            "start": {"date": "2026-06-12"},
                        },
                    ]
                }
                tool = GoogleCalendarTool(_CAL_CREDS)
                result = tool.run(action="list_events",
                                  date_from="2026-06-01", date_to="2026-06-30")

        assert result.success
        assert "Demo Producto" in result.output
        assert "Llamada de seguimiento" in result.output

    def test_list_events_http_error(self):
        with patch.object(GoogleCalendarTool, "_get_headers",
                          return_value={"Authorization": "Bearer fake"}):
            with patch("tools.crm.calendar_tool.HTTPClient") as MockHTTP:
                mock_client = MagicMock()
                MockHTTP.return_value = mock_client
                mock_client.get.return_value = None
                tool = GoogleCalendarTool(_CAL_CREDS)
                result = tool.run(action="list_events",
                                  date_from="2026-06-01", date_to="2026-06-30")

        assert not result.success

    def test_list_events_no_google_auth(self):
        with patch.object(GoogleCalendarTool, "_get_headers", return_value=None):
            tool = GoogleCalendarTool(_CAL_CREDS)
            result = tool.run(action="list_events",
                              date_from="2026-06-01", date_to="2026-06-30")
        assert not result.success

    def test_unknown_action(self):
        tool = GoogleCalendarTool(_CAL_CREDS)
        result = tool.run(action="nope")
        assert not result.success
