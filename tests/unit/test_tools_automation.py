"""Tests for tools/automation/, tools/storage/ and automation groups."""
from pathlib import Path
from unittest.mock import patch, MagicMock

import httpx
import pytest

from tools.automation.scheduler import SchedulerTool
from tools.automation.trigger import TriggerTool
from tools.automation.webhook_receiver import WebhookReceiverTool
from tools.automation.zapier_webhook import ZapierWebhookTool
from tools.automation.make_webhook import MakeWebhookTool
from tools.automation.n8n_webhook import N8NWebhookTool
from tools.storage.google_drive import GoogleDriveTool
from tools.storage.dropbox import DropboxTool
from groups.daily_report import create_daily_report
from groups.social_autopilot import create_social_autopilot
from groups.lead_nurturing import create_lead_nurturing


# ---------------------------------------------------------------------------
# SchedulerTool — cron validation
# ---------------------------------------------------------------------------

def test_scheduler_validate_valid_cron():
    tool = SchedulerTool()
    result = tool.run(action="validate_cron", cron_expression="0 9 * * 1-5")
    assert result.success


def test_scheduler_validate_star_cron():
    tool = SchedulerTool()
    result = tool.run(action="validate_cron", cron_expression="* * * * *")
    assert result.success


def test_scheduler_validate_step_cron():
    tool = SchedulerTool()
    result = tool.run(action="validate_cron", cron_expression="*/30 * * * *")
    assert result.success


def test_scheduler_validate_invalid_cron():
    tool = SchedulerTool()
    result = tool.run(action="validate_cron", cron_expression="invalid cron here")
    assert not result.success
    assert "Formato" in result.error or "min" in result.error


def test_scheduler_validate_too_few_fields():
    tool = SchedulerTool()
    result = tool.run(action="validate_cron", cron_expression="0 9 * *")
    assert not result.success


def test_scheduler_schedule_task(tmp_path, monkeypatch):
    import tools.automation.scheduler as sched_mod
    monkeypatch.setattr(sched_mod, "_DATA_FILE", tmp_path / "scheduled_tasks.json")
    tool = SchedulerTool()
    result = tool.run(
        action="schedule",
        group_name="content_pipeline",
        task="Generar contenido semanal",
        cron_expression="0 9 * * 1",
    )
    assert result.success
    assert "content_pipeline" in result.output
    assert result.raw_data["group_name"] == "content_pipeline"
    assert result.raw_data["active"] is True


def test_scheduler_schedule_invalid_cron_returns_error(tmp_path, monkeypatch):
    import tools.automation.scheduler as sched_mod
    monkeypatch.setattr(sched_mod, "_DATA_FILE", tmp_path / "scheduled_tasks.json")
    tool = SchedulerTool()
    result = tool.run(
        action="schedule",
        group_name="content_pipeline",
        task="test",
        cron_expression="bad cron expression!!",
    )
    assert not result.success


def test_scheduler_list_empty(tmp_path, monkeypatch):
    import tools.automation.scheduler as sched_mod
    monkeypatch.setattr(sched_mod, "_DATA_FILE", tmp_path / "empty.json")
    tool = SchedulerTool()
    result = tool.run(action="list_tasks")
    assert result.success
    assert result.raw_data["tasks"] == []


def test_scheduler_list_with_tasks(tmp_path, monkeypatch):
    import tools.automation.scheduler as sched_mod
    monkeypatch.setattr(sched_mod, "_DATA_FILE", tmp_path / "tasks.json")
    tool = SchedulerTool()
    tool.run(action="schedule", group_name="grp1", task="t1", cron_expression="0 8 * * 1")
    tool.run(action="schedule", group_name="grp2", task="t2", cron_expression="*/30 * * * *")
    result = tool.run(action="list_tasks")
    assert result.success
    assert len(result.raw_data["tasks"]) == 2


def test_scheduler_cancel_task(tmp_path, monkeypatch):
    import tools.automation.scheduler as sched_mod
    monkeypatch.setattr(sched_mod, "_DATA_FILE", tmp_path / "tasks.json")
    tool = SchedulerTool()
    sched = tool.run(
        action="schedule", group_name="g", task="t", cron_expression="0 9 * * 1-5"
    )
    tid = sched.raw_data["id"]
    cancel = tool.run(action="cancel", task_id=tid)
    assert cancel.success
    tasks = tool.run(action="list_tasks").raw_data["tasks"]
    assert not tasks[0]["active"]


