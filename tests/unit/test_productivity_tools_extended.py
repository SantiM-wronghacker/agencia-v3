"""Extended tests for productivity tools (Notion, Slack, Trello)."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from tools.productivity.notion import NotionTool
from tools.productivity.slack import SlackTool
from tools.productivity.trello import TrelloTool


# ---------------------------------------------------------------------------
# NotionTool
# ---------------------------------------------------------------------------

_NOTION_CREDS = {"token": "secret-notion-tok", "default_database_id": "db-abc-123"}


class TestNotionTool:

    # --- create_page ---

    def test_create_page_success(self):
        with patch("tools.productivity.notion.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"id": "page-notion-001"}
            tool = NotionTool(_NOTION_CREDS)
            result = tool.run(
                action="create_page",
                title="Proceso de ventas",
                content="Documento de proceso detallado.",
            )
        assert result.success
        assert result.raw_data["page_id"] == "page-notion-001"

    def test_create_page_with_explicit_db_id(self):
        with patch("tools.productivity.notion.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"id": "page-002"}
            tool = NotionTool({"token": "tok"})
            result = tool.run(
                action="create_page",
                title="Página",
                database_id="db-explicit-xyz",
            )
        assert result.success

    def test_create_page_no_db_id(self):
        tool = NotionTool({"token": "tok"})  # no default_database_id
        result = tool.run(action="create_page", title="Test")
        assert not result.success
        assert "database_id" in result.error.lower()

    def test_create_page_no_token(self):
        tool = NotionTool({})
        result = tool.run(action="create_page", title="Test", database_id="db-123")
        assert not result.success
        assert "token" in result.error.lower()

    def test_create_page_http_error(self):
        with patch("tools.productivity.notion.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = None
            tool = NotionTool(_NOTION_CREDS)
            result = tool.run(action="create_page", title="Test")
        assert not result.success

    def test_create_page_with_extra_properties(self):
        with patch("tools.productivity.notion.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"id": "page-003"}
            tool = NotionTool(_NOTION_CREDS)
            result = tool.run(
                action="create_page",
                title="Con props",
                properties={"Status": {"select": {"name": "En proceso"}}},
            )
        assert result.success

    # --- query_database ---

    def test_query_database_success(self):
        with patch("tools.productivity.notion.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {
                "results": [
                    {
                        "id": "page-x",
                        "properties": {
                            "Name": {
                                "type": "title",
                                "title": [{"text": {"content": "Tarea A"}}],
                            }
                        },
                    },
                ]
            }
            tool = NotionTool(_NOTION_CREDS)
            result = tool.run(action="query_database")
        assert result.success
        assert "Tarea A" in result.output

    def test_query_database_with_filter(self):
        with patch("tools.productivity.notion.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"results": []}
            tool = NotionTool(_NOTION_CREDS)
            result = tool.run(
                action="query_database",
                filter_property="Status",
                filter_value="Done",
            )
        assert result.success

    def test_query_database_no_db_id(self):
        tool = NotionTool({"token": "tok"})
        result = tool.run(action="query_database")
        assert not result.success

    def test_query_database_http_error(self):
        with patch("tools.productivity.notion.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = None
            tool = NotionTool(_NOTION_CREDS)
            result = tool.run(action="query_database")
        assert not result.success

    # --- update_page ---

    def test_update_page_success(self):
        with patch("tools.productivity.notion.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"id": "page-upd"}
            tool = NotionTool(_NOTION_CREDS)
            result = tool.run(
                action="update_page",
                page_id="page-upd",
                properties={"Status": {"select": {"name": "Completado"}}},
            )
        assert result.success
        assert "page-upd" in result.output

    def test_update_page_no_page_id(self):
        tool = NotionTool(_NOTION_CREDS)
        result = tool.run(action="update_page")
        assert not result.success
        assert "page_id" in result.error.lower()

    def test_update_page_http_error(self):
        with patch("tools.productivity.notion.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = None
            tool = NotionTool(_NOTION_CREDS)
            result = tool.run(action="update_page", page_id="page-fail")
        assert not result.success

    # --- get_page ---

    def test_get_page_success(self):
        with patch("tools.productivity.notion.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = {
                "id": "page-get",
                "properties": {
                    "Name": {
                        "type": "title",
                        "title": [{"text": {"content": "Mi página"}}],
                    },
                    "Status": {
                        "type": "select",
                        "select": "En proceso",
                    },
                    "Count": {
                        "type": "number",
                        "number": 42,
                    },
                },
            }
            tool = NotionTool(_NOTION_CREDS)
            result = tool.run(action="get_page", page_id="page-get")
        assert result.success
        assert "Mi página" in result.output

    def test_get_page_with_rich_text_property(self):
        with patch("tools.productivity.notion.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = {
                "id": "page-rt",
                "properties": {
                    "Description": {
                        "type": "rich_text",
                        "rich_text": [{"text": {"content": "Texto descriptivo"}}],
                    },
                    "Done": {
                        "type": "checkbox",
                        "checkbox": True,
                    },
                },
            }
            tool = NotionTool(_NOTION_CREDS)
            result = tool.run(action="get_page", page_id="page-rt")
        assert result.success

    def test_get_page_no_page_id(self):
        tool = NotionTool(_NOTION_CREDS)
        result = tool.run(action="get_page")
        assert not result.success

    def test_get_page_http_error(self):
        with patch("tools.productivity.notion.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = None
            tool = NotionTool(_NOTION_CREDS)
            result = tool.run(action="get_page", page_id="page-err")
        assert not result.success

    def test_unknown_action(self):
        tool = NotionTool(_NOTION_CREDS)
        result = tool.run(action="nope")
        assert not result.success


# ---------------------------------------------------------------------------
# SlackTool
# ---------------------------------------------------------------------------

_SLACK_CREDS = {"bot_token": "xoxb-slack-bot-token"}


class TestSlackTool:

    # --- send_message ---

    def test_send_message_success(self):
        with patch("tools.productivity.slack.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"ok": True, "ts": "1234567890.001"}
            tool = SlackTool(_SLACK_CREDS)
            result = tool.run(
                action="send_message",
                channel="general",
                text="Reporte diario listo.",
            )
        assert result.success
        assert "general" in result.output

    def test_send_message_with_blocks(self):
        with patch("tools.productivity.slack.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"ok": True, "ts": "ts-001"}
            tool = SlackTool(_SLACK_CREDS)
            result = tool.run(
                action="send_message",
                channel="reportes",
                text="Reporte",
                blocks=[{"type": "section", "text": {"type": "mrkdwn", "text": "*Hola*"}}],
            )
        assert result.success

    def test_send_message_slack_error(self):
        with patch("tools.productivity.slack.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"ok": False, "error": "channel_not_found"}
            tool = SlackTool(_SLACK_CREDS)
            result = tool.run(action="send_message", channel="unknown", text="test")
        assert not result.success
        assert "channel_not_found" in result.error

    def test_send_message_http_none(self):
        with patch("tools.productivity.slack.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = None
            tool = SlackTool(_SLACK_CREDS)
            result = tool.run(action="send_message", channel="general", text="test")
        assert not result.success

    def test_send_message_no_token(self):
        tool = SlackTool({})
        result = tool.run(action="send_message", channel="general", text="test")
        assert not result.success
        assert "bot_token" in result.error.lower()

    # --- send_dm ---

    def test_send_dm_success(self):
        with patch("tools.productivity.slack.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            # First post: conversations.open
            # Second post: chat.postMessage
            mock_client.post.side_effect = [
                {"ok": True, "channel": {"id": "D001"}},
                {"ok": True, "ts": "ts-dm-001"},
            ]
            tool = SlackTool(_SLACK_CREDS)
            result = tool.run(action="send_dm", user_id="U123", text="Hola!")
        assert result.success
        assert "U123" in result.output

    def test_send_dm_open_fails(self):
        with patch("tools.productivity.slack.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"ok": False, "error": "user_not_found"}
            tool = SlackTool(_SLACK_CREDS)
            result = tool.run(action="send_dm", user_id="U999", text="test")
        assert not result.success

    def test_send_dm_open_returns_none(self):
        with patch("tools.productivity.slack.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = None
            tool = SlackTool(_SLACK_CREDS)
            result = tool.run(action="send_dm", user_id="U999", text="test")
        assert not result.success

    def test_send_dm_message_fails(self):
        with patch("tools.productivity.slack.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.side_effect = [
                {"ok": True, "channel": {"id": "D001"}},
                {"ok": False, "error": "not_in_channel"},
            ]
            tool = SlackTool(_SLACK_CREDS)
            result = tool.run(action="send_dm", user_id="U123", text="test")
        assert not result.success

    # --- list_channels ---

    def test_list_channels_success(self):
        with patch("tools.productivity.slack.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = {
                "ok": True,
                "channels": [
                    {"id": "C001", "name": "general", "is_private": False},
                    {"id": "C002", "name": "secreto", "is_private": True},
                ],
            }
            tool = SlackTool(_SLACK_CREDS)
            result = tool.run(action="list_channels")
        assert result.success
        assert "general" in result.output
        assert "secreto" in result.output

    def test_list_channels_slack_error(self):
        with patch("tools.productivity.slack.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = {"ok": False, "error": "missing_scope"}
            tool = SlackTool(_SLACK_CREDS)
            result = tool.run(action="list_channels")
        assert not result.success

    def test_list_channels_http_none(self):
        with patch("tools.productivity.slack.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = None
            tool = SlackTool(_SLACK_CREDS)
            result = tool.run(action="list_channels")
        assert not result.success

    def test_unknown_action(self):
        tool = SlackTool(_SLACK_CREDS)
        result = tool.run(action="nope")
        assert not result.success


# ---------------------------------------------------------------------------
# TrelloTool
# ---------------------------------------------------------------------------

_TRELLO_CREDS = {"api_key": "trello-api-key", "token": "trello-token"}


class TestTrelloTool:

    # --- create_card ---

    def test_create_card_success(self):
        with patch("tools.productivity.trello.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {
                "id": "card-001",
                "url": "https://trello.com/c/abc",
            }
            tool = TrelloTool(_TRELLO_CREDS)
            result = tool.run(
                action="create_card",
                list_id="list-xyz",
                name="Implementar feature X",
                description="Descripción detallada",
                due_date="2026-06-30",
            )
        assert result.success
        assert "Implementar feature X" in result.output

    def test_create_card_without_due_date(self):
        with patch("tools.productivity.trello.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"id": "card-002", "url": ""}
            tool = TrelloTool(_TRELLO_CREDS)
            result = tool.run(action="create_card", list_id="list-1", name="Card sin fecha")
        assert result.success

    def test_create_card_http_error(self):
        with patch("tools.productivity.trello.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = None
            tool = TrelloTool(_TRELLO_CREDS)
            result = tool.run(action="create_card", list_id="list-1", name="test")
        assert not result.success

    def test_create_card_no_api_key(self):
        tool = TrelloTool({"token": "tok"})
        result = tool.run(action="create_card", list_id="list-1", name="test")
        assert not result.success
        assert "api_key" in result.error.lower()

    def test_create_card_no_token(self):
        tool = TrelloTool({"api_key": "key"})
        result = tool.run(action="create_card", list_id="list-1", name="test")
        assert not result.success
        assert "token" in result.error.lower()

    # --- move_card ---

    def test_move_card_success(self):
        with patch("tools.productivity.trello.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"id": "card-001", "idList": "list-done"}
            tool = TrelloTool(_TRELLO_CREDS)
            result = tool.run(action="move_card", card_id="card-001", list_id="list-done")
        assert result.success
        assert "list-done" in result.output

    def test_move_card_http_error(self):
        with patch("tools.productivity.trello.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = None
            tool = TrelloTool(_TRELLO_CREDS)
            result = tool.run(action="move_card", card_id="card-x", list_id="list-y")
        assert not result.success

    # --- get_board ---

    def test_get_board_success_list_response(self):
        with patch("tools.productivity.trello.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = [
                {"name": "Card 1", "idList": "list-todo"},
                {"name": "Card 2", "idList": "list-done"},
            ]
            tool = TrelloTool(_TRELLO_CREDS)
            result = tool.run(action="get_board", board_id="board-abc")
        assert result.success
        assert "Card 1" in result.output

    def test_get_board_success_dict_response(self):
        with patch("tools.productivity.trello.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = {
                "cards": [
                    {"name": "Card A", "idList": "list-1"},
                ]
            }
            tool = TrelloTool(_TRELLO_CREDS)
            result = tool.run(action="get_board", board_id="board-abc")
        assert result.success

    def test_get_board_http_error(self):
        with patch("tools.productivity.trello.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = None
            tool = TrelloTool(_TRELLO_CREDS)
            result = tool.run(action="get_board", board_id="board-abc")
        assert not result.success

    # --- get_lists ---

    def test_get_lists_success(self):
        with patch("tools.productivity.trello.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = [
                {"id": "list-1", "name": "Por hacer"},
                {"id": "list-2", "name": "En progreso"},
                {"id": "list-3", "name": "Terminado"},
            ]
            tool = TrelloTool(_TRELLO_CREDS)
            result = tool.run(action="get_lists", board_id="board-abc")
        assert result.success
        assert "Por hacer" in result.output
        assert "Terminado" in result.output

    def test_get_lists_http_error(self):
        with patch("tools.productivity.trello.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = None
            tool = TrelloTool(_TRELLO_CREDS)
            result = tool.run(action="get_lists", board_id="board-abc")
        assert not result.success

    def test_unknown_action(self):
        tool = TrelloTool(_TRELLO_CREDS)
        result = tool.run(action="nope")
        assert not result.success