def test_scheduler_cancel_nonexistent(tmp_path, monkeypatch):
    import tools.automation.scheduler as sched_mod
    monkeypatch.setattr(sched_mod, "_DATA_FILE", tmp_path / "tasks.json")
    tool = SchedulerTool()
    result = tool.run(action="cancel", task_id="NOTEXIST")
    assert not result.success


def test_scheduler_unknown_action():
    tool = SchedulerTool()
    assert not tool.run(action="invalida").success


def test_scheduler_cron_descriptions():
    tool = SchedulerTool()
    cases = [
        ("0 9 * * 1-5", "viernes"),
        ("0 8 * * 1", "lunes"),
        ("*/30 * * * *", "30"),
    ]
    for cron, keyword in cases:
        desc = tool._describe_cron(cron)
        assert keyword.lower() in desc.lower() or len(desc) > 5


# ---------------------------------------------------------------------------
# TriggerTool
# ---------------------------------------------------------------------------

def test_trigger_register(tmp_path, monkeypatch):
    import tools.automation.trigger as trig_mod
    monkeypatch.setattr(trig_mod, "_DATA_FILE", tmp_path / "triggers.json")
    tool = TriggerTool()
    result = tool.run(
        action="register",
        trigger_name="nuevo_lead",
        group_name="lead_nurturing",
        event_type="webhook",
    )
    assert result.success
    assert "nuevo_lead" in result.output
    assert "webhook" in result.output.lower()
    assert "/webhooks/agencia/nuevo_lead" in result.raw_data.get("webhook_url", "")


def test_trigger_invalid_event_type(tmp_path, monkeypatch):
    import tools.automation.trigger as trig_mod
    monkeypatch.setattr(trig_mod, "_DATA_FILE", tmp_path / "triggers.json")
    tool = TriggerTool()
    result = tool.run(
        action="register",
        trigger_name="test",
        group_name="test",
        event_type="tipo_invalido",
    )
    assert not result.success


def test_trigger_list(tmp_path, monkeypatch):
    import tools.automation.trigger as trig_mod
    monkeypatch.setattr(trig_mod, "_DATA_FILE", tmp_path / "triggers.json")
    assert TriggerTool().run(action="list").success


def test_trigger_deactivate(tmp_path, monkeypatch):
    import tools.automation.trigger as trig_mod
    monkeypatch.setattr(trig_mod, "_DATA_FILE", tmp_path / "triggers.json")
    tool = TriggerTool()
    reg = tool.run(
        action="register",
        trigger_name="trg1",
        group_name="g",
        event_type="schedule",
    )
    tid = reg.raw_data["id"]
    result = tool.run(action="deactivate", trigger_id=tid)
    assert result.success


def test_trigger_unknown_action():
    tool = TriggerTool()
    assert not tool.run(action="activate").success


# ---------------------------------------------------------------------------
# WebhookReceiverTool
# ---------------------------------------------------------------------------

def test_webhook_receiver_create_endpoint(tmp_path, monkeypatch):
    import tools.automation.webhook_receiver as wh_mod
    monkeypatch.setattr(wh_mod, "_ENDPOINTS_FILE", tmp_path / "endpoints.json")
    monkeypatch.setattr(wh_mod, "_EVENTS_FILE", tmp_path / "events.json")
    tool = WebhookReceiverTool()
    result = tool.run(
        action="create_endpoint",
        name="form_contacto",
        group_name="lead_nurturing",
        description="Formulario de contacto web",
    )
    assert result.success
    assert "form_contacto" in result.output
    assert "/webhooks/" in result.output
    assert result.raw_data.get("secret") is not None
    assert len(result.raw_data["secret"]) >= 8


def test_webhook_receiver_list(tmp_path, monkeypatch):
    import tools.automation.webhook_receiver as wh_mod
    monkeypatch.setattr(wh_mod, "_ENDPOINTS_FILE", tmp_path / "endpoints.json")
    monkeypatch.setattr(wh_mod, "_EVENTS_FILE", tmp_path / "events.json")
    assert WebhookReceiverTool().run(action="list_endpoints").success


def test_webhook_receiver_get_recent_events_empty(tmp_path, monkeypatch):
    import tools.automation.webhook_receiver as wh_mod
    monkeypatch.setattr(wh_mod, "_ENDPOINTS_FILE", tmp_path / "endpoints.json")
    monkeypatch.setattr(wh_mod, "_EVENTS_FILE", tmp_path / "events.json")
    tool = WebhookReceiverTool()
    result = tool.run(action="get_recent_events", endpoint_name="noexiste")
    assert result.success


def test_webhook_endpoint_has_secret(tmp_path, monkeypatch):
    import tools.automation.webhook_receiver as wh_mod
    monkeypatch.setattr(wh_mod, "_ENDPOINTS_FILE", tmp_path / "endpoints.json")
    monkeypatch.setattr(wh_mod, "_EVENTS_FILE", tmp_path / "events.json")
    tool = WebhookReceiverTool()
    result = tool.run(action="create_endpoint", name="test_secret", group_name="content_pipeline")
    assert result.success
    assert result.raw_data.get("secret") is not None
    assert len(result.raw_data["secret"]) >= 8


def test_webhook_unknown_action():
    tool = WebhookReceiverTool()
    assert not tool.run(action="delete_endpoint").success


# ---------------------------------------------------------------------------
# ZapierWebhookTool
# ---------------------------------------------------------------------------

def test_zapier_no_url_returns_error():
    tool = ZapierWebhookTool({})
    result = tool.run(action="send", data={"test": "value"})
    assert not result.success
    assert "URL" in result.error or "zapier" in result.error.lower()


def test_zapier_with_url_sends():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.raise_for_status = MagicMock()
    with patch("httpx.post", return_value=mock_resp):
        tool = ZapierWebhookTool({})
        result = tool.run(
            action="send",
            data={"nombre": "Test", "email": "t@t.com"},
            webhook_url="https://hooks.zapier.com/fake/123",
        )
    assert result.success
    assert "exitosamente" in result.output.lower()


def test_zapier_trigger_success():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.raise_for_status = MagicMock()
    with patch("httpx.post", return_value=mock_resp):
        tool = ZapierWebhookTool({})
        result = tool.run(
            action="trigger",
            zap_name="Mi Zap",
            payload={"event": "new_lead"},
            webhook_url="https://hooks.zapier.com/fake/456",
        )
    assert result.success
    assert "Mi Zap" in result.output


def test_zapier_unknown_action():
    tool = ZapierWebhookTool({})
    assert not tool.run(action="delete").success


# ---------------------------------------------------------------------------
# MakeWebhookTool
# ---------------------------------------------------------------------------

def test_make_no_url_returns_error():
    tool = MakeWebhookTool({})
    result = tool.run(action="send", data={"test": "x"})
    assert not result.success
    assert "Make" in result.error or "URL" in result.error


def test_make_with_url_sends():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    with patch("httpx.post", return_value=mock_resp):
        tool = MakeWebhookTool({})
        result = tool.run(
            action="send",
            data={"key": "value"},
            webhook_url="https://hook.make.com/fake123",
        )
    assert result.success
    assert "200" in result.output


def test_make_unknown_action():
    tool = MakeWebhookTool({"webhook_url": "http://make.com/x"})
    assert not tool.run(action="trigger").success


# ---------------------------------------------------------------------------
# N8NWebhookTool
# ---------------------------------------------------------------------------

def test_n8n_no_url_returns_error():
    tool = N8NWebhookTool({})
    result = tool.run(action="send", data={"test": "x"})
    assert not result.success
    assert "webhook_url" in result.error or "n8n" in result.error.lower()


def test_n8n_with_url_sends():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.raise_for_status = MagicMock()
    with patch("httpx.post", return_value=mock_resp):
        tool = N8NWebhookTool({"webhook_url": "http://n8n.local/webhook/abc"})
        result = tool.run(action="send", data={"key": "val"}, workflow_name="Mi Workflow")
    assert result.success
    assert "Mi Workflow" in result.output


def test_n8n_trigger_no_url():
    tool = N8NWebhookTool({})
    result = tool.run(action="trigger", data={}, workflow_name="test")
    assert not result.success


def test_n8n_unknown_action():
    tool = N8NWebhookTool({"webhook_url": "http://n8n.local/webhook/x"})
    assert not tool.run(action="invalida").success


# ---------------------------------------------------------------------------
# GoogleDriveTool
# ---------------------------------------------------------------------------

def test_google_drive_no_credentials_returns_error():
    tool = GoogleDriveTool({})
    result = tool.run(action="upload", file_path="test.txt")
    assert not result.success
    assert "service_account_json" in result.error


def test_google_drive_file_not_found():
    tool = GoogleDriveTool({"service_account_json": "/fake/path.json"})
    result = tool.run(action="upload", file_path="/no/existe/archivo.txt")
    assert not result.success
    assert "no encontrado" in result.error.lower()


def test_google_drive_download_no_creds():
    tool = GoogleDriveTool({})
    result = tool.run(action="download", file_id="abc123")
    assert not result.success


def test_google_drive_list_no_creds():
    tool = GoogleDriveTool({})
    result = tool.run(action="list")
    assert not result.success


def test_google_drive_create_folder_no_creds():
    tool = GoogleDriveTool({})
    result = tool.run(action="create_folder", name="Test Folder")
    assert not result.success


def test_google_drive_unknown_action():
    tool = GoogleDriveTool({"service_account_json": "/fake.json"})
    assert not tool.run(action="delete").success


def test_google_drive_upload_success(tmp_path):
    test_file = tmp_path / "report.pdf"
    test_file.write_bytes(b"PDF content")

    mock_service = MagicMock()
    mock_service.files().create().execute.return_value = {
        "id": "abc123", "name": "report.pdf", "webViewLink": "https://drive.google.com/abc"
    }

    with patch.object(GoogleDriveTool, "_get_service", return_value=mock_service):
        with patch("googleapiclient.http.MediaFileUpload", MagicMock()):
            tool = GoogleDriveTool({"service_account_json": "/fake.json"})
            result = tool.run(action="upload", file_path=str(test_file))

    assert result.success
    assert "abc123" in result.output


def test_google_drive_list_success():
    mock_service = MagicMock()
    mock_service.files().list().execute.return_value = {
        "files": [
            {"id": "f1", "name": "doc1.pdf"},
            {"id": "f2", "name": "doc2.xlsx"},
        ]
    }
    with patch.object(GoogleDriveTool, "_get_service", return_value=mock_service):
        tool = GoogleDriveTool({"service_account_json": "/fake.json"})
        result = tool.run(action="list")
    assert result.success
    assert "doc1.pdf" in result.output
    assert len(result.raw_data["files"]) == 2


def test_google_drive_create_folder_success():
    mock_service = MagicMock()
    mock_service.files().create().execute.return_value = {"id": "fold1", "name": "Reportes"}
    with patch.object(GoogleDriveTool, "_get_service", return_value=mock_service):
        tool = GoogleDriveTool({"service_account_json": "/fake.json"})
        result = tool.run(action="create_folder", name="Reportes")
    assert result.success
    assert "fold1" in result.output


def test_google_drive_service_none_upload(tmp_path):
    test_file = tmp_path / "x.pdf"
    test_file.write_bytes(b"data")
    with patch.object(GoogleDriveTool, "_get_service", return_value=None):
        tool = GoogleDriveTool({"service_account_json": "/fake.json"})
        result = tool.run(action="upload", file_path=str(test_file))
    assert not result.success
    assert "Drive" in result.error


# ---------------------------------------------------------------------------
# DropboxTool
# ---------------------------------------------------------------------------

def test_dropbox_no_token_returns_error():
    tool = DropboxTool({})
    result = tool.run(action="upload", file_path="test.txt")
    assert not result.success
    assert "access_token" in result.error


def test_dropbox_file_not_found():
    tool = DropboxTool({"access_token": "fake_token"})
    result = tool.run(action="upload", file_path="/nonexistent/file.pdf")
    assert not result.success


def test_dropbox_download_no_token():
    tool = DropboxTool({})
    result = tool.run(action="download", dropbox_path="/test.txt")
    assert not result.success


def test_dropbox_list_no_token():
    tool = DropboxTool({})
    result = tool.run(action="list")
    assert not result.success


def test_dropbox_share_no_token():
    tool = DropboxTool({})
    result = tool.run(action="share", dropbox_path="/file.pdf")
    assert not result.success


def test_dropbox_unknown_action():
    tool = DropboxTool({"access_token": "x"})
    assert not tool.run(action="invalida").success


# ---------------------------------------------------------------------------
# Group creation tests
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# DropboxTool — success paths with mocked httpx
# ---------------------------------------------------------------------------

def test_dropbox_upload_success(tmp_path):
    test_file = tmp_path / "report.pdf"
    test_file.write_bytes(b"PDF content")
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"path_display": "/report.pdf"}
    mock_resp.raise_for_status = MagicMock()
    with patch("httpx.post", return_value=mock_resp):
        tool = DropboxTool({"access_token": "tok_test"})
        result = tool.run(action="upload", file_path=str(test_file))
    assert result.success
    assert "/report.pdf" in result.output


def test_dropbox_list_success():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "entries": [
            {"name": "file1.pdf", ".tag": "file"},
            {"name": "folder1", ".tag": "folder"},
        ]
    }
    mock_resp.raise_for_status = MagicMock()
    with patch("httpx.post", return_value=mock_resp):
        tool = DropboxTool({"access_token": "tok_test"})
        result = tool.run(action="list", folder_path="")
    assert result.success
    assert "file1.pdf" in result.output
    assert len(result.raw_data["entries"]) == 2


def test_dropbox_share_success():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"url": "https://www.dropbox.com/s/abc/report.pdf?dl=0"}
    mock_resp.raise_for_status = MagicMock()
    with patch("httpx.post", return_value=mock_resp):
        tool = DropboxTool({"access_token": "tok_test"})
        result = tool.run(action="share", dropbox_path="/report.pdf")
    assert result.success
    assert "dropbox.com" in result.output


def test_dropbox_download_success(tmp_path):
    mock_resp = MagicMock()
    mock_resp.content = b"file content"
    mock_resp.raise_for_status = MagicMock()
    with patch("httpx.post", return_value=mock_resp):
        tool = DropboxTool({"access_token": "tok_test"})
        result = tool.run(
            action="download",
            dropbox_path="/report.pdf",
            destination=str(tmp_path),
        )
    assert result.success
    assert "report.pdf" in result.output


# ---------------------------------------------------------------------------
# N8NWebhookTool — success paths
# ---------------------------------------------------------------------------

def test_n8n_trigger_success():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.raise_for_status = MagicMock()
    with patch("httpx.post", return_value=mock_resp):
        tool = N8NWebhookTool({"webhook_url": "http://n8n.local/webhook/abc"})
        result = tool.run(action="trigger", data={"event": "form_submit"}, workflow_name="CRM Sync")
    assert result.success
    assert "CRM Sync" in result.output


def test_n8n_send_with_api_key():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.raise_for_status = MagicMock()
    with patch("httpx.post", return_value=mock_resp) as mock_post:
        tool = N8NWebhookTool({
            "webhook_url": "http://n8n.local/webhook/abc",
            "n8n_api_key": "secret_key",
        })
        result = tool.run(action="send", data={"test": "val"})
    assert result.success
    call_kwargs = mock_post.call_args[1]
    assert call_kwargs["headers"].get("X-N8N-API-KEY") == "secret_key"


# ---------------------------------------------------------------------------
# WebhookReceiver — events
# ---------------------------------------------------------------------------

def test_webhook_receiver_get_recent_events_with_data(tmp_path, monkeypatch):
    import json
    import tools.automation.webhook_receiver as wh_mod
    events_file = tmp_path / "events.json"
    events_data = [
        {"endpoint_name": "form_contacto", "received_at": "2026-04-10T10:00:00", "summary": "New lead"},
        {"endpoint_name": "form_contacto", "received_at": "2026-04-10T11:00:00", "summary": "Another lead"},
        {"endpoint_name": "other", "received_at": "2026-04-10T12:00:00", "summary": "Other"},
    ]
    events_file.write_text(json.dumps(events_data), encoding="utf-8")
    monkeypatch.setattr(wh_mod, "_ENDPOINTS_FILE", tmp_path / "endpoints.json")
    monkeypatch.setattr(wh_mod, "_EVENTS_FILE", events_file)
    tool = WebhookReceiverTool()
    result = tool.run(action="get_recent_events", endpoint_name="form_contacto", limit=10)
    assert result.success
    assert len(result.raw_data["events"]) == 2
    assert "form_contacto" in result.output


# ---------------------------------------------------------------------------
# MakeWebhookTool — credential path
# ---------------------------------------------------------------------------

def test_make_with_credential_sends():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    with patch("httpx.post", return_value=mock_resp):
        tool = MakeWebhookTool({"webhook_url": "https://hook.make.com/abc"})
        result = tool.run(action="send", data={"campo": "valor"})
    assert result.success


# ---------------------------------------------------------------------------
# ZapierWebhookTool — credential path
# ---------------------------------------------------------------------------

def test_zapier_with_credential_sends():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.raise_for_status = MagicMock()
    with patch("httpx.post", return_value=mock_resp):
        tool = ZapierWebhookTool({"webhook_url": "https://hooks.zapier.com/abc"})
        result = tool.run(action="send", data={"campo": "valor"})
    assert result.success


def test_daily_report_group_created():
    group = create_daily_report()
    assert group.name == "daily_report"
    assert len(group.agents) == 4
    roles = [a.role for a in group.agents]
    assert "data_collector" in roles
    assert "daily_analyst" in roles
    assert "report_writer" in roles
    assert "report_distributor" in roles


def test_social_autopilot_group_created():
    group = create_social_autopilot()
    assert group.name == "social_autopilot"
    assert len(group.agents) == 4
    assert group.mode == "pipeline"


def test_lead_nurturing_group_created():
    group = create_lead_nurturing()
    assert group.name == "lead_nurturing"
    assert len(group.agents) == 4
    roles = [a.role for a in group.agents]
    assert "lead_qualifier" in roles
    assert "crm_updater" in roles
